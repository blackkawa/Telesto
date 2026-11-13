#ifndef PALFX_H
#define PALFX_H

/* Cria os bancos de paleta e registra a paleta padrao usada pelo carregador de TGA de 8 bits.
   Chamar ANTES de assets_load(). */
void palfx_init(void);

/* Recalcula os bancos para a hora do dia (minutos 0..1439). Nao escreve na Color RAM: marca "sujo". */
void palfx_set_time(int minutes);

/* Escreve na Color RAM imediatamente (uso no boot, depois de carregar os TGA). */
void palfx_commit_now(void);

/* Callback de VBLANK: escreve na Color RAM somente se algo mudou. */
void palfx_vblank(void);

/* Seleciona o banco (0..PAL_BANKS-1) para os sprites de 8 bits desenhados em seguida. */
void palfx_bind(int bank);

/* Diagnostico para o overlay. */
int  palfx_cram_direct(void);
int  palfx_bank_id(int bank);
int  palfx_writes(void);

#endif
