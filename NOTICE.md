# NOTICE — 素材授权、署名与数据来源

本文件说明 **肥鱼跳宇宙 · 星尘远航（FatFish-Playable）** 中不同部分的授权归属。
请先读这一条，它对整个仓库有效：

> **代码与素材的授权是分开的。**
> 源代码、构建脚本与文档按根目录 [`LICENSE`](LICENSE) 的 **MIT** 许可发布；
> `assets/` 下的图像素材、角色立绘与天文数据**不属于 MIT 授权范围**，保留各自
> 原作者的授权与署名要求（如下所列）。整体再分发本仓库（含 `assets/`）时，必须
> 同时遵守本文件。
>
> 本项目是**非官方、非商业**的粉丝向 / 同人作品，与任何 AI 公司无关联。

---

## 1. 代码 / Code

- 授权：**MIT**，见 [`LICENSE`](LICENSE)
- 版权：© 2026 FatFish-Playable contributors
- 范围：`src/`、`build/`、`tools/`、`docs/`、`reports/` 中的文本文件，
  以及构建产物 `index.html` 中的**代码部分**（不含其中内联的贴图与立绘数据）。

## 2. 天文数据与算法 / Astronomical data

游戏内所有距离、方位与轨道位置都来自公开天文数据与公开算法，逐项说明见
[`docs/astronomy-notes.md`](docs/astronomy-notes.md)：

| 数据 / 算法 | 来源 | 授权 / 使用条件 |
|---|---|---|
| 行星实时位置（J2000 开普勒轨道根数 + 世纪变率 → 日心坐标） | JPL SSD, *Approximate Positions of the Major Planets*（E. M. Standish）<br>https://ssd.jpl.nasa.gov/planets/approx_pos.html | 公开数据 / 算法说明 |
| 行星、月球物理常数（半径、重力比、轨道半长轴等） | NASA Planetary Fact Sheet / Moon Fact Sheet<br>https://nssdc.gsfc.nasa.gov/planetary/factsheet/ | 公共领域（NASA） |
| 行星定义、轨道要素 | IAU（国际天文学联合会）<br>https://www.iau.org/ | 公开标准 |
| 恒星距离 / 视差 | Gaia 任务（ESA）与 SIMBAD 汇编<br>https://www.cosmos.esa.int/web/gaia | 公开科学数据 |
| 星系 / 星系团距离 | NASA/IPAC NED<br>https://ned.ipac.caltech.edu/ | 公开科学数据 |
| 可观测宇宙尺度 | Planck 2018 Results VI<br>https://doi.org/10.1051/0004-6361/201833910 | 公开科学论文 |
| 参考值交叉验证 | JPL DE421 本地计算 + 独立 VSOP87 实现（见 astronomy-notes §10） | 公开历表数据 |

## 3. 行星、月球与太阳贴图（`assets/tex/globe_*.png`）

等距柱状（equirectangular）真实天体贴图 → 本项目处理为 512×512 正交球体 PNG。
逐张记录见 [`assets/manifest-textures.json`](assets/manifest-textures.json)。

| 贴图文件 | 天体对象 | 原始素材 | 授权 |
|---|---|---|---|
| `globe_earth.png` | 地球 | Solar System Scope `2k_earth_daymap.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_moon.png` | 月球 | Solar System Scope `2k_moon.jpg`（基于 NASA LRO / SELENE 月面数据） | **CC BY 4.0** — Solar System Scope |
| `globe_mercury.png` | 水星 | Solar System Scope `2k_mercury.jpg`（基于 NASA MESSENGER） | **CC BY 4.0** — Solar System Scope |
| `globe_venus.png` | 金星 | Solar System Scope `2k_venus_surface.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_mars.png` | 火星 | Solar System Scope `2k_mars.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_jupiter.png` | 木星 | Solar System Scope `2k_jupiter.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_saturn.png` | 土星 | Solar System Scope `2k_saturn.jpg`（光环由游戏层绘制） | **CC BY 4.0** — Solar System Scope |
| `globe_uranus.png` | 天王星 | Solar System Scope `2k_uranus.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_neptune.png` | 海王星 | Solar System Scope `2k_neptune.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_sun.png` | 太阳 | Solar System Scope `2k_sun.jpg` | **CC BY 4.0** — Solar System Scope |
| `globe_pluto.png` | 冥王星 | **NASA/JHUAPL/SwRI** New Horizons，PIA19952<br>https://images.nasa.gov/details/PIA19952 | **公共领域**（NASA Media Usage Guidelines） |
| `bg_milkyway.jpg` | 银河系背景全景 | Solar System Scope `2k_stars_milky_way.jpg` | **CC BY 4.0** — Solar System Scope |

- Solar System Scope 素材库主页与授权说明：https://www.solarsystemscope.com/textures/
- NASA 媒体使用规范：https://www.nasa.gov/nasa-brand-center/images-and-media/

## 4. 星系照片（`assets/tex/gal_*.jpg`）

真实观测照片，用于抵达界面圆形取景与银河系 / 宇宙地图缩略图：

| 贴图文件 | 天体 | 来源 | 授权 |
|---|---|---|---|
| `gal_andromeda.jpg` | 仙女座星系 M31 | **NASA/JPL-Caltech**（Herschel + Planck + IRAS + COBE 多波段合成，PIA25163）<br>https://images.nasa.gov/details/PIA25163 | **公共领域**（NASA） |
| `gal_triangulum.jpg` | 三角座星系 M33 | **ESO**/VST，`eso1424a`<br>https://www.eso.org/public/images/eso1424a/ | **CC BY 4.0** — ESO |
| `gal_lmc.jpg` | 大麦哲伦云 | **ESO**/VISTA，`eso1914a`<br>https://www.eso.org/public/images/eso1914a/ | **CC BY 4.0** — ESO |
| `gal_smc.jpg` | 小麦哲伦云 | **ESO**，`eso1008b`<br>https://www.eso.org/public/images/eso1008b/ | **CC BY 4.0** — ESO |

## 5. 恒星贴图（`assets/tex/star_*.png`，13 张）

逐张色温、来源与处理见 [`assets/manifest-stars.json`](assets/manifest-stars.json) 与
[`reports/star-assets.md`](reports/star-assets.md)。

### 5.1 真实观测图像（2 张）

| 贴图文件 | 对象 | 来源 | 授权 |
|---|---|---|---|
| `star_sun.png` | 太阳 | **NASA SDO/AIA** 171 Å 全日面影像<br>https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg | **公共领域**（NASA） |
| `star_galactic_center.png` | 银河系中心 Sgr A* | **EHT Collaboration** 首张 Sgr A* 图像，经 ESO 发布（`eso2208-eht-mwb`）<br>https://www.eso.org/public/images/eso2208-eht-mwb/ | **CC BY 4.0**（EHT Collaboration / ESO） |

> **使用 EHT 图像时必须保留署名：`Credit: EHT Collaboration`。**
> 本仓库在游戏内「玩法说明」页、本文件与 README 中均保留该署名。

### 5.2 程序化重建（11 张，本项目原创）

`star_alpha_cen`、`star_barnard`、`star_wolf359`、`star_sirius`、`star_eps_eri`、
`star_procyon`、`star_tau_cet`、`star_altair`、`star_vega`、`star_arcturus`
共 10 颗恒星的贴图，以及 `star_galactic_edge`（银河系盘面外缘），均为
`assets/tex/raw/star/make_stars.py` **程序化生成**的原创图像：

- 由有效温度（Teff）→ 普朗克黑体谱 → CIE 1931 配色函数积分得到主色，
  叠加临边昏暗、米粒组织/暗巷、星斑耀斑、色球环、日冕光晕与衍射星芒，256×256 RGBA 透明底；
- 无第三方图像素材，本项目以 MIT / 公有领域方式提供；
- 星体距离、光谱型等参数来自公开天文数据（见第 2 节）。

## 6. 角色立绘（`assets/chars/*.webp` 与 `hero.png`）

### 6.1 默认角色

- 文件：`hero.png`（构建时内联为 `TEX.hero`），角色「深海小鲸娘 / DeepSeek」
- 来源：**用户提供的 AI 生成图**，原角色形象来自 **上善无形 / ZipZipPipe**
- 授权：**CC BY-NC-SA 4.0**（署名 — 非商业性使用 — 相同方式共享）
- 本项目原样复用该图（未改动），并按 CC BY-NC-SA 4.0 保留署名链。
- 提示：**CC BY-NC-SA 4.0 禁止商业使用**，因此本项目只能在非商业场景下分发、游玩与再创作。

### 6.2 其余 8 位 AI 拟人角色

`chatgpt`、`claude`、`gemini`、`grok`、`kimi`、`glm`、`qwen`、`minimax`
（文件名见 `assets/chars/`）为用户提供的 **社区 AI 拟人二创** 立绘，仅做去白底、
裁切与 300×400 透明 WebP 转码（`assets/chars/process_chars.py`），不改画风。

对应产品与商标归各自公司所有：

| 角色 id | 游戏内名字 | 对应产品 / 商标持有人 |
|---|---|---|
| `chatgpt` | 聊天酱 | ChatGPT — OpenAI |
| `claude` | 小星芒 | Claude — Anthropic |
| `gemini` | 双星喵 | Gemini — Google |
| `grok` | 格萝克 | Grok — xAI |
| `kimi` | 月音酱 | Kimi — 月之暗面（Moonshot AI） |
| `glm` | 墨卷酱 | GLM（ChatGLM）— 智谱 AI |
| `qwen` | 千问酱 | Qwen（通义千问）— 阿里巴巴 |
| `minimax` | 小麦克 | MiniMax — 稀宇科技 |

> 本项目与上述公司**无任何关联、非官方、未获其背书**。角色形象为粉丝创作的
> 拟人化/戏仿表达，名称仅用于说明对应产品；若相关权利人提出要求，将立即移除
> 对应素材。

## 7. 音乐 / Music

本项目内置**两首第三方音乐作品**（用户提供的音频文件），仅用于非商业的本地演示 / 试玩：

| 曲目 | 文件 | 说明 |
|---|---|---|
| **罐装毕加索**《Let Me Go（共创版）》 | `assets/audio/bgm_canned_picasso.mp3` | 原文件约 4.87 MB / 02:04 → 96 kbps 1.42 MB，内联进 `index.html` |
| **星落落oi**《Let me go》 | `assets/audio/bgm_xingluoluo.mp3` | 原文件约 8.52 MB / 03:38 → 96 kbps 2.50 MB，内联进 `index.html` |

- **版权归原权利人**（罐装毕加索 / 星落落oi），**不适用本仓库的 MIT 许可**；
- 仅随本地副本用于**非商业的个人试玩**；本项目**不主张**对这两首曲目的任何权利；
- **公开再分发或商业使用前，请自行向原权利人取得授权**；
  如相关权利人提出要求，将立即移除对应音频；
- `assets/audio/raw/` 是用户提供的原始 mp3，已在 `.gitignore` 中排除，不随仓库分发。

### 7.1 用户上传的音乐

游戏内「上传音乐」功能只在**用户自己的浏览器**里保存文件
（IndexedDB `fatfish_audio_v1/tracks`）——本项目**不收集、不转存、不上传**任何用户音频；
上传曲目的版权与使用责任归上传者本人。

## 8. 字体与音效

- **字体**：不加载任何外部字体，使用系统字体（`system-ui` / 微软雅黑 / 苹方等）。
- **音效**：由 WebAudio 实时合成（无第三方音频素材）；音量可在设置里无极调节。

## 9. 合规速查

| 素材 | 可以再分发吗 | 必须做什么 | 不得做什么 |
|---|---|---|---|
| 代码（src/build/tools/docs） | 可以 | 保留 MIT 版权与许可声明 | — |
| Solar System Scope 贴图 | 可以 | 署名 Solar System Scope（CC BY 4.0） | — |
| NASA SDO / New Horizons 图像 | 可以 | 注明 NASA 来源 | 暗示 NASA 背书 |
| EHT Sgr A* 图像 | 可以 | 保留 **Credit: EHT Collaboration** | 去掉该署名 |
| ESO 星系照片 | 可以 | 署名 ESO（CC BY 4.0） | — |
| 程序化恒星贴图 | 可以 | 注明本项目原创 | — |
| 内置音乐（两首） | **不建议公开再分发** | 注明原权利人（罐装毕加索 / 星落落oi）、非商业个人使用 | 商业使用；未取得授权就再分发 |
| 用户上传的音乐 | 仅上传者本人 | 只存在本机浏览器（IndexedDB），不上传 | 转存 / 分发他人音乐 |
| 默认角色 `hero.png` | 仅非商业 | 署名 上善无形 / ZipZipPipe，相同方式共享 | **商业使用** |
| 其余 8 位角色立绘 | 仅非商业 | 注明非官方、商标归各公司 | 商业使用、暗示官方授权 |

如你是素材权利人并希望调整署名或移除素材，请开 issue 联系维护者。
