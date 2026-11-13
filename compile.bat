@echo off
REM Rode dentro de <JoEngine>\Projects\jo_farm_proto  (mesmo fluxo da documentacao do Jo Engine)
set PATH=%~dp0..\..\Compiler\WINDOWS\Other Utilities;%~dp0..\..\Compiler\WINDOWS\bin;%PATH%
call clean.bat
make re
JoEngineCueMaker
python tools\add_cd_audio.py sl_coff.cue music
