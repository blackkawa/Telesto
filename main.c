/* Prototipo "fazenda 2D" para Sega Saturn / Jo Engine.
   Testa: mapa 64x64, paletas regeneradas no VBLANK (dia/noite + luz de lampadas), save de ~7 KB,
   carga de pacote do CD, PCM junto com CD-DA e 24 sprites animados em cena. */
#include <jo/jo.h>
#include "config.h"
#include "game.h"
#include "palfx.h"
#include "assets.h"
#include "world.h"
#include "entities.h"
#include "render.h"
#include "audio.h"
#include "save.h"

game_t G;

static int camx, camy;
static int spr_count = 0;
static int msg_t = 0;
static char msg[40] = "";
static int sfx_test = 0;
static int boot_assets = 0, boot_sfx = 0, boot_map = 0, boot_save = 0;

/* ------------------------------------------------------------------ texto de depuracao */
static int put_int(char *d, int v, int width, char pad)
{
    char t[12];
    int n = 0, i, k = 0;
    if (v < 0) { d[k++] = '-'; v = -v; }
    if (v == 0) t[n++] = '0';
    while (v > 0) { t[n++] = (char)('0' + v % 10); v /= 10; }
    for (i = n; i < width; i++) d[k++] = pad;
    for (i = n - 1; i >= 0; i--) d[k++] = t[i];
    return k;
}

static int put_str(char *d, const char *s)
{
    int k = 0;
    while (s[k]) { d[k] = s[k]; k++; }
    return k;
}

static void line(int row, const char *s)
{
    char b[41];
    int i = 0;
    while (s[i] && i < 40) { b[i] = s[i]; i++; }
    while (i < 40) b[i++] = ' ';
    b[40] = 0;
    jo_printf(0, row, "%s", b);
}

static void say(const char *s)
{
    int i = 0;
    while (s[i] && i < 39) { msg[i] = s[i]; i++; }
    msg[i] = 0;
    msg_t = 180;
}

static void hud(void)
{
    char b[48];
    int k;

    k = 0;
    k += put_str(b + k, "FPS ");  k += put_int(b + k, jo_core_get_fps(), 2, ' ');
    k += put_str(b + k, " SPR ");  k += put_int(b + k, spr_count, 3, ' ');
    k += put_str(b + k, " DIA ");  k += put_int(b + k, G.day, 1, '0');
    k += put_str(b + k, " ");      k += put_int(b + k, G.minutes / 60, 2, '0');
    k += put_str(b + k, ":");      k += put_int(b + k, G.minutes % 60, 2, '0');
    b[k] = 0; line(24, b);

    k = 0;
    k += put_str(b + k, "LUZ ");
    k += put_str(b + k, G.lamps_mode == LAMPS_AUTO ? "auto" : (G.lamps_mode == LAMPS_ON ? "on  " : "off "));
    k += put_str(b + k, " CRAM ");
    k += put_str(b + k, palfx_cram_direct() ? "direto" : "REG   ");
    k += put_str(b + k, " PAL ");  k += put_int(b + k, palfx_writes(), 1, '0');
    k += put_str(b + k, " COL ");  k += put_int(b + k, G.harvest, 1, '0');
    b[k] = 0; line(25, b);

    k = 0;
    k += put_str(b + k, "TGA "); k += put_int(b + k, boot_assets, 1, '0');
    k += put_str(b + k, " SFX "); k += put_int(b + k, boot_sfx, 1, '0');
    k += put_str(b + k, " MAP "); k += put_int(b + k, boot_map, 1, '0');
    k += put_str(b + k, " SAV "); k += put_str(b + k, save_exists() ? "sim" : "nao");
    k += put_str(b + k, " MUS "); k += put_int(b + k, music_state(), 1, '0');
    b[k] = 0; line(26, b);

    if (msg_t > 0) { msg_t--; line(27, msg); }
    else           line(27, "A enxada B agua C planta X hora Y luz");
}

/* ------------------------------------------------------------------ tempo */
static void time_add(int minutes)
{
    while (minutes-- > 0) {
        G.minutes++;
        if (G.minutes >= MINUTES_PER_DAY) G.minutes = 0;
        if (G.minutes == NEW_DAY_MINUTE) { G.day++; world_new_day(); }
    }
}

static int lamps_on(void)
{
    if (G.lamps_mode == LAMPS_ON) return 1;
    if (G.lamps_mode == LAMPS_OFF) return 0;
    return G.minutes >= 18 * 60 || G.minutes < 6 * 60;
}

/* ------------------------------------------------------------------ jogador */
static void facing_tile(int *tx, int *ty)
{
    int dx = 0, dy = 0;
    switch (G.facing) {
        case FACE_D: dy = 1; break;
        case FACE_U: dy = -1; break;
        case FACE_R: dx = 1; break;
        default:     dx = -1; break;
    }
    *tx = G.px / TILE + dx;
    *ty = (G.py - 4) / TILE + dy;
}

static int walkable(int x, int y)
{
    return !world_blocked((x - 6) / TILE, (y - 2) / TILE) && !world_blocked((x + 6) / TILE, (y - 2) / TILE);
}

static void player_move(void)
{
    int dx = 0, dy = 0;
    if (jo_is_pad1_key_pressed(JO_KEY_LEFT))  { dx = -2; G.facing = FACE_L; }
    if (jo_is_pad1_key_pressed(JO_KEY_RIGHT)) { dx =  2; G.facing = FACE_R; }
    if (jo_is_pad1_key_pressed(JO_KEY_UP))    { dy = -2; G.facing = FACE_U; }
    if (jo_is_pad1_key_pressed(JO_KEY_DOWN))  { dy =  2; G.facing = FACE_D; }
    if (dx || dy) G.walk_t++; else G.walk_t = 0;
    if (dx && walkable(G.px + dx, G.py)) G.px += dx;
    if (dy && walkable(G.px, G.py + dy)) G.py += dy;
    if (G.px < 8) G.px = 8;
    if (G.py < 8) G.py = 8;
    if (G.px > MAP_PX_W - 8) G.px = MAP_PX_W - 8;
    if (G.py > MAP_PX_H - 2) G.py = MAP_PX_H - 2;
}

static void actions(void)
{
    int tx, ty;
    facing_tile(&tx, &ty);

    if (jo_is_pad1_key_pressed(JO_KEY_L) && jo_is_pad1_key_pressed(JO_KEY_R)) {
        if (jo_is_pad1_key_down(JO_KEY_L) || jo_is_pad1_key_down(JO_KEY_R)) {
            entities_gather(G.px, G.py);
            say("24 sprites reunidos");
        }
        return;
    }
    if (jo_is_pad1_key_down(JO_KEY_A)) {
        if (world_harvest(tx, ty)) { G.harvest++; sfx_play(SFX_HARVEST); fx_spawn(tx * TILE, ty * TILE); say("Colheu!"); }
        else if (world_till(tx, ty)) { sfx_play(SFX_HOE); fx_spawn(tx * TILE, ty * TILE); }
        else sfx_play(SFX_CURSOR);
    }
    if (jo_is_pad1_key_down(JO_KEY_B)) {
        if (world_water(tx, ty)) sfx_play(SFX_WATER); else sfx_play(SFX_CURSOR);
    }
    if (jo_is_pad1_key_down(JO_KEY_C)) {
        if (world_plant(tx, ty, G.sel)) {
            sfx_play(SFX_PLANT);
            G.sel = G.sel % 6 + 1;
        } else sfx_play(SFX_CURSOR);
    }
    if (jo_is_pad1_key_down(JO_KEY_X)) { time_add(180); sfx_play(SFX_OK); }
    if (jo_is_pad1_key_down(JO_KEY_Y)) {
        G.lamps_mode = (G.lamps_mode + 1) % 3;
        sfx_play(SFX_OK);
    }
    if (jo_is_pad1_key_down(JO_KEY_Z)) {
        if (save_write()) { sfx_play(SFX_DING); say("Salvo (7168 bytes)"); }
        else say("Falha ao salvar");
    }
    if (jo_is_pad1_key_down(JO_KEY_START)) {
        if (save_read()) { sfx_play(SFX_DING); say("Carregado"); }
        else say("Sem save valido");
    }
    if (jo_is_pad1_key_down(JO_KEY_L)) {
        int s = music_cycle();
        say(s == 0 ? "Musica parada" : (s == 1 ? "CD-DA faixa 2" : "CD-DA faixa 3"));
    }
    if (jo_is_pad1_key_down(JO_KEY_R)) {
        sfx_play(sfx_test);
        say(sfx_name(sfx_test));
        sfx_test = (sfx_test + 1) % SFX_COUNT;
    }
}

/* ------------------------------------------------------------------ quadro */
static void game_frame(void)
{
    if (jo_is_pad1_available()) {
        player_move();
        actions();
    }
    G.time_sub += TIME_SPEED;
    if (G.time_sub >= 256) { time_add(G.time_sub >> 8); G.time_sub &= 255; }
    palfx_set_time(G.minutes);          /* recalcula; a Color RAM e escrita no VBLANK */

    entities_update();
    fx_update();

    camx = G.px - SCREEN_W / 2;
    camy = G.py - 24 - SCREEN_H / 2;
    if (camx < 0) camx = 0;
    if (camy < 0) camy = 0;
    if (camx > MAP_PX_W - SCREEN_W) camx = MAP_PX_W - SCREEN_W;
    if (camy > MAP_PX_H - SCREEN_H) camy = MAP_PX_H - SCREEN_H;

    spr_count = render_frame(camx, camy, lamps_on());
    hud();
}

void jo_main(void)
{
    jo_core_init(JO_COLOR_Black);

    palfx_init();                       /* bancos + paleta padrao do carregador de TGA */
    boot_assets = assets_load();        /* 106 TGA */
    boot_sfx    = audio_init();         /* 12 PCM */
    boot_map    = world_load();
    boot_save   = save_init();

    G.minutes = 8 * 60;
    G.day = 1;
    G.px = 31 * TILE; G.py = 12 * TILE;
    G.facing = FACE_D;
    G.sel = 1;
    G.lamps_mode = LAMPS_AUTO;

    entities_init();
    palfx_set_time(G.minutes);
    palfx_commit_now();                 /* sobrescreve a paleta que o carregador de TGA deixou */

    jo_audio_set_cd_volume(JO_AUDIO_CD_VOLUME_MAX);
    jo_core_add_vblank_callback(palfx_vblank);
    jo_core_add_callback(game_frame);
    jo_core_run();
}
