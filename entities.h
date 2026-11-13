#ifndef ENTITIES_H
#define ENTITIES_H

typedef struct {
    int x, y;           /* pes (centro-baixo), em pixels do mundo */
    int kind;           /* 'C' galinha, 'S' slime */
    int dx, dy, timer;
    int anim;
} ent_t;

extern ent_t ents[24];
extern int   n_ents;

void entities_init(void);                      /* cria os 24 a partir de w_spawns */
void entities_update(void);
void entities_gather(int px, int py);          /* junta os 24 ao redor de (px,py): teste de carga */

typedef struct { int x, y, t; } fx_t;
void fx_spawn(int px, int py);
void fx_update(void);
extern fx_t fx[6];

unsigned rnd(void);

#endif
