# -*- coding: utf-8 -*-
"""FatFish Playable · 商城角色立绘生成器（char-art / task-3）

以 hero.png（296x394 RGBA）为基底，生成与默认角色同一画风的两个幼态拟人立绘：

  chatgpt  「聊天酱 · ChatGPT娘」   青绿色系 #10A37F
  claude   「小星芒 · Claude娘」    橙桃色系 #D97757

方法（不依赖任何外部素材）：
  1. 基底调色：只对蓝色族像素（头发/裙子/蝴蝶结/眼睛/鲸鱼尾巴）做 HSV 重映射
     —— 色相压缩到主题色相带、饱和度/明度曲线按角色调整；白色蕾丝、皮肤、
     线稿明度、透明通道原样保留，所以线稿与赛璐璐结构 100% 与 hero.png 一致。
  2. 配饰：在 4x 超采样画布上手绘赛璐璐风格配件（粗描边 + 平涂 + 单层阴影 + 高光），
     预乘 alpha 盒式降采样回 296x394，边缘干净无白边。
  3. ChatGPT：头戴式耳机（双侧耳罩 + 麦克风吊臂）+ 对话气泡发夹 + 四叶草挂饰。
  4. Claude：六角星发饰两级 + 星星胸针 + 散落星芒 + 暖色蝴蝶结（随调色）。

依赖：Pillow + numpy（本机 python 运行时已带）。
用法：python build_chars.py            # 生成 chatgpt.png / claude.png / preview_compare.png
      python build_chars.py --check    # 额外打印自检数据
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERO = os.path.join(ROOT, "hero.png")
OUT = os.path.join(ROOT, "assets", "chars")
W, H = 296, 394
S = 4                      # 配饰超采样倍数
CW, CH = W * S, H * S


# ---------------------------------------------------------------- color utils
def rgb_to_hsv_np(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx = rgb.max(axis=-1)
    mn = rgb.min(axis=-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-8
    i = m & (mx == r); h[i] = ((g[i] - b[i]) / d[i]) % 6
    i = m & (mx == g); h[i] = (b[i] - r[i]) / d[i] + 2
    i = m & (mx == b); h[i] = (r[i] - g[i]) / d[i] + 4
    return h / 6.0, np.where(mx > 1e-8, d / np.maximum(mx, 1e-8), 0), mx


def hsv_to_rgb_np(h, s, v):
    h6 = (h % 1.0) * 6.0
    i = np.floor(h6).astype(np.int32)
    f = h6 - i
    p = v * (1 - s); q = v * (1 - s * f); t = v * (1 - s * (1 - f))
    i = i % 6
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def smoothstep(x, a, b):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def recolor(im, hue_deg, sat_boost=1.0, vcurve=None, sat_floor=0.16, sat_full=0.44,
            line_keep=0.88, warm_skin=None, hue_lo=195, hue_hi=272, hue_compress=1.0):
    """把 hero 的蓝色族像素重映射到角色主题色相；alpha 完全不动。

    - hue_lo/hue_hi: 参与调色的源色相范围（度）
    - hue_compress:  源色相绕 230° 锚点压缩的比例（1.0=纯旋转，越小越集中）
    - sat_floor/full: 低饱和像素不全量调色，保护皮肤/白裙/浅阴影
    - line_keep:     极暗线稿保留多少原色相（保证描边仍然"黑"
    """
    a = np.array(im, dtype=np.float32) / 255.0
    rgb, alpha = a[..., :3], a[..., 3:4]
    h, s, v = rgb_to_hsv_np(rgb)
    hdeg = h * 360.0
    in_band = smoothstep(hdeg, hue_lo - 6, hue_lo + 10) * (1 - smoothstep(hdeg, hue_hi - 10, hue_hi + 6))
    w = in_band * smoothstep(s, sat_floor, sat_full)
    w = w * (1.0 - (1.0 - line_keep) * (1 - smoothstep(v, 0.05, 0.25)))
    target = (hue_deg + (hdeg - 230.0) * hue_compress) / 360.0
    dh = (target - h + 0.5) % 1.0 - 0.5
    new_h = (h + w * dh) % 1.0
    new_s = np.clip(s * (1.0 + (sat_boost - 1.0) * w), 0, 1)
    if vcurve is None:
        new_v = v
    else:
        xs = np.array([k[0] for k in vcurve], dtype=np.float32)
        ys = np.array([k[1] for k in vcurve], dtype=np.float32)
        new_v = np.clip(v * (1 - w) + np.interp(v, xs, ys).astype(np.float32) * w, 0, 1)
    out = hsv_to_rgb_np(new_h, new_s, new_v)
    if warm_skin is not None:
        sha = smoothstep(s, 0.06, 0.14) * (1 - smoothstep(s, 0.42, 0.60))
        shv = smoothstep(v, 0.45, 0.70)
        shh = smoothstep(hdeg, 2, 10) * (1 - smoothstep(hdeg, 36, 52))
        sk = (sha * shv * shh)[..., None]
        out = out * (1 - sk) + out * sk * np.array(warm_skin)
    rgba = np.concatenate([np.clip(out, 0, 1), alpha], axis=-1)
    return Image.fromarray(np.round(rgba * 255).astype(np.uint8), "RGBA")


def retint_eyes(im, target_deg=33.0, amount=0.78, desat=0.06, lift=1.02):
    """虹膜色相单独重定向（Claude 用琥珀色眼睛）。只动两个眼睛椭圆内的饱和像素。"""
    a = np.array(im, dtype=np.float32) / 255.0
    rgb, alpha = a[..., :3], a[..., 3]
    h, s, v = rgb_to_hsv_np(rgb)
    yy, xx = np.mgrid[0:H, 0:W]
    region = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in ((118, 181, 25.0, 27.0), (182, 181, 25.0, 27.0)):
        region |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0
    w = region & (s > 0.20) & (v > 0.10) & (alpha > 0.9)
    tgt = target_deg / 360.0
    dh = (tgt - h + 0.5) % 1.0 - 0.5
    h2 = np.where(w, (h + amount * dh) % 1.0, h)
    s2 = np.where(w, np.clip(s * (1 - desat), 0, 1), s)
    v2 = np.where(w, np.clip(v * (1 + (lift - 1) * w), 0, 1), v)
    out = hsv_to_rgb_np(h2, s2, v2)
    rgba = np.concatenate([np.clip(out, 0, 1), alpha[..., None]], axis=-1)
    return Image.fromarray(np.round(rgba * 255).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------- masks
def _L():
    return Image.new("L", (CW, CH), 0)


def _xy(pts):
    return [(x * S, y * S) for x, y in pts]


def m_ellipse(cx, cy, rx, ry, ang=0.0, n=180):
    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    t = np.linspace(0, 2 * np.pi, n)
    x, y = rx * np.cos(t), ry * np.sin(t)
    pts = [(cx + x[i] * ca - y[i] * sa, cy + x[i] * sa + y[i] * ca) for i in range(n)]
    m = _L()
    ImageDraw.Draw(m).polygon(_xy(pts), fill=255)
    return m


def m_poly(pts):
    m = _L()
    ImageDraw.Draw(m).polygon(_xy(pts), fill=255)
    return m


def m_round_rect(x0, y0, x1, y1, r):
    m = _L()
    ImageDraw.Draw(m).rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=255)
    return m


def m_band(points, width):
    m = _L()
    ImageDraw.Draw(m).line(_xy(points), fill=255, width=int(round(width * S)), joint="curve")
    return m


def m_star(cx, cy, r_out, r_in, points=6, rot=-90.0):
    pts = []
    for i in range(points * 2):
        rr = r_out if i % 2 == 0 else r_in
        a = np.radians(rot + i * 180.0 / points)
        pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
    return m_poly(pts)


def m_clover(cx, cy, r):
    m = _L()
    d = ImageDraw.Draw(m)
    off, leaf = r * 0.52, r * 0.60
    for ang in (90, 0, 270, 180):
        a = np.radians(ang)
        ex, ey = cx + off * np.cos(a), cy + off * np.sin(a)
        pts = [(ex + leaf * np.cos(t), ey + leaf * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 90)]
        d.polygon(_xy(pts), fill=255)
    d.line(_xy([(cx, cy + r * 0.9), (cx + r * 0.1, cy + r * 1.55)]), fill=255,
           width=max(2, int(r * 0.22 * S)))
    return m


def shift_mask(mask, dx, dy):
    out = Image.new("L", mask.size, 0)
    out.paste(mask, (int(dx), int(dy)))
    return out


def dilate(mask, px):
    r = max(1, int(round(px)))
    bbox = mask.getbbox()
    if bbox is None:
        return mask
    x0, y0, x1, y1 = bbox
    pad = r + 2
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(mask.size[0], x1 + pad), min(mask.size[1], y1 + pad)
    out = Image.new("L", mask.size, 0)
    out.paste(mask.crop((x0, y0, x1, y1)).filter(ImageFilter.MaxFilter(2 * r + 1)), (x0, y0))
    return out


# -------------------------------------------------------------- cel painting
def cel(layer, mask, base, shade=None, outline=None, ow=2.6, light=(-6, -7),
        hi=None, hi_mask=None, hi_alpha=225, cast=None):
    """在 RGBA 图层上画一个赛璐璐风格形状：粗描边 + 平涂 + 右下阴影 + 高光 + 投影。"""
    bbox = mask.getbbox()
    if bbox is None:
        return
    r = max(1, int(round(ow * S / 2)))
    pad = r + 3
    x0, y0 = max(0, bbox[0] - pad), max(0, bbox[1] - pad)
    x1, y1 = min(CW, bbox[2] + pad), min(CH, bbox[3] + pad)
    box = (x0, y0, x1, y1)
    sub = mask.crop(box)
    sw, sh = sub.size

    if cast is not None:
        cs = shift_mask(dilate(mask, int(cast * S)).crop(box), 1.5 * S, 2.0 * S)
        cast_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        cast_img.putalpha(cs.point(lambda v: int(v * 0.20)))
        layer.alpha_composite(cast_img, (x0, y0))

    out = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    if outline is not None:
        out.paste(outline, (0, 0), sub.filter(ImageFilter.MaxFilter(2 * r + 1)))
    out.paste(base, (0, 0), sub)
    if shade is not None:
        out.paste(shade, (0, 0), ImageChops.subtract(sub, shift_mask(sub, light[0] * S, light[1] * S)))
    if hi is not None and hi_mask is not None:
        hm = ImageChops.multiply(hi_mask.crop(box), sub)
        if hi_alpha < 255:
            hm = hm.point(lambda v: int(v * hi_alpha / 255))
        out.paste(hi, (0, 0), hm)
    layer.alpha_composite(out, (x0, y0))


def cel_flat(layer, mask, color):
    layer.paste(color, (0, 0), mask)


# ------------------------------------------------------------------ palettes
PAL = {
    "chatgpt": dict(
        hue=172.0, sat=1.20, hue_compress=0.38,
        vcurve=[(0, 0), (0.12, 0.115), (0.35, 0.38), (0.55, 0.60), (0.75, 0.80), (1, 1)],
        line="#06231E",
        c_main="#23C6A6", c_shade="#0E947A", c_dark="#0A6E5A", c_deep="#06483C",
        c_light="#7FEBD3", c_cream="#F5FFFC", c_white="#FFFFFF",
        brand="#10A37F",
    ),
    "claude": dict(
        hue=18.0, sat=1.12, hue_compress=0.45,
        vcurve=[(0, 0), (0.10, 0.10), (0.30, 0.40), (0.45, 0.60), (0.55, 0.72),
                (0.63, 0.83), (0.78, 0.93), (1, 1)],
        warm_skin=(1.03, 1.0, 0.965),
        line="#2A1510",
        c_main="#EF9B74", c_shade="#CB6B45", c_dark="#A9522F", c_deep="#7A3826",
        c_light="#FFD8C4", c_cream="#FFF4EC", c_white="#FFFFFF",
        brand="#D97757",
    ),
}


# --------------------------------------------------------------- accessories
def draw_chatgpt(p):
    """头戴式耳机（双耳罩、吊臂麦克风）+ 对话气泡发夹 + 四叶草挂饰。"""
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    line, main, shade, deep = p["line"], p["c_main"], p["c_shade"], p["c_deep"]
    light = p["c_light"]

    # 双耳罩（画在鲸鱼鳍耳位置，盖住耳鳍根部）
    for cx, ang in ((52, -5), (245, 5)):
        cy = 181
        cel(lay, m_ellipse(cx, cy, 23.0, 26.0, ang), main, shade, line,
            ow=2.8, light=(-6, -7),
            hi=light, hi_mask=m_ellipse(cx - 7, cy - 11, 7.0, 4.6, ang), hi_alpha=175, cast=2.2)
        cel(lay, m_ellipse(cx, cy, 14.6, 18.2, ang), deep, None, line, ow=2.2, light=(-5, -6))
        cel_flat(lay, m_ellipse(cx, cy, 3.2, 3.2), main)

    # 麦克风吊臂：左耳罩 -> 嘴角
    boom = []
    for t in np.linspace(0, 1, 50):
        x = (1 - t) ** 2 * 52 + 2 * (1 - t) * t * 82 + t * t * 106
        y = (1 - t) ** 2 * 196 + 2 * (1 - t) * t * 214 + t * t * 199
        boom.append((x, y))
    cel(lay, m_band(boom, 3.6), deep, None, line, ow=1.5, light=(-4, -5))
    cel(lay, m_round_rect(103, 192, 117, 204, 5.5), main, shade, line, ow=2.0, light=(-4, -5),
        hi=light, hi_mask=m_round_rect(105, 193.5, 111, 197, 2.0), hi_alpha=205, cast=1.2)
    cel_flat(lay, m_ellipse(113, 199, 1.7, 1.7), deep)

    # 对话气泡发夹（左侧头发上，白底青绿点）
    body = ImageChops.lighter(m_round_rect(64, 76, 104, 108, 10),
                              m_poly([(73, 104), (86, 104), (70, 122)]))
    cel(lay, body, p["c_cream"], None, line, ow=2.4, light=(-5, -6), cast=1.6)
    for dx in (-9, 0, 9):
        cel_flat(lay, m_ellipse(84 + dx, 92, 3.0, 3.0), p["brand"])
    lay.paste(p["c_white"], (0, 0), m_star(96, 83, 4.8, 1.5, points=4, rot=-90))

    # 四叶草挂饰（右耳罩下）
    cel(lay, m_band([(245, 205), (248, 212)], 1.5), shade, None, line, ow=1.0)
    cel(lay, m_clover(249, 222, 6.2), light, shade, line, ow=1.6, light=(-4, -5), cast=0.8,
        hi=p["c_white"], hi_mask=m_ellipse(247, 219.5, 2.4, 1.8), hi_alpha=210)
    return lay


def draw_claude(p):
    """六角星发饰两级 + 星星胸针 + 散落星芒（暖色点缀；蝴蝶结随调色变珊瑚色）。"""
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    line, main, shade = p["line"], p["c_main"], p["c_shade"]

    def star(x, y, ro, ri, points=6, rot=-90, ow=2.2, cast=1.3, sparkle=True):
        cel(lay, m_star(x, y, ro, ri, points=points, rot=rot), main, shade, line,
            ow=ow, light=(-5, -6), cast=cast)
        if sparkle:
            lay.paste(p["c_cream"], (0, 0),
                      m_star(x - ro * 0.16, y - ro * 0.16, max(2.0, ro * 0.30),
                             max(0.8, ro * 0.11), points=4, rot=-90))

    star(240, 101, 13.5, 5.0, ow=2.4, cast=1.6)      # 右侧大发饰（蝴蝶结上方）
    star(88, 117, 9.6, 3.5, ow=2.0, cast=1.2)        # 左侧刘海小星
    for (x, y, ro) in ((56, 206, 7.0), (254, 244, 7.4), (235, 292, 5.2)):   # 散落星芒
        cel(lay, m_star(x, y, ro, ro * 0.22, points=4, rot=-90),
            p["c_light"], None, line, ow=1.7, light=(-4, -5))
        cel_flat(lay, m_ellipse(x - 0.5, y - 0.5, ro * 0.26, ro * 0.26), p["c_cream"])
    star(160, 260, 5.0, 1.9, ow=1.4, cast=0.7, sparkle=False)   # 胸针
    return lay


# ------------------------------------------------------------------ compose
def downscale_acc(lay):
    """预乘 alpha 的 SxS 盒式降采样：超采样配饰 -> 1x，边缘不产生白/黑边。"""
    a = np.asarray(lay, dtype=np.float32) / 255.0
    rgb, al = a[..., :3], a[..., 3]
    pr = rgb * al[..., None]
    resh = lambda arr: arr.reshape(H, S, W, S, *arr.shape[2:]).mean(axis=(1, 3))
    al2, pr2 = resh(al), resh(pr)
    rgb2 = np.divide(pr2, np.maximum(al2[..., None], 1e-6))
    out = np.concatenate([np.clip(rgb2, 0, 1), np.clip(al2, 0, 1)[..., None]], axis=-1)
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA")


def build(kind):
    p = PAL[kind]
    hero = Image.open(HERO).convert("RGBA")
    base = recolor(hero, hue_deg=p["hue"], sat_boost=p["sat"], vcurve=p["vcurve"],
                   warm_skin=p.get("warm_skin"), hue_compress=p.get("hue_compress", 1.0))
    if kind == "claude":
        base = retint_eyes(base)
    accs = draw_chatgpt(p) if kind == "chatgpt" else draw_claude(p)
    base.alpha_composite(downscale_acc(accs))
    return base


# ------------------------------------------------------------------- preview
def make_preview(chat, clau):
    """三图并排（hero / chatgpt / claude），深色底 + 标注；仅供自检与报告。"""
    scale = 1.5
    gap, top, bottom, side = 22, 76, 52, 26
    hero = Image.open(HERO).convert("RGBA")
    pw, ph = int(W * scale), int(H * scale)
    panel_w = pw + gap
    cw = side * 2 + panel_w * 3 - gap
    chh = top + ph + bottom
    bg = Image.new("RGBA", (cw, chh), (10, 16, 32, 255))
    d = ImageDraw.Draw(bg)
    for y in range(chh):                       # 竖直渐变 + 星点
        k = y / chh
        d.line([(0, y), (cw, y)], fill=(int(10 + 12 * k), int(16 + 14 * k), int(32 + 26 * k), 255))
    rng = np.random.default_rng(7)
    for _ in range(90):
        x, y = int(rng.uniform(0, cw)), int(rng.uniform(0, chh))
        b = int(rng.uniform(90, 210))
        d.point((x, y), fill=(b, b, min(255, b + 30), 255))

    font_path = "C:/Windows/Fonts/msyh.ttc"
    try:
        f_title = ImageFont.truetype(font_path, 22)
        f_tag = ImageFont.truetype(font_path, 15)
        f_small = ImageFont.truetype(font_path, 13)
    except Exception:
        f_title = f_tag = f_small = ImageFont.load_default()

    items = [
        ("默认角色", "DeepSeek 金鱼娘 · hero.png", (143, 166, 216), hero),
        ("聊天酱", "ChatGPT娘 · 青绿色系 #10A37F", (79, 209, 181), chat),
        ("小星芒", "Claude娘 · 橙桃色系 #D97757", (240, 168, 130), clau),
    ]
    d.text((side, 14), "肥鱼跳宇宙 · 商城幼态拟人立绘（同一画风自检）",
           font=f_title, fill=(226, 236, 255, 255))
    x = side
    for name, tag, col, im in items:
        panel = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        panel.alpha_composite(im.resize((pw, ph), Image.LANCZOS))
        # 淡色卡座 + 边缘描线
        card = Image.new("RGBA", (pw, ph), (255, 255, 255, 10))
        card.alpha_composite(panel)
        bg.alpha_composite(card, (x, top))
        d.rectangle([x, top, x + pw - 1, top + ph - 1], outline=(70, 90, 130, 255), width=1)
        d.text((x, 50), name, font=f_tag, fill=col + (255,))
        d.text((x, top + ph + 8), tag, font=f_small, fill=(186, 200, 224, 255))
        x += panel_w
    d.text((side, top + ph + 28),
           "生成方式：hero.png 基底 HSV 主题调色（线稿/透明通道原样）+ 4x 手绘赛璐璐配饰；无外部素材。",
           font=f_small, fill=(150, 164, 190, 255))
    return bg


# ---------------------------------------------------------------------- main
def qa(im, path):
    a = np.array(im)
    al = a[..., 3]
    tr = a[al == 0]
    ys, xs = np.where(al > 8)
    info = dict(
        file=os.path.basename(path),
        size=list(im.size),
        bytes=os.path.getsize(path),
        bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        opaque_ratio=round(float((al > 250).sum()) / (im.size[0] * im.size[1]), 4),
        semi_px=int(((al > 0) & (al < 255)).sum()),
        transparent_rgb_max=int(tr[:, :3].max()) if len(tr) else 0,
        has_alpha=im.mode == "RGBA",
    )
    return info


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    imgs = {}
    for kind in ("chatgpt", "claude"):
        im = build(kind)
        path = os.path.join(OUT, kind + ".png")
        im.save(path, optimize=True)
        imgs[kind] = im
        print("[build] %s -> %s" % (kind, path))
    prev = make_preview(imgs["chatgpt"], imgs["claude"])
    ppath = os.path.join(OUT, "preview_compare.png")
    prev.convert("RGB").save(ppath, optimize=True)
    print("[build] preview -> %s" % ppath)

    if "--check" in sys.argv:
        for kind in ("chatgpt", "claude"):
            print("[qa]", qa(Image.open(os.path.join(OUT, kind + ".png")).convert("RGBA"),
                             os.path.join(OUT, kind + ".png")))
        print("[qa] preview", os.path.getsize(ppath), "bytes", prev.size)
