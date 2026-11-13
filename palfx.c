/* Paletas: 4 bancos de 256 entradas (so 128 usadas). O pixel de um sprite = 16*grupo + indice.
   Banco b = mistura entre a cor com a tintura da fase do dia (b = 0) e a cor plena (b = 3).
   Assim, o chao perto de uma lampada usa um banco mais claro que o chao longe dela. */
#include <jo/jo.h>
#include "config.h"
#include "palettes_bank.h"
#include "palfx.h"

static jo_palette bank[PAL_BANKS];
static unsigned short cur[PAL_BANKS][PAL_ENTRIES];
static volatile int dirty = 0;
static int cram_direct = 0;
static int bound = -1;
static int writes = 0;

typedef struct { short minute; short r, g, b; } kf_t;   /* tintura em 1/256 */
static const kf_t KF[] = {
    {    0,  70,  85, 170 },   /* noite */
    {  300,  70,  85, 170 },
    {  420, 210, 170, 190 },   /* amanhecer */
    {  540, 256, 256, 256 },   /* dia */
    { 1020, 256, 256, 256 },
    { 1140, 256, 175, 130 },   /* entardecer */
    { 1260,  70,  85, 170 },   /* noite */
    { 1440,  70,  85, 170 }
};
#define KF_N ((int)(sizeof(KF) / sizeof(KF[0])))

void palfx_init(void)
{
    int b;
    unsigned a;
    for (b = 0; b < PAL_BANKS; b++)
        jo_create_palette(&bank[b]);
    /* Obrigatorio para TGA de 8 bits: o carregador preenche esta paleta (nos a reescrevemos depois). */
    jo_set_tga_default_palette(&bank[0]);
    a = (unsigned)(unsigned long)(bank[0].data) & 0x0FFFFFFFu;
    cram_direct = (a >= 0x05F00000u && a < 0x05F01000u);
}

static void lerp_tint(int minutes, int *r, int *g, int *b)
{
    int i;
    for (i = 0; i < KF_N - 1; i++) {
        if (minutes <= KF[i + 1].minute) {
            int span = KF[i + 1].minute - KF[i].minute;
            int t = minutes - KF[i].minute;
            if (span <= 0) span = 1;
            *r = KF[i].r + ((KF[i + 1].r - KF[i].r) * t) / span;
            *g = KF[i].g + ((KF[i + 1].g - KF[i].g) * t) / span;
            *b = KF[i].b + ((KF[i + 1].b - KF[i].b) * t) / span;
            return;
        }
    }
    *r = KF[KF_N - 1].r; *g = KF[KF_N - 1].g; *b = KF[KF_N - 1].b;
}

void palfx_set_time(int minutes)
{
    int tr, tg, tb, bk, i;
    lerp_tint(minutes, &tr, &tg, &tb);
    for (bk = 0; bk < PAL_BANKS; bk++) {
        int mr = tr + ((256 - tr) * bk) / (PAL_BANKS - 1);
        int mg = tg + ((256 - tg) * bk) / (PAL_BANKS - 1);
        int mb = tb + ((256 - tb) * bk) / (PAL_BANKS - 1);
        for (i = 0; i < PAL_ENTRIES; i++) {
            unsigned c = PAL_BASE[i];
            unsigned r = ((c & 31) * mr) >> 8;
            unsigned g = (((c >> 5) & 31) * mg) >> 8;
            unsigned b = (((c >> 10) & 31) * mb) >> 8;
            if (r > 31) r = 31;
            if (g > 31) g = 31;
            if (b > 31) b = 31;
            cur[bk][i] = (unsigned short)((b << 10) | (g << 5) | r);
        }
    }
    dirty = 1;
}

void palfx_commit_now(void)
{
    int bk, i;
    for (bk = 0; bk < PAL_BANKS; bk++) {
        for (i = 0; i < PAL_ENTRIES; i++) {
            unsigned short c = (unsigned short)(cur[bk][i] | 0x8000);
            if (bank[bk].data)
                bank[bk].data[i + PAL_BIAS] = c;
            /* Se a paleta nao aponta para a Color RAM, escreve pelo registrador (indice absoluto = banco*256 + i). */
            if (!cram_direct)
                jo_set_palette_register((unsigned short)(bank[bk].id * 256 + i + PAL_BIAS), c);
        }
    }
    writes++;
    dirty = 0;
}

void palfx_vblank(void)
{
    if (dirty)
        palfx_commit_now();
}

void palfx_bind(int b)
{
    if (b == bound)
        return;
    bound = b;
    jo_sprite_set_palette(bank[b].id);
}

int palfx_cram_direct(void) { return cram_direct; }
int palfx_bank_id(int b)    { return bank[b].id; }
int palfx_writes(void)      { return writes; }
