# Protótipo "fazenda 2D" – Jo Engine (Sega Saturn)

Código do protótipo já organizado como **projeto Jo Engine com pasta `cd/` pronta** e scripts para gerar a imagem de disco e abrir num emulador.

> **Status honesto:** o código **não foi compilado com a toolchain SH-2 nem rodado num Saturn/emulador** (não há essa toolchain no ambiente onde o escrevi). Verifiquei: (1) sintaxe e tipos com o gcc do host contra um `jo/jo.h` falso escrito a partir da documentação oficial; (2) a lógica (leitura do mapa e de `LAMPS.TXT`, enxada/água/plantio/colheita/novo dia, save de 7168 bytes com ida e volta, paletas de dia/noite, movimento das entidades) com um harness no host lendo os arquivos reais de `cd/`. Espere ajustar 1 ou 2 detalhes de API no primeiro build — veja **Pontos a confirmar**.

## 1. Instalar e compilar
1. Baixe o Jo Engine (https://jo-engine.org) para `JoEngine\` (pastas `jo_engine\`, `Compiler\`, `Projects\`).
2. Copie esta pasta para `JoEngine\Projects\jo_farm_proto\` (o Makefile usa `../../jo_engine` e `../../Compiler`).
3. Abra um terminal nessa pasta e rode `compile.bat` (Windows, mesmo fluxo da documentação: `make re` → `JoEngineCueMaker`; depois o script acrescenta as faixas CD-DA ao `.cue`).
4. Resultado: `sl_coff.cue` + `sl_coff.iso` (dados) + `BGMFARM.wav`/`BGMMINE.wav` (faixas 2 e 3).

## 2. Rodar no emulador
- **Primeiro teste, só gráficos/lógica:** Yabause, como na documentação do Jo: `yabause.exe -a -i sl_coff.cue` (a doc avisa que é impreciso).
- **Teste mais fiel (inclui CD-DA):** Mednafen (`run_mednafen.sh`) ou Kronos / Yaba Sanshiro, abrindo o `.cue`.
- **Hardware real:** Satiator/Saroo com o `.cue` e os WAV (ou converta as faixas conforme o seu dispositivo).

## 3. Estrutura
| Arquivo | Função |
|---|---|
| `main.c` | `jo_main`, laço de quadro, entrada, ações, hora do dia, overlay de depuração |
| `config.h` | constantes e os 2 parâmetros a confirmar (`TRANSP`, `PAL_BIAS`) |
| `palfx.c/.h` | 4 bancos de paleta, mistura por fase do dia, escrita na Color RAM **no VBLANK** |
| `assets.c/.h` | carrega os 106 TGA |
| `world.c/.h` | mapa 64×64, lâmpadas, spawns, enxada/água/plantio/colheita/novo dia |
| `render.c/.h` | tilemap com sprites VDP1, banco de luz por tile, entidades, jogador, HUD |
| `entities.c/.h` | 16 galinhas + 8 slimes (os 24 sprites) e efeitos |
| `audio.c/.h` | 12 PCM + ciclo de faixas CD-DA |
| `save.c/.h` | memória interna, 7168 bytes, checksum |
| `palettes_bank.h` | **gerado**: paleta base RGB555 (8 grupos × 16) |
| `cd/` | 106 TGA, 12 PCM, `FARM64.MAP`, `LAMPS.TXT` (vai para o disco) |
| `music/`, `tools/` | WAV de teste, `add_cd_audio.py`, geradores (`build_project.py` refaz `cd/` e `palettes_bank.h`) |

## 4. Controles
D-pad anda · **A** enxada (ou colhe cultura madura) · **B** regar · **C** plantar (tipo cicla 1–6) · **X** +3 h (passar das 06:00 faz regados crescerem) · **Y** luz das lâmpadas auto/on/off · **Z** salvar · **START** carregar · **L** música CD-DA (off → faixa 2 → faixa 3) · **R** toca o próximo efeito (teste de PCM junto com o CD-DA) · **L+R** reúne os 24 sprites ao redor do jogador (teste de carga).

Overlay (4 linhas no rodapé): FPS, nº de sprites, dia/hora; modo da luz, `CRAM direto|REG`, nº de escritas de paleta, colheitas; TGA/SFX/MAP carregados (esperado 106/12/1), save existente, estado da música.

## 5. Como cada meta do protótipo é testada
| Meta | Onde / como |
|---|---|
| Mapa 64×64 com paleta por tile | `render.c`: cada tile escolhe 1 de 4 bancos (`tile_bank`). **Desvio:** usa sprites VDP1, não um plano VDP2 — o Jo não expõe tilemap VDP2 com paleta por tile; isso exigiria chamadas SGL diretas (fase 2) |
| Regeneração de paleta no VBLANK | `palfx_set_time` calcula; `palfx_vblank` grava 512 entradas só quando mudou. Use **X** e veja dia→entardecer→noite |
| Luz de lâmpadas | à noite, tiles perto das 4 lâmpadas usam bancos mais claros (**Y** força on/off) |
| Save ~7 KB | **Z** grava 7168 B; **START** recarrega o mapa do CD e aplica o save |
| Carga de pacote do CD | `world_load` lê `FARM64.MAP` + `LAMPS.TXT`; `assets_load` lê 106 TGA; `audio_init` lê 12 PCM |
| PCM + CD-DA juntos | **L** liga a música, **R** dispara efeitos por cima |
| 24 sprites em cena | **L+R** reúne todos; observe FPS e SPR no overlay |

## 6. Pontos a confirmar no primeiro boot
1. **Cores/transparência.** Os TGA têm índice 0 transparente e pixels `16*grupo+índice`. A doc do Jo diz que "o primeiro índice da paleta é 1". Se as cores vierem deslocadas, ponha `PAL_BIAS 1` em `config.h`; se o fundo aparecer magenta ou preto, revise `TRANSP`.
2. **Escrita na Color RAM.** `jo_palette.data` deve apontar para a Color RAM; o overlay mostra `CRAM direto`. Se mostrar `REG`, o código usa `jo_set_palette_register(banco*256+i)`, cujo índice é suposição minha.
3. **Campo `.id` de `jo_palette`.** Usado em `jo_sprite_set_palette`; se não compilar, confira `jo/types.h`.
4. **Limite de sprites/comandos por quadro.** Uma tela desenha ~350–430 sprites (SPR no overlay). Se itens sumirem ou o FPS cair, reduza a área desenhada ou agrupe o chão.
5. **Tipos** de `jo_fs_read_file` (usei `int *len`), `jo_printf` e `JO_COMPILE_WITH_FS_MODULE` (exigido por `jo_audio_play_cd_track`, conforme a doc de áudio) — confirmados só em parte pela documentação.
6. **PCM.** Carrego como `JoSoundMono16Bit` e fixo `sample_rate = 15360`; se o tom sair errado, ajuste `PCM_RATE` em `audio.c`. Volume em `jo_audio_set_volume(100)` (faixa 0–127).
7. **Z.** "Maior = mais longe"; o plano de corte é 80 (HUD usa 120).
8. **Memória do `malloc`:** 384 KB no Makefile; ajuste se o Jo reclamar.
9. **CUE.** `add_cd_audio.py` anexa faixas ao `.cue` que o `JoEngineCueMaker` gerar; confira o resultado no seu emulador.

## 7. Ordem sugerida de depuração
1. Só `jo_core_init` + um sprite (comente o resto em `main.c`) para fechar o item 1.
2. Mapa e jogador sem áudio/save (item 2, 3, 4).
3. Save e carga (`Z`/`START`).
4. Áudio PCM, depois CD-DA.
5. Estresse (`L+R`) e medição no hardware real.

## 8. Regenerar assets
`python3 tools/build_project.py` (Python 3 + Pillow, NumPy, SciPy) refaz `cd/` e `palettes_bank.h`. Para arte final, converta com o conversor do pacote anterior e mantenha: 8 bits indexado, índice 0 transparente, pixel = `16*grupo + índice`, largura múltipla de 8, nomes 8.3 maiúsculos.

O Jo Engine é de Johannes Fetz (licença BSD de 3 cláusulas); mantenha os avisos dele ao distribuir.
