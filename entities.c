#include <jo/jo.h>
#include "config.h"
#include "world.h"
#include "entities.h"

ent_t ents[24];
int   n_ents = 0;
fx_t  fx[6];

static unsigned seed = 12345u;
unsigned rnd(void)
{
    seed = seed * 1103515245u + 12345u;
    return (seed >> 16) & 0x7FFF;
}

void entities_init(void)
{
    int i;
    n_ents = 0;
    for (i = 0; i < w_nspawns && n_ents < MAX_ENTS; i++) {
        ent_t *e = &ents[n_ents++];
        e->kind = w_spawns[i].kind;
        e->x = w_spawns[i].x + 8;
        e->y = w_spawns[i].y + 16;
        e->dx = e->dy = 0;
        e->timer = (int)(rnd() % 60);
        e->anim = (int)(rnd() % 32);
    }
    for (i = 0; i < MAX_FX; i++) fx[i].t = -1;
}

void entities_update(void)
{
    int i;
    for (i = 0; i < n_ents; i++) {
        ent_t *e = &ents[i];
        int nx, ny;
        e->anim++;
        if (--e->timer <= 0) {
            e->dx = (int)(rnd() % 3) - 1;
            e->dy = (int)(rnd() % 3) - 1;
            e->timer = 30 + (int)(rnd() % 60);
        }
        if (e->kind == 'S' && (e->anim & 1)) continue;     /* slime anda na metade da velocidade */
        if (e->anim & 1) continue;                          /* galinha: 1 px a cada 2 quadros */
        nx = e->x + e->dx;
        ny = e->y + e->dy;
        if (!world_blocked(nx / TILE, (ny - 2) / TILE) && nx > 8 && ny > 16 && nx < MAP_PX_W - 8 && ny < MAP_PX_H - 2) {
            e->x = nx; e->y = ny;
        } else {
            e->timer = 0;
        }
    }
}

void entities_gather(int px, int py)
{
    int i;
    for (i = 0; i < n_ents; i++) {
        ents[i].x = px + ((i % 6) - 3) * 28 + 14;
        ents[i].y = py - 70 + (i / 6) * 30;
        ents[i].dx = ents[i].dy = 0;
    }
}

void fx_spawn(int px, int py)
{
    int i;
    for (i = 0; i < MAX_FX; i++) {
        if (fx[i].t < 0) { fx[i].x = px; fx[i].y = py; fx[i].t = 0; return; }
    }
}

void fx_update(void)
{
    int i;
    for (i = 0; i < MAX_FX; i++) {
        if (fx[i].t >= 0 && ++fx[i].t >= 12) fx[i].t = -1;
    }
}
