#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess


def ensure_path_in_shell_config(bin_dir):
    home_dir = os.path.expanduser("~")
    export_line = f'export PATH="{bin_dir}:$PATH"\n'
    shell_files = [".bashrc", ".profile", ".bash_profile", ".bash_login"]
    wrote_any = False

    for shell_file in shell_files:
        config_path = os.path.join(home_dir, shell_file)
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                content = f.read()
            if export_line.strip() in content:
                continue
            with open(config_path, "a") as f:
                f.write("\n# Add gtag-pckg command to PATH\n")
                f.write(export_line)
            wrote_any = True
            print(f"Added PATH export to {config_path}")

    if not wrote_any:
        config_path = os.path.join(home_dir, ".bashrc")
        with open(config_path, "a") as f:
            f.write("\n# Add gtag-pckg command to PATH\n")
            f.write(export_line)
        print(f"Created {config_path} and added PATH export")
        wrote_any = True

    return wrote_any


def install():
    
    home_dir = os.path.expanduser("~")
    install_dir = os.path.join(home_dir, ".gtag-pckg-manag")
    bin_dir = os.path.join(home_dir, ".local/bin")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    src_dir = os.path.join(project_root, "src")
    
    print(f"Installing gtag-pckg-manag to {install_dir}...")
    
    os.makedirs(install_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)
    ensure_path_in_shell_config(bin_dir)
    
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(install_dir, item)
        
        if os.path.isfile(src_path):
            print(f"Copying {item}...")
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            print(f"Copying directory {item}...")
    
    wrapper_path = os.path.join(bin_dir, "gtag-pckg")
    wrapper_script = f"""#!/usr/bin/env python3
import sys
import os

# Change to install directory
os.chdir(os.path.expanduser("~/.gtag-pckg-manag"))

# Import and run main module
sys.path.insert(0, os.path.expanduser("~/.gtag-pckg-manag"))
from Main import install_mod
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Gorilla Tag mods")
    parser.add_argument("command", help="Command to run (install, list)")
    parser.add_argument("mod_name", nargs='?', help="Name of the mod to install")
    parser.add_argument("--link", help="Direct URL link to the mod (bypass registry lookup)")
    
    args = parser.parse_args()
    
    if args.command.lower() == "install":
        if not args.mod_name:
            print("Error: Please specify a mod name")
            sys.exit(1)
        install_mod(args.mod_name, url=args.link)
    elif args.command.lower() == "list":
        import json
        try:
            with open("mods.json", "r") as f:
                registry = json.load(f)
            print("Available mods:")
            for mod_name in sorted(registry.keys()):
                print(f"  - {{mod_name}}")
        except FileNotFoundError:
            print("Error: mods.json not found")
    else:
        print(f"Unknown command: {{args.command}}")
        print("Available commands: install, list")
"""
    
    print(f"Creating command wrapper at {wrapper_path}...")
    with open(wrapper_path, "w") as f:
        f.write(wrapper_script)
    
    os.chmod(wrapper_path, 0o755)
    
    main_py = os.path.join(install_dir, "Main.py")
    os.chmod(main_py, 0o755)
    
    print("\n✓ Installation complete!")
    print(f"✓ Files installed to: {install_dir}")
    print(f"✓ Command created at: {wrapper_path}")
    print("\nTo use gtag-pckg, add ~/.local/bin to your PATH:")
    print("  export PATH=\"$HOME/.local/bin:$PATH\"")
    print("\nThen you can use:")
    print("  gtag-pckg install MODNAME")
    print("  gtag-pckg install MODNAME --link URL")
    print("  gtag-pckg list")

if __name__ == "__main__":
    try:
        install()
    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)
