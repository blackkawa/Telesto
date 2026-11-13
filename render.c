/* Mapa de tiles desenhado com sprites VDP1 de 8 bits (nao e um plano VDP2 - ver README).
   Cada tile escolhe um banco de paleta (0..3) conforme a distancia das lampadas. */
#include <jo/jo.h>
#include "config.h"
#include "game.h"
#include "assets.h"
#include "palfx.h"
#include "world.h"
#include "entities.h"
#include "render.h"

static int drawn;

static void spr(int id, int x, int y, int z, int bank)
{
    palfx_bind(bank);
    jo_sprite_draw3D2(id, x, y, z);       /* coordenadas a partir do canto superior esquerdo */
    drawn++;
}

/* banco de luz do tile: 0 = ambiente ... 3 = junto da lampada */
static int tile_bank(int tx, int ty, int lamps_on)
{
    int i, best = 0;
    if (!lamps_on) return 0;
    for (i = 0; i < w_nlamps; i++) {
        int dx = tx - w_lamps[i].x, dy = ty - w_lamps[i].y;
        int r2 = w_lamps[i].r * w_lamps[i].r;
        int d2 = dx * dx + dy * dy;
        if (d2 < r2) {
            int lv = ((r2 - d2) * 4) / r2;
            if (lv > PAL_BANKS - 1) lv = PAL_BANKS - 1;
            if (lv > best) best = lv;
        }
    }
    return best;
}

int render_frame(int camx, int camy, int lamps_on)
{
    int tx0 = camx / TILE, ty0 = camy / TILE;
    int ox = camx % TILE, oy = camy % TILE;
    int ix, iy, i;
    drawn = 0;

    for (iy = 0; iy < SCREEN_H / TILE + 1; iy++) {
        int ty = ty0 + iy;
        if (ty >= MAP_H) break;
        for (ix = 0; ix < SCREEN_W / TILE + 1; ix++) {
            int tx = tx0 + ix;
            int sx, sy, b;
            unsigned short c;
            if (tx >= MAP_W) break;
            sx = ix * TILE - ox;
            sy = iy * TILE - oy;
            b = tile_bank(tx, ty, lamps_on);
            spr(spr_trn[w_ground[ty][tx]], sx, sy, Z_GROUND, b);
            c = w_crop[ty][tx];
            if (c) spr(spr_crop[CROP_TYPE(c)][CROP_STAGE(c)], sx, sy, Z_CROP, b);
            if (w_obj[ty][tx]) spr(spr_str[w_obj[ty][tx] - 1], sx, sy, Z_OBJECT, b);
        }
    }

    /* entidades (24) */
    for (i = 0; i < n_ents; i++) {
        ent_t *e = &ents[i];
        int w = (e->kind == 'S') ? 32 : 16;
        int h = w;
        int sx = e->x - w / 2 - camx, sy = e->y - h - camy;
        int b;
        if (sx < -w || sy < -h || sx > SCREEN_W || sy > SCREEN_H) continue;
        b = tile_bank(e->x / TILE, e->y / TILE, lamps_on);
        if (e->kind == 'S') spr(spr_slm[(e->anim >> 4) & 3], sx, sy, Z_CHAR - (e->y >> 4), b);
        else                spr(spr_chk[(e->anim >> 3) & 3], sx, sy, Z_CHAR - (e->y >> 4), b);
    }

    /* jogador 32x48 (esquerda = direita espelhada) */
    {
        int sx = G.px - 16 - camx, sy = G.py - 48 - camy;
        int b = tile_bank(G.px / TILE, G.py / TILE, lamps_on);
        int row = (G.facing == FACE_L) ? FACE_R : G.facing;
        int frame = (G.walk_t >> 3) & 3;
        if (G.facing == FACE_L) jo_sprite_enable_horizontal_flip();
        spr(spr_pl[row][frame], sx, sy, Z_CHAR - (G.py >> 4), b);
        if (G.facing == FACE_L) jo_sprite_disable_horizontal_flip();
    }

    /* poeira */
    for (i = 0; i < MAX_FX; i++) {
        if (fx[i].t >= 0)
            spr(spr_dst[fx[i].t / 3], fx[i].x - camx, fx[i].y - camy, Z_FX, 0);
    }

    /* HUD: enxada, regador, saco de sementes */
    spr(spr_icn[0], 4,  4, Z_HUD, 3);
    spr(spr_icn[1], 24, 4, Z_HUD, 3);
    spr(spr_icn[2], 44, 4, Z_HUD, 3);
    return drawn;
}
