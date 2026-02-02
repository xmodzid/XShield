#!/usr/bin/env python
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
# CEK PYTHON
# =========================
if sys.version_info[0] >= 3:
    PYTHON_VER = 3
else:
    PYTHON_VER = 2
print(f"{color.G}[INFO]{color.N} Python version {PYTHON_VER} terdeteksi.")

# =========================
# CEK CLANG / GCLANG
# =========================
def check_command(cmd):
    return subprocess.call(f"command -v {cmd}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

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
# CLONE REPO JIKA BELUM ADA
# =========================
REPO_URL = "https://github.com/xmodzid/XModShield-LLVM.git"
TARGET_DIR = "XModShield-LLVM"

if not os.path.isdir(TARGET_DIR):
    print(f"{color.C}[INFO]{color.N} Meng-clone repo...")
    os.system(f"git clone {REPO_URL}")
else:
    print(f"{color.C}[INFO]{color.N} Repo sudah ada, update saja...")
    os.chdir(TARGET_DIR)
    os.system("git pull")
    os.chdir("..")

# =========================
# COMPILE xshield.c JIKA ADA
# =========================
c_file = os.path.join(TARGET_DIR, "xshield.c")
binary_file = os.path.join(TARGET_DIR, "xshield")

if os.path.isfile(c_file):
    print(f"{color.C}[INFO]{color.N} Meng-compile xshield.c...")
    os.system(f"{CC} {c_file} -o {binary_file}")
    print(f"{color.G}[INFO]{color.N} Compile selesai. Binary: {binary_file}")
else:
    print(f"{color.Y}[WARN]{color.N} xshield.c tidak ditemukan di repo!")

# =========================
# JALANKAN run.py YANG ADA DI REPO
# =========================
repo_run_py = os.path.join(TARGET_DIR, "run.py")
if os.path.isfile(repo_run_py):
    print(f"{color.C}[INFO]{color.N} Menjalankan run.py dari repo...")
    os.system(f"{sys.executable} {repo_run_py}")
else:
    print(f"{color.Y}[WARN]{color.N} run.py tidak ditemukan di repo!")

print(f"{color.G}[INFO]{color.N} Semua proses selesai.")