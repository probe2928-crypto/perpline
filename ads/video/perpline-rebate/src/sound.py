#!/usr/bin/env python3
"""Synthesised sound design for the Perpline rebate ad (no outside audio at all).

  python3 src/sound.py  ->  assets/audio/perpline-rebate-mix.wav (48 kHz stereo, 20 s)

Cue times come from the GSAP timeline in src/template.html; each hit lands one frame
(33 ms) after its picture. Edit CUES below when the timeline moves.
"""
import numpy as np, pathlib
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

import sys
TARGET_RMS = float(sys.argv[1]) if len(sys.argv) > 1 else -15.5
SR = 48000; DUR = 20.0; N = int(SR * DUR); F = 1 / 30
rng = np.random.default_rng(20261110)
out = np.zeros((N, 2))

def t_(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def add(x, at, gain=1.0, pan=0.0):
    i = int((at) * SR); x = x[: max(0, N - i)]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    out[i : i + len(x), 0] += x * gain * l * 1.414; out[i : i + len(x), 1] += x * gain * r * 1.414
def env(n, a, d):  # attack / exponential decay
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d); return e

# ---- pad bed: E minor9 (cool, the fee) → G major7 lydian from the hero → E major add9 end card
def pad(freqs, start, end, gain, fade_in=1.2, fade_out=1.0):
    t = t_(end - start); x = np.zeros_like(t)
    for k, f in enumerate(freqs):
        for det in (-0.12, 0.12):
            ph = rng.uniform(0, 2 * np.pi)
            x += np.sin(2 * np.pi * (f + det) * t + ph) + 0.22 * np.sin(4 * np.pi * (f + det) * t + ph)
    x *= (0.78 + 0.22 * np.sin(2 * np.pi * 0.16 * t))
    x = lp(x, 2400); e = np.minimum(1, t / fade_in) * np.minimum(1, (t[-1] - t) / fade_out)
    return x * e * gain / len(freqs)
add(pad([41.2, 82.4, 164.8, 196.0, 246.9, 293.7, 370.0], 0.0, 1.45, 0.15, 0.05, 0.25), 0.0)
add(pad([41.2, 82.4, 164.8, 207.7, 246.9, 370.0, 493.9], 1.3, 11.0, 0.17, 0.3, 0.4), 1.3)
add(pad([49.0, 98.0, 196, 246.9, 293.7, 370.0, 587.3], 10.7, 17.25, 0.17, 0.6, 0.5), 10.7)
add(pad([41.2, 82.4, 164.8, 207.7, 246.9, 370.0, 659.3], 17.0, 20.0, 0.18, 0.25, 0.9), 17.0)

# ---- soft pulse (104 BPM) under the site flow + cards, again under the week
def kick(g=1.0):
    t = t_(0.35); f = 46 + 54 * np.exp(-t * 32); ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * env(len(t), 0.004, 0.12)
    return lp(x, 900) * g
beat = 60 / 104
for k in range(int((9.75 - 2.52) / beat)):
    add(kick(0.36 if k % 2 == 0 else 0.26), 2.52 + F + k * beat)
for k in range(int((15.2 - 13.0) / beat)):
    add(kick(0.26), 13.0 + F + k * beat)
for k in range(int((6.9 - 2.82) / beat)):
    n = rng.standard_normal(int(0.05 * SR)); add(bp(n, 5000, 11000) * env(len(n), 0.002, 0.016), 2.82 + beat / 2 + k * beat, 0.035, 0.3 * (-1) ** k)

# ---- hook: low ticker hum, the light line slices (rising air + bright edge), the new fee blooms
t = t_(1.0); add(lp(rng.standard_normal(len(t)), 300) * np.minimum(1, t / 0.05) * np.exp(-t / 0.7), 0.0, 0.12)
for k in range(14):
    add(np.sin(2 * np.pi * rng.uniform(2400, 4200) * t_(0.04)) * env(int(0.04 * SR), 0.001, 0.01), 0.05 + k * 0.065 + rng.uniform(0, 0.02), 0.025, rng.uniform(-0.7, 0.7))
t = t_(0.5); ph = 2 * np.pi * np.cumsum(np.geomspace(500, 3000, len(t))) / SR
add(bp(rng.standard_normal(len(t)), 2000, 9000) * np.sin(np.pi * t / 0.5) ** 2 * 0.6 + np.sin(ph) * np.sin(np.pi * t / 0.5) ** 2 * 0.15, 0.48, 0.16, -0.4)
tt = t_(1.6); add(lp(np.sin(2 * np.pi * 82.4 * tt) + 0.5 * np.sin(2 * np.pi * 164.8 * tt) + 0.2 * np.sin(2 * np.pi * 329.6 * tt), 1000) * env(len(tt), 0.03, 0.5), 0.91 + F, 0.32)
tt = t_(1.2); add(np.sin(2 * np.pi * 1318.5 * tt) * env(len(tt), 0.004, 0.35) * 0.5 + np.sin(2 * np.pi * 1975.5 * tt) * env(len(tt), 0.004, 0.25) * 0.25, 0.93 + F, 0.07)

# ---- whooshes (varied)
def whoosh(d, lo, hi, up=True, g=1.0):
    t = t_(d); n = rng.standard_normal(len(t)); fc = np.geomspace(lo, hi, len(t)) if up else np.geomspace(hi, lo, len(t))
    y = np.zeros_like(t); bands = np.geomspace(min(lo, hi), max(lo, hi), 7)
    for b0, b1 in zip(bands[:-1], bands[1:]):
        w = np.exp(-((np.log(fc) - np.log((b0 * b1) ** 0.5)) ** 2) / 0.18); y += bp(n, b0, b1) * w
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6
    return y * e * g
for at, d, lo, hi, up, g, pan in [
    (2.38, 0.45, 300, 4000, True, 0.24, 0.0),    # push-through
    (2.5, 0.6, 2200, 300, False, 0.14, 0.2),     # phone rises in
    (3.54, 0.5, 2600, 500, False, 0.07, -0.2),   # page scroll
    (4.06, 0.7, 300, 2200, True, 0.08, 0.0),     # push to the BTCC row
    (6.06, 0.5, 2600, 500, False, 0.07, 0.2),    # page scroll
    (6.9, 0.6, 2500, 250, False, 0.22, -0.2),    # phone drops away
    (7.12, 0.8, 200, 2400, True, 0.15, 0.3),     # cards fan out
    (9.3, 0.5, 600, 4500, True, 0.18, 0.0),      # cards gather
    (9.8, 1.1, 180, 1400, True, 0.12, -0.3),     # hero swing
    (10.78, 0.78, 250, 2000, True, 0.12, 0.0),   # macro push
    (12.38, 0.5, 2000, 300, False, 0.13, 0.0),   # pull back
    (12.75, 0.5, 3500, 250, False, 0.16, 0.0),   # hero leaves
    (12.95, 0.7, 250, 2600, True, 0.13, 0.2),    # week arrives
    (15.88, 0.3, 500, 3500, True, 0.1, 0.0),     # copy swap
    (16.86, 0.8, 250, 3500, True, 0.2, 0.0),     # iris flood
]:
    add(whoosh(d, lo, hi, up, 1.0), at, g, pan)

# ---- UI taps, highlight, page change
def tick(f=2200, d=0.03, g=1.0):
    t = t_(d); n = rng.standard_normal(len(t)); return (bp(n, f * 0.6, f * 1.6) + 0.6 * np.sin(2 * np.pi * f * t)) * env(len(t), 0.0008, d / 5) * g
add(tick(2400, 0.03), 3.42 + F, 0.17)
tt = t_(0.4); add((np.sin(2 * np.pi * 987.8 * tt) * 0.5 + np.sin(2 * np.pi * 1479.98 * tt) * 0.25) * env(len(tt), 0.003, 0.1), 4.5 + F, 0.09, 0.15)
add(tick(1500, 0.06), 5.3 + F, 0.24)
tt = t_(0.5); add((np.sin(2 * np.pi * 659.3 * tt) * 0.6 + np.sin(2 * np.pi * 987.8 * tt) * 0.3) * env(len(tt), 0.004, 0.12), 5.36 + F, 0.12)
# ---- decisive moment: bright strike line, a counter-wheel click as the old fee falls, soft sub + glass ting as 0.018% lands
t = t_(0.26); add(bp(rng.standard_normal(len(t)), 3000, 10000) * np.sin(np.pi * t / 0.26) ** 2, 11.5, 0.07, -0.2)
for k in range(5):
    add(tick(1900 - k * 120, 0.025), 11.74 + k * 0.022 + F, 0.09 - k * 0.012)
t = t_(0.6)
click = bp(rng.standard_normal(len(t)), 1800, 7000) * env(len(t), 0.0005, 0.008)
body = lp(np.sin(2 * np.pi * 196 * t), 800) * env(len(t), 0.002, 0.05)
sub = np.sin(2 * np.pi * 49.0 * t) * env(len(t), 0.01, 0.28)
add(click * 0.8 + body * 0.35 + sub * 0.4, 11.84 + F, 0.5)
tt = t_(2.0)
glass = sum(a * np.sin(2 * np.pi * f * tt) * env(len(tt), 0.003, d) for f, a, d in [(1567.98, .5, .7), (2349.3, .28, .5), (3135.96, .14, .35), (4698.6, .06, .2)])
add(glass, 11.86 + F, 0.09, 0.15)
add(tick(2800, 0.02), 11.98 + F, 0.08, 0.3); add(tick(1200, 0.05), 12.28 + F, 0.12)
# ---- week: light along the days, ticks as fee bars rise, coin chime on Monday
t = t_(1.2); ph = 2 * np.pi * np.cumsum(np.geomspace(330, 660, len(t))) / SR
add(np.sin(ph) * np.sin(np.pi * t / 1.2) ** 2 * 0.25 + bp(rng.standard_normal(len(t)), 2000, 6000) * np.sin(np.pi * t / 1.2) ** 2 * 0.12, 13.2, 0.1)
for k in range(7):
    add(tick(3000 + k * 80, 0.02), 13.3 + k * 0.155 + F, 0.07, (k % 3 - 1) * 0.3)
for k, f in enumerate([1318.5, 1661.2, 1975.5, 2637.0]):
    tt = t_(0.9); add(np.sin(2 * np.pi * f * tt) * env(len(tt), 0.002, 0.3), 14.42 + k * 0.045 + F, 0.07, (k - 1.5) * 0.2)
t = t_(0.4); add(lp(np.sin(2 * np.pi * 98 * t), 600) * env(len(t), 0.004, 0.12), 14.42 + F, 0.3)
for k in range(4):
    add(tick(2600, 0.02), 13.15 + k * 0.45 + F, 0.07)
# ---- copy: underline shimmer; end card: wordmark hit + CTA tick
n = rng.standard_normal(int(0.5 * SR)); t = t_(0.5); add(bp(n, 4000, 10000) * np.sin(np.pi * t / 0.5) ** 2, 16.5, 0.07)
tt = t_(1.6); add(lp(np.sin(2 * np.pi * 82.4 * tt) + 0.6 * np.sin(2 * np.pi * 164.8 * tt) + 0.3 * np.sin(2 * np.pi * 329.6 * tt), 1200) * env(len(tt), 0.006, 0.55), 17.4 + F, 0.42)
add(tick(1600, 0.05), 17.5 + F, 0.16)

# ---- room: short plate on everything
ir_t = t_(0.9); ir = rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t / 0.22)[:, None]
ir[:, 0] = hp(ir[:, 0], 250); ir[:, 1] = hp(ir[:, 1], 250)
wet = np.stack([fftconvolve(out[:, c], ir[:, c])[:N] for c in range(2)], 1)
mix = out + wet * (0.18 / np.abs(ir).sum(0).max() * 40)

# master: fade tail, gentle limit, normalise towards ~ -15 LUFS-ish RMS, peak ≤ -1 dBFS
tail = np.ones(N); i0 = int((DUR - 0.7) * SR); tail[i0:] = np.linspace(1, 0, N - i0) ** 1.5
mix *= tail[:, None]
rms = np.sqrt(np.mean(mix ** 2)); mix *= 10 ** (TARGET_RMS / 20) / max(rms, 1e-9)
mix = np.tanh(mix * 1.2) / 1.2
mix *= 10 ** (-1.2 / 20) / max(np.abs(mix).max(), 1e-9) if np.abs(mix).max() > 10 ** (-1.2 / 20) else 1
dst = pathlib.Path(__file__).resolve().parent.parent / "assets/audio/perpline-rebate-mix.wav"
wavfile.write(dst, SR, (mix * 32767).astype(np.int16))
print("wrote", dst, "peak", round(20 * np.log10(np.abs(mix).max()), 2), "dBFS rms", round(20 * np.log10(np.sqrt(np.mean(mix ** 2))), 2))
