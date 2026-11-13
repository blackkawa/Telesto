/* Layout do save (SAVE_SIZE = 7168 bytes):
     0..3    "FSAV"          4 versao        5 modo das lampadas
     6..7 dia   8..9 minutos   10..11 px   12..13 py   14..15 colhidos   16 semente   17 direcao
     18..19  soma de verificacao (bytes 64..4671)
     64..4159    culturas (1 byte por tile: tipo | estagio<<3 | regado<<6)
     4160..4671  bitmap de tiles arados (1 bit por tile)
     4672..7167  reservado (inventario, NPCs, animais ...), zeros */
#include <jo/jo.h>
#include "config.h"
#include "game.h"
#include "world.h"
#include "save.h"

#define OFF_CROP  64
#define OFF_TILL  (OFF_CROP + MAP_W * MAP_H)
#define OFF_END   (OFF_TILL + MAP_W * MAP_H / 8)

static unsigned char buf[SAVE_SIZE];
static char fname[]   = "FARMPROT";
static char comment[] = "FARM PROTO";
static int mounted = 0;

static void put16(int o, int v) { buf[o] = (unsigned char)(v >> 8); buf[o + 1] = (unsigned char)v; }
static int  get16(const unsigned char *b, int o) { return (b[o] << 8) | b[o + 1]; }

static int checksum(const unsigned char *b)
{
    unsigned s = 0;
    int i;
    for (i = OFF_CROP; i < OFF_END; i++) s = (s + b[i]) & 0xFFFF;
    return (int)s;
}

int save_init(void)
{
    mounted = jo_backup_mount(JoInternalMemoryBackup);
    return mounted;
}

int save_exists(void)
{
    return mounted && jo_backup_file_exists(JoInternalMemoryBackup, fname);
}

int save_write(void)
{
    int x, y, i;
    if (!mounted) return 0;
    for (i = 0; i < SAVE_SIZE; i++) buf[i] = 0;
    buf[0] = 'F'; buf[1] = 'S'; buf[2] = 'A'; buf[3] = 'V'; buf[4] = 1;
    buf[5] = (unsigned char)G.lamps_mode;
    put16(6, G.day); put16(8, G.minutes); put16(10, G.px); put16(12, G.py);
    put16(14, G.harvest); buf[16] = (unsigned char)G.sel; buf[17] = (unsigned char)G.facing;
    for (y = 0; y < MAP_H; y++) {
        for (x = 0; x < MAP_W; x++) {
            i = y * MAP_W + x;
            buf[OFF_CROP + i] = (unsigned char)(w_crop[y][x] & 0x7F);
            if (w_ground[y][x] == T_TIL || w_ground[y][x] == T_WET)
                buf[OFF_TILL + (i >> 3)] |= (unsigned char)(1 << (i & 7));
        }
    }
    put16(18, checksum(buf));
    return jo_backup_save_file_contents(JoInternalMemoryBackup, fname, comment, buf, SAVE_SIZE) ? 1 : 0;
}

int save_read(void)
{
    unsigned int len = 0;
    unsigned char *p;
    int x, y;
    if (!mounted || !save_exists()) return 0;
    p = (unsigned char *)jo_backup_load_file_contents(JoInternalMemoryBackup, fname, &len);
    if (p == JO_NULL) return 0;
    if (len < OFF_END || p[0] != 'F' || p[1] != 'S' || p[2] != 'A' || p[3] != 'V' || get16(p, 18) != checksum(p)) {
        jo_free(p);
        return 0;
    }
    if (!world_load()) { jo_free(p); return 0; }     /* base do CD (testa a carga do pacote) */
    G.lamps_mode = p[5]; G.day = get16(p, 6); G.minutes = get16(p, 8);
    G.px = get16(p, 10); G.py = get16(p, 12); G.harvest = get16(p, 14);
    G.sel = p[16] ? p[16] : 1; G.facing = p[17] & 3;
    for (y = 0; y < MAP_H; y++) {
        for (x = 0; x < MAP_W; x++) {
            int i = y * MAP_W + x;
            unsigned c = p[OFF_CROP + i];
            int tilled = (p[OFF_TILL + (i >> 3)] >> (i & 7)) & 1;
            if (CROP_TYPE(c) > 6) c = 0;
            w_crop[y][x] = (unsigned short)c;
            if (tilled) {
                if (w_ground[y][x] <= T_D1 || w_ground[y][x] == T_WET) w_ground[y][x] = (c & CROP_WET) ? T_WET : T_TIL;
            } else if (w_ground[y][x] == T_TIL || w_ground[y][x] == T_WET) {
                w_ground[y][x] = T_G0;
            }
        }
    }
    jo_free(p);
    return 1;
}
