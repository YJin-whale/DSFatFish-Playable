# 恒星贴图交付报告（v4 · 银河系 10 颗恒星 + 太阳/银心/银边）

- 负责人：**star-art**（共享任务 `task-3`）
- 契约：`docs/SPEC-v4.md` §7（恒星贴图契约）+ §1.7（银河系阶段恒星去同质化）
- 生成脚本：`assets/tex/raw/star/make_stars.py`（Pillow + numpy，确定性可复跑）
- 图源下载脚本：`assets/tex/raw/star/fetch_star_sources.py`
- 清单：`assets/manifest-stars.json`
- 对比图：`reports/star-contact-sheet.png`（#060A22 深蓝底，4×3 大图 + 底部小尺寸节点预览）

## 1. 交付清单

13 张，全部 **256×256 RGBA 透明底、单张 ≤120KB**（合计 573.8KB，未超预算）：

| key | 恒星 | 光谱 | Teff(K) | 主色（display） | 光球直径@256 | 星芒 | 体积 |
|---|---|---|---|---|---|---|---|
| star_alpha_cen | 半人马座α | G2V | 5790 | `#FFD99E` 黄白 | 113px | 6 | 47.6KB |
| star_barnard | 巴纳德星 | M4V | 3190 | `#FFB257` 橙红 | 90px | 4（弱） | 27.3KB |
| star_wolf359 | 沃尔夫359 | M6V | 2800 | `#FFA947` 深橙红 | 88px | 0 | 24.0KB |
| star_sirius | 天狼星 | A1V | 9940 | `#ADCBFF` 蓝白 | 118px | 8 | 43.6KB |
| star_eps_eri | 波江座ε | K2V | 5084 | `#FFC97A` 橙 | 108px | 6 | 43.7KB |
| star_procyon | 南河三 | F5IV | 6530 | `#FFEDD1` 黄白 | 115px | 8 | 48.4KB |
| star_tau_cet | 天仓五 | G8V | 5344 | `#FFD28F` 黄 | 109px | 6 | 44.3KB |
| star_altair | 牛郎星 | A7V | 7550 | `#E0ECFF` 白 | 114px | 8 | 40.0KB |
| star_vega | 织女星 | A0V | 9600 | `#A3C4FF` 蓝白 | 118px | 8 | 43.0KB |
| star_arcturus | 大角星 | K1.5III | 4286 | `#FFBC61` 橙红 | 119px | 4（弱） | 56.1KB |
| star_sun（可选） | 太阳 | G2V | 5772 | 真实 SDO/AIA 171Å | 128px | — | 52.1KB |
| star_galactic_center（可选） | 银河系中心 Sgr A* | — | — | 真实 EHT 图像 | 环直径 107px | — | 22.8KB |
| star_galactic_edge（可选） | 银河系边缘 | — | — | 程序化银蓝星尘 | 圆形支撑域 91% | — | 80.7KB |

> 光球直径 = 画布边长 × `disk_frac`（`_stats.json` 里有逐张 `disk_frac / halo_reach / rays`）。

## 2. 色温 → 主色（物理链路）

1. `planck_spectrum(Teff)`：360–830nm、2nm 步长计算普朗克谱。
2. 乘 CIE 1931 2° 配色函数（Wyman/Sloan/Shirley 2013 解析近似）积分 → XYZ → 线性 sRGB。
3. 白平衡到 **7500K**（`WB_REF_K`）：A7V≈中性白，因此 A 型偏蓝白、F 型暖白、G 型黄白、K 型橙、M 型橙红。色相顺序完全由黑体谱决定，不是逐通道手调。
4. 色度：按恒星设定 HSV 饱和度（`hsv_sat`，0.10–0.72），**只放大色度、不改色相**。原因：黑体色在 sRGB 里 G5–K2 之间天然非常接近，若不放大，10 张会都像“白/淡黄球”，无法满足 §1.7“不同颜色”。
5. 其余细节在**线性光空间**计算（临边昏暗≈真实光强比），最后统一 gamma 编码，避免“被照亮的球面”观感。

## 3. 写实细节实现

- **球形光球 + 临边昏暗**：正交球面法线，分波段理米粒系数（蓝端更暗 → 临边更红/橙），线性光下乘性压暗；再叠一个高斯“过曝白热核”（`glare_*`）让中心读作自发光。
- **米粒组织/对流纹理**：球面 3D 值噪声 fbm（无接缝、随球面透视压缩）+ 高频“沸腾”噪声 + 用独立噪声零交叉生成**暗巷网络**（granular lanes）。
- **星斑/耀斑**：K/M 矮星加暗而偏红的星斑；Wolf 359 额外加 2 处耀斑亮斑（其“耀星”特性）。
- **色球环**：临边极薄暖色环（热星偏 Hα 红）。
- **日冕光晕**：双指数核 + 宽尾 × 双尺度角向扰动，统一标定成“紧凑内层日冕 + 淡而短尾”；外缘在 `halo_reach` 处 alpha 平滑归 0。**巨星光晕更大更亮**（Arcturus 非空像素 65%、`halo_reach` 0.995），**M 矮星更小更暗**（14.5%–17.1%、`halo_reach` 0.69–0.72）。
- **衍射星芒**：4/6/8 道（按光谱型），线性宽度、外端随光晕衰减，颜色取恒星色 → 白混合。
- **透明底**：画布四边强制 alpha=0；四角恒为 0；圆形支撑域内才可能有光晕，因此不存在方形黑底/暗边。

## 4. 真实图像来源与授权

### 4.1 太阳 — NASA SDO/AIA 171Å（公共领域）

- 原图：`https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg`（2026-11-18 抓取，存档 `assets/tex/raw/star/sdo_171.jpg`）
- 授权：**NASA 公共领域**（NASA media usage guidelines），可自由使用；已注明来源。
- 处理：按径向亮度定位日面半径（≈480px/1024），裁 1.42×半径方形；**底部左侧日期戳/水印先按邻近黑色覆盖**再重采样；亮度提升（×1.42, γ0.86）；日面最外圈轻微提亮（SDO 171Å 的 EUV 暗边修成暖色，避免“大气层暗边”）；alpha = 不透明日面 + 仅保留真实日冕亮结构（阈值 0.22–0.48 亮度），**圆形支撑域 r≤0.67 半画布**，之外 alpha 恒 0。
- 备用：同时抓了 `sdo_304.jpg`（304Å 红色版本），未用于成品。

### 4.2 银河系中心 — EHT Sgr A*（CC BY 4.0）

- 原图：EHT Collaboration 首张 Sgr A* 图像，经 ESO 发布；抓取自 `https://www.eso.org/public/archives/images/large/eso2208-eht-mwb.jpg` 同系列干净图（存档 `assets/tex/raw/star/eht_mwa.jpg`，4076×4076）。
- 参考页：`https://www.eso.org/public/images/eso2208-eht-mwb/`
- 授权：**CC BY 4.0（EHT Collaboration / ESO）**。使用时必须保留 **Credit: EHT Collaboration** 署名（建议游戏内致谢/帮助页与 README 中注明）。
- 处理：径向亮度定位吸积环半径（≈738px/4076）→ 以环半径 1.45× 圆形裁切 → 缩放到画布 → 轻度提亮/对比 + unsharp mask → 圆形 alpha 支持域 0.61 半画布，四角透明。

### 4.3 其余 10 颗恒星 / 银河系边缘

- 全部为**程序化生成**（`make_stars.py`，原创），无第三方图像版权问题。
- 银河系边缘（可选）：程序化“银蓝尘埃带 + 稀疏暗星场 + 少量四芒前景星”，圆形透明底。

## 5. 逐张校验（脚本自动统计）

| 文件 | 尺寸 | 体积 | 不透明像素(α>0.98) | 非空像素(α>0.03) | 四边 α max | 四角 α max |
|---|---|---|---|---|---|---|
| star_alpha_cen.png | 256×256 | 47.6KB | 14.9% | 50.3% | 0 | 0 |
| star_barnard.png | 256×256 | 27.3KB | 9.4% | 17.1% | 0 | 0 |
| star_wolf359.png | 256×256 | 24.0KB | 9.1% | 14.5% | 0 | 0 |
| star_sirius.png | 256×256 | 43.6KB | 16.4% | 38.1% | 0 | 0 |
| star_eps_eri.png | 256×256 | 43.7KB | 13.6% | 40.4% | 0 | 0 |
| star_procyon.png | 256×256 | 48.4KB | 15.5% | 56.2% | 0 | 0 |
| star_tau_cet.png | 256×256 | 44.3KB | 14.0% | 43.6% | 0 | 0 |
| star_altair.png | 256×256 | 40.0KB | 15.2% | 39.1% | 0 | 0 |
| star_vega.png | 256×256 | 43.0KB | 16.3% | 36.8% | 0 | 0 |
| star_arcturus.png | 256×256 | 56.1KB | 16.7% | 65.0% | 0 | 0 |
| star_sun.png | 256×256 | 52.1KB | 19.0% | 33.0% | 0 | 0 |
| star_galactic_center.png | 256×256 | 22.8KB | 26.2% | 28.5% | 0 | 0 |
| star_galactic_edge.png | 256×256 | 80.7KB | 0.0% | 63.2% | 0 | 0 |

- **透明性**：13 张全部 `border_alpha_max = 0`、`corner_alpha_max = 0`，即四边/四角完全透明，无方形黑底、无方形暗边。
- **太阳复核**：透明后 98.4% 不透明问题已修（当前不透明 19.0%，只覆盖日面）；在 #060A22 深蓝底上放大目检无黑方块、无日期水印文字，日面外 alpha=0。
- **目检结论（#060A22 深色底逐张）**：
  - alpha_cen：黄白，米粒组织+暗巷清晰，6 道星芒，临边偏橙红，边缘干净。
  - barnard / wolf359：橙红/深橙红，光球小、光晕小且暗、几乎无星芒；Wolf 359 可见 2 处耀斑亮斑。
  - sirius / vega：蓝白，8 道细星芒，亮度最高，光晕偏冷。
  - eps_eri / tau_cet：橙 / 黄，暖色临边，6 星芒。
  - procyon：黄白极淡，8 星芒；altair：近纯白，8 星芒。
  - arcturus：橙红巨星，光球最大、光晕最宽最亮（非空 65%），4 道弱星芒。
  - sun：真实 NASA 日面+日冕（金色假彩色），圆形外全透明。
  - galactic_center：EHT 环状结构（真实图像固有模糊），圆形透明裁切。
  - galactic_edge：银蓝尘埃 + 稀疏星场，圆形透明底。
- **未发现**：方形暗边/黑底、过火星芒（最亮 A 星星芒 alpha 峰值约 0.6）、行星式硬边大气环（已把临边光晕标定收窄）。

## 6. 与渲染层集成建议（给 Lead）

- 贴图是**完整方形精灵**：光球 + 光晕 + 星芒都在图里，alpha 已含圆形淡出。建议按方形绘制：
  - 目标光球直径 D（px）→ 绘制边长 ≈ `D / disk_frac`（例：抵达场景想光球 180px，alpha_cen 画布画 180/0.44 ≈ 409px 见方）。
  - 参考：`disk_frac` ∈ 0.345–0.465（M 矮星小、A 型/巨星大），见 manifest `note` 或 `_stats.json`。
- 由于 alpha 已带光晕，**不建议再叠加强程序化 glow**；若要额外辉光，加很淡一层即可，避免再次“行星雾”。
- `star_galactic_edge.png` 已交付，但 `src/render.js` 的 `GALAXY_TEX` 目前没有映射 `galactic_edge`（Lead 若要用，加一行映射即可）；不加则继续走程序化兜底。
- 不建议裁剪成圆形后再画（会把光晕/星芒切掉）；若必须圆形取景，半径按光球半径×1.35 估。

## 7. 风险与限制

| 风险 | 说明 / 缓解 |
|---|---|
| 银心原图模糊 | EHT 干涉成像本身分辨率有限，256px 下偏“柔”；已做轻度 unsharp，未过度锐化。 |
| 太阳是 EUV 假彩色 | NASA SDO/AIA 171Å 并非可见光真实颜色（真实太阳偏白）；这是官方图像的标准配色，报告中已注明。 |
| G/K 型色相接近 | 黑体谱在 G5–K2 的 sRGB 色差本来就小；为保证小尺寸可辨识，按星设定 HSV 饱和度（色相仍物理）。白平衡 7500K 是显示选择（与 astronomy.js 里 v3 的直观色系一致度更高）。 |
| 体积上限 | 120KB 内以轻度量化/压缩保存，仍是 RGBA（未用调色板，兼容 canvas alpha）。 |
| 接入缺省 | 未修改 `src/render.js`；贴图需 Lead 加绘制分支。缺图时现有程序化兜底不受影响。 |

## 8. 复跑方式

```bat
"C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe" ^
  assets\tex\raw\star\fetch_star_sources.py
"C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe" ^
  assets\tex\raw\star\make_stars.py
```

- `fetch_star_sources.py`：下载 SDO 171Å/304Å 与 EHT Sgr A*（已存在则跳过）。
- `make_stars.py`：生成 13 张 PNG + `assets/manifest-stars.json` + `reports/star-contact-sheet.png` + `raw/star/_stats.json`；随机数按 star id 播种，重复运行结果一致。
- 不运行 `build/build.py`（属 Lead 作用域）；`star_*` 前缀会被其 `collect_textures()` 自动内联。
