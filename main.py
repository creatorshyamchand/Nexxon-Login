#!/usr/bin/env python3
"""
Nexxon Hacker - Secure Login System for Termux
Installer + authentication setup
Kali Linux ASCII logo only
"""

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

# ============ CONFIG ============
HOME = Path.home()
INSTALL_DIR = HOME / ".nexxon_system"
VAULT_FILE = INSTALL_DIR / "vault.enc"
CONFIG_FILE = INSTALL_DIR / "config.json"
SALT_FILE = INSTALL_DIR / "salt.key"
SOUND_DIR = INSTALL_DIR / "sound"
BASHRC = HOME / ".bashrc"
ZSH = HOME / ".zshrc"

# ============ KALI LINUX ASCII LOGO ============
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

# ============ COLORS ============
class C:
    R = '\033[0;31m'
    G = '\033[0;32m'
    Y = '\033[0;33m'
    B = '\033[0;34m'
    M = '\033[0;35m'
    CY = '\033[0;36m'
    W = '\033[0;37m'
    BR = '\033[1;31m'
    BG = '\033[1;32m'
    BY = '\033[1;33m'
    BB = '\033[1;34m'
    BM = '\033[1;35m'
    BC = '\033[1;36m'
    BW = '\033[1;37m'
    X = '\033[0m'


def clear():
    os.system('clear' if os.name != 'nt' else 'cls')


def binary_rain(duration=2.5, colors=None):
    if colors is None:
        colors = [C.G, C.BR, C.BY, C.BB, C.BC, C.BM]
    try:
        cols = shutil.get_terminal_size().columns
    except Exception:
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


def play_sound(name):
    path = SOUND_DIR / name
    if not path.exists():
        return
    try:
        subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        try:
            subprocess.Popen(
                ["termux-media-player", "play", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def generate_salt():
    return base64.b64encode(os.urandom(32)).decode()


def encrypt_data(data, password, salt):
    key = hashlib.sha256((password + salt).encode()).digest()
    data_bytes = json.dumps(data).encode()
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(data_bytes))
    return base64.b64encode(encrypted).decode()


def print_install_banner():
    clear()
    print(C.BC + KALI_LOGO + C.X)
    print(C.BG + "═" * 62 + C.X)
    print(C.BY + "      🔐 NEXXON HACKER - SECURE LOGIN INSTALLER 🔐" + C.X)
    print(C.BG + "═" * 62 + C.X)
    print()


def install():
    print_install_banner()

    print(C.BC + "[*] Initializing secure installation..." + C.X)
    time.sleep(0.8)
    binary_rain(duration=2)

    INSTALL_DIR.mkdir(exist_ok=True)
    SOUND_DIR.mkdir(exist_ok=True)
    print(C.BG + "[✓] Created secure vault directory" + C.X)
    time.sleep(0.4)

    # Step 1: Username
    print()
    print(C.BY + "┌─[SETUP: STEP 1/3]" + C.X)
    username = input(C.BC + "└──╼ " + C.BW + "Enter Username: " + C.X).strip()
    while not username:
        username = input(C.BR + "✗ Username cannot be empty!\n" + C.BC +
                         "└──╼ " + C.BW + "Enter Username: " + C.X).strip()

    # Step 2: Password
    print()
    print(C.BY + "┌─[SETUP: STEP 2/3]" + C.X)
    password = getpass.getpass(C.BC + "└──╼ " + C.BW + "Enter Password: " + C.X)
    while len(password) < 4:
        print(C.BR + "✗ Password must be at least 4 characters!" + C.X)
        password = getpass.getpass(C.BC + "└──╼ " + C.BW + "Enter Password: " + C.X)

    confirm = getpass.getpass(C.BC + "└──╼ " + C.BW + "Confirm Password: " + C.X)
    while password != confirm:
        print(C.BR + "✗ Passwords don't match!" + C.X)
        confirm = getpass.getpass(C.BC + "└──╼ " + C.BW + "Confirm Password: " + C.X)

    # Step 3: Nickname
    print()
    print(C.BY + "┌─[SETUP: STEP 3/3]" + C.X)
    nickname = input(C.BC + "└──╼ " + C.BW + "Enter Nickname: " + C.X).strip()
    while not nickname:
        nickname = input(C.BR + "✗ Nickname cannot be empty!\n" + C.BC +
                         "└──╼ " + C.BW + "Enter Nickname: " + C.X).strip()

    # Summary
    clear()
    print(C.BG + "═" * 62 + C.X)
    print(C.BY + "      📋 ACCOUNT SUMMARY - PLEASE REVIEW" + C.X)
    print(C.BG + "═" * 62 + C.X)
    print()
    print(f"  {C.BC}Username :{C.X} {C.BW}{username}{C.X}")
    print(f"  {C.BC}Password :{C.X} {C.BW}{'•' * len(password)}{C.X}")
    print(f"  {C.BC}Nickname :{C.X} {C.BW}{nickname}{C.X}")
    print()
    print(C.BG + "═" * 62 + C.X)
    print()
    print(C.BR + "⚠  DISCLAIMER:" + C.X)
    print(C.BY + "  • Your password is encrypted and stored locally." + C.X)
    print(C.BY + "  • If you FORGET your password, you CANNOT login again." + C.X)
    print(C.BY + "  • You will need to CLEAR DATA and reinstall the system." + C.X)
    print(C.BY + "  • There is NO password recovery option." + C.X)
    print()
    print(C.BG + "═" * 62 + C.X)

    choice = input(C.BY + "\n💾 Save this account? (Y/N): " + C.X).strip().upper()
    while choice not in ["Y", "N"]:
        choice = input(C.BR + "✗ Invalid! Enter Y or N: " + C.X).strip().upper()

    if choice == "N":
        print(C.BR + "\n✗ Installation cancelled!" + C.X)
        sys.exit(0)

    # Save encrypted
    salt = generate_salt()
    pass_hash = hash_password(password, salt)

    vault_data = {
        "username": username,
        "nickname": nickname,
        "password_hash": pass_hash,
        "salt": salt,
        "created": time.time()
    }

    encrypted = encrypt_data(vault_data, password, salt)
    with open(VAULT_FILE, 'w') as f:
        f.write(encrypted)

    config = {
        "username": username,
        "nickname": nickname,
        "installed": time.time()
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

    with open(SALT_FILE, 'w') as f:
        f.write(salt)

    os.chmod(VAULT_FILE, 0o600)
    os.chmod(SALT_FILE, 0o600)

    print(C.BG + "\n[✓] Account saved securely!" + C.X)
    time.sleep(0.5)

    # Sound files
    print(C.BC + "\n[*] Installing sound files..." + C.X)
    script_dir = Path(__file__).parent
    sound_src = script_dir / "sound"
    if sound_src.exists():
        for f in sound_src.glob("*.mp3"):
            shutil.copy2(f, SOUND_DIR / f.name)
        print(C.BG + f"[✓] {len(list(SOUND_DIR.glob('*.mp3')))} sound files installed" + C.X)
    else:
        print(C.BR + "[!] sound/ folder not found! Sound effects disabled." + C.X)

    # Copy scripts
    shutil.copy2(Path(__file__).parent / "login.py", INSTALL_DIR / "login.py")
    shutil.copy2(Path(__file__).parent / "shell.py", INSTALL_DIR / "shell.py")

    # Autostart in bashrc/zshrc
    print(C.BC + "\n[*] Configuring auto-login on Termux startup..." + C.X)

    autostart = f'''
# ====== NEXXON HACKER SECURE LOGIN ======
if [ -f "{INSTALL_DIR}/login.py" ]; then
    python "{INSTALL_DIR}/login.py"
fi
# =========================================
'''

    for rc in [BASHRC, ZSH]:
        if rc.exists():
            with open(rc, 'r') as f:
                content = f.read()
            if "# ====== NEXXON HACKER SECURE LOGIN ======" in content:
                start = content.find("# ====== NEXXON HACKER SECURE LOGIN ======")
                end = content.find("# =========================================")
                if end != -1:
                    content = content[:start] + content[end + len("# ========================================="):]
                    with open(rc, 'w') as f:
                        f.write(content)

    with open(BASHRC, 'a') as f:
        f.write(autostart)
    print(C.BG + "[✓] Added to .bashrc" + C.X)

    if ZSH.exists():
        with open(ZSH, 'a') as f:
            f.write(autostart)
        print(C.BG + "[✓] Added to .zshrc" + C.X)

    # mpv check
    print(C.BC + "\n[*] Checking audio support..." + C.X)
    try:
        subprocess.run(["mpv", "--version"], capture_output=True, check=True)
        print(C.BG + "[✓] mpv already installed" + C.X)
    except Exception:
        print(C.BY + "[*] Installing mpv for sound effects..." + C.X)
        try:
            subprocess.run(["pkg", "install", "mpv", "-y"], capture_output=True)
            print(C.BG + "[✓] mpv installed" + C.X)
        except Exception:
            print(C.BR + "[!] Could not install mpv. Install manually: pkg install mpv" + C.X)

    # Done
    clear()
    print(C.BC + KALI_LOGO + C.X)
    print(C.BG + "═" * 62 + C.X)
    print(C.BY + "      ✅ INSTALLATION COMPLETE! ✅" + C.X)
    print(C.BG + "═" * 62 + C.X)
    print()
    print(C.BG + "  Welcome to Nexxon Hacker Secure Login System!" + C.X)
    print()
    print(C.BY + "  📌 IMPORTANT:" + C.X)
    print(C.BC + "  • CLOSE and REOPEN Termux to activate login" + C.X)
    print(C.BC + "  • OR run: source ~/.bashrc" + C.X)
    print()
    print(C.BR + "  ⚠  REMEMBER: If you forget your password," + C.X)
    print(C.BR + "     you CANNOT login. Clear data to reset." + C.X)
    print()
    print(C.BG + "═" * 62 + C.X)
    print(C.BM + "\n  🔥 Nexxon Hacker - Stay Secure! 🔥\n" + C.X)


def uninstall():
    print(C.BR + "\n[!] Uninstalling Nexxon Secure Login..." + C.X)
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
        print(C.BG + "[✓] Removed vault directory" + C.X)

    for rc in [BASHRC, ZSH]:
        if rc.exists():
            with open(rc, 'r') as f:
                content = f.read()
            if "# ====== NEXXON HACKER SECURE LOGIN ======" in content:
                start = content.find("# ====== NEXXON HACKER SECURE LOGIN ======")
                end = content.find("# =========================================")
                if end != -1:
                    content = content[:start] + content[end + len("# ========================================="):]
                    with open(rc, 'w') as f:
                        f.write(content)
    print(C.BG + "[✓] Removed auto-login entries" + C.X)
    print(C.BY + "\n[!] Uninstall complete. Restart Termux.\n" + C.X)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall()
    else:
        if VAULT_FILE.exists():
            print(C.BY + "[!] Account already exists!" + C.X)
            choice = input(C.BY + "Reinstall and overwrite? (Y/N): " + C.X).strip().upper()
            if choice == "Y":
                if INSTALL_DIR.exists():
                    shutil.rmtree(INSTALL_DIR)
                install()
            else:
                print(C.BC + "[*] Keeping existing account." + C.X)
        else:
            install()


if __name__ == "__main__":
    main()
