#ifndef WORLD_H
#define WORLD_H
#include "config.h"

/* ids de terreno (TRNxx) */
enum { T_G0, T_G1, T_G2, T_D0, T_D1, T_TIL, T_WET, T_PA0, T_PA1, T_W0, T_W1, T_SHN, T_SHS, T_SHE, T_SHW, T_SAND };
/* ids de estrutura (STRxx); no mapa o valor armazenado e id+1 (0 = vazio) */
enum { S_FH, S_FV, S_FP, S_TRUNK, S_CANOPY, S_ROCK, S_BUSH, S_WFLOOR, S_WWALL, S_RL, S_RM, S_RR, S_DOOR, S_WIN, S_SIGN, S_CHEST };

/* cultura: bits 0-2 tipo (1..6), 3-5 estagio (0..4), 6 regado */
#define CROP_TYPE(c)   ((c) & 7)
#define CROP_STAGE(c)  (((c) >> 3) & 7)
#define CROP_WET       0x40

typedef struct { int x, y, r; } lamp_t;
typedef struct { char kind; int x, y; } spawn_t;

extern unsigned char  w_ground[MAP_H][MAP_W];
extern unsigned char  w_obj[MAP_H][MAP_W];
extern unsigned short w_crop[MAP_H][MAP_W];
extern lamp_t  w_lamps[MAX_LAMPS];   extern int w_nlamps;
extern spawn_t w_spawns[MAX_SPAWNS]; extern int w_nspawns;

int  world_load(void);                 /* le FARM64.MAP e LAMPS.TXT do CD; 1 = ok */
int  world_blocked(int tx, int ty);
int  world_till(int tx, int ty);       /* enxada */
int  world_water(int tx, int ty);
int  world_plant(int tx, int ty, int type);
int  world_harvest(int tx, int ty);    /* 1 se colheu */
void world_new_day(void);

#endif
