#!/usr/bin/env python3
"""Nexxon Hacker - Home Shell with command suggestions"""

import os
import sys
import json
import subprocess
import time
import random
import shutil
import shlex
from pathlib import Path

HOME = Path.home()
INSTALL_DIR = HOME / ".nexxon_system"
CONFIG_FILE = INSTALL_DIR / "config.json"
SOUND_DIR = INSTALL_DIR / "sound"

class C:
    R='\033[0;31m'; G='\033[0;32m'; Y='\033[0;33m'; B='\033[0;34m'
    M='\033[0;35m'; CY='\033[0;36m'; W='\033[0;37m'
    BR='\033[1;31m'; BG='\033[1;32m'; BY='\033[1;33m'; BB='\033[1;34m'
    BM='\033[1;35m'; BC='\033[1;36m'; BW='\033[1;37m'; X='\033[0m'

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

# ============ COMMAND DATABASE ============
COMMANDS = {
    # termux pkg
    "pkg install": "Install a package",
    "pkg uninstall": "Remove a package",
    "pkg update": "Update package lists",
    "pkg upgrade": "Upgrade all packages",
    "pkg search": "Search for packages",
    "pkg list-all": "List all available packages",
    "pkg list-installed": "List installed packages",
    "pkg show": "Show package info",
    # apt
    "apt update": "Update apt repositories",
    "apt upgrade": "Upgrade packages via apt",
    "apt install": "Install via apt",
    "apt remove": "Remove via apt",
    # filesystem
    "ls": "List directory contents",
    "ls -la": "List all with details",
    "cd": "Change directory",
    "pwd": "Print working directory",
    "mkdir": "Create directory",
    "rmdir": "Remove empty directory",
    "rm -rf": "Remove recursively (DANGEROUS)",
    "cp": "Copy files",
    "mv": "Move files",
    "touch": "Create empty file",
    "cat": "Show file contents",
    "nano": "Edit file with nano",
    "vim": "Edit file with vim",
    # network
    "ping": "Ping a host",
    "ifconfig": "Show network interfaces",
    "ip addr": "Show IP addresses",
    "curl": "Fetch URL",
    "wget": "Download file",
    "ssh": "SSH connection",
    "nmap": "Network scanner",
    "netstat": "Network statistics",
    # system
    "clear": "Clear screen",
    "exit": "Exit Nexxon shell",
    "logout": "Logout",
    "whoami": "Show current user",
    "uname -a": "System info",
    "df -h": "Disk usage",
    "free -h": "Memory usage",
    "top": "Process monitor",
    "ps aux": "List processes",
    "kill": "Kill process",
    "history": "Command history",
    "date": "Show date/time",
    "uptime": "System uptime",
    "neofetch": "System info fancy",
    # python
    "python": "Run Python",
    "python3": "Run Python 3",
    "pip install": "Install Python package",
    # git
    "git clone": "Clone repository",
    "git pull": "Pull changes",
    "git push": "Push changes",
    "git status": "Show git status",
    # termux api
    "termux-battery-status": "Check battery",
    "termux-camera-photo": "Take a photo",
    "termux-clipboard-get": "Get clipboard",
    "termux-clipboard-set": "Set clipboard",
    "termux-toast": "Show toast notification",
    "termux-vibrate": "Vibrate device",
    "termux-tts-speak": "Text to speech",
    # sound
    "play sound": "Play a random welcome sound",
    "sound1": "Play welcome1",
    "sound2": "Play welcome2",
    # system info
    "device": "Show device info",
    "info": "Show system info",
    "help": "Show this help",
    "commands": "List all commands",
}

def get_suggestions(prefix):
    """Get command suggestions for prefix"""
    prefix = prefix.strip().lower()
    if not prefix:
        return []
    matches = [cmd for cmd in COMMANDS.keys() if cmd.lower().startswith(prefix)]
    return matches[:6]

def get_device_info():
    """Get device info"""
    info = {}
    info["device"] = os.uname().machine
    info["kernel"] = os.uname().sysname + " " + os.uname().release
    
    # Storage
    try:
        st = shutil.disk_usage(str(HOME))
        total_gb = st.total / (1024**3)
        used_gb = st.used / (1024**3)
        info["storage"] = f"{used_gb:.1f}GB / {total_gb:.1f}GB"
    except:
        info["storage"] = "Unknown"
    
    return info

def show_home(config, device):
    """Display home screen"""
    clear()
    user = config.get("username", "user")
    nick = config.get("nickname", "hacker")
    
    # Kali logo (compact)
    logo_lines = [
        "     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄    ",
        "   ▄██████████████████▄  ",
        "  █████▀▀▀▀▀▀▀▀▀▀███████ ",
        " ████▀            ▀██████ ",
        " ████     ▄████▄   ██████ ",
        " ████    ████████  ██████ ",
        " ████    ████████  ██████ ",
        " ████     ▀████▀   ██████ ",
        " ████▄            ▄██████ ",
        "  █████▄▄▄▄▄▄▄▄▄▄███████ ",
        "   ▀██████████████████▀  ",
        "     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    ",
    ]
    
    # Print header with Kali logo side by side
    print(C.BR + "═" * 62 + C.X)
    print(C.BY + "         ⚡ NEXXON HACKER TERMINAL ⚡" + C.X)
    print(C.BR + "═" * 62 + C.X)
    
    logo_colored = [C.BC + l + C.X for l in logo_lines]
    info_lines = [
        "",
        f"  {C.BW}User  : {C.BG}{user}{C.X}",
        f"  {C.BW}Nick  : {C.BM}{nick}{C.X}",
        f"  {C.BW}Device: {C.BY}{device['device']}{C.X}",
        f"  {C.BW}Kernel: {C.BC}{device['kernel']}{C.X}",
        f"  {C.BW}Storage:{C.BG} {device['storage']}{C.X}",
        f"  {C.BW}Status: {C.BG}● ONLINE{C.X}",
        "",
    ]
    
    for i in range(max(len(logo_colored), len(info_lines))):
        left = logo_colored[i] if i < len(logo_colored) else " " * 27
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left} {right}")
    
    print(C.BR + "═" * 62 + C.X)
    print(C.BY + f"  {nick}@nexxon" + C.CY + " ── " + C.BW + "NexxonExploits" + C.X)
    print(C.BR + "─" * 62 + C.X)
    print(C.BY + "  💡 Type 'help' for commands, 'exit' to logout" + C.X)
    print(C.BR + "─" * 62 + C.X)
    print()

def run_command(cmd):
    """Execute command"""
    cmd = cmd.strip()
    if not cmd:
        return True
    
    # Built-in commands
    if cmd == "exit" or cmd == "logout":
        print(C.BY + "\n[*] Logging out... Goodbye, hacker! 👋" + C.X)
        time.sleep(1)
        return False
    if cmd == "clear":
        return True
    if cmd == "help":
        print(C.BC + "\n  Available commands:" + C.X)
        for c, d in list(COMMANDS.items())[:30]:
            print(f"  {C.BG}{c:<25}{C.X} {C.BW}{d}{C.X}")
        print(f"  {C.BY}... and more. Type 'commands' for full list.{C.X}\n")
        return True
    if cmd == "commands":
        print(C.BC + "\n  All available commands:" + C.X)
        for c, d in COMMANDS.items():
            print(f"  {C.BG}{c:<28}{C.X} {C.BW}{d}{C.X}")
        print()
        return True
    if cmd == "device" or cmd == "info":
        d = get_device_info()
        for k, v in d.items():
            print(f"  {C.BY}{k}:{C.X} {C.BW}{v}{C.X}")
        return True
    if cmd == "play sound":
        play_sound(f"welcome{random.randint(1,5)}.mp3")
        return True
    if cmd.startswith("sound") and cmd[5:].isdigit():
        n = int(cmd[5:])
        if 1 <= n <= 5:
            play_sound(f"welcome{n}.mp3")
        return True
    
    # Run as system command
    try:
        result = subprocess.run(cmd, shell=True, cwd=str(HOME))
        return True
    except KeyboardInterrupt:
        print()
        return True
    except Exception as e:
        print(C.BR + f"[!] Error: {e}" + C.X)
        return True

def play_sound(name):
    path = SOUND_DIR / name
    if not path.exists():
        return
    try:
        subprocess.Popen(["mpv", "--no-video", "--really-quiet", str(path)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        try:
            subprocess.Popen(["termux-media-player", "play", str(path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

def main():
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except:
        print(C.BR + "[!] Config not found. Run installer!" + C.X)
        sys.exit(1)
    
    device = get_device_info()
    show_home(config, device)
    
    nick = config.get("nickname", "hacker")
    
    while True:
        try:
            prompt = f"{C.BM}<{nick}>" + C.CY + " ~~ " + C.BW
            cmd = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print(C.BY + "\n[*] Use 'exit' to logout" + C.X)
            continue
        
        if not cmd:
            continue
        
        # Show suggestions before running
        if cmd and not cmd.startswith(("cd ", "exit", "clear")):
            suggestions = get_suggestions(cmd)
            if suggestions and cmd not in COMMANDS:
                print(C.CY + "  💡 Suggestions: " + C.X)
                for s in suggestions[:3]:
                    print(f"    {C.BG}→ {s}{C.X}  {C.BW}{COMMANDS[s]}{C.X}")
        
        if not run_command(cmd):
            break
        
        print()

if __name__ == "__main__":
    main()
