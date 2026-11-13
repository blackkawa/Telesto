"""Biblioteca comum: canvas indexado, paletas, escrita de TGA 8 bits e PNG."""
import struct
import numpy as np
from PIL import Image


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    """Imagem indexada (índices 0..15). Índice 0 = transparente."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w), np.uint8)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return int(self.a[y, x])
        return 0

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def ell(self, cx, cy, rx, ry, c, only_over=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    if only_over is None or self.get(x, y) in only_over:
                        self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def outline(self, c):
        """Contorno de 1 px nos pixels transparentes vizinhos (4 vizinhos)."""
        src = self.a.copy()
        for y in range(self.h):
            for x in range(self.w):
                if src[y, x] == 0:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < self.w and 0 <= yy < self.h and src[yy, xx] not in (0, c):
                            self.a[y, x] = c
                            break

    def flip(self):
        o = Canvas(self.w, self.h)
        o.a = self.a[:, ::-1].copy()
        return o

    def paste(self, o, x, y):
        for yy in range(o.h):
            for xx in range(o.w):
                v = o.a[yy, xx]
                if v:
                    self.px(x + xx, y + yy, int(v))

    def copy(self):
        o = Canvas(self.w, self.h)
        o.a = self.a.copy()
        return o


class Palette:
    """Paleta de 16 entradas: 0 = transparente, 1..14 = cores, 15 = reservada."""

    def __init__(self, name, colors14):
        assert len(colors14) == 14, (name, len(colors14))
        self.name = name
        self.rgb = [(255, 0, 255)] + [hx(c) for c in colors14] + [(0, 0, 0)]


def to_rgba(cv, pal, scale=1):
    a = np.zeros((cv.h, cv.w, 4), np.uint8)
    for i, (r, g, b) in enumerate(pal.rgb):
        m = cv.a == i
        a[m] = (r, g, b, 0 if i == 0 else 255)
    im = Image.fromarray(a, "RGBA")
    if scale != 1:
        im = im.resize((cv.w * scale, cv.h * scale), Image.NEAREST)
    return im


def write_tga(path, cv, pal):
    """TGA 8 bits com mapa de cores (tipo 1), sem compressão, origem inferior esquerda.
    16 entradas de paleta (BGR de 24 bits)."""
    assert cv.w % 8 == 0, "largura precisa ser múltipla de 8 (VDP1)"
    assert cv.a.max() <= 14, "índices acima de 14 não são usados"
    hdr = struct.pack("<BBBHHBHHHHBB", 0, 1, 1, 0, 16, 24, 0, 0, cv.w, cv.h, 8, 0)
    cmap = b"".join(bytes((b, g, r)) for (r, g, b) in pal.rgb)
    rows = b"".join(cv.a[y].tobytes() for y in range(cv.h - 1, -1, -1))
    with open(path, "wb") as f:
        f.write(hdr + cmap + rows)


def rgb555(r, g, b):
    return ((b >> 3) << 10) | ((g >> 3) << 5) | (r >> 3)


def write_tga_packed(path, cv, pal, group):
    """TGA 8 bits para o Jo Engine com banco de 256 cores: pixels != 0 recebem +16*group.
    O mapa de cores tem 16*(group+1) entradas (as anteriores ficam pretas); o jogo reescreve o banco inteiro."""
    assert cv.w % 8 == 0 and cv.a.max() <= 14 and group <= 14
    off = 16 * group
    n = off + 16
    a = np.where(cv.a == 0, 0, cv.a + off).astype(np.uint8)
    hdr = struct.pack("<BBBHHBHHHHBB", 0, 1, 1, 0, n, 24, 0, 0, cv.w, cv.h, 8, 0)
    cm = [(0, 0, 0)] * off + list(pal.rgb)
    cmap = b"".join(bytes((b, g_, r)) for (r, g_, b) in cm)
    rows = b"".join(a[y].tobytes() for y in range(cv.h - 1, -1, -1))
    with open(path, "wb") as f:
        f.write(hdr + cmap + rows)
