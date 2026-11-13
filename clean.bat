@echo off
del /q *.o sl_coff.coff sl_coff.map sl_coff.bin sl_coff.iso sl_coff.cue 2>nul
if exist cd\0.bin del /q cd\0.bin
