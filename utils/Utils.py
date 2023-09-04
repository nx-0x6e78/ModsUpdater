import os
import sys
import time
import shutil
import requests
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns

sys.dont_write_bytecode = True

class Utils():
   def __init__(self):
      self.mods_path = os.path.join(os.getenv('APPDATA'), '.minecraft')#, 'mods')

   def clear(self):
      os.system('cls' if os.name == 'nt' else 'clear')

   def shorten(self, url):
      try:
         return requests.get("http://tinyurl.com/api-create.php", params=dict(url=url))
      except Exception as e:
         return "An error occured"

   def move_folder(self, version, default_path:bool):
      if default_path: path = self.mods_path
      else: path = os.path.dirname(self.mods_path)
      shutil.move(f".\mods_{version}", path)

   def exit_gracefully(self):
      self.clear()
      console = Console()

      goodbye_panel = Panel.fit("Thanks for using the program.", title="[bold]Goodbye!", border_style="green")
      
      columns = Columns([goodbye_panel])
      console.print(columns)

      time.sleep(1)

if __name__ == "__main__":
   Utils()