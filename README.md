# Gtag-pckg Installation Guide

## Installation

Run the installer from the project root:

```bash
python3 Installer/install.py
```

This will:
- Copy files to `~/.gtag-pckg-manag`
- Create a `gtag-pckg` command in `~/.local/bin`

## Setup PATH

Add `~/.local/bin` to your PATH (add to ~/.bashrc or ~/.zshrc):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.bashrc
```

## Usage

After installation, you can use:

```bash
# Install a mod from the registry
gtag-pckg install ModName

# Install a mod from a direct link
gtag-pckg install ModName --link https://example.com/mod.dll

# List available mods
gtag-pckg list
```

## Examples

```bash
gtag-pckg install YizzyCameraMod
gtag-pckg install YizzyCameraMod --link https://example.com/YizzyCameraMod.dll
gtag-pckg list
```

<img width="653" height="485" alt="image" src="https://github.com/user-attachments/assets/9b72f513-ad07-430a-87a6-a9a98745f1d3" />

