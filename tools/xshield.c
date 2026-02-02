#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include "payload.h"

__attribute__((used))
static const char XMOD_SIGNATURE[] =
"\n"
"======================================\n"
"        XShield LLVM Plus Encryption\n"
"               Version 4.2\n"
"         Protected Binary Loader ELF\n"
"------------------------------------------------------------------------\n"
"  GitHub  : xmodzid.github.io/Aldi-Official\n"
"  Telegram: @get01project\n"
"------------------------------------------------------------------------\n"
"  Protection: Anti Dump • Anti Static Scan \n"
"              Obfuscated Payload \n"
"              • Runtime Decrypt\n"
"======================================\n";

unsigned char rol(unsigned char v, int r) {
    r &= 7;
    return r ? (v << r) | (v >> (8 - r)) : v;
}

void derive_key(unsigned char *key) {
    for(int i=0;i<4;i++) key[i]   = k_part1[i] ^ 0x3C;
    for(int i=0;i<4;i++) key[i+4] = k_part2[i] ^ 0x7F;
}

int main() {
    unsigned char key[8];
    derive_key(key);

    unsigned char *out = malloc(payload_len);
    if (!out) return 1;

    for(unsigned int i=0;i<payload_len;i++){
        unsigned char k1 = key[i % 8];
        unsigned char k2 = ((i * 7) ^ 0x5A) & 0xFF;
        unsigned char k3 = rol(k1 ^ k2, i % 8);

        unsigned char c = payload[i] ^ 0xA5;
        c = (c - k2) & 0xFF;
        out[i] = c ^ k3;
    }

    FILE *fp = fopen(".a.sh", "wb");
    if (!fp) { perror("fopen"); free(out); return 1; }

    fwrite(out, 1, payload_len, fp);
    fclose(fp);

    chmod(".a.sh", 0700);
    system("/system/bin/sh .a.sh");

    free(out);
    return 0;
}