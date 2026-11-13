#ifndef AUDIO_H
#define AUDIO_H

enum { SFX_HOE, SFX_WATER, SFX_PLANT, SFX_HARVEST, SFX_PICKUP, SFX_CURSOR, SFX_OK, SFX_SIZZLE, SFX_DING, SFX_SWING, SFX_HIT, SFX_ROCK, SFX_COUNT };

int  audio_init(void);                 /* carrega os 12 PCM; retorna quantos carregaram */
void sfx_play(int id);
const char *sfx_name(int id);

/* musica CD-DA: 0 = parada, 1 = faixa 2 (fazenda), 2 = faixa 3 (mina). Cada chamada avanca o ciclo. */
int  music_cycle(void);
int  music_state(void);

#endif
