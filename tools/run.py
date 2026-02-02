#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

# =========================
# WARNA TERMINAL
# =========================
class color:
    R = '\033[1;31m'
    G = '\033[1;32m'
    Y = '\033[1;33m'
    C = '\033[1;36m'
    W = '\033[1;37m'
    N = '\033[0m'

# =========================
# PASTIKAN RUN DARI /XShield/tools
# =========================
EXPECTED_DIR_NAME = "tools"
cwd = os.path.basename(os.getcwd())
if cwd != EXPECTED_DIR_NAME:
    print(f"{color.R}[ERROR]{color.N} Jalankan script hanya dari folder '{EXPECTED_DIR_NAME}'!")
    sys.exit(1)

# =========================
# CEK PYTHON
# =========================
PYTHON_VER = sys.version_info[0]
print(f"{color.G}[INFO]{color.N} Python version {PYTHON_VER} terdeteksi.")

# =========================
# CEK CLANG / GCLANG
# =========================
def check_command(cmd):
    return subprocess.call(f"command -v {cmd}", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

if check_command("clang"):
    CC = "clang"
elif check_command("gclang"):
    CC = "gclang"
else:
    print(f"{color.R}[ERROR]{color.N} Clang atau GClang tidak ditemukan!")
    print(f"{color.Y}Silakan install dengan: pkg install clang{color.N}")
    sys.exit(1)

print(f"{color.G}[INFO]{color.N} Compiler ditemukan: {CC}")

# =========================
# PATH REPO
# =========================
SCRIPT_DIR = os.getcwd()  # sekarang pasti /XShield/tools
TARGET_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # parent folder = repo root

REPO_URL = "https://github.com/xmodzid/XShield.git"

# =========================
# CLONE / UPDATE REPO
# =========================
if not os.path.isdir(TARGET_DIR):
    print(f"{color.C}[INFO]{color.N} Meng-clone repo...")
    os.system(f"git clone {REPO_URL} {TARGET_DIR}")
else:
    print(f"{color.C}[INFO]{color.N} Repo sudah ada, update saja...")
    os.chdir(TARGET_DIR)
    os.system("git pull")
    os.chdir(SCRIPT_DIR)

# =========================
# PATH FILES DI TOOLS
# =========================
c_file = os.path.join(SCRIPT_DIR, "xshield.c")
binary_file = os.path.join(TARGET_DIR, "xshield")
repo_run_py = os.path.join(SCRIPT_DIR, "run.py")

# =========================
# COMPILE xshield.c
# =========================
if os.path.isfile(c_file):
    print(f"{color.C}[INFO]{color.N} Meng-compile xshield.c...")
    os.system(f"{CC} {c_file} -o {binary_file}")
    print(f"{color.G}[INFO]{color.N} Compile selesai. Binary: {binary_file}")
else:
    print(f"{color.Y}[WARN]{color.N} xshield.c tidak ditemukan!")

# =========================
# JALANKAN run.py
# =========================
if os.path.isfile(repo_run_py):
    print(f"{color.C}[INFO]{color.N} Menjalankan run.py dari repo...")
    os.system(f"{sys.executable} {repo_run_py}")
else:
    print(f"{color.Y}[WARN]{color.N} run.py tidak ditemukan!")

# =========================
# SELESAI
# =========================
print(f"{color.G}[INFO]{color.N} Semua proses selesai.")