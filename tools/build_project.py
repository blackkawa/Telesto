import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alib import write_tga_packed, rgb555
import gen_gfx as g, gen_map as m, gen_audio as a

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.makedirs(f"{OUT}/cd", exist_ok=True)
GROUP = {"TERR": 0, "STRC": 1, "CROP": 2, "PLYR": 3, "CHKN": 4, "SLM1": 5, "ICON": 6, "EFFX": 7}
for name, cv, pal, grp in g.ASSETS:
    write_tga_packed(f"{OUT}/cd/{name}.TGA", cv, pal, GROUP[pal.name])
ground, obj, crop, lamps, spawns, stats = m.build()
open(f"{OUT}/cd/FARM64.MAP", "wb").write(m.pack(ground, obj, crop))
open(f"{OUT}/cd/LAMPS.TXT", "w").write("# x y raio\n" + "".join(f"L {x} {y} {r}\n" for x, y, r in lamps) +
    "# tipo x_px y_px\n" + "".join(f"{t[0]} {x} {y}\n" for t, x, y in spawns))   # C = galinha, S = slime
for n, x in a.sfx().items():
    open(f"{OUT}/cd/{n}.PCM", "wb").write(a.to_s16be(x))

# palettes_bank.h: 8 grupos x 16 = 128 entradas RGB555 (sem bit 15). Os 4 bancos de luz sao derivados em tempo de execucao.
order = ["TERR", "STRC", "CROP", "PLYR", "CHKN", "SLM1", "ICON", "EFFX"]
base = []
for k in order:
    base += [rgb555(*c) for c in g.P[k].rgb]
h = f"""/* GERADO por tools/build_project.py - NAO EDITE. Paleta base RGB555 (sem o bit 15). */
#ifndef PALETTES_BANK_H
#define PALETTES_BANK_H
#define PAL_GROUPS      8
#define PAL_ENTRIES     (PAL_GROUPS * 16)
/* grupos: 0 TERR, 1 STRC, 2 CROP, 3 PLYR, 4 CHKN, 5 SLM, 6 ICON, 7 EFFX (pixel = 16*grupo + indice, 0 = transparente) */
static const unsigned short PAL_BASE[PAL_ENTRIES] = {{
    {", ".join(f"0x{v:04X}" for v in base)}
}};
#endif
"""
open(f"{OUT}/palettes_bank.h", "w").write(h)
print(len(g.ASSETS), "TGA;", stats)
