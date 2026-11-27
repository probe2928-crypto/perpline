#!/usr/bin/env python3
"""Synthesised sound for Perpline "Break-even, after fees." (no outside audio).
python3 src/sound.py [target RMS dB] -> assets/audio/breakeven-mix.wav (48 kHz stereo, 15.6 s)
Cues = picture + 1 frame (33 ms)."""
import numpy as np, pathlib, sys
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
TARGET = float(sys.argv[1]) if len(sys.argv) > 1 else -17.0
SR = 48000; DUR = 15.0; N = int(SR * DUR); F = 1 / 30
rng = np.random.default_rng(20261127); out = np.zeros((N, 2))
def t_(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d)
def add(x, at, g=1.0, pan=0.0):
    i = int(at * SR); x = x[: max(0, N - i)]; l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    out[i:i + len(x), 0] += x * g * l * 1.414; out[i:i + len(x), 1] += x * g * r * 1.414
def pad(fr, a, b, g, fi=.4, fo=.6):
    t = t_(b - a); x = np.zeros_like(t)
    for f in fr:
        for d in (-.15, .15): ph = rng.uniform(0, 6.28); x += np.sin(2*np.pi*(f+d)*t+ph) + .2*np.sin(4*np.pi*(f+d)*t+ph)
    x = lp(x * (0.8 + 0.2*np.sin(2*np.pi*.2*t)), 2200); e = np.minimum(1, t/fi) * np.minimum(1, (t[-1]-t)/fo)
    add(x * e * g / len(fr), a)
pad([55, 110, 130.8, 164.8, 196, 246.9], 0, 3.4, .16, .05, .5)            # tension
pad([65.4, 130.8, 164.8, 196, 246.9, 329.6], 3.1, 9.6, .16, .4, .6)        # relief once the line drops
pad([43.65, 87.3, 130.8, 174.6, 220, 261.6, 329.6], 9.2, 15, .17, .3, .9)  # end
def tick(f=2200, d=.03): t = t_(d); n = rng.standard_normal(len(t)); return (bp(n, f*.6, f*1.6) + .6*np.sin(2*np.pi*f*t)) * env(len(t), .0008, d/5)
for k in range(16): add(tick(2600 + (k % 3) * 180, .025), k * 0.4 + F, .05, .35)       # price ticks
for k in range(10): add(tick(2500 + (k % 2) * 200, .02), 10.9 + k * 0.4 + F, .03, .3)    # end-card dot
def whoosh(d, lo, hi, g):
    t = t_(d); n = rng.standard_normal(len(t)); y = np.zeros_like(t); fc = np.geomspace(lo, hi, len(t)); bands = np.geomspace(min(lo,hi), max(lo,hi), 7)
    for b0, b1 in zip(bands[:-1], bands[1:]): y += bp(n, b0, b1) * np.exp(-((np.log(fc) - np.log((b0*b1)**.5))**2)/.18)
    return y * np.sin(np.pi*np.clip(t/d, 0, 1))**1.6 * g
n = rng.standard_normal(int(.5*SR)); add(bp(n, 3000, 9000) * np.sin(np.pi*t_(.5)/.5)**2, 0.9, .05)
for at, d, lo, hi, g in [(1.72,.45,2400,500,.08),(3.1,.35,500,3000,.06),(3.48,.5,400,3500,.09),(5.98,.4,300,4200,.18),(6.3,.8,3800,250,.13),(8.93,.3,500,3800,.12),(9.2,.8,2800,250,.1)]:
    add(whoosh(d, lo, hi, 1), at, g)
t = t_(.5); click = bp(rng.standard_normal(len(t)), 1800, 7000) * env(len(t), .0005, .008)
add(click * .8 + lp(np.sin(2*np.pi*196*t), 800) * env(len(t), .002, .05) * .35 + np.sin(2*np.pi*49*t) * env(len(t), .01, .25) * .35, 2.5 + F, .5)
t = t_(1.0); f = np.geomspace(660, 440, len(t)); add(np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/1.0)**2 * .5, 2.8 + F, .09)
tt = t_(1.6); ding = sum(a*np.sin(2*np.pi*fr*tt)*env(len(tt), .003, d) for fr, a, d in [(1046.5,.5,.6),(1568,.3,.45),(2093,.15,.3)])
add(ding, 3.42 + F, .12, .1)
add(tick(1900, .04), 3.74 + F, .1)
n = rng.standard_normal(int(.4*SR)); add(bp(n, 1500, 5000) * np.sin(np.pi*t_(.4)/.4)**2, 7.05 + F, .07)
tt = t_(1.8); add(lp(np.sin(2*np.pi*87.3*tt) + .6*np.sin(2*np.pi*174.6*tt) + .3*np.sin(2*np.pi*349.2*tt), 1200) * env(len(tt), .006, .6), 9.33 + F, .4)
add(tick(1500, .05), 9.6 + F, .14)
ir_t = t_(.8); ir = rng.standard_normal((len(ir_t), 2)) * np.exp(-ir_t/.2)[:, None]; ir[:, 0] = hp(ir[:, 0], 250); ir[:, 1] = hp(ir[:, 1], 250)
wet = np.stack([fftconvolve(out[:, c], ir[:, c])[:N] for c in range(2)], 1); mix = out + wet * (0.18 / np.abs(ir).sum(0).max() * 40)
tail = np.ones(N); i0 = int((DUR - .6) * SR); tail[i0:] = np.linspace(1, 0, N - i0) ** 1.5; mix *= tail[:, None]
mix *= 10 ** (TARGET/20) / max(np.sqrt(np.mean(mix**2)), 1e-9); mix = np.tanh(mix*1.2)/1.2
pk = np.abs(mix).max(); lim = 10 ** (-1.2/20)
if pk > lim: mix *= lim / pk
dst = pathlib.Path(__file__).resolve().parent.parent / "assets/audio/breakeven-mix.wav"
wavfile.write(dst, SR, (mix*32767).astype(np.int16)); print("wrote", dst, "peak", round(20*np.log10(np.abs(mix).max()), 2))
