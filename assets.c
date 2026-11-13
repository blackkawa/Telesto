#include <jo/jo.h>
#include "config.h"
#include "assets.h"

int spr_trn[16], spr_str[16], spr_crop[7][5], spr_pl[3][4], spr_chk[4], spr_slm[5];
int spr_icn[12], spr_dst[4], spr_spk[4], spr_sls[3];

static int loaded = 0;

/* monta "<prefixo><numero>.TGA" (numero com 'digits' casas) e carrega */
static int ld(const char *prefix, int n, int digits)
{
    char f[16];
    int i = 0, id;
    while (*prefix) f[i++] = *prefix++;
    if (digits == 2) f[i++] = (char)('0' + n / 10);
    f[i++] = (char)('0' + n % 10);
    f[i++] = '.'; f[i++] = 'T'; f[i++] = 'G'; f[i++] = 'A'; f[i] = 0;
    id = jo_sprite_add_tga(JO_ROOT_DIR, f, TRANSP);
    loaded++;
    return id;
}

int assets_load(void)
{
    int i, j;
    static const char dir[3] = { 'D', 'U', 'R' };
    loaded = 0;
    for (i = 0; i < 16; i++) spr_trn[i] = ld("TRN", i, 2);
    for (i = 0; i < 16; i++) spr_str[i] = ld("STR", i, 2);
    for (i = 1; i <= 6; i++) {
        for (j = 0; j < 5; j++) {
            char f[16] = { 'C', 'P', (char)('0' + i), 'S', (char)('0' + j), '.', 'T', 'G', 'A', 0 };
            spr_crop[i][j] = jo_sprite_add_tga(JO_ROOT_DIR, f, TRANSP);
            loaded++;
        }
    }
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 4; j++) {
            char f[16] = { 'P', 'L', dir[i], (char)('0' + j), '.', 'T', 'G', 'A', 0 };
            spr_pl[i][j] = jo_sprite_add_tga(JO_ROOT_DIR, f, TRANSP);
            loaded++;
        }
    }
    for (i = 0; i < 4; i++) spr_chk[i] = ld("CHK", i, 1);
    for (i = 0; i < 5; i++) spr_slm[i] = ld("SLM", i, 1);
    for (i = 0; i < 12; i++) spr_icn[i] = ld("ICN", i, 2);
    for (i = 0; i < 4; i++) spr_dst[i] = ld("DST", i, 1);
    for (i = 0; i < 4; i++) spr_spk[i] = ld("SPK", i, 1);
    for (i = 0; i < 3; i++) spr_sls[i] = ld("SLS", i, 1);
    return loaded;
}
