
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

int main() {
    unsigned char key[4];

    // Key asli builder
    for(int i=0;i<4;i++)
        key[i] = k_part1[i] ^ k_part2[i];

    unsigned char *out = malloc(payload_len);
    if (!out) return 1;

    for(unsigned int i=0;i<payload_len;i++)
        out[i] = payload[i] ^ key[i % 4];

    FILE *fp = fopen(".a.sh", "wb");
    if (!fp) { free(out); return 1; }

    fwrite(out, 1, payload_len, fp);
    fclose(fp);

    chmod(".a.sh", 0700);
    system("/system/bin/sh .a.sh");

    free(out);
    return 0;
}