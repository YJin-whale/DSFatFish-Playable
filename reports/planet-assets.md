# 贴图资产交付报告（planet-assets / task-1）

日期：2026-11-18 ｜ 交付目录：`assets/tex/` ｜ 运行期资产总计 **1.35 MB**（≤ 4 MB 预算）

## 1. 交付清单与校验

所有 globe 为 512×512 透明底正射球体 PNG；alpha 覆盖率指「非全透明像素占全图比例」，`圆外 max alpha` 用半径 0.94 的圆外区域统计。

| 文件 | 尺寸 | 体积 | PNG 模式 | alpha 非零 | 圆外 max α | 来源 | 授权 |
|---|---|---|---|---|---|---|---|
| globe_earth.png | 512×512 | 77.1 KB | P+tRNS | 70.06% | 0 | Solar System Scope `2k_earth_daymap` | CC BY 4.0 |
| globe_moon.png | 512×512 | 103.8 KB | LA（灰+α） | 70.23% | 1/255 | SSS `2k_moon` | CC BY 4.0 |
| globe_mercury.png | 512×512 | 101.5 KB | LA（灰+α） | 70.23% | 1/255 | SSS `2k_mercury` | CC BY 4.0 |
| globe_venus.png | 512×512 | 119.8 KB | P+tRNS | 70.06% | 0 | SSS `2k_venus_surface` | CC BY 4.0 |
| globe_mars.png | 512×512 | 119.8 KB | P+tRNS | 70.06% | 0 | SSS `2k_mars` | CC BY 4.0 |
| globe_jupiter.png | 512×512 | 107.6 KB | P+tRNS | 70.06% | 0 | SSS `2k_jupiter` | CC BY 4.0 |
| globe_saturn.png | 512×512 | 72.2 KB | P+tRNS | 70.06% | 0 | SSS `2k_saturn` | CC BY 4.0 |
| globe_uranus.png | 512×512 | 71.6 KB | RGBA | 70.23% | 1/255 | SSS `2k_uranus` | CC BY 4.0 |
| globe_neptune.png | 512×512 | 66.1 KB | P+tRNS | 70.06% | 0 | SSS `2k_neptune` | CC BY 4.0 |
| globe_pluto.png | 512×512 | 96.4 KB | P+tRNS | 70.06% | 0 | NASA/JHUAPL/SwRI PIA19952 | Public Domain |
| globe_sun.png | 512×512 | 114.9 KB | P+tRNS | 70.06% | 0 | SSS `2k_sun` | CC BY 4.0 |
| bg_milkyway.jpg | 1400×700 | 36.9 KB | JPEG | — | — | SSS `2k_stars_milky_way` | CC BY 4.0 |
| gal_andromeda.jpg | 720×411 | 18.7 KB | JPEG | — | — | NASA/JPL-Caltech PIA25163 | Public Domain |
| gal_triangulum.jpg | 720×605 | 67.5 KB | JPEG | — | — | ESO/VST `eso1424a` | CC BY 4.0 |
| gal_lmc.jpg | 650×720 | 94.7 KB | JPEG | — | — | ESO/VISTA `eso1914a` | CC BY 4.0 |
| gal_smc.jpg | 697×720 | 111.3 KB | JPEG | — | — | ESO `eso1008b` | CC BY 4.0 |

- P+tRNS / LA 的 PNG 在现代浏览器与 canvas 中解码结果与 32 位 RGBA 完全一致（逐像素 alpha 保留）；`uranus` 直接是 RGBA。
- `LA` 与圆外 1/255 的 144 个像素是 Lanczos 降采样振铃造成的边缘微光，肉眼不可见；`P+tRNS` 为严格 0。
- 单张 66–120 KB，全部 ≤ 120 KB（SPEC 建议值）；`raw/` 原始等距柱状图 5.8 MB 按 SPEC 保留用于重建，**不参与构建内联**。

## 2. 生成方法（可复现）

脚本：`assets/tex/_build/build_globes.py`（Pillow 12 + numpy 2），`build_galaxies.py`。

1. **几何**：输出画布 512²，先以 2× 超采样（1024²）逐像素反算：`p=(x,y)/0.94`，`N=(px,py,√(1-|p|²))`；`lat=asin(py)`，`lon=atan2(px,pz)+lon0`，按等距柱状图 `u=0.5+lon/2π`、`v=0.5-lat/π` 双线性采样（经度方向环绕，避免接缝错位）；北极朝上，无上下颠倒。
2. **光照**：主光方向左上偏前（≈(-0.6,0.44,0.65)），`ambient` 0.12–0.30 + smoothstep 晨昏线（宽度 0.34–0.5，柔和过渡）+ 轻微临边昏暗；再乘各天体亮度/对比/饱和度。
3. **大气辉光**：Fresnel `(1-Nz)^k` 环，按天体着色（地球蓝、金星淡黄、火星橙、天王/海王青蓝、太阳橙红），强度 0.04–0.40，只作用在球体内部（圆外 alpha 保持 0）。
4. **太阳**：自发光，无晨昏线；临边昏暗 + 暖色临边，不叠加主光。
5. **圆盘**：圆内（r≤0.94）不透明，外部透明；2× 超采样后用 **预乘 alpha 的 Lanczos** 降到 512²，得到干净抗锯齿轮廓。
6. **PNG 预算**：先存 32 位 RGBA；超 120 KB 时改用 8 位调色板 + `tRNS` 逐索引 alpha（内部 200 色 + 边缘 6 色×8 alpha 级），并对内部色做 8×8 Bayer 有序抖动抑制色带；灰体（月/水星）改用灰+α PNG（无损、无色带）。水星/月球最终为 `smooth=1.0` 轻微柔化以压到预算内，环形山/月海清晰可辨。
7. **冥王星**：公开源没有完整覆盖的等距柱状图（SSS 无 Pluto，NASA 的 PIA19858/PIA11707 全球图只覆盖部分纬度、南半球为黑块），因此改用 New Horizons 真彩色全盘影像 **PIA19952**：先对圆盘做 RANSAC 圆拟合（中心 2513.8, 2482.9，半径 2166.6 px），再按正射圆盘采样可见半球，最后叠加同一套光照/临边处理。
8. **星系照片**：ESO/NASA 原图居中留黑边缩放到 1024² 再压缩（构建期 `build/optimize_assets.py` 又统一裁黑边、降到 ≤720 px）。`bg_milkyway` 为 2048×1024 等距柱状全景（横向可无缝平铺），构建期缩为 1400×700。

## 3. 自查记录（逐张 read_image 目检）

- 轮廓：11 张均为正圆、左右/上下无镜像错位、无接缝错位、无拉伸；圆外透明。
- 月球：月海、第谷环形山与亮辐射纹清晰（灰+α 无损编码，无色带）；水星环形山可辨。
- 地球：非洲/欧洲/大西洋、极冠清晰，蓝色大气临边；木星：大红斑居中可见；火星：水手谷可见；土星：云带平滑（环由游戏层绘制）；天王/海王/太阳无黑白色块，太阳有真实米粒/活动区纹理。
- 冥王星：完整圆盘、心形「汤博区」清晰、无黑边/缺口（此前阈值检测版本有缺角，已用圆拟合修复）。
- 星系：仙女座（Herschel 红外多波段）、三角座（VST）、大/小麦哲伦云（VISTA/ESO）均为真实照片，构图居中、无黑边残留。
- 透明通道：圆外 alpha 仅 Lanczos 振铃的 1/255×144 px（肉眼不可见），其余严格 0。

## 4. 授权与游戏内署名建议

- Solar System Scope 贴图 **CC BY 4.0**（https://www.solarsystemscope.com/textures/）。
- ESO 影像 **CC BY 4.0**（eso1424a / eso1914a / eso1008b）。
- NASA/JPL-Caltech PIA25163、NASA/JHUAPL/SwRI PIA19952 按 NASA Media Usage Guidelines 使用（公共领域）。

建议「玩法说明 / 关于」页署名（已与 Lead 的 README 署名一致）：

> 星球表面贴图：Solar System Scope（solarsystemscope.com），CC BY 4.0。
> 星系与冥王星影像：NASA/JPL-Caltech、NASA/JHUAPL/SwRI（公共领域）、ESO（CC BY 4.0）。

## 5. 已知取舍 / 未交付项

- `gal_virgo / gal_coma / gal_horizon`（室女座星系团、后发座星系团、可观测宇宙视界）没有合适的单张真实图，按 SPEC 由渲染层程序化绘制，本任务未提供图片。
- 金星按 SPEC 使用**表面**贴图（SSS 偏橙的雷达高程着色），不是云顶照片；如后续想要云顶观感可换 `2k_venus_atmosphere`。
- 土星环不由贴图提供（SPEC 允许游戏层绘制）。
- 构建期由 `build/optimize_assets.py` 对星系 JPG 做统一裁边/降采样，所以本报告记录的是**构建后**尺寸；原始下载件在 `assets/tex/_build/sources/`。
- `assets/manifest-textures.json` 由本任务脚本按当前成品重新生成（16 项，含 key/file/w/h/source/url/license/note/bytes），与上表一致。
