#ifndef SAVE_H
#define SAVE_H

/* Retornos: 1 = ok, 0 = falhou */
int save_init(void);       /* monta a memoria interna */
int save_write(void);      /* grava SAVE_SIZE bytes */
int save_read(void);       /* recarrega o mapa do CD e aplica o save */
int save_exists(void);

#endif
