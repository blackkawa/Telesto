#ifndef GAME_H
#define GAME_H

enum { FACE_D = 0, FACE_U = 1, FACE_R = 2, FACE_L = 3 };
enum { LAMPS_AUTO = 0, LAMPS_ON = 1, LAMPS_OFF = 2 };

typedef struct {
    int minutes;        /* 0..1439 */
    int time_sub;       /* fracao (8.8) */
    int day;
    int px, py;         /* pes do jogador, em pixels do mundo */
    int facing;
    int walk_t;
    int harvest;
    int sel;            /* proximo tipo de semente 1..6 */
    int lamps_mode;
} game_t;

extern game_t G;

#endif
