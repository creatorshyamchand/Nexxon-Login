#!/usr/bin/env python3
"""Nexxon Hacker - Login Interface
Unlimited attempts + random sound on success
Sound files: sound1.mp3, sound2.mp3, sound3.mp3
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

HOME = Path.home()
INSTALL_DIR = HOME / ".nexxon_system"
VAULT_FILE = INSTALL_DIR / "vault.enc"
CONFIG_FILE = INSTALL_DIR / "config.json"
SOUND_DIR = INSTALL_DIR / "sound"
SALT_FILE = INSTALL_DIR / "salt.key"

# Available sound files (random pick on successful login)
SOUND_FILES = ["sound1.mp3", "sound2.mp3", "sound3.mp3"]

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


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def decrypt_data(encrypted_str, password, salt):
    try:
        key = hashlib.sha256((password + salt).encode()).digest()
        encrypted = base64.b64decode(encrypted_str.encode())
        decrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))
        return json.loads(decrypted.decode())
    except Exception:
        return None


# ============ SOUND PLAYER (FIXED) ============
def play_sound(name):
    """Play a sound file from SOUND_DIR with multiple fallback players"""
    path = SOUND_DIR / name

    if not path.exists():
        # Try other common locations
        alt_paths = [
            HOME / name,
            HOME / "Nexxon-Login" / "sound" / name,
            Path(__file__).parent / "sound" / name,
            Path(__file__).parent / name,
        ]
        for p in alt_paths:
            if p.exists():
                path = p
                break
        else:
            # No sound file found - silent fail
            return False

    # Try mpv first
    if shutil.which("mpv"):
        try:
            subprocess.Popen(
                ["mpv", "--no-video", "--really-quiet", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            pass

    # Fallback: termux-media-player
    if shutil.which("termux-media-player"):
        try:
            subprocess.Popen(
                ["termux-media-player", "play", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            pass

    # Fallback: ffplay
    if shutil.which("ffplay"):
        try:
            subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            pass

    # Fallback: aplay (WAV only, but try anyway)
    if shutil.which("aplay"):
        try:
            subprocess.Popen(
                ["aplay", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception:
            pass

    return False


def play_random_welcome():
    """Pick a random sound file and play it"""
    if not SOUND_DIR.exists():
        return
    available = [f for f in SOUND_FILES if (SOUND_DIR / f).exists()]
    if not available:
        # Fallback: any mp3 in the folder
        available = [p.name for p in SOUND_DIR.glob("*.mp3")]
    if not available:
        return
    chosen = random.choice(available)
    play_sound(chosen)


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

    if len(sys.argv) > 1 and sys.argv[1] == "--shell":
        return

    clear()
    print(C.BC + "\n  [*] Initializing secure session...\n" + C.X)
    time.sleep(0.5)
    binary_rain(duration=2)

    show_login_banner()

    wrong_count = 0

    while True:
        print(C.BY + "┌─[AUTHENTICATION REQUIRED]" + C.X)

        try:
            username = input(C.BC + "├──╼ " + C.BW + "Username: " + C.X).strip()
        except (KeyboardInterrupt, EOFError):
            print(C.BR + "\n[!] Login cancelled." + C.X)
            time.sleep(1)
            show_login_banner()
            continue

        if not username:
            print(C.BR + "  ✗ Username cannot be empty!" + C.X)
            time.sleep(1)
            show_login_banner()
            continue

        try:
            password = getpass.getpass(C.BC + "└──╼ " + C.BW + "Password: " + C.X)
        except (KeyboardInterrupt, EOFError):
            print(C.BR + "\n[!] Login cancelled." + C.X)
            time.sleep(1)
            show_login_banner()
            continue

        if not password:
            print(C.BR + "  ✗ Password cannot be empty!" + C.X)
            time.sleep(1)
            show_login_banner()
            continue

        print(C.BC + "\n  [*] Verifying credentials..." + C.X)
        time.sleep(0.8)

        # Load vault
        try:
            with open(SALT_FILE) as f:
                salt = f.read().strip()
            with open(VAULT_FILE) as f:
                encrypted = f.read().strip()
        except Exception:
            print(C.BR + "[!] Vault corrupted! Run installer again." + C.X)
            sys.exit(1)

        vault_data = decrypt_data(encrypted, password, salt)

        # Verify
        if vault_data and vault_data.get("username") == username:
            pass_hash = vault_data.get("password_hash")
            if hash_password(password, salt) == pass_hash:
                # ========== SUCCESS ==========
                clear()
                print(C.BG + "\n  [✓] ACCESS GRANTED\n" + C.X)
                time.sleep(0.3)

                # Play random welcome sound BEFORE animation
                play_random_welcome()

                # Green/colorful binary rain animation
                binary_rain(duration=3, colors=[C.G, C.BR, C.BY, C.BB, C.BC, C.BM])

                # Wait a bit so the sound gets time to finish
                time.sleep(2)

                # Launch shell
                os.execv(sys.executable, [sys.executable, str(INSTALL_DIR / "shell.py")])
                return

        # ========== FAILED ==========
        wrong_count += 1
        print(C.BR + "\n  ✗ ACCESS DENIED! Wrong username or password." + C.X)
        print(C.BY + f"  ↻ Attempts: {wrong_count}  (Unlimited - try again)\n" + C.X)
        time.sleep(1.2)
        show_login_banner()


if __name__ == "__main__":
    login()
