# -*- coding: utf-8 -*-
"""FatFish Playable v4 · 角色立绘处理流水线（char-art / task-2）

把用户提供的 8 张 AI 角色立绘统一成游戏可用素材：

  输入：assets/chars/raw/<id>.png   （用户原图，只读存档，不覆盖）
  输出：assets/chars/<id>.webp      （游戏用，300x400，透明底，单张 <= 90KB）
        assets/chars/raw/processed/<id>.png （同内容 PNG，便于对比/复查）

处理步骤（对「白底 RGB 原图」和「已带 alpha 的原图」都适用）：
  1. 白底判定：从图像四条边泛洪填充（flood fill），容差 tol（默认 18/24 可配）。
     用「行游程 + 并查集」做 4 连通分量，只把「与外边框连通」的近白区域判为背景 ——
     角色内部的白色服装/白发（白裙、白披风、白龙角）不会被挖掉。
  1b 地面阴影：白底图脚底常有浅灰投影（225~245，泛洪 tol 吃不到），单独一步
     只在底部 12% 找「低饱和浅灰、且与背景连通」的整块并进背景；纯白衣料不参与。
  2. 去噪：删掉面积 < min_island 的孤岛 alpha 分量（AI 出图的白底噪点/杂点），
     填补面积 < min_hole 的针孔。
  3. 羽化：alpha 做半径 ~0.7px 高斯后再拉伸，得到 1~2px 柔和边缘。
  4. 去白边（un-matte）：对半透明像素按「原图是白底直通 alpha」反解前景色
     c = (c_obs - bg*(1-a)) / a，去掉深色背景上会露出的白边；alpha=0 的像素
     RGB 统一刷成背景色，避免 WebP 有损压缩把底色渗到边缘。
  5. 裁切内容 bounding box，四周留 4% padding，等比缩放（预乘 alpha 的 LANCZOS，
     避免缩放时透明像素的白 RGB 渗进轮廓），透明底 300x400，水平居中、底部对齐。

可复跑（用户之后会用幼态新图同名覆盖 Grok/Kimi/GLM/Qwen/MiniMax）：
    python process_chars.py                      # 处理全部 8 张 + 重建 preview/manifest
    python process_chars.py --only grok,kimi     # 只重做指定角色（同名新图直接覆盖 raw/ 后跑）
    python process_chars.py --key grok --in D:\\new\\grok_v2.png   # 指定输入图，输出仍叫 grok.webp
    python process_chars.py --preview             # 只重建 assets/chars/preview_compare.png
    python process_chars.py --manifest            # 只重建 assets/manifest-chars.json
    python process_chars.py --check               # 打印尺寸/体积/alpha 自检表
    python process_chars.py --qa                  # 生成深色底放大边检图 raw/_qa_sheet.png

依赖：Pillow + numpy（本机 dsh Python 运行时已带）。
运行时：C:\\Users\\admin\\.dsh\\dsh-runtimes\\dsh-plugin-desktop-primary-runtime\\dependencies\\python\\python.exe
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ------------------------------------------------------------------ paths
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW_DIR = os.path.join(HERE, "raw")
PROCESSED_DIR = os.path.join(RAW_DIR, "processed")
CACHE = os.path.join(RAW_DIR, "_process_report.json")
HERO = os.path.join(ROOT, "hero.png")

CANVAS_W, CANVAS_H = 300, 400
PAD_RATIO = 0.04            # 内容四周留白 = 内容长边的 4%
MAX_BYTES = 90 * 1024       # 单张 webp 上限（SPEC：<=90KB）
WEBP_QUALITIES = (88, 86, 84, 82)   # SPEC：quality 82~88，按此顺序试到满足体积

# 角色配置：id -> 处理参数。tol 为泛洪容差（max channel diff，0-255）。
# extra_bg_seeds 是「被角色轮廓包住的白底空洞」的手动补种点（归一化坐标 0..1）；
# 只有在目检发现封闭白底残留时才用，不要拿它去戳白色衣服。
CHARS = [
    dict(key="chatgpt", name="聊天酱", en="ChatGPT",  price=1200, color="#10A37F",
         mode="auto", tol=18, min_island=8,  min_hole=8,
         note="白发龙角/调色盘+画笔/幼态三头身；原图自带透明底（alpha 模式）"),
    dict(key="claude",  name="小星芒", en="Claude",   price=1800, color="#D97757",
         mode="auto", tol=18, min_island=8,  min_hole=8,
         note="橙发向日葵/抱书/幼态；原图自带透明底（alpha 模式）"),
    dict(key="gemini",  name="双星喵", en="Gemini",   price=2600, color="#A88BFF",
         mode="auto", tol=18, min_island=8,  min_hole=8,
         note="紫发猫耳/星星装饰/幼态；原图自带透明底（alpha 模式）"),
    dict(key="grok",    name="格萝克", en="Grok",     price=2900, color="#C9A227",
         mode="whitebg", tol=20, min_island=12, min_hole=10,
         note="金发双马尾/蝙蝠翼/黑红哥特裙/巨斧/全身；白底待幼态替换"),
    dict(key="kimi",    name="月音酱", en="Kimi",     price=3200, color="#8FB8FF",
         mode="whitebg", tol=12, min_island=12, min_hole=10,
         note="银白蓝发/长笛礼服/全身；白底+白裙，tol 收紧到 12 防止白裙被泛洪吃掉；待幼态替换"),
    dict(key="glm",     name="墨卷酱", en="GLM",      price=3500, color="#6E7B9A",
         mode="whitebg", tol=12, min_island=12, min_hole=10,
         note="黑发狼耳/抱 GLM 书本/全身；白底+白裙，tol 收紧到 12；待幼态替换"),
    dict(key="qwen",    name="千问酱", en="Qwen",     price=3800, color="#4A6BD8",
         mode="whitebg", tol=20, min_island=12, min_hole=10,
         note="蓝发汉服/折扇/全身；白底；待幼态替换"),
    dict(key="minimax", name="小麦克", en="MiniMax",  price=4100, color="#FF8A5B",
         mode="whitebg", tol=20, min_island=12, min_hole=10,
         note="橙发记者帽/麦克风/MINIMAX 包/全身；白底；待幼态替换"),
]
CHARS_BY_KEY = {c["key"]: c for c in CHARS}


# --------------------------------------------------------------- utilities
def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def border_color(rgb):
    """四条边最外 2px 的中位色，作为背景色估计。"""
    h, w = rgb.shape[:2]
    band = max(1, min(3, h // 100 + 1))
    px = np.concatenate([
        rgb[:band].reshape(-1, 3), rgb[-band:].reshape(-1, 3),
        rgb[:, :band].reshape(-1, 3), rgb[:, -band:].reshape(-1, 3),
    ], axis=0)
    return np.median(px, axis=0)


def components(mask):
    """4 连通分量标记（行游程 + 并查集，纯 Python 但按 run 处理，1600px 图 <1s）。

    返回 (labels, sizes)：labels 是 HxW int32，-1 表示不在 mask 内；
    sizes[label] = 该分量像素数（index 0..n-1）。
    """
    h, w = mask.shape
    row_starts, row_ends, row_of = [], [], []
    for y in range(h):
        row = mask[y]
        if not row.any():
            continue
        pad = np.zeros(w + 2, dtype=bool)
        pad[1:-1] = row
        d = np.diff(pad.astype(np.int8))
        s = np.flatnonzero(d == 1)
        e = np.flatnonzero(d == -1)
        row_starts.append(s)
        row_ends.append(e)
        row_of.append(np.full(s.size, y))
    if not row_starts:
        return np.full((h, w), -1, np.int32), []

    starts = np.concatenate(row_starts)
    ends = np.concatenate(row_ends)
    rows = np.concatenate(row_of)
    n = starts.size

    parent = np.arange(n, dtype=np.int64)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    # 每行游程的 id 区间 [row_first[y], row_first[y+1])
    row_first = np.searchsorted(rows, np.arange(h + 1))
    for y in range(h - 1):
        a0, a1 = row_first[y], row_first[y + 1]
        b0, b1 = row_first[y + 1], row_first[y + 2]
        i, j = a0, b0
        while i < a1 and j < b1:
            if starts[i] < ends[j] and starts[j] < ends[i]:
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[rb] = ra
            if ends[i] < ends[j]:
                i += 1
            else:
                j += 1

    # 压缩 label：root -> 0..n-1
    labels = np.full((h, w), -1, np.int32)
    root_to_label = {}
    sizes = []
    for i in range(n):
        r = find(i)
        lb = root_to_label.get(r)
        if lb is None:
            lb = len(sizes)
            root_to_label[r] = lb
            sizes.append(0)
        y = rows[i]
        labels[y, starts[i]:ends[i]] = lb
        sizes[lb] += int(ends[i] - starts[i])
    return labels, sizes


def flood_bg_mask(rgb, bg, tol, extra_seeds=()):
    """从四条边泛洪填充近白背景；返回背景 boolean mask（True=背景）。"""
    diff = np.abs(rgb.astype(np.int16) - bg.astype(np.int16)).max(axis=-1)
    cand = diff <= tol
    labels, sizes = components(cand)
    h, w = cand.shape
    bg_labels = set()

    # 外边框上的游程 = 泛洪种子
    for y in (0, h - 1):
        row = labels[y]
        for lb in np.unique(row[row >= 0]):
            bg_labels.add(int(lb))
    for x in (0, w - 1):
        col = labels[:, x]
        for lb in np.unique(col[col >= 0]):
            bg_labels.add(int(lb))
    # 手动补种（封闭白底空洞）
    for nx, ny in extra_seeds:
        x = min(w - 1, max(0, int(round(nx * w))))
        y = min(h - 1, max(0, int(round(ny * h))))
        lb = labels[y, x]
        if lb >= 0:
            bg_labels.add(int(lb))
    if not bg_labels:
        return np.zeros((h, w), bool)
    keep = np.zeros(len(sizes), bool)
    for lb in bg_labels:
        keep[lb] = True
    return np.isin(labels, np.flatnonzero(keep))


def clean_ground_shadow(rgb, bg, bgm, bottom_frac=0.12, passes=4):
    """去掉脚底的地面色阴影（AI 白底图常见的浅灰投影）。

    泛洪填充只能吃掉「白到接近背景」的像素，地面阴影是 225~245 的浅灰，
    tol 调大会连白发/白纱的边缘一起削掉，所以单独一步处理：只在图像底部
    12% 区域内找「低饱和 + 浅灰（150<=min，max<=249，明显浅于背景但非纯白）」
    的连通块，凡是与已判定背景相邻的整块并进背景。纯白服装（>=250）和高饱和
    部件不参与，因此不会误删白色衣料。
    """
    h, w = rgb.shape[:2]
    mn = rgb.min(axis=-1)
    mx = rgb.max(axis=-1)
    chroma = mx - mn
    diff = np.abs(rgb - bg[None, None, :]).max(axis=-1)
    region = np.zeros((h, w), bool)
    region[int(h * (1.0 - bottom_frac)):] = True
    cand = region & (chroma <= 22) & (mn >= 150) & (mx <= 249) & (diff <= 70)
    min_area = max(30, int(0.00003 * h * w))
    added = 0
    for _ in range(passes):
        labels, sizes = components(cand & ~bgm)
        if not sizes:
            break
        bgd = np.asarray(Image.fromarray(bgm.astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(3))) > 0
        new = np.zeros((h, w), bool)
        for lb in range(len(sizes)):
            if sizes[lb] < min_area:
                continue
            m = labels == lb
            if (m & bgd).any():
                new |= m
        if not new.any():
            break
        added += int(new.sum())
        bgm = bgm | new
    return bgm, added


def despeckle(fg, min_island, min_hole):
    """删掉 < min_island 的前景孤岛；填补 < min_hole 的背景针孔。返回新的 fg。"""
    fg = fg.copy()
    labels, sizes = components(fg)
    if sizes:
        drop = np.array([s < min_island for s in sizes], dtype=bool)
        drop_ids = np.flatnonzero(drop)
        if drop_ids.size:
            for lb in drop_ids:
                fg[labels == lb] = False
    labels, sizes = components(~fg)
    if sizes:
        fill = np.array([s < min_hole for s in sizes], dtype=bool)
        fill_ids = np.flatnonzero(fill)
        # 最外圈贴边的「背景」不补（那是真外边界）
        border_labels = set()
        for arr in (labels[0], labels[-1], labels[:, 0], labels[:, -1]):
            for lb in np.unique(arr[arr >= 0]):
                border_labels.add(int(lb))
        for lb in fill_ids:
            if int(lb) in border_labels:
                continue
            fg[labels == lb] = True
    return fg


def resize_premul(im, size):
    """预乘 alpha 的 LANCZOS 缩放：透明像素的白 RGB 不会渗进轮廓。"""
    a = np.asarray(im, dtype=np.float32)
    al = a[..., 3] / 255.0
    prem = a[..., :3] * al[..., None]
    al2 = np.asarray(Image.fromarray(al * 255.0, "F").resize(size, Image.LANCZOS)) / 255.0
    prem2 = np.stack([
        np.asarray(Image.fromarray(prem[..., c], "F").resize(size, Image.LANCZOS))
        for c in range(3)
    ], axis=-1)
    out = np.zeros((size[1], size[0], 4), np.float32)
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb = prem2 / np.maximum(al2[..., None], 1e-4)
    out[..., :3] = np.clip(rgb, 0, 255)
    out[..., 3] = np.clip(al2 * 255.0, 0, 255)
    return Image.fromarray(np.round(out).astype(np.uint8), "RGBA")


# ------------------------------------------------------------------ core
def process_one(cfg, in_path=None, out_path=None, tol=None, mode=None, verbose=False):
    key = cfg["key"]
    in_path = in_path or os.path.join(RAW_DIR, key + ".png")
    out_path = out_path or os.path.join(HERE, key + ".webp")
    tol = cfg["tol"] if tol is None else int(tol)
    mode = mode or cfg["mode"]

    src = Image.open(in_path)
    src_sha = sha256_of(in_path)
    src_rgba = src.convert("RGBA")
    arr = np.asarray(src_rgba)
    rgb = arr[..., :3].astype(np.float32)
    src_alpha = arr[..., 3]
    h, w = rgb.shape[:2]

    transparent_ratio = float((src_alpha < 250).mean())
    if mode == "auto":
        mode = "alpha" if transparent_ratio > 0.02 else "whitebg"

    bg = border_color(rgb) if mode == "whitebg" else np.array([255.0, 255.0, 255.0], np.float32)
    shadow_px = 0

    if mode == "whitebg":
        bgm = flood_bg_mask(rgb, bg, tol, cfg.get("extra_bg_seeds", ()))
        if cfg.get("ground_shadow", True):
            bgm, shadow_px = clean_ground_shadow(rgb, bg, bgm)
        fg = ~bgm
        fg = despeckle(fg, cfg.get("min_island", 12), cfg.get("min_hole", 10))
        # 软 alpha：blur + 拉伸，边缘 1~2px 过渡
        base = (fg * 255.0).astype(np.float32)
        blur = np.asarray(Image.fromarray(base.astype(np.uint8), "L").filter(
            ImageFilter.GaussianBlur(0.75)), dtype=np.float32)
        alpha = np.clip((blur - 12.0) * 255.0 / 232.0, 0, 255)
        # 去白边：反解白底直通 alpha，再 clamp
        al = alpha / 255.0
        den = np.maximum(al, 0.03)[..., None]
        unmatt = (rgb - bg[None, None, :] * (1.0 - al[..., None])) / den
        band = ((al > 0.02) & (al < 0.98))[..., None]
        rgb_out = np.where(band, np.clip(unmatt, 0, 255), rgb)
    else:  # alpha: 原图已抠好透明底，保留原 alpha，只做去孤岛/补针孔 + 轻羽化
        fg = src_alpha > 8
        fg = despeckle(fg, cfg.get("min_island", 8), cfg.get("min_hole", 8))
        a = np.where(fg, src_alpha.astype(np.float32), 0.0)
        blur = np.asarray(Image.fromarray(a.astype(np.uint8), "L").filter(
            ImageFilter.GaussianBlur(0.6)), dtype=np.float32)
        alpha = np.clip((blur - 6.0) * 255.0 / 243.0, 0, 255)
        rgb_out = rgb

    # 全透明像素 RGB 刷成背景色，避免缩放出白/黑边
    alpha_u8 = np.round(alpha).astype(np.uint8)
    rgb_out = np.where((alpha_u8 < 3)[..., None], bg[None, None, :], rgb_out)

    rgba = np.dstack([np.clip(rgb_out, 0, 255), alpha_u8]).astype(np.uint8)
    work = Image.fromarray(rgba, "RGBA")

    # 裁切内容 + 4% padding
    ys, xs = np.where(alpha_u8 > 10)
    if xs.size == 0:
        raise RuntimeError("%s: 处理后没有不透明内容" % key)
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    cw, ch = x1 - x0, y1 - y0
    pad = int(round(PAD_RATIO * max(cw, ch)))
    padded = Image.new("RGBA", (cw + 2 * pad, ch + 2 * pad), (0, 0, 0, 0))
    padded.paste(work.crop((x0, y0, x1, y1)), (pad, pad))

    scale = min(CANVAS_W / padded.width, CANVAS_H / padded.height)
    tw = max(1, int(round(padded.width * scale)))
    th = max(1, int(round(padded.height * scale)))
    scaled = resize_premul(padded, (tw, th))
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    paste_x = (CANVAS_W - tw) // 2
    paste_y = CANVAS_H - th                       # 底部对齐
    canvas.paste(scaled, (paste_x, paste_y))

    # WebP：按 88->82 试到 <=90KB；PNG 留档 raw/processed/
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    q_used = None
    for q in WEBP_QUALITIES:
        canvas.save(out_path, "WEBP", quality=q, method=6, alpha_quality=95)
        q_used = q
        if os.path.getsize(out_path) <= MAX_BYTES:
            break
    png_path = os.path.join(PROCESSED_DIR, key + ".png")
    canvas.save(png_path, "PNG", optimize=True)

    out_arr = np.asarray(canvas)
    out_alpha = out_arr[..., 3]
    oys, oxs = np.where(out_alpha > 8)
    report = dict(
        key=key,
        input=os.path.relpath(in_path, ROOT),
        input_dims=[w, h],
        input_mode=src.mode,
        input_sha256=src_sha,
        method=mode + ("-floodfill" if mode == "whitebg" else "-keepalpha"),
        tol=tol,
        ground_shadow_px=shadow_px,
        bg_color=[int(round(v)) for v in bg],
        content_bbox_src=[x0, y0, x1, y1],
        content_size_src=[cw, ch],
        pad_px=pad,
        scale=round(scale, 4),
        canvas=[CANVAS_W, CANVAS_H],
        content_bbox_canvas=[int(oxs.min()), int(oys.min()), int(oxs.max()) + 1, int(oys.max()) + 1],
        alpha_coverage=round(float((out_alpha > 250).mean()), 4),
        semi_px=int(((out_alpha > 0) & (out_alpha < 255)).sum()),
        transparent_rgb_max=int(out_arr[out_alpha == 0][:, :3].max()) if (out_alpha == 0).any() else 0,
        webp=dict(path=os.path.relpath(out_path, ROOT), bytes=os.path.getsize(out_path), quality=q_used),
        png=dict(path=os.path.relpath(png_path, ROOT), bytes=os.path.getsize(png_path)),
    )
    if verbose:
        print("[chars] %-8s %s  %dx%d -> 300x400  webp %5.1f KB (q%d)  bbox=%s"
              % (key, mode, w, h, report["webp"]["bytes"] / 1024.0, q_used,
                 report["content_bbox_canvas"]))
    return report


# ------------------------------------------------------------------ preview
def _font(size):
    for p in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyhbd.ttc",
              "C:/Windows/Fonts/simhei.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def make_preview(out_path=None):
    """9 人并排对比图：deepseek 用 hero.png，其余用处理后的 <id>.webp。"""
    out_path = out_path or os.path.join(HERE, "preview_compare.png")
    items = [dict(key="deepseek", name="深海小鲸娘", en="DeepSeek", price=0,
                  color="#5AA9FF", path=HERO, pending=False)]
    for c in CHARS:
        items.append(dict(key=c["key"], name=c["name"], en=c["en"], price=c["price"],
                          color=c["color"], path=os.path.join(HERE, c["key"] + ".webp"),
                          pending=c["mode"] in ("whitebg",) or c.get("pending", False)))

    pw, ph = 252, 336            # 面板内容区（300x400 -> 等比）
    gap, top, bottom, side = 14, 92, 88, 22
    cols = 9
    cw = side * 2 + cols * pw + (cols - 1) * gap
    chh = top + ph + bottom
    bg = Image.new("RGBA", (cw, chh), (9, 13, 30, 255))
    d = ImageDraw.Draw(bg)
    for y in range(chh):         # 深空渐变
        k = y / max(1, chh - 1)
        d.line([(0, y), (cw, y)],
               fill=(int(9 + 10 * k), int(13 + 12 * k), int(30 + 22 * k), 255))
    rng = np.random.default_rng(20261118)
    for _ in range(360):
        x, y = int(rng.uniform(0, cw)), int(rng.uniform(0, chh))
        b = int(rng.uniform(70, 200))
        d.point((x, y), fill=(b, b, min(255, b + 40), 255))
        if rng.random() < 0.05:
            d.point((x + 1, y), fill=(b // 2, b // 2, b, 255))

    f_title = _font(24)
    f_name = _font(19)
    f_small = _font(13)
    f_tiny = _font(12)
    d.text((side, 16), "肥鱼跳宇宙 v4 · 商城 9 位角色立绘总览（300×400 透明底 WebP）",
           font=f_title, fill=(228, 238, 255, 255))
    d.text((side, 50), "深色底为游戏内实际背景色；虚线框外留白即透明区。"
                       "  ※5 张标「待替换幼态」的角色立绘，用户确认幼态新图后同名覆盖即可。",
           font=f_small, fill=(150, 166, 196, 255))
    d.text((side, 68), "配图来源：用户提供的 8 张 AI 立绘 + hero.png（默认深海小鲸娘）",
           font=f_small, fill=(150, 166, 196, 255))

    x = side
    for i, it in enumerate(items):
        p = it["path"]
        col = tuple(int(it["color"][j:j + 2], 16) for j in (1, 3, 5))
        card = Image.new("RGBA", (pw, ph), (255, 255, 255, 8))
        # 卡座：主题色底 + 透明棋盘提示（不画棋盘，直接用深色）
        card_bg = Image.new("RGBA", (pw, ph), (16, 22, 42, 255))
        tint = Image.new("RGBA", (pw, ph), col + (26,))
        card_bg = Image.alpha_composite(card_bg, tint)
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            s = min(pw / im.width, ph / im.height)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
            card_bg.alpha_composite(im, ((pw - im.width) // 2, ph - im.height))
        bg.alpha_composite(card_bg, (x, top))
        d.rectangle([x, top, x + pw - 1, top + ph - 1], outline=(64, 82, 120, 255), width=1)
        d.rectangle([x, top, x + pw - 1, top + 3], fill=col + (255,))
        d.text((x + 6, top + ph + 8), "%02d %s" % (i + 1, it["name"]), font=f_name,
               fill=col + (255,))
        d.text((x + 6, top + ph + 34), "%s · %s" % (it["en"], "默认" if it["price"] == 0 else "%d 星辰币" % it["price"]),
               font=f_small, fill=(184, 198, 222, 255))
        if it["pending"]:
            d.text((x + 6, top + ph + 54), "待替换幼态", font=f_tiny, fill=(255, 190, 120, 255))
        else:
            d.text((x + 6, top + ph + 54), "最终立绘", font=f_tiny, fill=(140, 220, 170, 255))
        x += pw + gap
    bg.convert("RGB").save(out_path, optimize=True)
    return out_path, bg.size


# ------------------------------------------------------------------ manifest
def _rel(*parts):
    """相对项目根目录的 POSIX 风格路径（manifest 里统一用 /）。"""
    return os.path.relpath(os.path.join(*parts), ROOT).replace(os.sep, "/")


def write_manifest(reports=None, path=None):
    path = path or os.path.join(ROOT, "assets", "manifest-chars.json")
    reports = reports or load_reports()
    by_key = {r["key"]: r for r in reports}
    chars = []
    for c in CHARS:
        r = by_key.get(c["key"])
        if not r:
            continue
        chars.append(dict(
            key=c["key"],
            file=_rel(HERE, c["key"] + ".webp"),
            png=_rel(PROCESSED_DIR, c["key"] + ".png"),
            w=CANVAS_W, h=CANVAS_H,
            bytes=r["webp"]["bytes"],
            displayName=c["name"],
            en=c["en"],
            brandColor=c["color"],
            price=c["price"],
            source="user-supplied-portrait",
            sourceFile=_rel(RAW_DIR, c["key"] + ".png"),
            sourceSha256=r["input_sha256"],
            sourceDims=r["input_dims"],
            processing=dict(
                method=r["method"],
                tol=r["tol"],
                bgColor=r["bg_color"],
                groundShadowPx=r.get("ground_shadow_px", 0),
                contentBboxSrc=r["content_bbox_src"],
                padPx=r["pad_px"],
                scale=r["scale"],
                webpQuality=r["webp"]["quality"],
                note=c["note"],
            ),
            note=c["note"],
        ))
    # deepseek 复用 hero.png：只登记，不复制、不改动
    hero_rep = None
    if os.path.exists(HERO):
        hi = Image.open(HERO).convert("RGBA")
        hero_rep = dict(key="deepseek", file="hero.png", png=None, w=hi.width, h=hi.height,
                        bytes=os.path.getsize(HERO), displayName="深海小鲸娘", en="DeepSeek",
                        brandColor="#5AA9FF", price=0, source="user-supplied-hero",
                        sourceFile="hero.png", sourceSha256=sha256_of(HERO),
                        sourceDims=[hi.width, hi.height],
                        processing=dict(method="unchanged", note="默认角色，原样复用 hero.png，未做任何改动"),
                        note="默认角色；游戏缺省形象，继续使用 hero.png")
    preview_file = os.path.join(HERE, "preview_compare.png")
    prev_size = Image.open(preview_file).size if os.path.exists(preview_file) else None
    total_bytes = sum(c["bytes"] for c in chars)

    manifest = dict(
        project="FatFish-Playable",
        version="v4",
        owner="char-art",
        updated="2026-11-18",
        canvas=dict(w=CANVAS_W, h=CANVAS_H, format="webp", background="transparent",
                    padding="4% of content long edge", align="horizontal-center / bottom"),
        script="assets/chars/process_chars.py",
        raw="assets/chars/raw/<id>.png",
        processed="assets/chars/raw/processed/<id>.png",
        chars=chars,
        default=hero_rep,
        preview=dict(file="assets/chars/preview_compare.png",
                     size=list(prev_size) if prev_size else None,
                     note="9 人并排对比（deepseek=hero.png + 8 张处理结果），仅自检/审阅用，不参与构建"),
        qa=dict(count=len(chars), totalBytes=total_bytes,
                maxBytes=max(c["bytes"] for c in chars) if chars else 0,
                limitBytes=MAX_BYTES, allUnderLimit=all(c["bytes"] <= MAX_BYTES for c in chars),
                rerun="python assets/chars/process_chars.py --check"),
        rerun="python assets/chars/process_chars.py --only <id>   # 同名新图覆盖 assets/chars/raw/<id>.png 后",
        buildNote=("build/build.py 的 collect_chars() 需把白名单扩到 9 个 id（deepseek 用 TEX.hero），"
                   "读取 assets/chars/<id>.webp；旧的 chatgpt.png/claude.png 已移到 assets/chars/raw/legacy/ 归档"),
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path, manifest


# ------------------------------------------------------------------ misc
def load_reports():
    if not os.path.exists(CACHE):
        return []
    with open(CACHE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_reports(reports):
    os.makedirs(RAW_DIR, exist_ok=True)
    old = {r["key"]: r for r in load_reports()}
    for r in reports:
        old[r["key"]] = r
    ordered = [old[c["key"]] for c in CHARS if c["key"] in old]
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)
        f.write("\n")


def build_qa_sheet(path=None):
    """深色底 2x 放大边检图（查白边/挖洞/残留白底），仅自检用，不参与构建。"""
    path = path or os.path.join(RAW_DIR, "_qa_sheet.jpg")
    hero = Image.open(HERO).convert("RGBA") if os.path.exists(HERO) else None
    srcs = [("deepseek", hero)] + [(c["key"], Image.open(os.path.join(HERE, c["key"] + ".webp")).convert("RGBA"))
                                   for c in CHARS]
    Z = 2
    tw, th = CANVAS_W * Z, CANVAS_H * Z
    cols, pad, cap = 5, 8, 22
    rows = (len(srcs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + cap + pad) + pad), (8, 12, 26))
    dr = ImageDraw.Draw(sheet)
    f = _font(15)
    for i, (k, im) in enumerate(srcs):
        # 左暗右亮双色底：白边看暗底、黑边看亮底
        cell_bg = Image.new("RGB", (tw, th), (12, 16, 34))
        light = Image.new("RGB", (tw // 2, th), (206, 210, 220))
        cell_bg.paste(light, (tw // 2, 0))
        if im is not None:
            big = im.resize((tw, th), Image.LANCZOS)
            cell_bg.paste(big, (0, 0), big)
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + cap + pad)
        sheet.paste(cell_bg, (x, y))
        dr.text((x, y + th + 3), k, font=f, fill=(240, 240, 240))
    sheet.save(path, quality=88, optimize=True)
    return path


def check(reports=None):
    reports = reports or load_reports()
    rows = []
    for r in reports:
        rows.append((r["key"], r["webp"]["bytes"], r["webp"]["quality"],
                     r["method"], r["content_bbox_canvas"], r["alpha_coverage"],
                     r["semi_px"], r["transparent_rgb_max"]))
    print("%-8s %10s %5s %-10s %-22s %8s %8s %8s" %
          ("key", "webp", "q", "method", "bbox_canvas", "opaque%", "semi_px", "tr_rgbmax"))
    total = 0
    for k, b, q, m, bbox, cov, semi, tr in rows:
        total += b
        print("%-8s %9.1fK %5d %-10s %-22s %8.1f %8d %8d" %
              (k, b / 1024.0, q, m, bbox, cov * 100, semi, tr))
        assert b <= MAX_BYTES, "%s 超 90KB: %d" % (k, b)
    print("合计 %.1f KB（%d 张）" % (total / 1024.0, len(rows)))
    return rows


# ------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="FatFish v4 角色立绘处理流水线")
    ap.add_argument("--only", help="只处理这些 id（逗号分隔），如 grok,kimi")
    ap.add_argument("--key", help="指定单个 id（与 --in 搭配，输出仍为 <key>.webp）")
    ap.add_argument("--in", dest="in_path", help="输入图路径（默认 assets/chars/raw/<key>.png）")
    ap.add_argument("--out", dest="out_path", help="输出 webp 路径（默认 assets/chars/<key>.webp）")
    ap.add_argument("--tol", type=int, help="覆盖泛洪容差")
    ap.add_argument("--mode", choices=("auto", "whitebg", "alpha"), help="覆盖处理模式")
    ap.add_argument("--preview", action="store_true", help="只重建 preview_compare.png")
    ap.add_argument("--manifest", action="store_true", help="只重建 assets/manifest-chars.json")
    ap.add_argument("--check", action="store_true", help="打印自检表")
    ap.add_argument("--qa", action="store_true", help="生成深色底边检图 raw/_qa_sheet.png")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    verbose = not args.quiet
    do_process = not (args.preview or args.manifest or args.check or args.qa)

    if do_process:
        keys = [c["key"] for c in CHARS]
        if args.key:
            if args.key not in CHARS_BY_KEY:
                print("未知 id: %s（可选：%s）" % (args.key, ", ".join(keys)))
                return 2
            keys = [args.key]
        elif args.only:
            keys = [k.strip() for k in args.only.split(",") if k.strip()]
            bad = [k for k in keys if k not in CHARS_BY_KEY]
            if bad:
                print("未知 id: %s（可选：%s）" % (", ".join(bad), ", ".join(keys)))
                return 2
        reports = []
        for k in keys:
            cfg = CHARS_BY_KEY[k]
            reports.append(process_one(cfg, in_path=(args.in_path if args.key else None),
                                       out_path=(args.out_path if args.key else None),
                                       tol=args.tol, mode=args.mode, verbose=verbose))
        save_reports(reports)
        p, size = make_preview()
        print("[preview] -> %s (%dx%d)" % (os.path.relpath(p, ROOT), size[0], size[1]))
        mp, man = write_manifest(reports=load_reports())
        print("[manifest] -> %s (%d chars)" % (os.path.relpath(mp, ROOT), len(man["chars"])))

    if args.check:
        check(load_reports())
    if args.qa:
        p = build_qa_sheet()
        print("[qa] 边检图 ->", os.path.relpath(p, ROOT))
    if args.preview:
        p, size = make_preview()
        print("[preview] -> %s (%dx%d)" % (os.path.relpath(p, ROOT), size[0], size[1]))
    if args.manifest:
        mp, man = write_manifest()
        print("[manifest] -> %s (%d chars)" % (os.path.relpath(mp, ROOT), len(man["chars"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
