import aiohttp
import json
import asyncio

# URLs for data updates
link_avatar = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/avatar.json"
link_weapons = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/weapons.json"
link_relict_sets = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/relict_sets.json"

class DataUpdater:
    def __init__(self, source_url, target_filename):
        self.source_url = source_url
        self.target_filename = target_filename
        self.DEViantUA = {}
        self.new = []

    async def fetch_json(self, url):
        """Fetches JSON data from the specified URL and returns it as text."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def save_data(self):
        """Saves updated data to a JSON file with the name {target_filename}.json."""
        with open(f"{self.target_filename}.json", "w", encoding="utf-8") as file:
            json.dump(self.DEViantUA, file, indent=4, ensure_ascii=False)

    async def print_result(self):
        """Prints information about received data updates."""
        if self.new:
            print(f"Received updated fields for {self.target_filename}: {len(self.new)}\n|--New ID: {self.new}")
        else:
            print(f"No new fields received for {self.target_filename}")

    async def updated_data(self):
        """Updates data in DEViantUA by adding new values from the source."""
        self.data = json.loads(self.data)
        self.DEViantUA = json.loads(self.DEViantUA)
        
        for key in self.data:
            if key.isnumeric():
                if not key in self.DEViantUA:
                    self.DEViantUA[key] = self.data[key]["name"]
                    self.new.append(key)

    async def start(self):
        """Starts the data update process."""
        print(f"Start update {self.target_filename}")
        self.data = await self.fetch_json(self.source_url)
        
        if self.target_filename == "avatar":
            self.DEViantUA = await self.fetch_json(link_avatar)
        elif self.target_filename == "weapons":
            self.DEViantUA = await self.fetch_json(link_weapons)
        else:
            self.DEViantUA = await self.fetch_json(link_relict_sets)
            
        await self.updated_data()
        await self.save_data()
        await self.print_result()

async def main():
    lang = input("Select the language from which you want to translate into Ukrainian [ru/en/cn]\n(Leave the field empty and the default will be 'ru'): ")
    if not lang:
        lang = "ru"
    if not lang in ["ru","en","cn"]:
        print("Incorrect or unsupported language.")
        return None
    
    links = [
        ("https://raw.githubusercontent.com/FortOfFans/HSRMaps/master/maps/ru/avatar.json", "avatar"),
        ("https://raw.githubusercontent.com/FortOfFans/HSRMaps/master/maps/ru/weapons.json", "weapons"),
        ("https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/index_new/ru/relic_sets.json", "relict_sets")
    ]
    
    tasks = [DataUpdater(source_url, target_filename) for source_url, target_filename in links]

    await asyncio.gather(*[task.start() for task in tasks])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
