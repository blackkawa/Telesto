"""Efeitos sonoros e música de teste, sintetizados por código."""
import wave
import numpy as np
from scipy import signal

SR = 15360      # taxa dos efeitos (o artigo do Jo Engine recomenda 15,36 ou 30,72 kHz)
rng = np.random.default_rng(11)


def t_(dur, sr=SR):
    return np.arange(int(dur * sr)) / sr


def sine(f, dur, sr=SR):
    return np.sin(2 * np.pi * f * t_(dur, sr))


def square(f, dur, duty=0.5, sr=SR):
    ph = (t_(dur, sr) * f) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def sweep(f0, f1, dur, sr=SR):
    t = t_(dur, sr)
    f = f0 + (f1 - f0) * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / sr)


def noise(dur, sr=SR):
    return rng.uniform(-1, 1, int(dur * sr))


def decay(n, k):
    return np.exp(-k * np.arange(n) / n)


def fade(x, a=0.004, r=0.01, sr=SR):
    na, nr = int(a * sr), int(r * sr)
    x = x.copy()
    if na:
        x[:na] *= np.linspace(0, 1, na)
    if nr:
        x[-nr:] *= np.linspace(1, 0, nr)
    return x


def band(x, lo, hi, sr=SR):
    nyq = sr / 2
    hi = min(hi, nyq * 0.95)
    b, a = signal.butter(2, [lo / nyq, hi / nyq], btype="band")
    return signal.lfilter(b, a, x)


def low(x, fc, sr=SR):
    b, a = signal.butter(2, fc / (sr / 2))
    return signal.lfilter(b, a, x)


def high(x, fc, sr=SR):
    b, a = signal.butter(2, fc / (sr / 2), btype="high")
    return signal.lfilter(b, a, x)


def cat(*parts):
    return np.concatenate(parts)


def mix(*parts):
    n = max(len(p) for p in parts)
    out = np.zeros(n)
    for p in parts:
        out[:len(p)] += p
    return out


def sfx():
    d = {}
    n = int(.18 * SR)
    d["HOE"] = fade(mix(sweep(150, 55, .18) * decay(n, 6), low(noise(.18), 900) * decay(n, 14) * 0.9))
    n = int(.25 * SR)
    wob = 0.7 + 0.3 * np.sin(2 * np.pi * 14 * t_(.25))
    d["WATER"] = fade(band(noise(.25), 600, 3200) * wob * np.linspace(1, 0.2, n), 0.02, 0.05)
    n = int(.10 * SR)
    d["PLANT"] = fade(sweep(280, 620, .10) * decay(n, 3))
    notes = [(784, .12), (1047, .12), (1319, .16)]
    d["HARVEST"] = cat(*[fade(sine(f, du) * decay(int(du * SR), 3.5) + 0.3 * sine(2 * f, du) * decay(int(du * SR), 6)) for f, du in notes])
    d["PICKUP"] = cat(*[fade(square(f, .05, 0.5) * 0.6, 0.002, 0.01) for f in (660, 880, 1320)])
    d["CURSOR"] = fade(square(1000, .03, 0.5) * decay(int(.03 * SR), 2), 0.001, 0.005)
    d["OK"] = cat(*[fade(square(f, .06, 0.25) * 0.6, 0.002, 0.012) for f in (880, 1320)])
    n = int(.40 * SR)
    crackle = np.zeros(n)
    idx = rng.integers(0, n, 40)
    crackle[idx] = rng.uniform(0.5, 1.0, 40) * rng.choice([-1, 1], 40)
    d["SIZZLE"] = fade(mix(high(noise(.40), 2200) * 0.7 * np.linspace(1, 0.3, n), crackle), 0.02, 0.08)
    n = int(.35 * SR)
    d["DING"] = fade((sine(1568, .35) + 0.4 * sine(3136, .35) + 0.2 * sine(4704, .35)) * decay(n, 5.5), 0.002, 0.02)
    n = int(.16 * SR)
    e = np.sin(np.pi * np.arange(n) / n) ** 1.5
    d["SWING"] = fade(band(noise(.16), 1500, 5500) * e, 0.01, 0.03)
    n = int(.12 * SR)
    d["HIT"] = fade(mix(noise(.05) * decay(int(.05 * SR), 5) * 0.9, sweep(120, 60, .12) * decay(n, 5)), 0.001, 0.01)
    parts = []
    for off, du in ((0, .08), (int(.07 * SR), .08), (int(.15 * SR), .10)):
        z = np.zeros(off + int(du * SR))
        z[off:] = band(noise(du), 400, 2500) * decay(int(du * SR), 5)
        parts.append(z)
    d["ROCK"] = fade(mix(*parts, sweep(90, 50, .2) * decay(int(.2 * SR), 6) * 0.8), 0.001, 0.02)
    for k, v in d.items():
        v = np.clip(v / (np.max(np.abs(v)) + 1e-9) * 0.85, -1, 1)
        d[k] = v
    return d


def to_s16be(x):
    return (np.clip(x, -1, 1) * 32767).astype(">i2").tobytes()


def write_wav(path, x, sr, channels=1):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------------ música (44,1 kHz estéreo)
MSR = 44100


def tri(f, dur):
    t = np.arange(int(dur * MSR)) / MSR
    return 2 * np.abs(2 * ((t * f) % 1.0) - 1) - 1


def sq(f, dur, duty=0.5):
    t = np.arange(int(dur * MSR)) / MSR
    return np.where(((t * f) % 1.0) < duty, 1.0, -1.0)


def hz(note):   # nota MIDI -> Hz
    return 440.0 * 2 ** ((note - 69) / 12)


def render(events, total, tail=1.0):
    """events: (tempo_s, dur_s, midi, voz, ganho, pan). Dobra a cauda sobre o início para o loop ficar contínuo."""
    n = int(total * MSR)
    buf = np.zeros((n + int(tail * MSR), 2))
    for (t0, du, m, voice, g, pan) in events:
        du_ = du + 0.25
        if voice == "tri":
            w = tri(hz(m), du_)
        elif voice == "sq":
            w = sq(hz(m), du_, 0.25) * 0.5
        else:
            w = tri(hz(m), du_) * 0.8
        k = len(w)
        env = np.ones(k)
        a = int(0.01 * MSR)
        env[:a] = np.linspace(0, 1, a)
        rel = int(0.25 * MSR)
        env[-rel:] *= np.linspace(1, 0, rel) ** 1.5
        env *= np.exp(-1.2 * np.arange(k) / (du_ * MSR))
        s = int(t0 * MSR)
        w = w * env * g
        buf[s:s + k, 0] += w * (1 - pan) * 0.5 * 2 ** 0.5 / 1.0
        buf[s:s + k, 1] += w * (1 + pan) * 0.5 * 2 ** 0.5 / 1.0
    out = buf[:n].copy()
    ex = buf[n:]
    out[:len(ex)] += ex
    return out


def hat(t0, g=0.12):
    n = int(0.05 * MSR)
    x = rng.uniform(-1, 1, n) * np.exp(-8 * np.arange(n) / n) * g
    b, a = signal.butter(2, 6000 / (MSR / 2), btype="high")
    return signal.lfilter(b, a, x)


def kick(g=0.5):
    n = int(0.16 * MSR)
    t = np.arange(n) / MSR
    f = 120 * np.exp(-20 * t) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / MSR) * np.exp(-14 * t) * g


def song_farm():
    bpm = 96
    beat = 60 / bpm
    total = 32 * beat           # 8 compassos de 4 tempos = 20 s
    chords = [(48, [0, 4, 7]), (45, [0, 3, 7]), (53, [0, 4, 7]), (43, [0, 4, 7])] * 2   # C Am F G
    ev = []
    for bar, (root, tri_) in enumerate(chords):
        t0 = bar * 4 * beat
        ev.append((t0, 2 * beat, root, "bass", 0.45, 0))
        ev.append((t0 + 2 * beat, 2 * beat, root + 7, "bass", 0.35, 0))
        for i in range(8):
            ev.append((t0 + i * beat / 2, beat / 2, root + 12 + tri_[i % 3], "tri", 0.18, -0.35))
    scale = [72, 74, 76, 79, 81, 84]   # C D E G A C
    mel = [[2, 3, 4, 3, 2, 1, 0, None], [4, 4, 3, 2, 3, None, 1, 2], [3, 4, 5, 4, 3, 2, 3, None], [2, 1, 0, 1, 2, 3, 2, None]] * 2
    for bar, row in enumerate(mel):
        for i, d in enumerate(row):
            if d is None:
                continue
            ev.append((bar * 4 * beat + i * beat / 2, beat / 2 * 1.4, scale[d], "sq", 0.22, 0.3))
    out = render(ev, total)
    for bar in range(8):
        for i in range(8):
            h = hat(0, 0.10 if i % 2 else 0.14)
            s = int((bar * 4 * beat + i * beat / 2) * MSR)
            out[s:s + len(h), 0] += h
            out[s:s + len(h), 1] += h
    return out


def song_mine():
    bpm = 78
    beat = 60 / bpm
    total = 32 * beat           # ~24,6 s
    prog = [(45, [0, 3, 7]), (41, [0, 4, 7]), (43, [0, 4, 7]), (40, [0, 3, 7])] * 2   # Am F G Em
    ev = []
    for bar, (root, tri_) in enumerate(prog):
        t0 = bar * 4 * beat
        ev.append((t0, 4 * beat, root - 12, "bass", 0.5, 0))
        for i in range(4):
            ev.append((t0 + i * beat, beat * 0.9, root + 12 + tri_[(i * 2) % 3], "tri", 0.2, 0.25))
    scale = [69, 72, 74, 76, 79, 81]   # A C D E G A
    mel = [[None, 3, None, 2, None, 1, None, None], [None, 2, None, 1, 0, None, None, None],
           [None, 4, None, 3, None, 2, None, None], [None, 1, None, 0, None, None, None, None]] * 2
    for bar, row in enumerate(mel):
        for i, d in enumerate(row):
            if d is None:
                continue
            ev.append((bar * 4 * beat + i * beat / 2, beat * 1.2, scale[d], "sq", 0.2, -0.25))
    out = render(ev, total)
    for bar in range(8):
        for i in (0, 2):
            k_ = kick(0.35)
            s = int((bar * 4 * beat + i * beat * 1.0 * 1.0) * MSR)
            out[s:s + len(k_), 0] += k_
            out[s:s + len(k_), 1] += k_
    return out


def norm_stereo(x, peak=0.8):
    return np.clip(x / (np.max(np.abs(x)) + 1e-9) * peak, -1, 1)


def write_stereo_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(MSR)
        w.writeframes(pcm.tobytes())
