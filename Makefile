# Projeto Jo Engine: coloque esta pasta em  <JoEngine>/Projects/jo_farm_proto
# (os caminhos abaixo assumem ../../jo_engine e ../../Compiler)
JO_COMPILE_WITH_VIDEO_MODULE = 0
JO_COMPILE_WITH_BACKUP_MODULE = 1
JO_COMPILE_WITH_TGA_MODULE = 1
JO_COMPILE_WITH_AUDIO_MODULE = 1
JO_COMPILE_WITH_FS_MODULE = 1
JO_COMPILE_WITH_3D_MODULE = 0
JO_COMPILE_WITH_PSEUDO_MODE7_MODULE = 0
JO_COMPILE_WITH_EFFECTS_MODULE = 0
JO_COMPILE_WITH_RAM_CARD_MODULE = 0
JO_GLOBAL_MEMORY_SIZE_FOR_MALLOC = 393216
JO_DEBUG = 0
SRCS = main.c assets.c palfx.c world.c entities.c render.c audio.c save.c
JO_ENGINE_SRC_DIR=../../jo_engine
COMPILER_DIR=../../Compiler
include $(COMPILER_DIR)/COMMON/jo_engine_makefile
