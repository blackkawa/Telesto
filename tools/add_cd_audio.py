#!/usr/bin/env python3
"""Acrescenta as faixas CD-DA (WAV) ao .cue gerado pelo JoEngineCueMaker.

Uso:  python3 tools/add_cd_audio.py [sl_coff.cue] [music_dir]
  - copia BGMFARM.wav e BGMMINE.wav para a pasta do .cue
  - acrescenta TRACK 02 e TRACK 03 (AUDIO, PREGAP 2 s) se ainda nao existirem
O jogo toca a faixa 2 (fazenda) e a faixa 3 (mina) com jo_audio_play_cd_track()."""
import os, shutil, sys

cue = sys.argv[1] if len(sys.argv) > 1 else "sl_coff.cue"
music = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music")
if not os.path.isfile(cue):
    sys.exit(f"nao achei {cue}: compile primeiro (compile.bat / make re + JoEngineCueMaker)")
folder = os.path.dirname(os.path.abspath(cue))
text = open(cue, encoding="utf-8", errors="replace").read()
if "BGMFARM.wav" in text:
    sys.exit("faixas de audio ja estao no .cue")
for n in ("BGMFARM.wav", "BGMMINE.wav"):
    shutil.copy(os.path.join(music, n), os.path.join(folder, n))
if not text.endswith("\n"):
    text += "\n"
text += ('FILE "BGMFARM.wav" WAVE\n  TRACK 02 AUDIO\n    PREGAP 00:02:00\n    INDEX 01 00:00:00\n'
         'FILE "BGMMINE.wav" WAVE\n  TRACK 03 AUDIO\n    PREGAP 00:02:00\n    INDEX 01 00:00:00\n')
open(cue, "w", encoding="utf-8", newline="\n").write(text)
print("ok:", cue)
