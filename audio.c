#include <jo/jo.h>
#include "audio.h"

#define PCM_RATE 15360

static jo_sound snd[SFX_COUNT];
static int ok[SFX_COUNT];
static int mus = 0;

static const char *const FILES[SFX_COUNT] = {
    "HOE.PCM", "WATER.PCM", "PLANT.PCM", "HARVEST.PCM", "PICKUP.PCM", "CURSOR.PCM",
    "OK.PCM", "SIZZLE.PCM", "DING.PCM", "SWING.PCM", "HIT.PCM", "ROCK.PCM"
};
static const char *const NAMES[SFX_COUNT] = {
    "HOE", "WATER", "PLANT", "HARVEST", "PICKUP", "CURSOR", "OK", "SIZZLE", "DING", "SWING", "HIT", "ROCK"
};

int audio_init(void)
{
    int i, n = 0;
    for (i = 0; i < SFX_COUNT; i++) {
        /* PCM cru, 16 bits, mono, big-endian, 15.360 Hz */
        ok[i] = jo_audio_load_pcm(FILES[i], JoSoundMono16Bit, &snd[i]);
        if (ok[i]) {
            snd[i].sample_rate = PCM_RATE;
            n++;
        }
    }
    jo_audio_set_volume(100);   /* ajuste se a faixa de volume do Jo for diferente */
    return n;
}

void sfx_play(int id)
{
    if (id >= 0 && id < SFX_COUNT && ok[id])
        jo_audio_play_sound(&snd[id]);
}

const char *sfx_name(int id) { return NAMES[id]; }

int music_cycle(void)
{
    mus = (mus + 1) % 3;
    if (mus == 0)      jo_audio_stop_cd();
    else if (mus == 1) jo_audio_play_cd_track(2, 2, 1);
    else               jo_audio_play_cd_track(3, 3, 1);
    return mus;
}

int music_state(void) { return mus; }
