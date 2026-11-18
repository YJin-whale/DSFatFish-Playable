# 贴图资产验收记录（Lead）

日期：2026-11-18 ｜ 交付方：planet-assets（task-1） ｜ 状态：**已集成并通过视觉验收**

## 交付清单（assets/tex/）

| 文件 | 尺寸 | 体积 | 用途 | 来源 |
|---|---|---|---|---|
| globe_moon.png | 512² | 119 KB | 月球（首个落点/贴图需求） | Solar System Scope 2k_moon（CC BY 4.0） |
| globe_mercury.png | 512² | 114 KB | 水星 | SSS 2k_mercury（CC BY 4.0） |
| globe_venus.png | 512² | 120 KB | 金星 | SSS 2k_venus_surface（CC BY 4.0） |
| globe_earth.png | 512² | 77 KB | 地球（标题页 / 太阳系地图 / 出发场景） | SSS 2k_earth_daymap（CC BY 4.0） |
| globe_mars.png | 512² | 120 KB | 火星 | SSS 2k_mars（CC BY 4.0） |
| globe_jupiter.png | 512² | 108 KB | 木星 | SSS 2k_jupiter（CC BY 4.0） |
| globe_saturn.png | 512² | 72 KB | 土星 | SSS 2k_saturn（CC BY 4.0） |
| globe_uranus.png | 512² | 72 KB | 天王星 | SSS 2k_uranus（CC BY 4.0） |
| globe_neptune.png | 512² | 66 KB | 海王星 | SSS 2k_neptune（CC BY 4.0） |
| globe_pluto.png | 512² | 96 KB | 冥王星（太阳系终点） | NASA/JHUAPL/SwRI PIA19952（Public Domain） |
| globe_sun.png | 512² | 115 KB | 太阳（地图/场景） | SSS 2k_sun（CC BY 4.0） |
| bg_milkyway.jpg | 1400×700 | 37 KB | 银河星空背景 | SSS 2k_stars_milky_way（CC BY 4.0） |
| gal_andromeda.jpg | 720×411 | 19 KB | 仙女座星系抵达页/宇宙地图 | NASA/ESA 真实影像 |
| gal_triangulum.jpg | 720×605 | 66 KB | 三角座星系 | NASA/ESA 真实影像 |
| gal_lmc.jpg | 650×720 | 93 KB | 大麦哲伦云 | NASA/ESA 真实影像 |
| gal_smc.jpg | 697×720 | 109 KB | 小麦哲伦云 | NASA/ESA 真实影像 |

## 验收内容

1. 逐张 `read_image` 目检：球体轮廓圆正、无上下颠倒/接缝错位、非黑非白；月球环形山、木星大红斑、地球大陆、冥王星心形平原均清晰可辨。
2. 透明通道：圆外 alpha=0，构建后游戏叠在星空上无白底。
3. 尺寸/体积：单张 ≤123 KB，总 assets ≈ 1.57 MB（内联 base64 后 index.html ≈ 2.74 MB，可接受）。
4. 游戏内实测截图（reports/shots/）：
   - 抵达月球 `g_arrive_moon.png`、抵达火星 `g_arrive_mars.png`、抵达仙女座 `gal_arr_andromeda.png`、抵达大麦哲伦云 `gal_arr_lmc.png`
   - 飞行中逼近月球 `g_flight_moon.png`、飞向三角座 `gal_flight_triangulum.png`
   - 标题页 `fin_title.png`、太阳系航线预演 `earth_map.png`
5. 构建期处理：`build/optimize_assets.py` 对星系照片自动裁掉黑边、降采样到 ≤720px 并压缩；`build/make_earth.py` 为地球/银河背景兜底（planet-assets 已交付，构建优先用其成品）。

## 备注

- `gal_virgo / gal_coma / gal_horizon` 无合适单张真实图，游戏用程序化星系团/宇宙网+CMB 视界兜底；这是刻意取舍，已在 README「已知局限」注明。
- 授权：Solar System Scope 为 CC BY 4.0，游戏内「玩法说明」与 README 均署名；NASA 图像按 NASA Media Usage Guidelines（公共领域）使用。
- 交付方的 `assets/manifest-textures.json` 由 Lead 终版整理（含来源/授权/尺寸），后续换图只需替换同名文件并重新构建。
