#!/usr/bin/env python3
"""Nexxon Hacker - Login Interface"""

import os
import sys
import json
import base64
import hashlib
import getpass
import subprocess
import time
import random
import shutil
from pathlib import Path

HOME = Path.home()
INSTALL_DIR = HOME / ".nexxon_system"
VAULT_FILE = INSTALL_DIR / "vault.enc"
CONFIG_FILE = INSTALL_DIR / "config.json"
SOUND_DIR = INSTALL_DIR / "sound"
SALT_FILE = INSTALL_DIR / "salt.key"

# ============ KALI LOGO ============
KALI_LOGO = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⣄⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⠀⠀⢢⣤⣀⣦⣄⡀⠙⣶⡘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣀⣨⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣯⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣽⣿⣿⣿⣿⠟⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⣻⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⢿⣷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⣴⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣷⣽⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⣾⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣯⠁⠀⠀⠀⠀
⠀⠀⠐⠛⢿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣷⣄⡀⠀⠀
⠀⠀⠀⠀⠘⠟⠿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⠇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠟⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠲⣶⣶⣦⠀⢀⣴⣶⣶⠖⠀⠀⠒⢶⣶⣶⣶⠀⠀⠐⢶⣶⣶⣦⠀⠀⠀⠒⢶⣶⣶⡆
⠀⣿⣿⣿⣠⣾⣿⡿⠋⠀⠀⠀⢠⣿⣿⣿⣿⣧⠀⠀⠠⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡇
⠀⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⣾⣿⣿⠹⣿⣿⣇⠀⠐⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡇
⠀⣿⣿⣿⠟⣿⣿⣿⣄⠀⠀⣼⣿⣿⣿⣶⣿⣿⣿⣆⢈⣿⣿⣿⣤⣤⣄⣀⣸⣿⣿⡇
⠀⣿⣿⡿⠀⠈⢿⣿⣿⡆⢸⣿⣿⠏⠉⠉⠉⢿⣿⡿⡄⣿⣿⣿⣿⢿⣿⡿⢸⣿⣿⡇
"""

class C:
    R='\033[0;31m'; G='\033[0;32m'; Y='\033[0;33m'; B='\033[0;34m'
    M='\033[0;35m'; CY='\033[0;36m'; W='\033[0;37m'
    BR='\033[1;31m'; BG='\033[1;32m'; BY='\033[1;33m'; BB='\033[1;34m'
    BM='\033[1;35m'; BC='\033[1;36m'; BW='\033[1;37m'; X='\033[0m'

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def binary_rain(duration=2.5, colors=None):
    if colors is None:
        colors = [C.G, C.BR, C.BY, C.BB, C.BC, C.BM]
    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 80
    frames = int(duration * 18)
    for _ in range(frames):
        line = ""
        for _ in range(cols):
            if random.random() < 0.4:
                line += random.choice(colors) + random.choice("01") + C.X
            else:
                line += " "
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        time.sleep(0.04)

def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def decrypt_data(encrypted_str, password, salt):
    try:
        key = hashlib.sha256((password + salt).encode()).digest()
        encrypted = base64.b64decode(encrypted_str.encode())
        decrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))
        return json.loads(decrypted.decode())
    except:
        return None

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

def play_random_welcome():
    play_sound(f"welcome{random.randint(1,5)}.mp3")

def show_login_banner():
    clear()
    print(C.BC + KALI_LOGO + C.X)
    print(C.BG + "═" * 62 + C.X)
    print(C.BY + "      🔐 NEXXON HACKER SECURE LOGIN SYSTEM 🔐" + C.X)
    print(C.BG + "═" * 62 + C.X)
    print()

def login():
    if not VAULT_FILE.exists():
        print(C.BR + "[!] No account found. Run main.py first!" + C.X)
        sys.exit(1)
    
    # Check if we should skip login (shell mode)
    if len(sys.argv) > 1 and sys.argv[1] == "--shell":
        return
    
    # Loading animation
    clear()
    print(C.BC + "\n  [*] Initializing secure session...\n" + C.X)
    time.sleep(0.5)
    binary_rain(duration=2)
    
    # Login form
    show_login_banner()
    
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        expected_user = config.get("username", "")
    except:
        expected_user = ""
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        print(C.BY + "┌─[AUTHENTICATION REQUIRED]" + C.X)
        username = input(C.BC + "├──╼ " + C.BW + "Username: " + C.X).strip()
        password = getpass.getpass(C.BC + "└──╼ " + C.BW + "Password: " + C.X)
        
        print(C.BC + "\n  [*] Verifying credentials..." + C.X)
        time.sleep(0.8)
        
        # Verify
        try:
            with open(SALT_FILE) as f:
                salt = f.read().strip()
            with open(VAULT_FILE) as f:
                encrypted = f.read().strip()
        except:
            print(C.BR + "[!] Vault corrupted!" + C.X)
            sys.exit(1)
        
        vault_data = decrypt_data(encrypted, password, salt)
        
        if vault_data and vault_data.get("username") == username:
            pass_hash = vault_data.get("password_hash")
            if hash_password(password, salt) == pass_hash:
                # SUCCESS
                clear()
                print(C.BG + "\n  [✓] ACCESS GRANTED\n" + C.X)
                time.sleep(0.4)
                
                # Welcome animation
                binary_rain(duration=3, colors=[C.G, C.BR, C.BY, C.BB, C.BC, C.BM])
                
                # Play welcome sound
                play_random_welcome()
                time.sleep(1.5)
                
                # Launch shell
                os.execv(sys.executable, [sys.executable, str(INSTALL_DIR / "shell.py")])
                return
        
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(C.BR + f"\n  ✗ ACCESS DENIED! {remaining} attempt(s) remaining\n" + C.X)
            time.sleep(1)
            show_login_banner()
        else:
            print(C.BR + "\n  ⛔ TOO MANY FAILED ATTEMPTS! LOCKED!\n" + C.X)
            play_sound("welcome1.mp3")
            time.sleep(2)
            sys.exit(1)

if __name__ == "__main__":
    login()
