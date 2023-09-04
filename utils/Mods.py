import os
import sys
import time
import json
import shutil
import zipfile
import requests
from .Utils import Utils
from rich.table import Table
from colorama import init, Fore
from rich.console import Console
from rich.progress import Progress

init(autoreset=True)
sys.dont_write_bytecode = True

class Mods:

   def __init__(self):
      self.mods_path = os.path.join(os.getenv('APPDATA'), '.minecraft', 'mods')
      self.__loader = None
      self.__version = None

   def set_loader_and_version(self, loader, version):
      self.loader = loader
      self.version = version

   def __get_mods_files_name(self):
      files = os.listdir(self.mods_path)
      jar_files = []
      for file in files:
         if file.endswith(".jar"):
            jar_files.append(file)
      return jar_files

   def __get_mods_by_id_or_name(self, id_or_name):
      mods = self.__get_mods_files_name()
      json_file = "fabric.mod.json"
      mods_name = []

      for mod in mods:
         with zipfile.ZipFile(os.path.join(self.mods_path, mod), 'r') as jar:
            if json_file in jar.namelist():
               with jar.open(json_file) as target_file:
                  content = target_file.read()
                  mods_name.append(json.loads(content.decode('utf-8'))["".join(id_or_name.lower())])
        
      return mods_name

   def __request_with(self, id_or_name, found=True):
      return requests.get(f"https://api.modrinth.com/v2/project/"+str(id_or_name).replace(" ", "-")+"/version",
      params=dict(
         loaders = "".join(f"[\"{self.loader}\"]"),
         game_versions = "".join(f"[\"{self.version}\"]")
      ))
   
   def __download_mod(self, url:str, file_name:str):
      response = requests.get(url, allow_redirects=True)
      open(os.path.join(f"mods_{self.version}", file_name), 'wb').write(response.content)

   def get_minecraft_versions(self):
      response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")

      if response.ok:
         data = response.json()
         versions = [entry["id"] for entry in data["versions"]]
         return versions
      else:
         print("Failed to fetch Minecraft versions.")
         return []

   def update(self):
      current_dir = os.getcwd()
      shutil.rmtree(os.path.join(current_dir, f"mods_{self.version}"), ignore_errors=True)
      os.mkdir(os.path.join(current_dir, f"mods_{self.version}"))

      mods_id = self.__get_mods_by_id_or_name("id")
      mods_name = self.__get_mods_by_id_or_name("name")

      if not mods_id and not mods_name:
         return False

      console = Console()

      mods_not_found_by_version = []
      mods_not_found = []

      table = Table(show_header=True, header_style="bold cyan", title="[bold]Mods Status", border_style="white")
      table.add_column("Status")
      table.add_column("Mods Name")

      with console.status(f"[bold green]Downloading mods..."):
         print(Fore.CYAN+"-"*10+" Downloading Mods "+10*"-")
         for mod_id, mod_name in zip(mods_id, mods_name):
            response = self.__request_with(mod_id)

            if not response.ok:
               response = self.__request_with(mod_name)

            if response.ok:
               try:
                  details = response.json()[0]["files"][0]
                  download_link = details["url"]
                  file_name = str(details["filename"]).replace("%2B", "+")

                  print(Fore.GREEN+f"Downloading {Fore.CYAN+mod_name}")
                  self.__download_mod(download_link, file_name)

                  table.add_row("[green]Downloaded", f"[cyan]{mod_name}")
               except IndexError as e:
                  mods_not_found_by_version.append(mod_name)
            else:
               mods_not_found.append(mod_name)

      time.sleep(2)
      Utils.clear(self)

      if mods_not_found or mods_not_found_by_version:
         table.add_section()
         
         for mod_not_found_by_version in mods_not_found_by_version:
            table.add_row("[red]Not Found by Version", f"[cyan]{mod_not_found_by_version}")

         table.add_section()

         for mod_not_found in mods_not_found:
            table.add_row("[red]Not Found", f"[cyan]{mod_not_found}")

      else:
         print(Fore.GREEN+"Successfully downloaded all the mods without errors!")

      console.print(table)
      return True

if __name__ == "__main__":
   Mods().update()
