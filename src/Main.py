import sys
import json
import subprocess
import os
import argparse

GAME_DIR = os.path.expanduser("~/.steam/steam/steamapps/common/Gorilla Tag/BepInEx/plugins")

def install_mod(mod_name, url=None):
    print(f"DEBUG: Installing {mod_name}...")
    
    if url is None:
        with open("mods.json", "r") as f:
            registry = json.load(f)
        
        if mod_name in registry:
            url = registry[mod_name]["url"]
        else:
            print("Error: Mod not found in database.")
            return
    
    if not os.path.exists(GAME_DIR):
        print(f"Error: Directory {GAME_DIR} not found. Is BepInEx installed?")
        return

    subprocess.run(["curl", "-L", url, "-o", f"{GAME_DIR}/{mod_name}.dll"])
    print(f"Success! {mod_name} installed to {GAME_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Gorilla Tag mods")
    parser.add_argument("command", help="Command: install, or mod name to install")
    parser.add_argument("mod_name", nargs='?', help="Name of the mod to install")
    parser.add_argument("--link", help="Direct URL link to the mod (bypass registry lookup)")
    
    args = parser.parse_args()
    
    if args.command.lower() == "install":
        if not args.mod_name:
            print("Error: Please specify a mod name")
            sys.exit(1)
        install_mod(args.mod_name, url=args.link)
    else:
        install_mod(args.command, url=args.link)