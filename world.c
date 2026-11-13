#include <jo/jo.h>
#include "world.h"

unsigned char  w_ground[MAP_H][MAP_W];
unsigned char  w_obj[MAP_H][MAP_W];
unsigned short w_crop[MAP_H][MAP_W];
lamp_t  w_lamps[MAX_LAMPS];   int w_nlamps;
spawn_t w_spawns[MAX_SPAWNS]; int w_nspawns;

static int be16(const unsigned char *p) { return (p[0] << 8) | p[1]; }

/* ---- parser de LAMPS.TXT (linhas: "L x y raio" | "C x y" | "S x y" | "# comentario") */
static const char *skip_ws(const char *s) { while (*s == ' ' || *s == '\t' || *s == '\r') s++; return s; }
static int rd_int(const char **ps)
{
    const char *s = skip_ws(*ps);
    int v = 0, neg = 0;
    if (*s == '-') { neg = 1; s++; }
    while (*s >= '0' && *s <= '9') { v = v * 10 + (*s - '0'); s++; }
    *ps = s;
    return neg ? -v : v;
}

static void parse_lamps(const char *s)
{
    w_nlamps = 0; w_nspawns = 0;
    while (*s) {
        s = skip_ws(s);
        if (*s == 'L' && w_nlamps < MAX_LAMPS) {
            s++;
            w_lamps[w_nlamps].x = rd_int(&s);
            w_lamps[w_nlamps].y = rd_int(&s);
            w_lamps[w_nlamps].r = rd_int(&s);
            w_nlamps++;
        } else if ((*s == 'C' || *s == 'S') && w_nspawns < MAX_SPAWNS) {
            w_spawns[w_nspawns].kind = *s; s++;
            w_spawns[w_nspawns].x = rd_int(&s);
            w_spawns[w_nspawns].y = rd_int(&s);
            w_nspawns++;
        }
        while (*s && *s != '\n') s++;
        if (*s == '\n') s++;
    }
}

int world_load(void)
{
    int len = 0, x, y, n;
    char *p;
    const unsigned char *u;
    static char txt[1024];

    p = jo_fs_read_file("FARM64.MAP", &len);
    if (p == JO_NULL || len < 8 + MAP_W * MAP_H * 4)
        return 0;
    u = (const unsigned char *)p;
    if (u[0] != 'F' || u[1] != 'A' || u[2] != 'R' || u[3] != 'M' || be16(u + 4) != MAP_W || be16(u + 6) != MAP_H) {
        jo_free(p);
        return 0;
    }
    u += 8;
    for (y = 0; y < MAP_H; y++) for (x = 0; x < MAP_W; x++) w_ground[y][x] = u[y * MAP_W + x];
    u += MAP_W * MAP_H;
    for (y = 0; y < MAP_H; y++) for (x = 0; x < MAP_W; x++) w_obj[y][x] = u[y * MAP_W + x];
    u += MAP_W * MAP_H;
    for (y = 0; y < MAP_H; y++) for (x = 0; x < MAP_W; x++) w_crop[y][x] = (unsigned short)be16(u + (y * MAP_W + x) * 2);
    jo_free(p);

    len = 0;
    p = jo_fs_read_file("LAMPS.TXT", &len);
    if (p != JO_NULL) {
        n = len < (int)sizeof(txt) - 1 ? len : (int)sizeof(txt) - 1;
        for (x = 0; x < n; x++) txt[x] = p[x];
        txt[n] = 0;
        jo_free(p);
        parse_lamps(txt);
    }
    return 1;
}

int world_blocked(int tx, int ty)
{
    int o;
    if (tx < 0 || ty < 0 || tx >= MAP_W || ty >= MAP_H)
        return 1;
    if (w_ground[ty][tx] == T_W0 || w_ground[ty][tx] == T_W1)
        return 1;
    o = w_obj[ty][tx];
    if (o && (o - 1) != S_CANOPY)
        return 1;
    return 0;
}

static int free_tile(int tx, int ty)
{
    return tx >= 0 && ty >= 0 && tx < MAP_W && ty < MAP_H && !w_obj[ty][tx] && !w_crop[ty][tx];
}

int world_till(int tx, int ty)
{
    if (!free_tile(tx, ty)) return 0;
    if (w_ground[ty][tx] <= T_D1) { w_ground[ty][tx] = T_TIL; return 1; }
    return 0;
}

int world_water(int tx, int ty)
{
    if (tx < 0 || ty < 0 || tx >= MAP_W || ty >= MAP_H) return 0;
    if (w_ground[ty][tx] != T_TIL && w_ground[ty][tx] != T_WET) return 0;
    w_ground[ty][tx] = T_WET;
    if (w_crop[ty][tx]) w_crop[ty][tx] |= CROP_WET;
    return 1;
}

int world_plant(int tx, int ty, int type)
{
    if (!free_tile(tx, ty) || type < 1 || type > 6) return 0;
    if (w_ground[ty][tx] != T_TIL && w_ground[ty][tx] != T_WET) return 0;
    w_crop[ty][tx] = (unsigned short)(type | (w_ground[ty][tx] == T_WET ? CROP_WET : 0));
    return 1;
}

int world_harvest(int tx, int ty)
{
    if (tx < 0 || ty < 0 || tx >= MAP_W || ty >= MAP_H) return 0;
    if (!w_crop[ty][tx] || CROP_STAGE(w_crop[ty][tx]) < 4) return 0;
    w_crop[ty][tx] = 0;
    return 1;
}

void world_new_day(void)
{
    int x, y;
    for (y = 0; y < MAP_H; y++) {
        for (x = 0; x < MAP_W; x++) {
            unsigned short c = w_crop[y][x];
            if (c) {
                if ((c & CROP_WET) && CROP_STAGE(c) < 4)
                    c = (unsigned short)(c + (1 << 3));
                c &= (unsigned short)~CROP_WET;
                w_crop[y][x] = c;
            }
            if (w_ground[y][x] == T_WET) w_ground[y][x] = T_TIL;
        }
    }
}
