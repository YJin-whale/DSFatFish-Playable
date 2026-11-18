# -*- coding: utf-8 -*-
"""
make_stars.py — 肥鱼跳宇宙 v4 · 银河系恒星写实贴图生成器 (star-art)

用法（项目根目录下任一路径均可执行）:
  C:\\Users\\admin\\.dsh\\dsh-runtimes\\dsh-plugin-desktop-primary-runtime\\dependencies\\python\\python.exe \\
      assets/tex/raw/star/make_stars.py

输入（可选，缺失时自动退回纯程序化）:
  raw/star/sdo_171.jpg      NASA SDO/AIA 171A 太阳全盘（公共领域）→ star_sun.png
  raw/star/eht_mwa.jpg      EHT Sgr A* 首张图像（ESO 发布，CC BY 4.0）→ star_galactic_center.png

输出:
  assets/tex/star_<id>.png                    10 颗恒星 256x256 RGBA 透明底
  assets/tex/star_sun.png                     （有 SDO 图时）
  assets/tex/star_galactic_center.png         （有 EHT 图时）
  assets/tex/star_galactic_edge.png           程序化“银河边缘”星尘（圆形透明底）
  assets/manifest-stars.json
  reports/star-contact-sheet.png              对比图（#060A22 深蓝底 + 小尺寸预览）
所有随机数按 star id 播种，输出确定可复跑。

物理/美术管线:
  Teff → Planck 光谱 × CIE1931 2° 配色函数 → XYZ → 线性 sRGB →
  白平衡到 7500K（A7V≈白；A 型偏蓝白、G 型黄白、K 型橙、M 型橙红）→
  HSV 色度按每颗星设定（保色相，仅为小尺寸可读性）→ gamma。
  光球: 线性光空间做临边昏暗（分波段，边缘更红）+ 米粒组织/对流暗巷（球面 3D 值噪声）
        + 星斑/耀斑（M 矮星）+ 色球环。
  日冕: 双指数辉光 × 角向扰动 + 4/6/8 道细衍射星芒；巨星光晕更大更亮，M 矮星更小更暗。
  真实图像: 太阳用 NASA SDO/AIA 171A；银河系中心用 EHT Sgr A*（CC BY 4.0）。
"""
import colorsys
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# ------------------------------------------------------------------ paths
HERE = os.path.dirname(os.path.abspath(__file__))          # assets/tex/raw/star
TEXDIR = os.path.dirname(os.path.dirname(HERE))           # assets/tex
ROOT = os.path.dirname(os.path.dirname(TEXDIR))           # project root
REPORTS = os.path.join(ROOT, 'reports')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest-stars.json')

OUT = 256
CANVAS = OUT * 2          # render at 512, downsample for clean anti-aliasing
HALF = CANVAS / 2.0
MAX_BYTES = 120 * 1024
GAME_BG = (6, 10, 34)     # #060A22，游戏深蓝背景

# 日冕相对强度标定：配置里给的是“相对值”，这里统一压到“光球明显更亮”的比例，
# 否则近临边处 alpha≈0.9 的白雾会把恒星糊成行星。
GLOW_CAL = dict(inner=0.42, mid=0.66, broad=0.82, mix=0.22)
HALO_FADE_WIDTH = 0.14    # 光晕外缘 alpha->0 的过渡带宽（half-canvas 单位）

# ------------------------------------------------------------------ colour
_WL = np.arange(360.0, 831.0, 2.0)


def _gauss(wl, mu, s1, s2):
    s = np.where(wl < mu, s1, s2)
    return np.exp(-0.5 * ((wl - mu) / s) ** 2)


# CIE 1931 2-deg observer, analytic approximation (Wyman/Sloan/Shirley 2013)
_XBAR = 1.056 * _gauss(_WL, 599.8, 37.9, 31.0) + 0.362 * _gauss(_WL, 442.0, 16.0, 26.7) \
        - 0.065 * _gauss(_WL, 501.1, 20.4, 26.2)
_YBAR = 0.821 * _gauss(_WL, 568.8, 46.9, 40.5) + 0.286 * _gauss(_WL, 530.9, 16.3, 31.1)
_ZBAR = 1.217 * _gauss(_WL, 437.0, 11.8, 36.0) + 0.681 * _gauss(_WL, 459.0, 26.0, 13.8)

_H = 6.62607015e-34
_C = 2.99792458e8
_K = 1.380649e-23

WB_REF_K = 7500.0   # 中性白参考：A7V≈白，F5V 暖白，G 黄白，K 橙，M 橙红


def planck_spectrum(teff):
    lam = _WL * 1e-9
    return (2.0 * _H * _C * _C / lam ** 5) / np.expm1(_H * _C / (lam * _K * teff))


def teff_to_linear_rgb(teff):
    """Blackbody spectrum -> CIE XYZ -> linear sRGB (relative, may exceed 1)."""
    spec = planck_spectrum(float(teff))
    X = (spec * _XBAR).sum()
    Y = (spec * _YBAR).sum()
    Z = (spec * _ZBAR).sum()
    x, y = X / (X + Y + Z), Y / (X + Y + Z)
    X2, Y2 = x / y, 1.0
    Z2 = (1.0 - x - y) / y
    r = 3.2406 * X2 - 1.5372 * Y2 - 0.4986 * Z2
    g = -0.9689 * X2 + 1.8758 * Y2 + 0.0415 * Z2
    b = 0.0557 * X2 - 0.2040 * Y2 + 1.0570 * Z2
    return np.array([r, g, b], dtype=np.float64)


_REF_LIN = teff_to_linear_rgb(WB_REF_K)


def srgb_to_linear(c):
    c = np.clip(np.asarray(c, dtype=np.float32), 0.0, 1.0)
    return np.where(c <= 0.04045, c / 12.92, np.power((c + 0.055) / 1.055, 2.4))


def lin_to_display(c):
    c = np.clip(np.asarray(c, dtype=np.float32), 0.0, None)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1.0 / 2.4) - 0.055)


def star_tint(teff, hsv_sat):
    """White-balanced blackbody colour with an explicit HSV chroma target.

    hue comes from the Planck spectrum (physical chromaticity); saturation is a
    documented per-star readability choice. Value=1 because photospheres are
    bright. Hue order M->K->G->F->A (orange -> white -> blue-white) is physical.
    """
    lin = np.clip(teff_to_linear_rgb(teff) / _REF_LIN, 0.0, None)
    lin = lin / lin.max()
    disp = np.clip(lin_to_display(lin), 0.0, 1.0)
    h, _, _ = colorsys.rgb_to_hsv(float(disp[0]), float(disp[1]), float(disp[2]))
    r, g, b = colorsys.hsv_to_rgb(h, float(hsv_sat), 1.0)
    return np.array([r, g, b], dtype=np.float64)


# ------------------------------------------------------------------ noise
class ValueNoise3D:
    """Seeded 3D value noise with smooth trilerp (vectorised, numpy only)."""

    def __init__(self, seed, res=48):
        self.res = int(res)
        rng = np.random.default_rng(int(seed))
        self.grid = rng.random((self.res, self.res, self.res)).astype(np.float32)

    def sample(self, P):
        P = np.asarray(P, dtype=np.float32)
        i = np.floor(P).astype(np.int64)
        f = (P - i).astype(np.float32)
        f = f * f * (3.0 - 2.0 * f)
        res = self.res
        ix, iy, iz = i[..., 0] % res, i[..., 1] % res, i[..., 2] % res

        def at(dx, dy, dz):
            return self.grid[(ix + dx) % res, (iy + dy) % res, (iz + dz) % res]

        c000, c100 = at(0, 0, 0), at(1, 0, 0)
        c010, c110 = at(0, 1, 0), at(1, 1, 0)
        c001, c101 = at(0, 0, 1), at(1, 0, 1)
        c011, c111 = at(0, 1, 1), at(1, 1, 1)
        fx, fy, fz = f[..., 0], f[..., 1], f[..., 2]
        c00 = c000 + (c100 - c000) * fx
        c10 = c010 + (c110 - c010) * fx
        c01 = c001 + (c101 - c001) * fx
        c11 = c011 + (c111 - c011) * fx
        c0 = c00 + (c10 - c00) * fy
        c1 = c01 + (c11 - c01) * fy
        return c0 + (c1 - c0) * fz

    def fbm(self, P, octaves=4, gain=0.5, lac=2.03, seed_off=0.0):
        total = np.zeros(P.shape[:-1], dtype=np.float32)
        amp, norm = 1.0, 0.0
        q = np.array(P, dtype=np.float32, copy=True)
        for o in range(octaves):
            q = q + np.float32(seed_off + 17.17 * o)
            total += amp * self.sample(q)
            norm += amp
            amp *= gain
            q = q * lac
        return total / norm


# ------------------------------------------------------------------ star configs
DEFAULTS = dict(
    disk=0.520,                 # photosphere radius, fraction of half-canvas
    halo_reach=0.945,           # glow fades to 0 at this radius (half-canvas units)
    gran_freq=9.0,              # convection cell frequency (features across sphere)
    gran_contrast=0.070,        # cell brightness amplitude (linear light)
    lane_depth=0.040,           # intergranular dark lane depth (linear)
    fine_grain=0.015,           # small-scale boiling amplitude
    spots=(),                   # (x,y,z, angular_sigma, depth)
    spot_contrast=0.20,         # linear brightness drop multiplier per spot depth
    rays=6,                     # diffraction rays total (4 / 6 / 8)
    spike_amp=0.20,
    spike_width=0.0085,         # linear half-width (half-canvas units)
    spike_decay=0.90,           # radial e-folding in units of disk radius
    core_white=0.03,            # linear mix of white into photosphere tint
    rim_strength=0.10,          # chromosphere ring emission (display units)
    rim_color=(1.0, 0.55, 0.42),
    glow_inner_amp=1.35,
    glow_inner_scale=0.17,
    glow_mid_amp=0.50,
    glow_mid_scale=0.58,
    glow_broad_amp=0.20,
    glow_broad_scale=1.75,
    glow_color_mix=0.20,        # 0 = tint, 1 = white
    halo_ang_amp=0.16,
    alpha_gain=1.05,
    flares=(),                  # (x,y,z, sigma, intensity)
    limb_a=(0.52, 0.60, 0.70),
    limb_b=(0.08, 0.10, 0.12),
    hsv_sat=0.30,
    glare_amp=0.50,             # 中心过曝白热核（display 相加）
    glare_sigma=0.52,           # 高斯宽度，单位=光球半径
    glare_white=0.55,           # 0 = 纯色温色核，1 = 纯白核
)


def cfg(**over):
    c = dict(DEFAULTS)
    c.update(over)
    return c


def calibrate(c):
    """全局美术标定（把配置里的相对量压成最终观感）：
    紧凑内层日冕 + 淡而短的宽尾 + 更细的米粒组织 + 很弱的色球环。
    """
    c['glow_inner_amp'] *= 0.50
    c['glow_inner_scale'] *= 0.55
    c['glow_mid_amp'] *= 0.13
    c['glow_mid_scale'] *= 0.95
    c['glow_broad_amp'] *= 0.12
    c['glow_broad_scale'] *= 1.20
    c['alpha_gain'] *= 1.18
    c['rim_strength'] *= 0.15
    c['gran_freq'] *= 1.30
    c['gran_contrast'] *= 0.85
    c['lane_depth'] *= 0.90
    c['spike_amp'] *= 1.10
    c['spike_decay'] *= 0.85
    return c


STARS = [
    dict(key='alpha_cen', spectral='G2V', teffK=5790.0,
         # 半人马座α A：G2V 类太阳黄白
         disk=0.440, halo_reach=0.965, gran_freq=9.5, gran_contrast=0.075,
         lane_depth=0.042, spots=((0.35, 0.42, 0.84, 0.42, 0.55),), spot_contrast=0.14,
         rays=6, spike_amp=0.22, spike_decay=0.95, hsv_sat=0.38, core_white=0.035,
         limb_a=(0.52, 0.60, 0.72), limb_b=(0.08, 0.10, 0.12),
         glow_inner_amp=1.40, glow_mid_amp=0.52, glow_broad_amp=0.21, glow_color_mix=0.18),
    dict(key='barnard', spectral='M4V', teffK=3190.0,
         # 巴纳德星：M4V 橙红矮星，小光球、小而暗的光晕、星芒极弱
         disk=0.352, halo_reach=0.720, gran_freq=14.0, gran_contrast=0.10,
         lane_depth=0.050, fine_grain=0.020,
         spots=((0.2, -0.5, 0.84, 0.44, 0.80), (0.6, 0.55, 0.58, 0.32, 0.60)),
         spot_contrast=0.28, rays=4, spike_amp=0.055, spike_width=0.011,
         spike_decay=0.45, hsv_sat=0.66, core_white=0.0, rim_strength=0.07,
         limb_a=(0.58, 0.70, 0.84), limb_b=(0.09, 0.11, 0.13),
         glow_inner_amp=0.85, glow_inner_scale=0.14, glow_mid_amp=0.30,
         glow_broad_amp=0.11, glow_broad_scale=1.35, glow_color_mix=0.06,
         halo_ang_amp=0.26, alpha_gain=0.95),
    dict(key='wolf359', spectral='M6V', teffK=2800.0,
         # 沃尔夫359：M6V 深橙红耀星，最小最暗，带耀斑
         disk=0.345, halo_reach=0.690, gran_freq=15.0, gran_contrast=0.11,
         lane_depth=0.055, fine_grain=0.022,
         spots=((0.1, -0.6, 0.79, 0.40, 0.85), (0.72, 0.4, 0.56, 0.30, 0.70),
                (-0.55, 0.35, 0.76, 0.28, 0.55)),
         spot_contrast=0.30, rays=0, spike_amp=0.0,
         flares=((-0.45, 0.30, 0.84, 0.17, 0.70), (0.55, -0.42, 0.72, 0.13, 0.50)),
         hsv_sat=0.72, core_white=0.0, rim_strength=0.06,
         limb_a=(0.60, 0.72, 0.86), limb_b=(0.09, 0.12, 0.14),
         glow_inner_amp=0.75, glow_inner_scale=0.13, glow_mid_amp=0.27,
         glow_broad_amp=0.10, glow_broad_scale=1.25, glow_color_mix=0.04,
         halo_ang_amp=0.30, alpha_gain=0.90),
    dict(key='sirius', spectral='A1V', teffK=9940.0,
         # 天狼星：A1V 蓝白，最亮，长星芒
         disk=0.462, halo_reach=0.980, gran_freq=10.5, gran_contrast=0.038,
         lane_depth=0.018, fine_grain=0.009, rays=8, spike_amp=0.40,
         spike_width=0.0072, spike_decay=1.25, hsv_sat=0.32, core_white=0.10,
         rim_strength=0.14, rim_color=(1.0, 0.72, 0.62),
         limb_a=(0.42, 0.40, 0.38), limb_b=(0.05, 0.05, 0.05),
         glow_inner_amp=1.65, glow_mid_amp=0.60, glow_broad_amp=0.27,
         glow_broad_scale=2.0, glow_color_mix=0.34, halo_ang_amp=0.12),
    dict(key='eps_eri', spectral='K2V', teffK=5084.0,
         # 波江座ε：K2V 橙色矮星
         disk=0.420, halo_reach=0.955, gran_freq=11.0, gran_contrast=0.075,
         lane_depth=0.042,
         spots=((0.5, -0.35, 0.79, 0.36, 0.70), (-0.4, 0.55, 0.73, 0.30, 0.50)),
         spot_contrast=0.18, rays=6, spike_amp=0.16, spike_decay=0.75,
         hsv_sat=0.52, core_white=0.02,
         limb_a=(0.54, 0.64, 0.78), limb_b=(0.08, 0.10, 0.12),
         glow_inner_amp=1.20, glow_mid_amp=0.46, glow_broad_amp=0.18,
         glow_color_mix=0.14),
    dict(key='procyon', spectral='F5IV', teffK=6530.0,
         # 南河三：F5IV 黄白，偏白但仍有暖意
         disk=0.448, halo_reach=0.972, gran_freq=10.0, gran_contrast=0.050,
         lane_depth=0.026, rays=8, spike_amp=0.30, spike_width=0.0078,
         spike_decay=1.05, hsv_sat=0.18, core_white=0.07, rim_strength=0.11,
         limb_a=(0.47, 0.53, 0.62), limb_b=(0.07, 0.08, 0.10),
         glow_inner_amp=1.55, glow_mid_amp=0.55, glow_broad_amp=0.23,
         glow_color_mix=0.28),
    dict(key='tau_cet', spectral='G8V', teffK=5344.0,
         # 天仓五：G8V 黄色，比太阳更暖
         disk=0.426, halo_reach=0.958, gran_freq=10.5, gran_contrast=0.072,
         lane_depth=0.040, rays=6, spike_amp=0.17, spike_decay=0.80,
         hsv_sat=0.44, core_white=0.02,
         limb_a=(0.53, 0.62, 0.75), limb_b=(0.08, 0.10, 0.12),
         glow_inner_amp=1.30, glow_mid_amp=0.49, glow_broad_amp=0.19,
         glow_color_mix=0.16),
    dict(key='altair', spectral='A7V', teffK=7550.0,
         # 牛郎星：A7V 白色（自转极快，画面上仍按球面处理）
         disk=0.444, halo_reach=0.972, gran_freq=10.5, gran_contrast=0.042,
         lane_depth=0.020, rays=8, spike_amp=0.28, spike_width=0.0078,
         spike_decay=1.00, hsv_sat=0.12, core_white=0.10, rim_strength=0.10,
         limb_a=(0.44, 0.47, 0.52), limb_b=(0.06, 0.07, 0.08),
         glow_inner_amp=1.45, glow_mid_amp=0.53, glow_broad_amp=0.22,
         glow_color_mix=0.30),
    dict(key='vega', spectral='A0V', teffK=9600.0,
         # 织女星：A0V 蓝白，星等零点，星芒明显
         disk=0.460, halo_reach=0.978, gran_freq=10.5, gran_contrast=0.036,
         lane_depth=0.016, fine_grain=0.009, rays=8, spike_amp=0.38,
         spike_width=0.0072, spike_decay=1.20, hsv_sat=0.36, core_white=0.11,
         rim_strength=0.13, rim_color=(1.0, 0.70, 0.60),
         limb_a=(0.42, 0.40, 0.38), limb_b=(0.05, 0.05, 0.05),
         glow_inner_amp=1.60, glow_mid_amp=0.58, glow_broad_amp=0.26,
         glow_broad_scale=1.95, glow_color_mix=0.34, halo_ang_amp=0.13),
    dict(key='arcturus', spectral='K1.5III', teffK=4286.0,
         # 大角星：K1.5III 橙红巨星，光球最大、光晕最大最亮，对流胞大而稀
         disk=0.465, halo_reach=0.995, gran_freq=5.2, gran_contrast=0.060,
         lane_depth=0.026, fine_grain=0.011,
         spots=((0.3, 0.35, 0.88, 0.30, 0.60), (-0.5, -0.3, 0.81, 0.26, 0.45)),
         spot_contrast=0.16, rays=4, spike_amp=0.10, spike_width=0.010,
         spike_decay=0.60, hsv_sat=0.62, core_white=0.02, rim_strength=0.13,
         limb_a=(0.55, 0.66, 0.80), limb_b=(0.08, 0.10, 0.12),
         glow_inner_amp=2.00, glow_inner_scale=0.22, glow_mid_amp=0.90,
         glow_mid_scale=0.78, glow_broad_amp=0.50, glow_broad_scale=2.50,
         glow_color_mix=0.10, halo_ang_amp=0.18),
]


# ------------------------------------------------------------------ grid
def _unit_grid():
    ys, xs = np.mgrid[0:CANVAS, 0:CANVAS].astype(np.float32)
    x = (xs + 0.5 - HALF) / HALF
    y = -(ys + 0.5 - HALF) / HALF
    return x, y


GRID_X, GRID_Y = _unit_grid()
GRID_R = np.sqrt(GRID_X * GRID_X + GRID_Y * GRID_Y)
GRID_ANG = np.arctan2(GRID_Y, GRID_X)


def _normalised(v):
    v = np.asarray(v, dtype=np.float64)
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / max(e1 - e0, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _halo_profile(c, r, R):
    s = np.maximum(r - R, 0.0) / R
    iso = GLOW_CAL['inner'] * float(c['glow_inner_amp']) * np.exp(
            -s / float(c['glow_inner_scale'])) \
        + GLOW_CAL['mid'] * float(c['glow_mid_amp']) * np.exp(
            -s / float(c['glow_mid_scale'])) \
        + GLOW_CAL['broad'] * float(c['glow_broad_amp']) * np.exp(
            -s / float(c['glow_broad_scale']))
    reach = float(c['halo_reach'])
    fade = _smoothstep(0.0, 1.0, np.clip((reach - r) / HALO_FADE_WIDTH, 0.0, 1.0))
    return iso, fade


# ------------------------------------------------------------------ render
def render_star(c, seed, tint):
    """Return float32 RGBA (CANVAS,CANVAS,4) in 0..1, straight alpha."""
    R = float(c['disk'])
    tint = np.asarray(tint, dtype=np.float32)
    tint_lin = srgb_to_linear(tint)
    x, y, r = GRID_X, GRID_Y, GRID_R
    px = 1.0 / HALF

    # star-local sphere normal (visible hemisphere, orthographic)
    qx = np.clip(x / R, -1.0, 1.0)
    qy = np.clip(y / R, -1.0, 1.0)
    qz = np.sqrt(np.clip(1.0 - qx * qx - qy * qy, 0.0, 1.0))
    mask = np.clip((R - r) / (1.4 * px) + 0.5, 0.0, 1.0)   # soft limb coverage

    # ---- convection / granulation (sampled on the unit sphere) -----------
    noise = ValueNoise3D(seed, res=48)
    noise_b = ValueNoise3D(seed * 7919 + 13, res=48)
    freq = float(c['gran_freq'])
    P1 = np.stack([qx * freq, qy * freq, qz * freq], axis=-1)
    base = noise.fbm(P1, octaves=4, gain=0.55, seed_off=3.1)
    lane_n = noise_b.fbm(P1 * 1.75, octaves=2, gain=0.5, seed_off=9.7)
    lane = np.exp(-((lane_n - 0.5) / 0.085) ** 2).astype(np.float32)
    fine = noise_b.fbm(P1 * 6.0, octaves=2, gain=0.5, seed_off=21.0)

    gran = 1.0 + float(c['gran_contrast']) * (base - 0.5) * 2.0 \
        - float(c['lane_depth']) * lane \
        + float(c['fine_grain']) * (fine - 0.5) * 2.0
    gran = np.clip(gran, 0.45, 1.55).astype(np.float32)
    gran_white = np.clip((base - 0.5) * 6.0 * float(c['gran_contrast']),
                         -0.08, 0.08).astype(np.float32)

    # ---- star spots (cooler, darker, redder) -----------------------------
    spot_d = np.zeros_like(r)
    spot_r = np.zeros_like(r)
    for (sx, sy, sz, sigma, depth) in c['spots']:
        n = _normalised((sx, sy, sz))
        cosang = np.clip(qx * n[0] + qy * n[1] + qz * n[2], -1.0, 1.0)
        ang = np.arccos(cosang)
        m = np.clip(1.0 - ang / max(sigma, 1e-6), 0.0, 1.0)
        m = m * m * (3.0 - 2.0 * m)
        spot_d += depth * m
        spot_r += depth * m
    spot_d = np.clip(spot_d * float(c['spot_contrast']), 0.0, 0.55)
    spot_r = np.clip(spot_r * 0.60, 0.0, 0.60)

    # ---- flares (Wolf 359) ----------------------------------------------
    flare_add = np.zeros_like(r)
    for (fx, fy, fz, sigma, inten) in c['flares']:
        n = _normalised((fx, fy, fz))
        cosang = np.clip(qx * n[0] + qy * n[1] + qz * n[2], -1.0, 1.0)
        ang = np.arccos(cosang)
        flare_add += float(inten) * np.exp(-((ang / max(sigma, 1e-6)) ** 2))
    flare_add = np.clip(flare_add, 0.0, 1.2)

    # ---- photosphere colour in linear light ------------------------------
    cw = float(c['core_white'])
    surf_lin = np.broadcast_to(tint_lin * (1.0 - cw) + cw,
                               (CANVAS, CANVAS, 3)).copy()
    a = [x * 1.02 for x in c['limb_a']]
    b = [x * 1.00 for x in c['limb_b']]
    q = 1.0 - qz
    for i in range(3):
        surf_lin[..., i] *= np.clip(1.0 - a[i] * q - b[i] * q * q, 0.02, 1.0)
    surf_lin *= gran[..., None]
    surf_lin += gran_white[..., None] * np.array([1.0, 0.97, 0.92], dtype=np.float32)
    surf_lin *= (1.0 - spot_d)[..., None]
    surf_lin[..., 0] *= (1.0 + 0.22 * spot_r)
    surf_lin[..., 2] *= (1.0 - 0.55 * spot_r)
    surf_lin += flare_add[..., None] * np.array([1.0, 0.66, 0.32], dtype=np.float32) * 0.85
    surf = lin_to_display(np.clip(surf_lin, 0.0, None))

    # ---- chromosphere rim -------------------------------------------------
    rn = r / R
    rim = _smoothstep(0.945, 0.995, rn) * (1.0 - _smoothstep(0.995, 1.012, rn))
    surf += (rim * float(c['rim_strength']))[..., None] * np.asarray(
        c['rim_color'], dtype=np.float32)

    # ---- white-hot overexposed core (this is what makes it read as a *star*,
    #      not a shaded planet: hot centre -> saturated photosphere -> dark limb)
    glare = float(c['glare_amp']) * np.exp(
        -((rn / max(float(c['glare_sigma']), 1e-6)) ** 2))
    gw = float(c['glare_white'])
    glare_col = np.clip(tint * (1.0 - gw) + gw, 0.0, 1.0)
    surf += glare[..., None] * glare_col
    surf = np.clip(surf, 0.0, 1.0)

    # ---- corona / halo ----------------------------------------------------
    iso, fade = _halo_profile(c, r, R)
    # two-scale angular irregularity: broad streamers + finer corona structure
    ang_a = noise.fbm(
        np.stack([np.cos(GRID_ANG) * 1.35, np.sin(GRID_ANG) * 1.35,
                  np.full_like(GRID_ANG, 0.37)], axis=-1),
        octaves=3, gain=0.55, seed_off=41.0)
    ang_b = noise_b.fbm(
        np.stack([np.cos(GRID_ANG) * 4.8, np.sin(GRID_ANG) * 4.8,
                  np.full_like(GRID_ANG, 0.71)], axis=-1),
        octaves=2, gain=0.55, seed_off=53.0)
    ang_noise = 0.62 * ang_a + 0.38 * ang_b
    iso = iso * (1.0 + float(c['halo_ang_amp']) * 1.6 * (ang_noise - 0.5) * 2.0)

    # diffraction rays (a ray count of 6 means three straight axes)
    spike_i = np.zeros_like(r)
    rays = int(c['rays'])
    if rays >= 2:
        s = np.maximum(r - R, 0.0) / R
        lines = max(rays // 2, 1)
        for i in range(lines):
            axis = math.pi * i / lines + 0.19
            d = np.abs(((GRID_ANG - axis + math.pi / 2.0) % math.pi) - math.pi / 2.0)
            perp = r * np.sin(np.minimum(d, math.pi / 2.0))
            prof = np.exp(-0.5 * (perp / max(c['spike_width'], 1e-6)) ** 2) \
                + 0.16 * np.exp(-0.5 * (perp / (3.2 * max(c['spike_width'], 1e-6))) ** 2)
            rad = np.exp(-s / max(c['spike_decay'], 1e-6)) + 0.9 * np.exp(-s / 0.09)
            spike_i += float(c['spike_amp']) * prof * rad
        spike_i *= _smoothstep(0.0, 0.02, s)
    iso *= fade
    spike_i *= fade

    glow_tint = np.clip(tint * (1.0 - float(c['glow_color_mix']) * GLOW_CAL['mix'])
                        + float(c['glow_color_mix']) * GLOW_CAL['mix'],
                        0.0, 1.0).astype(np.float32)
    spike_col = np.clip(tint * 0.45 + 0.55, 0.0, 1.0).astype(np.float32)

    L = iso + spike_i
    col_w = np.maximum(L, 1e-6)[..., None]
    glow_rgb = (iso[..., None] * glow_tint[None, None, :]
                + spike_i[..., None] * spike_col[None, None, :]) / col_w
    alpha_glow = (1.0 - np.exp(-L * float(c['alpha_gain']))) * fade
    alpha_glow = np.clip(alpha_glow, 0.0, 1.0)

    alpha = np.clip(mask + (1.0 - mask) * alpha_glow, 0.0, 1.0)
    rgb = (surf * mask[..., None] + glow_rgb * (alpha_glow * (1.0 - mask))[..., None])
    rgb = rgb / np.maximum(alpha, 1e-6)[..., None]
    rgb = np.clip(rgb, 0.0, 1.0)
    rgb[alpha <= 1e-5] = 0.0
    alpha[0, :] = alpha[-1, :] = alpha[:, 0] = alpha[:, -1] = 0.0
    rgb[alpha <= 0.0] = 0.0
    return np.dstack([rgb, alpha[..., None]]).astype(np.float32)


# ------------------------------------------------------------------ png save
def _premul_resize(rgba, size):
    img = Image.fromarray((np.clip(rgba, 0, 1) * 255.0 + 0.5).astype(np.uint8), 'RGBA')
    if img.size[0] == size:
        return img
    a = np.asarray(img, dtype=np.float32) / 255.0
    pm = np.dstack([a[..., :3] * a[..., 3:4], a[..., 3:4]])
    pm_img = Image.fromarray((np.clip(pm, 0, 1) * 255.0 + 0.5).astype(np.uint8), 'RGBA')
    pm_img = pm_img.resize((size, size), Image.LANCZOS)
    b = np.asarray(pm_img, dtype=np.float32) / 255.0
    al = b[..., 3]
    rgb = np.zeros((size, size, 3), dtype=np.float32)
    nz = al > 1e-4
    rgb[nz] = b[..., :3][nz] / np.maximum(al[nz], 1e-6)[..., None]
    rgb = np.clip(rgb, 0.0, 1.0)
    res = np.dstack([rgb, al[..., None]]).astype(np.float32)
    res[0, :, 3] = res[-1, :, 3] = res[:, 0, 3] = res[:, -1, 3] = 0.0
    res[res[..., 3] <= 0.0] = 0.0
    return Image.fromarray((res * 255.0 + 0.5).astype(np.uint8), 'RGBA')


def _quantize(img, a_levels, bits):
    a = np.asarray(img, dtype=np.float32)
    al = a[..., 3]
    if a_levels:
        steps = max(a_levels - 1, 1)
        al = np.round(al / 255.0 * steps) / steps * 255.0
    rgb = a[..., :3]
    if bits < 8:
        step = float(1 << (8 - bits))
        rgb = np.clip(np.floor(rgb / step + 0.5) * step, 0.0, 255.0)
    out = np.dstack([rgb, al]).round().clip(0, 255).astype(np.uint8)
    out[0, :, 3] = out[-1, :, 3] = out[:, 0, 3] = out[:, -1, 3] = 0
    out[out[..., 3] == 0, :3] = 0
    return Image.fromarray(out, 'RGBA')


def save_png(img, path):
    """Save under MAX_BYTES, progressively quantising if needed. Returns bytes."""
    from io import BytesIO
    attempts = [(None, 8), (40, 7), (28, 7), (20, 6), (14, 6), (10, 5)]
    best = None
    for a_levels, bits in attempts:
        work = _quantize(img, a_levels, bits) if a_levels else img
        buf = BytesIO()
        work.save(buf, 'PNG', optimize=True, compress_level=9)
        data = buf.getvalue()
        best = data
        if len(data) <= MAX_BYTES:
            with open(path, 'wb') as f:
                f.write(data)
            return len(data)
    with open(path, 'wb') as f:
        f.write(best)
    print('  ! still over budget:', path, len(best))
    return len(best)


def png_stats(path):
    img = Image.open(path)
    a = np.asarray(img.convert('RGBA'), dtype=np.float32) / 255.0
    alpha = a[..., 3]
    corners = float(max(alpha[0, 0], alpha[0, -1], alpha[-1, 0], alpha[-1, -1]))
    return dict(
        w=img.size[0], h=img.size[1], mode=img.mode,
        bytes=os.path.getsize(path),
        alpha_mean=round(float(alpha.mean()), 4),
        opaque_ratio=round(float((alpha > 0.98).mean()), 4),
        nonempty_ratio=round(float((alpha > 0.03).mean()), 4),
        border_alpha_max=round(float(max(alpha[0, :].max(), alpha[-1, :].max(),
                                        alpha[:, 0].max(), alpha[:, -1].max())), 4),
        corner_alpha_max=round(corners, 4),
        rgb_mean=[round(float(a[..., i][alpha > 0.5].mean()), 3) if (alpha > 0.5).any() else 0
                  for i in range(3)],
    )


# ------------------------------------------------------------------ real photo: sun
def find_radial_profile(rgb):
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    rr = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    bins = np.arange(0, min(h, w) / 2.0, 2.0)
    prof = []
    for i in range(len(bins) - 1):
        m = (rr >= bins[i]) & (rr < bins[i + 1])
        prof.append(float(lum[m].mean()) if m.any() else 0.0)
    return np.array(prof), bins[:-1], lum


def _disk_radius(rgb):
    prof, rbin, _ = find_radial_profile(rgb)
    peak = float(np.percentile(prof[:max(int(len(prof) * 0.6), 2)], 98))
    idx = np.where(prof > 0.30 * peak)[0]
    if len(idx):
        return float(rbin[min(idx[-1] + 1, len(rbin) - 1)])
    return min(rgb.shape[0], rgb.shape[1]) * 0.44


def make_sun_photo(src, out_path, disk_frac=0.500, corona_reach=1.34):
    """SDO/AIA sun -> circular transparent sprite.

    The real photosphere + real corona/prominences are kept; everything outside the
    sun's circular footprint becomes alpha=0 (no square, no black plaque). The SDO
    date stamp in the bottom-left corner is painted out before resampling.
    """
    img = Image.open(src).convert('RGB')
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape[:2]
    disk_r = _disk_radius(arr)
    print('  sun photo: source disk radius ~%.0f px of %d' % (disk_r, w))

    R = disk_frac * HALF                     # photosphere radius in canvas px
    scale = R / disk_r
    crop_r = min(disk_r * 1.42, min(h, w) / 2.0 - 2)
    side_src = int(round(crop_r * 2))
    x0 = int(round(w / 2.0 - side_src / 2.0))
    y0 = int(round(h / 2.0 - side_src / 2.0))
    patch = np.asarray(img.crop((x0, y0, x0 + side_src, y0 + side_src)),
                       dtype=np.float32) / 255.0

    # paint out the SDO bottom-left timestamp/watermark (always in the bottom-left)
    wm_x0, wm_x1 = 0, int(side_src * 0.42)
    wm_y0, wm_y1 = int(side_src * 0.94), side_src
    if wm_y1 > wm_y0 and wm_x1 > wm_x0:
        donor = patch[max(wm_y0 - 60, 0):max(wm_y0 - 10, 1), wm_x0:wm_x1]
        fill = np.median(donor.reshape(-1, 3), axis=0) if donor.size else np.zeros(3, np.float32)
        patch[wm_y0:wm_y1, wm_x0:wm_x1] = fill
        # feather the patch seams a little
        patch = np.clip(patch, 0.0, 1.0)

    patch = np.clip(patch * 1.42, 0.0, 1.0) ** 0.86       # lift for game sprite
    tgt = max(int(round(side_src * scale)), 8)
    patch_img = Image.fromarray((patch * 255.0 + 0.5).astype(np.uint8)).resize(
        (tgt, tgt), Image.LANCZOS)
    pa = np.asarray(patch_img, dtype=np.float32) / 255.0
    real = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)
    ph, pw = pa.shape[:2]
    ox, oy = (CANVAS - pw) // 2, (CANVAS - ph) // 2
    real[oy:oy + ph, ox:ox + pw] = pa

    x, y, r = GRID_X, GRID_Y, GRID_R
    rn = r / disk_frac
    pl = 0.299 * real[..., 0] + 0.587 * real[..., 1] + 0.114 * real[..., 2]
    inside = 1.0 - _smoothstep(0.985, 1.004, rn)
    # real corona: only genuinely bright loops/prominences, radially capped just
    # beyond the photosphere so the SDO black background never becomes opaque
    corona = _smoothstep(0.22, 0.48, pl) * (1.0 - _smoothstep(1.00, corona_reach, rn))
    alpha_real = np.clip(np.maximum(inside, 0.70 * corona), 0.0, 1.0)
    alpha_real = np.where(inside > 0.5, alpha_real,
                          np.minimum(alpha_real, 0.70 * _smoothstep(0.20, 0.42, pl)))

    disk_mask = rn < 0.85
    mean_rgb = np.clip(real[disk_mask].mean(axis=0), 0, 1) if disk_mask.any() \
        else np.array([1.0, 0.72, 0.30], dtype=np.float32)
    tint = np.clip(mean_rgb / max(float(mean_rgb.max()), 1e-6) * 0.7 + 0.3, 0.0, 1.0)

    # SDO/AIA 171A 的日面边缘本身偏暗（EUV 光学厚度），会像“大气层暗边”。
    # 这里在贴图内部把最外圈轻微提亮成暖色，避免行星式暗边观感。
    limb_fix = _smoothstep(0.86, 0.982, rn) * (1.0 - _smoothstep(0.982, 1.006, rn))
    warm = np.clip(tint * 0.85 + 0.15, 0.0, 1.0).astype(np.float32)
    real = np.clip(real * (1.0 - 0.62 * limb_fix[..., None])
                   + (0.62 * limb_fix[..., None]) * warm, 0.0, 1.0)

    # procedural glare, kept inside the circular footprint so there is no square
    support = disk_frac * corona_reach        # half-canvas units
    s = np.maximum(r - disk_frac, 0.0) / disk_frac
    iso = 0.36 * np.exp(-s / 0.10) + 0.06 * np.exp(-s / 0.50)
    fade = _smoothstep(0.0, 1.0, np.clip((support - r) / 0.045, 0.0, 1.0))
    ga = np.clip(1.0 - np.exp(-iso * 1.24), 0.0, 1.0) * fade
    glow_col = np.clip(tint * 0.58 + 0.42, 0.0, 1.0).astype(np.float32)
    glow_rgb = np.broadcast_to(glow_col, (CANVAS, CANVAS, 3))

    alpha_out = np.clip(alpha_real + (1.0 - alpha_real) * ga, 0.0, 1.0)
    rgb_out = (real * alpha_real[..., None]
               + glow_rgb * (ga * (1.0 - alpha_real))[..., None])
    rgb_out = rgb_out / np.maximum(alpha_out, 1e-6)[..., None]
    out = np.dstack([np.clip(rgb_out, 0.0, 1.0), alpha_out])
    out[0, :, 3] = out[-1, :, 3] = out[:, 0, 3] = out[:, -1, 3] = 0.0
    out[out[..., 3] <= 0.0] = 0.0
    img_out = _premul_resize(out, OUT)
    size = save_png(img_out, out_path)
    return dict(disk_r_px=round(disk_r, 1), bytes=size,
                tint=[round(float(v), 3) for v in tint])


# ------------------------------------------------------------------ real photo: Sgr A*
def make_galactic_center_photo(src, out_path, ring_frac=0.420, crop_ratio=1.45):
    """EHT Sgr A* image -> circular transparent sprite. ring_frac = ring radius
    as fraction of the half-canvas; the circular alpha support is
    ring_frac*crop_ratio (must stay < 0.98 so the corners stay transparent)."""
    img = Image.open(src).convert('RGB')
    arr = np.asarray(img, dtype=np.float32) / 255.0
    h, w = arr.shape[:2]
    prof, rbin, lum = find_radial_profile(arr)
    start = max(int(len(prof) * 0.15), 1)
    ring_r = float(rbin[start + int(np.argmax(prof[start:]))])
    print('  sgra photo: source ring radius ~%.0f px of %d' % (ring_r, w))

    alpha_radius = ring_frac * crop_ratio
    crop_r = min(ring_r * crop_ratio, min(h, w) / 2.0 - 2)
    side_src = int(round(crop_r * 2))
    x0 = int(round(w / 2.0 - side_src / 2.0))
    y0 = int(round(h / 2.0 - side_src / 2.0))
    tgt = int(round(alpha_radius * 2.0 * HALF))
    patch = img.crop((x0, y0, x0 + side_src, y0 + side_src)).resize(
        (tgt, tgt), Image.LANCZOS)
    pa = np.asarray(patch, dtype=np.float32) / 255.0

    # gentle grade + unsharp mask so the ring reads at 256 px (source is blurred)
    pa = np.clip(pa * 1.22, 0.0, 1.0) ** 0.92
    pa = np.clip((pa - 0.045) / 0.90, 0.0, 1.0) ** 0.95
    pimg = Image.fromarray((np.clip(pa, 0, 1) * 255.0 + 0.5).astype(np.uint8))
    blur = np.asarray(pimg.filter(ImageFilter.GaussianBlur(radius=max(tgt / 160.0, 0.8))),
                      dtype=np.float32) / 255.0
    pa = np.clip(pa + 0.75 * (pa - blur), 0.0, 1.0)
    canvas = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)
    ph, pw = pa.shape[:2]
    ox, oy = (CANVAS - pw) // 2, (CANVAS - ph) // 2
    canvas[oy:oy + ph, ox:ox + pw] = pa

    x, y, r = GRID_X, GRID_Y, GRID_R
    alpha = 1.0 - _smoothstep(0.945 * alpha_radius, 0.995 * alpha_radius, r)
    out = np.dstack([canvas, alpha[..., None]])
    out[0, :, 3] = out[-1, :, 3] = out[:, 0, 3] = out[:, -1, 3] = 0.0
    out[out[..., 3] <= 0.0] = 0.0
    img_out = _premul_resize(out, OUT)
    size = save_png(img_out, out_path)
    return dict(ring_r_px=round(ring_r, 1), crop_r_px=round(crop_r, 1),
                alpha_radius_frac=round(alpha_radius, 3), bytes=size)


# ------------------------------------------------------------------ galactic edge (procedural)
def make_galactic_edge(out_path, seed=4242):
    """稀疏暗星场 + 银色尘埃，圆形透明底（不画成方图）。"""
    noise = ValueNoise3D(seed, res=40)
    noise_b = ValueNoise3D(seed + 77, res=40)
    x, y, r = GRID_X, GRID_Y, GRID_R
    ang = GRID_ANG
    # a faint, tilted galactic band (dust lane) across the circle
    band = np.exp(-((y * 1.0 - x * 0.42 + 0.04) ** 2) / (2.0 * 0.20 ** 2))
    band2 = np.exp(-((y * 1.0 - x * 0.42 - 0.10) ** 2) / (2.0 * 0.46 ** 2))
    # large-scale dust clouds
    P = np.stack([x * 2.4, y * 2.4, np.full_like(x, 0.5)], axis=-1)
    clouds = noise.fbm(P, octaves=5, gain=0.55, seed_off=5.0)
    fil = noise_b.fbm(np.stack([x * 7.0, y * 7.0, np.full_like(x, 1.7)], axis=-1),
                      octaves=3, gain=0.55, seed_off=12.0)
    fil2 = noise.fbm(np.stack([x * 19.0, y * 19.0, np.full_like(x, 2.3)], axis=-1),
                     octaves=2, gain=0.5, seed_off=31.0)
    dust = np.clip(0.08 + 0.50 * band * clouds + 0.26 * band2 * (0.35 + fil)
                   + 0.13 * band2 * (fil2 - 0.5) * 2.0, 0.0, 1.0)
    # dust colour: silver-blue, brighter along the band
    c_dust = np.stack([
        0.42 + 0.36 * dust,          # R
        0.52 + 0.34 * dust,          # G
        0.72 + 0.26 * dust,          # B
    ], axis=-1)
    surf = c_dust
    a_d = np.clip(dust * 0.55, 0.0, 0.85)

    # sparse stars (deterministic)
    rng = np.random.default_rng(seed + 11)
    n_stars = 170
    lum = np.zeros((CANVAS, CANVAS), dtype=np.float32)
    col = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)
    yy, xx = np.mgrid[0:CANVAS, 0:CANVAS].astype(np.float32)
    for i in range(n_stars):
        rr = 0.965 * np.sqrt(rng.random())
        th = rng.random() * 2 * math.pi
        sx = math.cos(th) * rr
        sy = math.sin(th) * rr
        cx = (sx + 1.0) * HALF
        cy = (1.0 - sy) * HALF
        sigma = 0.45 + 1.55 * rng.random() ** 2.2
        bright = 0.22 + 0.78 * rng.random() ** 2.4
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma ** 2))
        lum += bright * g
        tint_s = np.array([0.86 + 0.14 * rng.random(),
                           0.90 + 0.10 * rng.random(),
                           1.00], dtype=np.float32)
        col += (bright * g)[..., None] * tint_s
    # a couple of brighter foreground stars with tiny 4-point sparkles
    for (sx, sy, br) in ((-0.28, 0.34, 0.95), (0.41, -0.22, 0.75)):
        cx = (sx + 1.0) * HALF
        cy = (1.0 - sy) * HALF
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * 2.0 ** 2))
        lum += br * g * 1.5
        col += (br * g * 1.5)[..., None] * np.array([0.90, 0.94, 1.0], np.float32)
        # 4 short rays
        for th in (0.0, math.pi / 2):
            d = np.abs(((GRID_ANG - th + math.pi / 2) % math.pi) - math.pi / 2)
            perp = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) * np.sin(np.minimum(d, math.pi / 2))
            along = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            ray = np.exp(-0.5 * (perp / 0.7) ** 2) * np.exp(-along / 22.0)
            lum += br * 0.30 * ray
            col += (br * 0.30 * ray)[..., None] * np.array([0.92, 0.95, 1.0], np.float32)

    lum = np.clip(lum, 0.0, 1.4)
    star_rgb = np.where(lum[..., None] > 1e-6,
                        col / np.maximum(lum[..., None], 1e-6), 0.0)
    star_alpha = np.clip(lum, 0.0, 1.0)

    # circular support: fade to exactly 0 before the canvas edge/corners
    support = 1.0 - _smoothstep(0.80, 0.955, r)
    # straight-alpha composite: stars over dust, then apply circular support
    a_s = star_alpha
    a_out = a_s + (1.0 - a_s) * a_d
    rgb = np.zeros((CANVAS, CANVAS, 3), dtype=np.float32)
    nz = a_out > 1e-6
    rgb[nz] = (star_rgb[nz] * a_s[nz][:, None] + surf[nz] * (a_d[nz] * (1.0 - a_s[nz]))[:, None]) \
        / a_out[nz][:, None]
    a_out = a_out * support
    rgb = np.clip(rgb, 0.0, 1.0)
    out = np.dstack([rgb, a_out])
    out[0, :, 3] = out[-1, :, 3] = out[:, 0, 3] = out[:, -1, 3] = 0.0
    out[out[..., 3] <= 0.0] = 0.0
    img_out = _premul_resize(out, OUT)
    size = save_png(img_out, out_path)
    return dict(bytes=size, support_frac=0.955)


# ------------------------------------------------------------------ contact sheet
def make_contact_sheet(entries, path, bg=GAME_BG):
    cols = 4
    rows = int(math.ceil(len(entries) / cols))
    tile, gap, lab, small = OUT, 10, 18, 64
    strip_h = small + lab + 6 * 2
    sheet = Image.new('RGB', (cols * tile + (cols + 1) * gap,
                              rows * (tile + lab) + (rows + 1) * gap + strip_h), bg)
    draw = ImageDraw.Draw(sheet)
    for i, (label, sub, fpath) in enumerate(entries):
        col, row = i % cols, i // cols
        x = gap + col * (tile + gap)
        y = gap + row * (tile + lab + gap)
        try:
            im = Image.open(fpath).convert('RGBA')
        except Exception:
            continue
        big = im.resize((tile, tile), Image.LANCZOS)
        bgim = Image.new('RGBA', (tile, tile), bg + (255,))
        bgim.alpha_composite(big)
        sheet.paste(bgim.convert('RGB'), (x, y))
        draw.text((x + 2, y + tile + 3), label, fill=(232, 234, 240))
        draw.text((x + 2 + 86, y + tile + 3), sub, fill=(155, 164, 180))
    ybase = gap + rows * (tile + lab + gap) + 4
    draw.text((gap, ybase - 2), '深蓝底 #060A22 · 小尺寸节点预览', fill=(150, 160, 178))
    for i, (label, _sub, fpath) in enumerate(entries):
        try:
            im = Image.open(fpath).convert('RGBA').resize((small, small), Image.LANCZOS)
        except Exception:
            continue
        x = gap + i * (small + 8)
        y = ybase + lab
        bgim = Image.new('RGBA', (small, small), bg + (255,))
        bgim.alpha_composite(im)
        sheet.paste(bgim.convert('RGB'), (x, y))
    sheet.save(path, optimize=True)
    return path


# ------------------------------------------------------------------ main
def main():
    os.makedirs(HERE, exist_ok=True)
    os.makedirs(REPORTS, exist_ok=True)
    manifest, sheet, stats = [], [], {}

    for idx, base in enumerate(STARS):
        key = base['key']
        c = calibrate(cfg(**{k: v for k, v in base.items()
                             if k not in ('key', 'spectral', 'teffK')}))
        tk = float(base['teffK'])
        # overexposed inner core keeps a star reading as self-luminous; the amount
        # of white is small so the blackbody hue stays readable at small sizes
        if tk < 4000:
            c.update(glare_amp=0.18, glare_white=0.05, glare_sigma=0.46)
        elif tk < 5200:
            c.update(glare_amp=0.22, glare_white=0.12, glare_sigma=0.50)
        elif tk < 6800:
            c.update(glare_amp=0.26, glare_white=0.22, glare_sigma=0.52)
        elif tk < 8500:
            c.update(glare_amp=0.28, glare_white=0.30, glare_sigma=0.54)
        else:
            c.update(glare_amp=0.30, glare_white=0.40, glare_sigma=0.55)
        # 亮星原配置的光晕量更大：把“面积”收回来、保留“亮度差”，
        # 避免贴图里出现一圈可见的灰色圆盘边界。
        if tk >= 9000:
            c['glow_inner_amp'] *= 0.58
            c['glow_mid_amp'] *= 0.52
            c['glow_broad_amp'] *= 0.45
            c['spike_amp'] *= 0.80
        elif tk >= 7000:
            c['glow_inner_amp'] *= 0.74
            c['glow_mid_amp'] *= 0.70
            c['glow_broad_amp'] *= 0.60
            c['spike_amp'] *= 0.90
        tint = star_tint(base['teffK'], c['hsv_sat'])
        seed = 1000 + idx * 137
        print('[%2d/13] %-10s Teff=%5.0f  tint=#%02X%02X%02X' % (
            idx + 1, key, base['teffK'],
            int(round(tint[0] * 255)), int(round(tint[1] * 255)), int(round(tint[2] * 255))))
        rgba = render_star(c, seed, tint)
        img = _premul_resize(rgba, OUT)
        out_path = os.path.join(TEXDIR, 'star_%s.png' % key)
        save_png(img, out_path)
        st = png_stats(out_path)
        st.update(disk_frac=c['disk'], halo_reach=c['halo_reach'], rays=c['rays'])
        stats[key] = st
        print('         -> %s  %.1f KB  opaque=%.2f nonempty=%.2f border=%s corner=%s' % (
            os.path.basename(out_path), st['bytes'] / 1024.0, st['opaque_ratio'],
            st['nonempty_ratio'], st['border_alpha_max'], st['corner_alpha_max']))
        manifest.append(dict(
            key='star_' + key, file='assets/tex/star_%s.png' % key,
            w=st['w'], h=st['h'], source='procedural', url='',
            license='original (project-generated, make_stars.py)',
            note='黑体色温主色+临边昏暗+米粒组织+日冕光晕+%d道星芒；透明底；光球直径≈画布边长%.0f%%'
                 % (c['rays'], c['disk'] * 100),
            spectral=base['spectral'], teffK=base['teffK']))
        sheet.append((key, '%s %.0fK' % (base['spectral'], base['teffK']), out_path))

    # ---- real Sun --------------------------------------------------------
    sun_src = os.path.join(HERE, 'sdo_171.jpg')
    sun_path = os.path.join(TEXDIR, 'star_sun.png')
    if os.path.isfile(sun_src):
        print('[11/13] star_sun  <- NASA SDO/AIA 171A')
        try:
            make_sun_photo(sun_src, sun_path)
            st = png_stats(sun_path)
            stats['sun'] = st
            print('         -> %.1f KB  opaque=%.2f nonempty=%.2f border=%s corner=%s' % (
                st['bytes'] / 1024.0, st['opaque_ratio'], st['nonempty_ratio'],
                st['border_alpha_max'], st['corner_alpha_max']))
            manifest.append(dict(
                key='star_sun', file='assets/tex/star_sun.png',
                w=st['w'], h=st['h'],
                source='NASA SDO/AIA 171A full-disk image',
                url='https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg',
                license='Public Domain (NASA)',
                note='真实观测影像（圆面+日冕）为底，圆形透明蒙版；SDO 日期戳/水印已覆盖并裁除',
                spectral='G2V', teffK=5772.0))
            sheet.append(('sun', 'G2V 5772K real', sun_path))
        except Exception as e:
            print('  sun photo failed:', repr(e))
    else:
        print('[11/13] star_sun  skipped (no raw/sdo_171.jpg)')

    # ---- real Sgr A* -----------------------------------------------------
    gc_src = os.path.join(HERE, 'eht_mwa.jpg')
    gc_path = os.path.join(TEXDIR, 'star_galactic_center.png')
    if os.path.isfile(gc_src):
        print('[12/13] star_galactic_center  <- EHT Sgr A* (ESO, CC BY 4.0)')
        try:
            make_galactic_center_photo(gc_src, gc_path)
            st = png_stats(gc_path)
            stats['galactic_center'] = st
            print('         -> %.1f KB  nonempty=%.2f border=%s corner=%s' % (
                st['bytes'] / 1024.0, st['nonempty_ratio'],
                st['border_alpha_max'], st['corner_alpha_max']))
            manifest.append(dict(
                key='star_galactic_center', file='assets/tex/star_galactic_center.png',
                w=st['w'], h=st['h'],
                source='EHT Collaboration — first image of Sgr A* (published via ESO)',
                url='https://www.eso.org/public/images/eso2208-eht-mwb/',
                license='CC BY 4.0 (EHT Collaboration / ESO)',
                note='真实观测图（吸积环），圆形裁切+透明底；署名必须保留 EHT Collaboration',
                spectral='Sgr A* (supermassive black hole)', teffK=None))
            sheet.append(('galactic_c', 'EHT Sgr A* real', gc_path))
        except Exception as e:
            print('  sgra photo failed:', repr(e))
    else:
        print('[12/13] star_galactic_center  skipped (no raw/eht_mwa.jpg)')

    # ---- procedural galactic edge ---------------------------------------
    edge_path = os.path.join(TEXDIR, 'star_galactic_edge.png')
    print('[13/13] star_galactic_edge  <- procedural silver dust + sparse stars')
    try:
        make_galactic_edge(edge_path)
        st = png_stats(edge_path)
        stats['galactic_edge'] = st
        print('         -> %.1f KB  nonempty=%.2f border=%s corner=%s' % (
            st['bytes'] / 1024.0, st['nonempty_ratio'],
            st['border_alpha_max'], st['corner_alpha_max']))
        manifest.append(dict(
            key='star_galactic_edge', file='assets/tex/star_galactic_edge.png',
            w=st['w'], h=st['h'], source='procedural', url='',
            license='original (project-generated, make_stars.py)',
            note='银河系盘面外缘：银色尘埃带 + 稀疏暗星场，圆形透明底（四角透明）',
            spectral='n/a (galactic disk rim)', teffK=None))
        sheet.append(('galactic_e', 'edge procedural', edge_path))
    except Exception as e:
        print('  galactic edge failed:', repr(e))

    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('manifest ->', MANIFEST)

    cs_path = os.path.join(REPORTS, 'star-contact-sheet.png')
    make_contact_sheet(sheet, cs_path)
    print('contact sheet ->', cs_path)

    with open(os.path.join(HERE, '_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    total = sum(s['bytes'] for s in stats.values())
    print('\nTOTAL %d files, %.1f KB' % (len(stats), total / 1024.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
