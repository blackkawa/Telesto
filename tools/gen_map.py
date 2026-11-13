"""Mapa de teste 64x64: camadas de solo, objetos e estado das culturas (2 bytes por tile)."""
import random
import struct
import numpy as np

W = H = 64
# ids de terreno (TRNxx)
G0, G1, G2, D0, D1, TIL, WET, PA0, PA1, W0, W1, SHN, SHS, SHE, SHW, SAND = range(16)
# ids de estrutura (STRxx)
FH, FV, FP, TRUNK, CANOPY, ROCK, BUSH, WFLOOR, WWALL, RL, RM, RR, DOOR, WIN, SIGN, CHEST = range(16)


def build():
    r = random.Random(2026)
    ground = np.zeros((H, W), np.uint8)
    obj = np.zeros((H, W), np.uint8)       # 0 = nada; senão id de estrutura + 1
    crop = np.zeros((H, W), np.uint16)     # bits 0-2 tipo (1..6), 3-5 estágio (0..4), 6 regado, 7 adubo
    for y in range(H):
        for x in range(W):
            v = r.random()
            ground[y, x] = G0 if v < 0.70 else (G1 if v < 0.92 else G2)

    # lagoa
    cx, cy, rx, ry = 50, 14, 8, 5
    for y in range(H):
        for x in range(W):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                ground[y, x] = W0
    water = (ground == W0)
    for y in range(H):
        for x in range(W):
            if water[y, x]:
                continue
            if y > 0 and water[y - 1, x]:
                ground[y, x] = SHN
            elif y < H - 1 and water[y + 1, x]:
                ground[y, x] = SHS
            elif x < W - 1 and water[y, x + 1]:
                ground[y, x] = SHE
            elif x > 0 and water[y, x - 1]:
                ground[y, x] = SHW

    # casa: telhado (2 linhas), paredes (2 linhas), porta
    for y in (5, 6):
        obj[y, 28] = RL + 1
        for x in range(29, 33):
            obj[y, x] = RM + 1
        obj[y, 33] = RR + 1
    for x in range(28, 34):
        obj[7, x] = (WIN if x in (29, 32) else WWALL) + 1
        obj[8, x] = WWALL + 1
    obj[8, 30] = DOOR + 1
    obj[8, 31] = DOOR + 1

    # caminho de cascalho de x=30..31, da porta até a borda sul
    for y in range(9, H):
        for x in (30, 31):
            ground[y, x] = PA0 if r.random() < 0.6 else PA1

    # lote cultivado com cerca
    x0, y0, x1, y1 = 10, 24, 33, 38
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if x in (30, 31):
                continue
            ground[y, x] = WET if r.random() < 0.30 else TIL
    for x in range(x0 - 1, x1 + 2):
        for y in (y0 - 1, y1 + 1):
            if x not in (30, 31):
                obj[y, x] = FH + 1
    for y in range(y0 - 1, y1 + 2):
        for x in (x0 - 1, x1 + 1):
            obj[y, x] = FV + 1
    for (x, y) in ((x0 - 1, y0 - 1), (x1 + 1, y0 - 1), (x0 - 1, y1 + 1), (x1 + 1, y1 + 1), (29, y0 - 1), (32, y0 - 1),
                   (29, y1 + 1), (32, y1 + 1)):
        obj[y, x] = FP + 1
    # culturas: faixas por tipo, estágios variados
    n_crops = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, 30):
            if x % 2 == 0 and y % 2 == 1:
                kind = ((x - x0) // 4) % 6 + 1
                stage = ((x + y) // 2) % 5
                wet = 1 if ground[y, x] == WET else 0
                crop[y, x] = kind | (stage << 3) | (wet << 6)
                n_crops += 1

    occupied = lambda x, y: bool(obj[y, x]) or ground[y, x] in (W0, SHN, SHS, SHE, SHW, PA0, PA1) or crop[y, x]
    # sinal e baú
    obj[10, 29] = SIGN + 1
    obj[9, 34] = CHEST + 1

    def free_margin(x, y):
        if not (1 <= x < W - 1 and 2 <= y < H - 1):
            return False
        if (x0 - 3 <= x <= x1 + 3 and y0 - 4 <= y <= y1 + 3) or (26 <= x <= 36 and 3 <= y <= 12):
            return False
        if 38 <= x <= 62 and 5 <= y <= 22:
            return False
        for yy in (y - 1, y):
            if occupied(x, yy):
                return False
        return True

    placed = 0
    tries = 0
    while placed < 26 and tries < 4000:
        tries += 1
        x, y = r.randrange(1, W - 1), r.randrange(2, H - 1)
        if free_margin(x, y):
            obj[y, x] = TRUNK + 1
            obj[y - 1, x] = CANOPY + 1
            placed += 1
    n_trees = placed
    for kind, count in ((ROCK, 12), (BUSH, 10)):
        placed = 0
        tries = 0
        while placed < count and tries < 4000:
            tries += 1
            x, y = r.randrange(1, W - 1), r.randrange(2, H - 1)
            if free_margin(x, y) and ground[y, x] in (G0, G1, G2):
                obj[y, x] = kind + 1
                placed += 1

    lamps = [(29, 9, 6), (33, 10, 6), (9, 22, 6), (34, 40, 6)]
    # pontos de nascimento de sprites para o teste de carga: 16 galinhas e 8 slimes (em pixels, canto superior esquerdo)
    spawns = []
    while len(spawns) < 24:
        x, y = r.randrange(2, W - 2), r.randrange(8, H - 2)
        if not occupied(x, y) and not (x0 - 1 <= x <= x1 + 1 and y0 - 1 <= y <= y1 + 1):
            spawns.append(("CHK" if len(spawns) < 16 else "SLM", x * 16, y * 16))
    stats = dict(crops=n_crops, trees=n_trees)
    return ground, obj, crop, lamps, spawns, stats


def pack(ground, obj, crop):
    b = bytearray(b"FARM" + struct.pack(">HH", W, H))
    b += ground.tobytes() + obj.tobytes()
    b += b"".join(struct.pack(">H", int(v)) for v in crop.flatten())
    return bytes(b)
