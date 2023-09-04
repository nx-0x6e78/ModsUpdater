import sys
import os, time
from zipfile import BadZipFile
from utils.Mods import Mods
from rich.panel import Panel
from utils.Utils import Utils
from colorama import init, Fore
from rich.console import Console
from rich.columns import Columns

util = Utils()
init(autoreset=True)

def updateMods():
   mod = Mods()
   util.clear()
   
   default_path = True

   print(Fore.YELLOW+"Maybe some mods couldn't be find, to find them you need to set Curse Forge API!")
   version_to_update = input(str(Fore.BLUE+"Insert the version you want to for updating your mods: "+Fore.CYAN))

   minecraft_versions = mod.get_minecraft_versions()

   if version_to_update not in minecraft_versions:
      return print(Fore.RED+"Insert a valid Minecraft version!")

   loaders = ["fabric", "forge"]

   print(Fore.BLUE+"Select your loader: ")
   print(Fore.CYAN+f"[0] - {loaders[0]}")
   print(Fore.CYAN+f"[1] - {loaders[1]}")

   l = int(input(Fore.BLUE+"Option: "+Fore.CYAN))

   try:
      loader = loaders[l]
   except IndexError:
      return print("Enter a valid option")

   # if loader == 0: loader = "fabric"
   # elif loader == 1: loader = "forge"
   # else: return print("Enter a valid option")

   custom_minecraft_folder = str(input(Fore.BLUE+f"Is {Fore.MAGENTA+mod.mods_path+Fore.BLUE}\nyour minecraft folder? y/n: "))
   custom_minecraft_folder = False if custom_minecraft_folder == "y" else True

   if custom_minecraft_folder:
      default_path = False

      custom_minecraft_folder = input(str(Fore.BLUE+"Insert your .minecraft folder path (Drag your .minecraft folder, it should paste the path): "+Fore.CYAN))

      if not os.path.exists(custom_minecraft_folder):
         return print("Path not valid")

      mod.mods_path = util.mods_path = custom_minecraft_folder

   mod.set_loader_and_version(loader, version_to_update)

   util.clear()

   if not mod.update():
      return print(Fore.RED+f"No mods found in {Fore.MAGENTA+mod.mods_path}")
      
   path = os.path.dirname(util.mods_path) if not default_path else util.mods_path
   move_the_folder = input(str(Fore.BLUE+f"Move mods_{version_to_update} in {path}? y/n: "+Fore.CYAN)).lower()
   move_the_folder = True if move_the_folder == "y" else False

   if move_the_folder:
      util.move_folder(version_to_update, default_path)

if __name__ == "__main__":
   try:
      updateMods()
   except Exception as e:
      util.clear()
      print(e)
      sys.exit(0)
   except KeyboardInterrupt:
      util.exit_gracefully()
