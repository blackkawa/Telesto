#ifndef ASSETS_H
#define ASSETS_H

extern int spr_trn[16];        /* terreno TRN00..15 */
extern int spr_str[16];        /* estruturas STR00..15 */
extern int spr_crop[7][5];     /* culturas CP{1..6}S{0..4} (indice 0 nao usado) */
extern int spr_pl[3][4];       /* jogador: [0]=frente(D) [1]=costas(U) [2]=direita(R); esquerda = espelho */
extern int spr_chk[4];         /* galinha */
extern int spr_slm[5];         /* slime (4 = derrotado) */
extern int spr_icn[12];        /* icones */
extern int spr_dst[4];         /* poeira 16x16 */
extern int spr_spk[4];         /* brilho 16x16 */
extern int spr_sls[3];         /* corte 32x32 */

/* Carrega os 106 TGA do CD. Retorna a quantidade carregada. */
int assets_load(void);

#endif
