"""Gráficos procedurais de placeholder para o protótipo (Jo Engine / Saturn)."""
import random
from alib import Canvas, Palette

# ---------------------------------------------------------------- paletas (14 cores + transparente)
P = {}
P["TERR"] = Palette("TERR", ["#2f6b2a", "#46902f", "#68b53c", "#9bd75a", "#6b4a2b", "#8f6a3e", "#b48d57",
                             "#2c5fa3", "#4a8fd6", "#9ed0f2", "#c9b78a", "#8a8576", "#f4e9a0", "#4a321c"])
P["STRC"] = Palette("STRC", ["#2a1f1a", "#6b4a2b", "#a8743e", "#d9a066", "#7d7d85", "#a9a9b3", "#d4d4dc",
                             "#2f6b2a", "#46902f", "#78c243", "#a8402f", "#d4573e", "#f2d27a", "#4a8fd6"])
P["CROP"] = Palette("CROP", ["#2a5a24", "#3f8a2e", "#7bc044", "#6b4a2b", "#9a6f3f", "#f2f0e6", "#8e4aa8",
                             "#d9382c", "#9c2018", "#f08a24", "#b85a10", "#f2d03c", "#b59a1c", "#4b2260"])
P["PLYR"] = Palette("PLYR", ["#2a1a2e", "#ffd9bf", "#e8a98c", "#8a4b2a", "#5e301a", "#2c7fb8", "#ffffff",
                             "#4aa86a", "#2f7a49", "#5b6fb5", "#3d4b86", "#6b4a2b", "#f0a0a0", "#e8c76a"])
P["CHKN"] = Palette("CHKN", ["#3a2a2a", "#fffaf0", "#e6d9c3", "#d9382c", "#f2b630", "#c98a1c", "#1a1a1a",
                             "#c58a4a", "#a86a2e", "#ffffff", "#f0a0a0", "#9a9a9a", "#d0d0d0", "#7a5a3a"])
for tier, (dk, md, lt) in enumerate((("#2f7a3a", "#49b85a", "#8fe08a"),
                                      ("#2a4fa0", "#4a86e0", "#9ac4ff"),
                                      ("#a02a2a", "#e0564a", "#ffa89a")), start=1):
    P["SLM%d" % tier] = Palette("SLM%d" % tier, ["#241a2e", dk, md, lt, "#ffffff", "#1a1a1a", "#e8a0a0",
                                                  "#3a2a40", "#5a4a60", "#ffd0d0", "#fff7c0", "#c0c0c8", "#80808a", "#503060"])
P["ICON"] = Palette("ICON", ["#2a1a2e", "#9aa5b5", "#dfe6ee", "#8f5a2e", "#c58a4a", "#d9382c", "#46902f",
                             "#f08a24", "#fffaf0", "#f2d03c", "#4a8fd6", "#8e4aa8", "#c8703a", "#f08fb0"])
P["EFFX"] = Palette("EFFX", ["#ffffff", "#fff7c0", "#f2d03c", "#cfeaff", "#7fb8f0", "#d8d8d8", "#9a9a9a",
                             "#d9c9a0", "#a08e66", "#ffd9e8", "#f08fb0", "#ffb060", "#e05030", "#605050"])

ASSETS = []   # (arquivo8, canvas, paleta, grupo)


def add(name, cv, pal, group):
    assert len(name) <= 8 and name == name.upper(), name
    ASSETS.append((name, cv, pal, group))


# ---------------------------------------------------------------- terreno
def grass(seed, flowers=False, tufts=False):
    r = random.Random(seed)
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 2)
    for _ in range(46):
        cv.px(r.randrange(16), r.randrange(16), 3)
    for _ in range(14):
        cv.px(r.randrange(16), r.randrange(16), 4)
    for _ in range(10):
        x, y = r.randrange(16), r.randrange(15)
        cv.px(x, y, 1)
    if tufts:
        for _ in range(3):
            x, y = r.randrange(2, 14), r.randrange(3, 14)
            cv.px(x, y, 4); cv.px(x - 1, y + 1, 3); cv.px(x + 1, y + 1, 3); cv.px(x, y + 1, 1)
    if flowers:
        for fx, fy in ((3, 4), (11, 9), (6, 12)):
            cv.px(fx, fy, 12); cv.px(fx - 1, fy, 4); cv.px(fx + 1, fy, 4); cv.px(fx, fy - 1, 4); cv.px(fx, fy + 1, 4)
            cv.px(fx, fy, 12)
    return cv


def dirt(seed, pebble=False):
    r = random.Random(seed)
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 6)
    for _ in range(40):
        cv.px(r.randrange(16), r.randrange(16), 5)
    for _ in range(18):
        cv.px(r.randrange(16), r.randrange(16), 7)
    if pebble:
        cv.rect(10, 9, 12, 10, 11); cv.px(10, 10, 12); cv.px(11, 10, 12); cv.px(12, 10, 12)
    return cv


def tilled(wet):
    cv = Canvas(16, 16)
    base, line, hi = (5, 14, 5) if wet else (6, 5, 7)
    cv.rect(0, 0, 15, 15, base)
    for y in (2, 6, 10, 14):
        cv.rect(0, y, 15, y, line)
        if not wet:
            cv.rect(0, y - 1, 15, y - 1, hi)
    if wet:
        for x, y in ((2, 4), (7, 8), (12, 4), (4, 12), (10, 12), (14, 8)):
            cv.px(x, y, 8)
    return cv


def path(seed):
    r = random.Random(seed)
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 11)
    for _ in range(9):
        x, y = r.randrange(1, 14), r.randrange(1, 14)
        cv.rect(x, y, x + 1, y + 1, 12)
    for _ in range(14):
        cv.px(r.randrange(16), r.randrange(16), 7)
    return cv


def water(frame):
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 9)
    off = 4 if frame else 0
    for (x, y) in ((1, 3), (9, 8), (4, 13), (12, 1)):
        xx = (x + off) % 14
        cv.rect(xx, y, xx + 3, y, 10)
        cv.rect(xx + 1, y + 1, xx + 4, y + 1, 8)
    return cv


def shore(side):
    r = random.Random(40 + ord(side))
    cv = grass(40 + ord(side))
    for i in range(3):
        for k in range(16):
            col = 11 if i < 2 else 7
            if side == "N":
                cv.px(k, i, col)
            elif side == "S":
                cv.px(k, 15 - i, col)
            elif side == "W":
                cv.px(i, k, col)
            else:
                cv.px(15 - i, k, col)
    for k in range(16):
        if side == "N": cv.px(k, 0, 8)
        elif side == "S": cv.px(k, 15, 8)
        elif side == "W": cv.px(0, k, 8)
        else: cv.px(15, k, 8)
    return cv


def sand(seed):
    r = random.Random(seed)
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 11)
    for _ in range(24):
        cv.px(r.randrange(16), r.randrange(16), 7)
    for _ in range(8):
        cv.px(r.randrange(16), r.randrange(16), 12)
    return cv


TERR = [grass(1), grass(2, tufts=True), grass(3, flowers=True), dirt(4), dirt(5, pebble=True), tilled(False), tilled(True),
        path(6), path(7), water(0), water(1), shore("N"), shore("S"), shore("E"), shore("W"), sand(8)]
for i, cv in enumerate(TERR):
    add("TRN%02d" % i, cv, P["TERR"], "terreno")


# ---------------------------------------------------------------- estruturas
def fence_h():
    cv = Canvas(16, 16)
    cv.rect(0, 6, 15, 7, 3); cv.rect(0, 8, 15, 8, 2)
    cv.rect(0, 10, 15, 11, 3); cv.rect(0, 12, 15, 12, 2)
    for x0 in (1, 12):
        cv.rect(x0, 3, x0 + 2, 14, 3); cv.rect(x0 + 2, 3, x0 + 2, 14, 2); cv.rect(x0, 3, x0, 14, 4)
    cv.outline(1)
    return cv


def fence_v():
    cv = Canvas(16, 16)
    cv.rect(6, 0, 7, 15, 3); cv.rect(8, 0, 8, 15, 2)
    cv.rect(10, 0, 11, 15, 3); cv.rect(12, 0, 12, 15, 2)
    cv.rect(4, 1, 13, 3, 3); cv.rect(4, 3, 13, 3, 2); cv.rect(4, 1, 13, 1, 4)
    cv.rect(4, 11, 13, 13, 3); cv.rect(4, 13, 13, 13, 2); cv.rect(4, 11, 13, 11, 4)
    cv.outline(1)
    return cv


def fence_post():
    cv = Canvas(16, 16)
    cv.rect(6, 3, 9, 14, 3); cv.rect(9, 3, 9, 14, 2); cv.rect(6, 3, 6, 14, 4)
    cv.outline(1)
    return cv


def tree_trunk():
    cv = Canvas(16, 16)
    cv.ell(8, 2, 7, 3, 9)                 # sombra inferior da copa
    cv.ell(8, 1, 6, 2, 8, only_over=[9])
    cv.rect(6, 4, 9, 13, 3); cv.rect(9, 4, 9, 13, 2); cv.rect(6, 4, 6, 13, 4)
    cv.rect(4, 13, 11, 14, 3); cv.rect(9, 13, 11, 14, 2)
    cv.outline(1)
    return cv


def tree_top():
    cv = Canvas(16, 16)
    cv.ell(8, 8, 7.5, 7.5, 9)
    cv.ell(10, 10, 5.5, 5.5, 8, only_over=[9])
    cv.ell(6, 5, 4, 3, 10, only_over=[9])
    for x, y in ((4, 9), (11, 4), (8, 11), (12, 8)):
        cv.px(x, y, 10)
    cv.outline(1)
    return cv


def rock():
    cv = Canvas(16, 16)
    cv.ell(8, 10, 6.5, 4.5, 5)
    cv.ell(7, 8, 4.5, 3, 6, only_over=[5])
    cv.ell(6, 7, 2.5, 1.5, 7, only_over=[6])
    cv.rect(4, 13, 12, 13, 5)
    cv.outline(1)
    return cv


def bush():
    cv = Canvas(16, 16)
    cv.ell(8, 10, 6.5, 4.5, 8)
    cv.ell(6, 9, 3.5, 3, 9, only_over=[8])
    cv.ell(11, 8, 3, 2.5, 9, only_over=[8])
    for x, y in ((5, 10), (9, 7), (11, 11)):
        cv.px(x, y, 11); cv.px(x + 1, y, 11); cv.px(x, y - 1, 12)
    cv.outline(1)
    return cv


def wood_floor():
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 3)
    for y in (3, 7, 11, 15):
        cv.rect(0, y, 15, y, 2)
    for x, y in ((3, 1), (11, 5), (6, 9), (13, 13)):
        cv.rect(x, y, x + 2, y, 4)
    for x, y in ((8, 0), (2, 4), (12, 8), (5, 12)):
        cv.px(x, y, 2)
    return cv


def wood_wall():
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 3)
    for x in (0, 5, 10, 15):
        cv.rect(x, 0, x, 15, 2)
    for x in (1, 6, 11):
        cv.rect(x, 0, x, 15, 4)
    cv.rect(0, 15, 15, 15, 2)
    return cv


def roof(side):
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 12)
    for y in (0, 4, 8, 12):
        cv.rect(0, y + 3, 15, y + 3, 11)
        off = 0 if (y // 4) % 2 == 0 else 4
        for x in range(off, 16, 8):
            cv.rect(x, y, x, y + 2, 11)
    for x in (2, 10):
        cv.px(x, 1, 13)
    if side == "L":
        cv.rect(0, 0, 0, 15, 1); cv.rect(1, 0, 1, 15, 11)
    if side == "R":
        cv.rect(15, 0, 15, 15, 1); cv.rect(14, 0, 14, 15, 11)
    cv.rect(0, 15, 15, 15, 1)
    return cv


def door():
    cv = Canvas(16, 16)
    cv.rect(1, 0, 14, 15, 2)
    cv.rect(3, 2, 12, 15, 3)
    cv.rect(8, 2, 8, 15, 2)
    cv.rect(3, 2, 3, 15, 4)
    cv.rect(10, 8, 11, 9, 13)
    cv.outline(1)
    return cv


def window():
    cv = Canvas(16, 16)
    cv.rect(0, 0, 15, 15, 3)
    for x in (0, 5, 10, 15):
        cv.rect(x, 0, x, 15, 2)
    cv.rect(3, 3, 12, 12, 2)
    cv.rect(4, 4, 11, 11, 14)
    cv.rect(4, 4, 11, 4, 13)
    cv.rect(7, 4, 8, 11, 2); cv.rect(4, 7, 11, 8, 2)
    cv.rect(5, 5, 6, 6, 13)
    return cv


def sign():
    cv = Canvas(16, 16)
    cv.rect(7, 8, 8, 15, 3); cv.rect(8, 8, 8, 15, 2)
    cv.rect(2, 2, 13, 8, 4); cv.rect(2, 8, 13, 8, 3)
    cv.rect(4, 4, 11, 4, 2); cv.rect(4, 6, 9, 6, 2)
    cv.outline(1)
    return cv


def chest():
    cv = Canvas(16, 16)
    cv.rect(2, 6, 13, 13, 3); cv.rect(2, 6, 13, 7, 4)
    cv.rect(2, 12, 13, 13, 2)
    cv.rect(2, 9, 13, 9, 2)
    cv.rect(2, 6, 3, 13, 6); cv.rect(12, 6, 13, 13, 6)
    cv.rect(7, 8, 8, 10, 13)
    cv.ell(8, 6, 6, 3, 3, only_over=[0])
    cv.outline(1)
    return cv


STRC = [fence_h(), fence_v(), fence_post(), tree_trunk(), tree_top(), rock(), bush(), wood_floor(), wood_wall(),
        roof("L"), roof("M"), roof("R"), door(), window(), sign(), chest()]
for i, cv in enumerate(STRC):
    add("STR%02d" % i, cv, P["STRC"], "estruturas")


# ---------------------------------------------------------------- culturas (6 tipos x 5 estágios)
def leaf(cv, x, y, d, big=False):
    rx, ry = (3, 1.6) if big else (2.2, 1.2)
    cx = x + d * rx
    cv.ell(cx, y, rx, ry, 2)
    cv.ell(cx, y - 0.4, rx * 0.6, ry * 0.5, 3, only_over=[2])


def crop(kind, stage):
    cv = Canvas(16, 16)
    cv.ell(8, 13.5, 5, 2, 4)
    cv.ell(8, 13, 4, 1.4, 5, only_over=[4])
    if stage == 0:
        cv.px(7, 12, 3); cv.px(9, 12, 3)
    elif stage == 1:
        cv.rect(8, 9, 8, 12, 2); leaf(cv, 8, 9, -1); leaf(cv, 8, 9, 1)
    elif stage == 2:
        cv.rect(8, 6, 8, 12, 2); leaf(cv, 8, 7, -1); leaf(cv, 8, 7, 1); leaf(cv, 8, 10, -1); leaf(cv, 8, 10, 1)
    else:
        cv.rect(8, 3, 8, 12, 2)
        leaf(cv, 8, 5, -1, True); leaf(cv, 8, 5, 1, True); leaf(cv, 8, 9, -1, True); leaf(cv, 8, 9, 1, True)
        if stage == 3:
            cv.px(6, 11, 3); cv.px(10, 11, 3); cv.px(8, 2, 3)
        else:
            fruit(cv, kind)
    cv.outline(1)
    return cv


def fruit(cv, kind):
    if kind == 0:   # nabo
        cv.ell(8, 11.5, 3.6, 3, 6); cv.ell(8, 10, 3.4, 1.6, 7, only_over=[6]); cv.px(6, 11, 5)
    elif kind == 1:  # tomate
        for x, y in ((5, 8), (11, 7), (7, 11)):
            cv.ell(x, y, 2.2, 2.2, 8); cv.px(x - 1, y - 1, 9 - 1 + 1); cv.px(x, y - 2, 2); cv.px(x - 1, y - 1, 7 + 0)
        cv.px(6, 9, 9); cv.px(12, 8, 9); cv.px(8, 12, 9)
    elif kind == 2:  # abóbora
        cv.ell(8, 11, 5.2, 3.4, 10); cv.rect(8, 8, 8, 14, 11); cv.rect(5, 9, 5, 13, 11); cv.rect(11, 9, 11, 13, 11)
        cv.px(7, 7, 2); cv.rect(8, 6, 8, 7, 2)
    elif kind == 3:  # milho
        cv.ell(5, 8, 1.6, 3, 12); cv.ell(11, 7, 1.6, 3, 12); cv.px(5, 9, 13); cv.px(11, 8, 13)
        cv.rect(7, 0, 9, 1, 13)
    elif kind == 4:  # morango
        for x, y in ((5, 11), (10, 10), (8, 13)):
            cv.ell(x, y, 1.8, 2, 8); cv.px(x, y - 2, 2); cv.px(x, y, 6)
        cv.px(6, 6, 6); cv.px(10, 5, 6)
    else:            # berinjela
        cv.ell(5, 10, 1.8, 3.4, 7); cv.ell(11, 10, 1.8, 3.4, 7); cv.px(5, 8, 14); cv.px(11, 8, 14)
        cv.rect(4, 6, 6, 6, 2); cv.rect(10, 6, 12, 6, 2)


for k in range(6):
    for s in range(5):
        add("CP%dS%d" % (k + 1, s), crop(k, s), P["CROP"], "culturas")


# ---------------------------------------------------------------- jogador 32x48
def player(d, frame):
    cv = Canvas(32, 48)
    step = (0, 1, 0, -1)[frame]
    legL = 45 - (1 if step > 0 else 0)
    legR = 45 - (1 if step < 0 else 0)
    aL, aR = step, -step
    if d in ("D", "U"):
        # pernas e botas
        cv.rect(11, 37, 15, legL, 10); cv.rect(15, 37, 15, legL, 11)
        cv.rect(16, 37, 20, legR, 10); cv.rect(20, 37, 20, legR, 11)
        cv.rect(10, legL - 2, 15, legL, 12); cv.rect(16, legR - 2, 21, legR, 12)
        # tronco
        cv.rect(10, 25, 21, 36, 8); cv.rect(19, 25, 21, 36, 9); cv.rect(10, 35, 21, 36, 9)
        cv.rect(10, 34, 21, 34, 11)
        # braços
        for (x0, ay) in ((6, aL), (22, aR)):
            cv.rect(x0, 26 + ay, x0 + 3, 29 + ay, 8)
            cv.rect(x0, 30 + ay, x0 + 2, 34 + ay, 2); cv.rect(x0 + 2, 30 + ay, x0 + 2, 34 + ay, 3)
        # cabeça
        cv.ell(16, 15, 10, 9, 2)
        cv.rect(8, 23, 24, 24, 3)
        if d == "D":
            cv.ell(16, 11, 11, 8, 4)
            cv.rect(5, 11, 7, 21, 4); cv.rect(25, 11, 27, 21, 4)
            for y in range(15, 25):
                for x in range(8, 25):
                    if ((x - 16) / 10) ** 2 + ((y - 15) / 9) ** 2 <= 1.0 and cv.get(x, y) in (4, 5) and y >= 15:
                        cv.px(x, y, 2)
            lens = [3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 3, 2, 1, 2, 3, 2, 1]
            for i, x in enumerate(range(8, 25)):
                for y in range(15, 15 + lens[i]):
                    cv.px(x, y, 4)
                cv.px(x, 15 + lens[i], 5)
            for ex in (10, 19):
                cv.rect(ex, 17, ex + 2, 17, 1); cv.rect(ex, 18, ex + 2, 20, 6)
                cv.px(ex, 18, 7); cv.px(ex + 1, 19, 1)
            cv.rect(8, 21, 9, 21, 13); cv.rect(22, 21, 23, 21, 13)
            cv.rect(15, 22, 16, 22, 1)
        else:
            cv.ell(16, 14, 11, 10, 4)
            cv.rect(6, 19, 26, 22, 4); cv.rect(8, 21, 24, 22, 5)
        # chapéu
        cv.ell(16, 8, 14, 3.5, 14); cv.ell(16, 5, 8, 4, 14)
        for x in range(9, 24):
            if cv.get(x, 6) == 14:
                cv.px(x, 6, 12)
        for x in range(3, 30):
            if cv.get(x, 10) == 14:
                cv.px(x, 10, 12 if x % 3 else 14)
    else:  # lado direito
        bx = (-2, 2, 0, 0)[frame] if step else 0
        # perna de trás e da frente
        back = -step * 2
        front = step * 2
        cv.rect(12 + back, 37, 16 + back, legL, 11); cv.rect(12 + back, legL - 2, 17 + back, legL, 12)
        cv.rect(15 + front, 37, 19 + front, legR, 10); cv.rect(15 + front, legR - 2, 21 + front, legR, 12)
        cv.rect(11, 25, 20, 36, 8); cv.rect(18, 25, 20, 36, 9); cv.rect(11, 35, 20, 36, 9)
        cv.rect(11, 34, 20, 34, 11)
        cv.rect(13, 26 + aL, 17, 29 + aL, 8)
        cv.rect(14, 30 + aL, 17, 34 + aL, 2); cv.rect(17, 30 + aL, 17, 34 + aL, 3)
        # cabeça
        cv.ell(15, 15, 9, 9, 2); cv.rect(8, 23, 22, 24, 3)
        cv.ell(13, 12, 10, 8, 4)
        cv.ell(6, 20, 3, 6, 4); cv.ell(6, 22, 2, 4, 5, only_over=[4])
        for y in range(15, 25):
            for x in range(16, 25):
                if ((x - 15) / 9) ** 2 + ((y - 15) / 9) ** 2 <= 1.0 and y >= 15:
                    cv.px(x, y, 2)
        for i, x in enumerate(range(15, 25)):
            for y in range(14, 14 + [3, 2, 3, 2, 1, 2, 1, 1, 1, 0][i]):
                cv.px(x, y, 4)
        cv.rect(19, 17, 21, 17, 1); cv.rect(19, 18, 21, 20, 6); cv.px(19, 18, 7); cv.px(20, 19, 1)
        cv.rect(20, 21, 21, 21, 13); cv.px(24, 19, 3); cv.px(21, 22, 1)
        cv.ell(15, 8, 14, 3.5, 14); cv.ell(14, 5, 8, 4, 14)
        for x in range(8, 22):
            if cv.get(x, 6) == 14:
                cv.px(x, 6, 12)
    cv.outline(1)
    return cv


for d in ("D", "U", "R"):
    for f in range(4):
        add("PL%s%d" % (d, f), player(d, f), P["PLYR"], "jogador")


# ---------------------------------------------------------------- galinha 16x16
def chicken(frame):
    cv = Canvas(16, 16)
    bob = 1 if frame == 1 else 0
    peck = frame == 2
    cv.ell(8, 9 + bob, 5, 4, 2)
    cv.ell(7, 10 + bob, 3.5, 2.4, 3, only_over=[2])
    cv.ell(3, 7 + bob, 2.2, 3, 3)
    hx_, hy = (12, 5 + bob) if not peck else (13, 9)
    cv.ell(hx_, hy, 3, 3, 2)
    cv.rect(hx_ - 1, hy - 4, hx_ + 1, hy - 3, 4)
    cv.px(hx_ + 3, hy, 5); cv.px(hx_ + 4, hy, 5) if not peck else cv.px(hx_ + 3, hy + 1, 5)
    cv.px(hx_ + 1, hy - 1, 7)
    cv.px(hx_ - 1, hy + 2, 4)
    l0, l1 = (7, 9) if frame != 1 else (6, 10)
    cv.rect(l0, 13 + bob, l0, 14, 5); cv.rect(l1, 13 + bob, l1, 14, 5)
    cv.rect(l0 - 1, 14, l0 + 1, 14, 6); cv.rect(l1, 14, l1 + 2, 14, 6)
    cv.outline(1)
    return cv


for f in range(4):
    add("CHK%d" % f, chicken(f), P["CHKN"], "animais")


# ---------------------------------------------------------------- slime 32x32 (3 níveis por paleta)
def slime(frame):
    cv = Canvas(32, 32)
    sx, sy, lean = {0: (13, 9, 0), 1: (11, 11, 0), 2: (13, 9, -2), 3: (13, 9, 2), 4: (14, 7, 0)}[frame]
    cy = 29 - sy
    cv.ell(16 + lean, cy, sx, sy, 3)
    cv.ell(16 + lean, cy + sy * 0.35, sx * 0.9, sy * 0.7, 2, only_over=[3])
    cv.rect(16 + lean - sx, 29, 16 + lean + sx, 31, 0)
    cv.ell(12 + lean, cy - sy * 0.45, 3, 2, 4, only_over=[3, 2])
    cv.px(10 + lean, cy - sy * 0.45, 5) if False else None
    ey = int(cy - sy * 0.1)
    if frame == 4:
        for ex in (11, 19):
            cv.line(ex + lean, ey - 2, ex + 3 + lean, ey + 1, 6); cv.line(ex + 3 + lean, ey - 2, ex + lean, ey + 1, 6)
    else:
        for ex in (11, 19):
            cv.ell(ex + 1.5 + lean, ey, 2, 2.6, 6)
            cv.px(ex + 1 + lean, ey - 1, 5)
    cv.rect(15 + lean, ey + 4, 17 + lean, ey + 4, 6)
    cv.rect(8 + lean, ey + 2, 9 + lean, ey + 2, 7); cv.rect(22 + lean, ey + 2, 23 + lean, ey + 2, 7)
    cv.outline(1)
    return cv


for f in range(5):
    add("SLM%d" % f, slime(f), P["SLM1"], "inimigos")


# ---------------------------------------------------------------- ícones 16x16
# paleta ICON: 1 contorno, 2 aço, 3 aço claro, 4 madeira escura, 5 madeira clara, 6 vermelho, 7 verde,
# 8 laranja, 9 branco, 10 amarelo, 11 azul, 12 roxo, 13 cobre, 14 rosa
def icon_hoe():
    cv = Canvas(16, 16)
    cv.line(3, 14, 12, 4, 4); cv.line(4, 14, 13, 4, 5)
    cv.rect(10, 2, 14, 3, 2); cv.rect(13, 2, 14, 6, 2); cv.rect(10, 2, 13, 2, 3)
    cv.outline(1)
    return cv


def icon_can():
    cv = Canvas(16, 16)
    cv.rect(3, 6, 10, 13, 11); cv.rect(8, 6, 10, 13, 12 - 1 + 1 - 1 + 0 if False else 11)
    cv.rect(9, 7, 10, 13, 2)
    cv.rect(4, 7, 4, 12, 3)
    cv.line(10, 9, 14, 5, 2); cv.line(10, 10, 14, 6, 2); cv.rect(13, 3, 15, 5, 2)
    cv.line(4, 6, 6, 3, 2); cv.line(8, 6, 6, 3, 2)
    cv.outline(1)
    return cv


def icon_seed():
    cv = Canvas(16, 16)
    cv.ell(8, 10, 5, 5, 4); cv.rect(5, 4, 10, 5, 5)
    cv.rect(6, 8, 9, 11, 9)
    cv.rect(8, 6, 8, 9, 7); cv.px(7, 6, 7); cv.px(9, 7, 7)
    cv.outline(1)
    return cv


def icon_turnip():
    cv = Canvas(16, 16)
    cv.ell(8, 10, 4.5, 4.5, 9); cv.ell(8, 8, 4.5, 2.4, 12, only_over=[9])
    cv.rect(8, 14, 8, 15, 9)
    cv.rect(7, 3, 7, 6, 7); cv.rect(9, 2, 9, 6, 7); cv.rect(5, 4, 6, 5, 7); cv.rect(10, 3, 11, 5, 7)
    cv.px(6, 11, 3)
    cv.outline(1)
    return cv


def icon_tomato():
    cv = Canvas(16, 16)
    cv.ell(8, 9, 5.5, 5, 6); cv.ell(6, 7, 2, 1.5, 14, only_over=[6])
    cv.rect(6, 3, 10, 4, 7); cv.rect(7, 2, 9, 2, 7); cv.rect(8, 1, 8, 1, 7)
    cv.outline(1)
    return cv


def icon_egg():
    cv = Canvas(16, 16)
    cv.ell(8, 9, 4.5, 5.5, 9); cv.ell(8, 11, 4, 3.5, 3, only_over=[9]); cv.px(6, 6, 9); cv.px(6, 7, 9)
    cv.outline(1)
    return cv


def icon_milk():
    cv = Canvas(16, 16)
    cv.rect(5, 5, 10, 14, 9); cv.rect(9, 5, 10, 14, 3)
    cv.rect(6, 2, 9, 4, 9); cv.rect(5, 2, 10, 2, 11)
    cv.rect(6, 8, 9, 11, 11)
    cv.outline(1)
    return cv


def icon_pick():
    cv = Canvas(16, 16)
    cv.line(4, 14, 11, 6, 4); cv.line(5, 14, 12, 6, 5)
    cv.ell(10, 6, 5, 2, 2); cv.rect(2, 4, 4, 6, 2); cv.rect(15, 4, 15, 6, 2)
    cv.ell(10, 5, 4, 1, 3, only_over=[2])
    cv.outline(1)
    return cv


def icon_sword():
    cv = Canvas(16, 16)
    cv.line(4, 12, 13, 3, 3); cv.line(5, 12, 14, 3, 2); cv.line(3, 12, 12, 3, 2)
    cv.rect(3, 9, 7, 10, 10); cv.rect(2, 13, 4, 14, 4); cv.line(3, 13, 6, 10, 5)
    cv.outline(1)
    return cv


def icon_ore():
    cv = Canvas(16, 16)
    cv.ell(8, 9, 6, 5, 2); cv.ell(7, 8, 4, 3, 3, only_over=[2])
    for x, y in ((5, 8), (9, 6), (10, 10), (7, 11)):
        cv.rect(x, y, x + 1, y + 1, 13)
    cv.outline(1)
    return cv


def icon_heart():
    cv = Canvas(16, 16)
    cv.ell(5, 6, 3.4, 3.2, 6); cv.ell(11, 6, 3.4, 3.2, 6)
    for y in range(7, 14):
        w = 7 - (y - 7)
        cv.rect(8 - w, y, 7 + w, y, 6)
    cv.px(4, 4, 14); cv.px(5, 4, 14); cv.px(4, 5, 14)
    cv.outline(1)
    return cv


def icon_coin():
    cv = Canvas(16, 16)
    cv.ell(8, 8, 6, 6, 8); cv.ell(8, 8, 4.6, 4.6, 10, only_over=[8]); cv.rect(7, 5, 8, 11, 8)
    cv.px(5, 5, 9); cv.px(6, 4, 9)
    cv.outline(1)
    return cv


ICONS = [icon_hoe(), icon_can(), icon_seed(), icon_turnip(), icon_tomato(), icon_egg(), icon_milk(), icon_pick(),
         icon_sword(), icon_ore(), icon_heart(), icon_coin()]
for i, cv in enumerate(ICONS):
    add("ICN%02d" % i, cv, P["ICON"], "icones")


# ---------------------------------------------------------------- efeitos
def dust(frame):
    cv = Canvas(16, 16)
    r = (2, 3.5, 5, 6.5)[frame]
    a = (7, 4, 2, 1)[frame]
    for ang in range(0, 360, 60):
        import math
        x = 8 + math.cos(math.radians(ang)) * r * 0.9
        y = 11 + math.sin(math.radians(ang)) * r * 0.45
        cv.ell(x, y, max(1.0, a * 0.5), max(1.0, a * 0.4), 8 if frame < 2 else 9)
    cv.ell(8, 11, max(1.0, 3 - frame * 0.7), max(1.0, 2 - frame * 0.4), 8)
    return cv


def sparkle(frame):
    cv = Canvas(16, 16)
    L = (2, 4, 6, 3)[frame]
    cv.rect(8 - L, 8, 8 + L, 8, 2); cv.rect(8, 8 - L, 8, 8 + L, 2)
    cv.rect(7, 7, 9, 9, 1); cv.px(8, 8, 1)
    if frame in (1, 2):
        cv.px(8 - L // 2, 8 - L // 2, 1); cv.px(8 + L // 2, 8 + L // 2, 1)
        cv.px(8 - L // 2, 8 + L // 2, 1); cv.px(8 + L // 2, 8 - L // 2, 1)
    return cv


def slash(frame):
    cv = Canvas(32, 32)
    import math
    for t in range(0, 100):
        ang = math.radians(-70 + t * (60 + frame * 25) / 100.0)
        for rr, c in ((13, 1 + 3), (12, 1), (11, 1), (10, 4 - 1)):
            x = 16 + math.cos(ang) * rr
            y = 18 + math.sin(ang) * rr
            cv.px(int(round(x)), int(round(y)), c)
    return cv


for f in range(4):
    add("DST%d" % f, dust(f), P["EFFX"], "efeitos")
for f in range(4):
    add("SPK%d" % f, sparkle(f), P["EFFX"], "efeitos")
for f in range(3):
    add("SLS%d" % f, slash(f), P["EFFX"], "efeitos")
