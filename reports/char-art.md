# char-art 交付报告 · v4 九角色立绘处理

任务：`task-2`（`docs/SPEC-v4.md` 第 8 节「角色美术契约」+ 第 1 节需求 8）
负责人：char-art
日期：2026-11-18
工作目录：`C:\Users\admin\Desktop\FatFish-Playable`
写作用域：`assets/chars/**`、`docs/chibi-generation-prompts.md`、`reports/char-art.md`

## 1. 交付清单

| 交付物 | 路径 | 说明 |
|---|---|---|
| 8 张游戏用立绘 | `assets/chars/{chatgpt,claude,gemini,grok,kimi,glm,qwen,minimax}.webp` | 300×400 透明底 WebP，全部 q88，单张 24.6~36.8 KB（限值 90 KB） |
| 处理脚本 | `assets/chars/process_chars.py` | 泛洪去白底 + 去地面阴影 + 去孤岛/补针孔 + 羽化 + 去白边 + 4% 留白 + 300×400 底对齐；参数化可复跑 |
| 原始图存档 | `assets/chars/raw/{id}.png` | 8 张用户原图复制存档，未改动（sha256 见 §2） |
| PNG 对比件 | `assets/chars/raw/processed/{id}.png` | 与 webp 同内容，便于逐张目检/对比 |
| 9 人并排预览 | `assets/chars/preview_compare.png` | 2424×516，deepseek 用 `hero.png` + 8 张处理结果；深色底、名称/价格、「待替换幼态」标记 |
| 边检图（自检） | `assets/chars/raw/_qa_sheet.jpg` | 2× 放大、左暗右亮双色底，专门看白边/黑边/残留白底；不参与构建 |
| 处理数据缓存 | `assets/chars/raw/_process_report.json` | 逐张参数/尺寸/体积，manifest 与 `--check` 的数据源 |
| 素材清单 | `assets/manifest-chars.json` | 每张 `key/file/w/h/bytes/source/processing/note` + 默认角色 hero 登记 + QA 汇总 |
| 幼态提示词 | `docs/chibi-generation-prompts.md` | Grok/Kimi/GLM/Qwen/MiniMax 五节，可直贴 genderswapai.com |
| 旧版归档 | `assets/chars/raw/legacy/{chatgpt,claude}-v3-recolor.png` | v3 被用户否决的「大肥鱼换色」产物，移出顶层避免误注入构建 |

**未改动**：`hero.png`、`src/**`、`docs/SPEC-v4.md`、`index.html`。`assets/chars/build_chars.py` 保留（v3 历史脚本，已被本流水线取代，本轮未执行）。

## 2. 来源（用户提供的 8 张立绘，已复制存档而非原地读取）

| id | 存档文件 | 原始附件 sha256 前缀 | 原始尺寸/模式 | 角色要素 |
|---|---|---|---|---|
| chatgpt | `raw/chatgpt.png` | `2bac4838…` | 537×640 RGBA（自带透明底） | 白发龙角、调色盘+画笔、幼态 |
| claude | `raw/claude.png` | `6452189e…` | 573×640 RGBA（自带透明底） | 橙发向日葵、抱书、幼态 |
| gemini | `raw/gemini.png` | `9f23ed43…` | 504×640 RGBA（自带透明底） | 紫发猫耳、星星装饰、幼态 |
| grok | `raw/grok.png` | `b0af75fa…` | 893×1600 RGB 白底 | 金发双马尾、蝙蝠翼、黑红哥特裙、巨斧、全身 |
| kimi | `raw/kimi.png` | `9d67b670…` | 900×1600 RGB 白底(253) | 银白蓝发、长笛、音乐会礼服、全身 |
| glm | `raw/glm.png` | `85890b3b…` | 900×1600 RGB 白底(253) | 黑发狼耳、抱 GLM 书本、全身 |
| qwen | `raw/qwen.png` | `176dea0b…` | 893×1600 RGB 白底 | 蓝发汉服、折扇、全身 |
| minimax | `raw/minimax.png` | `d326f0c8…` | 893×1600 RGB 白底 | 橙发记者帽、麦克风、MINIMAX 包、全身 |

完整 sha256 见 `assets/manifest-chars.json` 的 `sourceSha256` 字段。

## 3. 处理方法（`process_chars.py`，逐张可复跑）

1. **模式判定**：原图透明像素占比 >2% 视为「已抠图」，保留其 alpha（chatgpt/claude/gemini）；否则按白底 RGB 走泛洪（grok/kimi/glm/qwen/minimax）。
2. **泛洪去白底**（不是全局白色阈值）：取四条边最外 2px 中位色为背景色；逐像素与背景色最大通道差 ≤ `tol` 作为候选，用「按行游程 + 并查集」做 4 连通分量，**只把与图像外边框连通的分量判为背景**。因此角色内部的白色服装/白发（Kimi 白纱裙、GLM 白围裙、Grok 白蕾丝、ChatGPT 白龙角）不会被挖掉。
   - 容差按图设定：彩色人物 20；Kimi/GLM 白裙 + 近白背景收紧到 **12**（防止白纱被泛洪吃掉）。
3. **去地面阴影**（Kimi/GLM 需要，其余自动 0 像素）：白底图脚底有 225~245 的浅灰投影，`tol` 吃不到、调大又会削白发/白纱边缘。单独一步：只在图像底部 12% 区域内找「低饱和（chroma ≤22）+ 浅灰（150≤min，max≤249，明显浅于背景但非纯白）且与背景连通」的整块并入背景 —— 纯白衣料（≥250）不参与。实测删除 19406 / 3534 px，目检确认只动了脚底阴影。
4. **去噪**：删掉面积 < `min_island`（8~12 px）的前景孤岛（AI 白底噪点），填补面积 < `min_hole` 的背景针孔。
5. **羽化**：alpha 做半径 0.6~0.75px 高斯后线性拉伸，得到 1~2px 柔和过渡，避免硬锯齿。
6. **去白边（un-matte）**：白底图 0.02<a<0.98 的半透明像素按 `c = (c_obs − bg·(1−a)) / a` 反解前景色，去掉深色背景上会露出的白边；alpha<3 的像素 RGB 统一刷成背景色，避免有损压缩把底色渗回边缘。
7. **裁切与排版**：对 alpha>10 的内容取 bounding box，四周加**内容长边 4%** 的透明 padding；等比缩放到 300×400（**预乘 alpha 的 LANCZOS**，避免透明像素 RGB 被插值进轮廓），透明底、**水平居中 + 底部对齐**。
8. **编码**：WebP q88 + `alpha_quality=95`、`method=6`；脚本在 q88→86→84→82 间自动降档直到 ≤90 KB（本次全部 q88 即达标）。同时输出 PNG 到 `raw/processed/`。

## 4. 逐张数据（`--check` 输出）

| id | 输入 | 方法 | tol | 内容 bbox（源） | 缩放 | 画布 bbox | WebP | q |
|---|---|---|---|---|---|---|---|---|
| chatgpt | 537×640 RGBA | alpha-保留 | 18 | 1,1–537,640 | 0.5102 | 13,60–287,387 | **30.8 KB** | 88 |
| claude | 573×640 RGBA | alpha-保留 | 18 | 1,1–572,639 | 0.4815 | 12,80–288,388 | **31.5 KB** | 88 |
| gemini | 504×640 RGBA | alpha-保留 | 18 | 1,0–504,640 | 0.5405 | 14,40–286,386 | **36.8 KB** | 88 |
| grok | 893×1600 RGB | 白底泛洪 | 20 | 11,43–893,1529 | 0.2494 | 39,15–260,386 | **32.5 KB** | 88 |
| kimi | 900×1600 RGB | 白底泛洪 + 去地面阴影 | 12 | 71,56–900,1592 | 0.2413 | 49,14–250,386 | **24.6 KB** | 88 |
| glm | 900×1600 RGB | 白底泛洪 + 去地面阴影 | 12 | 67,69–863,1540 | 0.2517 | 50,15–250,385 | **24.7 KB** | 88 |
| qwen | 893×1600 RGB | 白底泛洪 | 20 | 53,44–852,1581 | 0.2411 | 53,14–247,386 | **26.0 KB** | 88 |
| minimax | 893×1600 RGB | 白底泛洪 | 20 | 57,41–879,1572 | 0.2420 | 50,14–249,386 | **26.2 KB** | 88 |

合计 **233.0 KB / 8 张**，全部 ≤ 90 KB，单张上限余量 ≈ 53 KB。默认角色 `hero.png`（296×394）原样复用，未做任何改动。

## 5. 自检与目检结论（`read_image` 逐张 + 双色底边检图）

- **无白底残留**：8 张在深色底（游戏实际背景）与浅灰底上分别合成，均无白块/白雾/残留白底；Kimi/GLM 原先脚底的浅灰地面阴影已彻底去除。
- **无挖洞**：白发（ChatGPT/Claude/Kimi）、白纱裙（Kimi）、白围裙+白衬衫（GLM）、白蕾丝/白袖口（Grok）、白外套（MiniMax）、白折扇（Qwen）均完整；龙角、猫耳、狼耳、蝙蝠翼、巨斧、长笛、书本、折扇、麦克风、托特包等标志物保留。
- **边缘干净**：2× 放大检查，深底无白边 halo、浅底无黑边；半透明边缘 1~2px 柔和，头发细丝/蕾丝未出现锯齿断层。
- **构图**：全部水平居中、底部对齐；顶端龙角/猫耳、底端鞋底完整未裁切。
- **体积**：全部 q88 达标，无需降质。

## 6. 已知问题 / 注意事项

1. **5 张待替换**：Grok/Kimi/GLM/Qwen/MiniMax 目前仍是「全身成熟版」；用户在 genderswapai.com 生成幼态图确认后，**同名覆盖 `assets/chars/raw/<id>.png` 再跑一次脚本即可**（见 §7）。`preview_compare.png` 上已标「待替换幼态」，`docs/chibi-generation-prompts.md` 提供现成提示词。
2. **幼态与全身的比例差异**：ChatGPT/Claude/Gemini 原图横向偏宽（内容宽高比 ≈0.75~0.84），按「等比 contain」排进 3:4 画布后内容高度占画布 77%~87%；全身角色约占 93%。这是等比缩放 + 固定画布的必然结果（不拉伸、不裁切），不是抠图问题。若商城卡里希望视觉高度统一，建议在渲染层按卡面高度等比缩放（Lead 侧）；5 张幼态替换后比例会自然拉近。
3. **透明像素 RGB 为白色**：为避免有损 WebP 把白底渗进轮廓、也便于目检，alpha=0 的像素 RGB 被刷成背景色（255,255,255），所以 `--check` 的 `transparent_rgb_max=255` 不代表「隐藏白底」。游戏按 alpha 合成，实测深/浅底均无残留；若 QA 有「透明区 RGB 必须为 0」的断言，请改判 alpha。
4. **Gemini 顶部/左侧贴边**：原图猫耳、呆毛、尾巴顶到图像边缘（源 bbox y0=0、x0=1），padding 无法在源图外扩展，已用透明补边，画布内不留空。
5. **build.py 集成（Lead 负责）**：`build/build.py` 的 `collect_chars()` 目前白名单只有 `chatgpt/claude/deepseek`，需要改成 9 个 id、读 `assets/chars/<id>.webp`（deepseek 用 `TEX.hero`）。旧 `chatgpt.png/claude.png` 已归档到 `assets/chars/raw/legacy/`，不会再被构建扫到（构建只扫 `assets/chars/` 顶层文件，`raw/` 是子目录）。
6. **`raw/_qa_sheet.jpg` 与 `raw/_process_report.json`** 是自检产物，不参与构建；仓库体积敏感可删，重跑 `--qa` 会重建。

## 7. 一键重跑（替换立绘后）

```bash
# 全部 8 张重跑（自动重建 preview_compare.png 与 manifest-chars.json）
python assets/chars/process_chars.py

# 只重跑某张：同名新图覆盖 assets/chars/raw/<id>.png 后
python assets/chars/process_chars.py --only grok
python assets/chars/process_chars.py --only grok,kimi,glm,qwen,minimax

# 指定输入/输出（不动 raw/ 存档时用）
python assets/chars/process_chars.py --key grok --in D:\tmp\grok_chibi.png

# 自检
python assets/chars/process_chars.py --check     # 尺寸/体积/alpha 表（超 90KB 会断言失败）
python assets/chars/process_chars.py --qa        # 重建 raw/_qa_sheet.jpg
python assets/chars/process_chars.py --preview   # 只重建预览图
python assets/chars/process_chars.py --manifest  # 只重建 manifest
```

幼态新图若仍是白底，脚本会自动泛洪抠图；若背景不是白色（浅蓝/浅粉等），用 `--tol` 调整，或先手动抠好存 RGBA（`mode=auto` 会自动走 alpha 分支）。

## 8. 与 v3 的关系（为什么不沿用旧方案）

v3 的 `assets/chars/build_chars.py` 以 `hero.png` 为基底做 HSV 调色 + 手绘配饰，产出的 chatgpt/claude 与默认角色共用同一张脸和身体轮廓，被用户明确否决（「不要大肥鱼换色」）。v4 改为**直接使用用户提供的 8 张独立 AI 立绘**做抠图/排版，不再复用 hero 的线稿与身体；`build_chars.py` 与它的两个产物仅作历史归档（`raw/legacy/`），不参与本轮构建。
