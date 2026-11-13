#ifndef CONFIG_H
#define CONFIG_H

/* ------------------------------------------------------------------ tela / mapa */
#define SCREEN_W        320
#define SCREEN_H        224
#define TILE            16
#define MAP_W           64
#define MAP_H           64
#define MAP_PX_W        (MAP_W * TILE)
#define MAP_PX_H        (MAP_H * TILE)

/* ------------------------------------------------------------------ itens a CONFIRMAR no primeiro boot (ver README, secao "Pontos a confirmar") */
/* Cor transparente passada ao jo_sprite_add_tga. Para TGA de 8 bits a documentacao diz "use JO_COLOR_Transparent". */
#define TRANSP          JO_COLOR_Transparent
/* Se as cores aparecerem deslocadas por 1 indice (o Jo diz que "o primeiro indice da paleta e 1"), troque para 1. */
#define PAL_BIAS        0

/* ------------------------------------------------------------------ paletas / luz */
#define PAL_BANKS       4           /* banco 0 = luz ambiente da fase do dia ... banco 3 = luz plena (lampada) */
#define MINUTES_PER_DAY 1440
#define TIME_SPEED      51          /* minutos de jogo por quadro em ponto fixo 8.8 (51 = ~12 min/s a 60 fps) */
#define NEW_DAY_MINUTE  360         /* 06:00: culturas regadas crescem */

/* ------------------------------------------------------------------ save */
#define SAVE_SIZE       7168        /* bytes gravados: meta do teste de ~7 KB */

/* ------------------------------------------------------------------ profundidade (maior = mais longe; plano proximo de corte = 80) */
#define Z_GROUND        500
#define Z_CROP          480
#define Z_OBJECT        460
#define Z_CHAR          440         /* personagens: Z_CHAR - (y / 16) para ordenar por linha */
#define Z_FX            420
#define Z_HUD           120

/* ------------------------------------------------------------------ limites */
#define MAX_LAMPS       8
#define MAX_SPAWNS      32
#define MAX_ENTS        24
#define MAX_FX          6

#endif
