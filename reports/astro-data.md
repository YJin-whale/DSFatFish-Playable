# astro-data 交付报告 · `src/astronomy.js`

> 任务：task-2（astro-data）
> 负责人：astro-data
> 规格：`docs/SPEC.md` 第 4 节（契约）
> 数据说明：`docs/astronomy-notes.md`
> 交付日期：2026-11-18

---

## 1. 交付物

| 文件 | 说明 |
|---|---|
| `src/astronomy.js` | 天文数据 + 航段计算模块，ES5 IIFE，无 DOM / 无外部依赖，暴露全局 `A` |
| `docs/astronomy-notes.md` | 每个距离的测算依据、物理含义与局限、来源 URL、与 SPEC 的取舍记录 |
| `reports/astro-data.md` | 本报告：自检结果、关键数值表、集成提示 |

---

## 2. 实现概要

- **28 站**：太阳系 9（`moon` … `pluto`）+ 银河系 12（`alpha_cen` … `galactic_edge`）+ 可观测宇宙 7（`lmc` … `observable_edge`）。
- **3 层级**：`solar`(km) / `stellar`(ly) / `cosmic`(ly)。
- 每站字段：契约要求字段全部给出，另加 `index`、`stageUnit`、`indexInStage`、`legDistanceKm/Ly/Label`、`totalDistanceKm/Ly/Label`、`distanceNote`、`distanceRule`、`src`、`launchSpeedKms`；`moon` 另有 `firstLegKm = 384400`。
- 契约 API 全部实现：
  `A.STAGES` / `A.STOPS` / `A.SEGMENTS` / `A.ACHIEVEMENTS` / `A.EARTH`（虚拟地球站）/
  `A.segment(i)` / `A.legInfo(i)` / `A.legDistance(from,to)` / `A.cumulative(stop)` /
  `A.indexOf(id)` / `A.byId(id)` / `A.stageOf(index)` / `A.launchSpeedKms(ratio)` /
  `A.fmtNumber(n)` / `A.fmtDistance(km,opts)` / `A.selftest()`；
  另加 `A.stageById(id)`、`A.stopsOf(stage)`、`A.STOP_COUNT`、`A.VERSION` 及四个常量（`AU_KM` / `LY_KM` / `EARTH_G` / `EARTH_ESCAPE_KMS`）。
- **唯一数据源**：`computeLeg()` 一套规则同时驱动 `A.STOPS` 的航段字段、`A.SEGMENTS`、`A.legDistance()`，界面说明与代码计算不会漂移。
- **成就**：11 条（`a_one_small_step`、`a_mars`、`a_jupiter`、`a_pluto`、`a_solar_left`、`a_galaxy_edge`、`a_cosmic_edge`、`a_wok`、`a_partner`、`a_rich`、`a_ufo10`）；前 7 条同时挂在对应站点的 `achievement` 字段上。

---

## 3. 自检结果

运行环境：`C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe`

```powershell
& "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe" -e `
  "var fs=require('fs');eval(fs.readFileSync('C:/Users/admin/Desktop/FatFish-Playable/src/astronomy.js','utf8')); console.log(A.STOPS.length); console.log(JSON.stringify(A.selftest()));"
```

| 检查项 | 结果 |
|---|---|
| `A.STOPS.length` | **28**（9 + 12 + 7）|
| `A.selftest()` | **`[]`**（0 条错误）|
| 每段 leg 顺序 / 单位 / 标签 | 与 SPEC 4.3 一致（见 §4 表）|
| 总累计航程 | **465 亿光年**（终点 `totalDistanceLy = 46500000000`）|
| `A.segment(0).from` | `{id:'earth', name:'地球', stage:'solar', orbitalAU:1, gravityRatio:1, …}` |
| `moon.legDistanceKm` | `384400`（`firstLegKm` 同值）|
| 地球是否在 STOPS 中 | 否；`A.indexOf('earth') === -1`，`A.byId('earth') === null`（虚拟地球用 `A.EARTH`）|
| 浏览器环境执行 | 通过：用 `vm` 沙箱（无 `module`/DOM）执行后 `ctx.A.STOPS.length === 28`、`ctx.A.selftest() === []` |
| ES5 语法 | 通过：无 `let` / `const` / 箭头函数 / 模板字符串 / `class` / `Object.assign` |
| 单位 | solar 段全部 km（`legDistanceLabel` 含 `km`）；stellar/cosmic 段全部 ly（标签含「光年」）|
| 单调性 | 28 站累计航程严格递增 |
| 成就与 engine 约定 | engine.js 里硬编码检查的 `a_mars / a_jupiter / a_pluto / a_solar_left / a_galaxy_edge / a_cosmic_edge / a_wok / a_partner / a_rich / a_ufo10` 全部存在 |

`selftest()` 覆盖：常量、层级字段、28 站顺序与 9/12/7 分段、字段完整性、贴图 key（`globe_*` / `star_*` / `gal_*`）、单位、轨道字段、重力比与 SPEC 表一致、每条 leg 与「半长轴差 / 径向差」规则独立重算一致、累计单调、`segment()`/`legInfo()`/`legDistance()`/`cumulative()`/`indexOf()`/`byId()`/`stageOf()`/`launchSpeedKms()`/`fmtNumber()`/`fmtDistance()` 返回值、成就 id/挂载关系、虚拟地球站。

---

## 4. 关键数值表（28 段）

> 由模块实际运行输出；`legDistanceKm` 列对 solar 段用 km 计数，对 stellar/cosmic 段给科学计数法（量级 1e13–1e23）。

| # | 起点 → 终点 | 单位 | legDistanceKm | legDistanceLy | legDistanceLabel | 累计航程 |
|---|---|---|---|---|---|---|
| 1 | 地球 → 月球 | km | 38.44 万 km | 4.063111e-8 | 38.44 万 km | 38.44 万 km |
| 2 | 月球 → 水星 | km | 9168.88 万 km | 9.691517e-6 | 9168.88 万 km | 9207.32 万 km |
| 3 | 水星 → 金星 | km | 5029.99 万 km | 5.316703e-6 | 5029.99 万 km | 1.42 亿 km |
| 4 | 金星 → 火星 | km | 1.20 亿 km | 1.265549e-5 | 1.2 亿 km | 2.62 亿 km |
| 5 | 火星 → 木星 | km | 5.51 亿 km | 5.820143e-5 | 5.51 亿 km | 8.13 亿 km |
| 6 | 木星 → 土星 | km | 6.55 亿 km | 6.923032e-5 | 6.55 亿 km | 14.68 亿 km |
| 7 | 土星 → 天王星 | km | 14.41 亿 km | 1.523662e-4 | 14.41 亿 km | 29.09 亿 km |
| 8 | 天王星 → 海王星 | km | 16.29 亿 km | 1.722235e-4 | 16.29 亿 km | 45.39 亿 km |
| 9 | 海王星 → 冥王星 | km | 14.02 亿 km | 1.481948e-4 | 14.02 亿 km | 59.41 亿 km |
| 10 | 冥王星 → 半人马座α | ly | 4.129013e+13 | 4.364370 | 4.36 光年 | 4.36 光年 |
| 11 | 半人马座α → 巴纳德星 | ly | 1.511825e+13 | 1.598000 | 1.60 光年 | 5.96 光年 |
| 12 | 巴纳德星 → 沃尔夫359 | ly | 1.790916e+13 | 1.893000 | 1.89 光年 | 7.86 光年 |
| 13 | 沃尔夫359 → 天狼星 | ly | 7.048244e+12 | 0.745000 | 0.75 光年 | 8.60 光年 |
| 14 | 天狼星 → 波江座ε | ly | 1.772941e+13 | 1.874000 | 1.87 光年 | 10.47 光年 |
| 15 | 波江座ε → 南河三 | ly | 9.337741e+12 | 0.987000 | 0.99 光年 | 11.46 光年 |
| 16 | 南河三 → 天仓五 | ly | 4.257329e+12 | 0.450000 | 0.45 光年 | 11.91 光年 |
| 17 | 天仓五 → 牛郎星 | ly | 4.558180e+13 | 4.818000 | 4.82 光年 | 16.73 光年 |
| 18 | 牛郎星 → 织女星 | ly | 7.861867e+13 | 8.310000 | 8.31 光年 | 25.04 光年 |
| 19 | 织女星 → 大角星 | ly | 1.103121e+14 | 11.660000 | 11.66 光年 | 36.70 光年 |
| 20 | 大角星 → 银河系中心 | ly | 2.456318e+17 | 25963.300000 | 2.6 万光年 | 2.6 万光年 |
| 21 | 银河系中心 → 银河系边缘 | ly | 2.270575e+17 | 24000.000000 | 2.4 万光年 | 5 万光年 |
| 22 | 银河系边缘 → 大麦哲伦云 | ly | 1.069063e+18 | 113000.000000 | 11.3 万光年 | 16.3 万光年 |
| 23 | 大麦哲伦云 → 小麦哲伦云 | ly | 3.500470e+17 | 37000.000000 | 3.7 万光年 | 20 万光年 |
| 24 | 小麦哲伦云 → 仙女座星系 | ly | 2.210973e+19 | 2337000.000000 | 233.7 万光年 | 253.7 万光年 |
| 25 | 仙女座星系 → 三角座星系 | ly | 1.825921e+18 | 193000.000000 | 19.3 万光年 | 273 万光年 |
| 26 | 三角座星系 → 室女座星系团 | ly | 4.831595e+20 | 51070000.000000 | 5107 万光年 | 5380 万光年 |
| 27 | 室女座星系团 → 后发座星系团 | ly | 2.527907e+21 | 267200000.000000 | 2.67 亿光年 | 3.21 亿光年 |
| 28 | 后发座星系团 → 可观测宇宙视界 | ly | 4.368871e+23 | 46179000000.000000 | 461.79 亿光年 | 465 亿光年 |

**汇总**

- 太阳系段累计：`5,940,587,328.57 km` = `59.41 亿 km`（= 39.710374 AU，含地月段）。
- 银河系段首段：`4.36437 ly`（从太阳系外缘 0.00063 ly 起算，标签 `4.36 光年`）。
- 银河系边缘累计：`49,999.999998 ly`（标签 `5 万光年`）。
- 终点累计：`46,500,000,000 ly` = **465 亿光年**（标签 `465 亿光年`）。

### 4.1 站点重力比与起跳基础速度（`launchSpeedKms = 11.186 × 重力比`）

| # | id | 中文名 | kind | 重力比 | 起跳速度 km/s | 轨道半长轴 / 距太阳 |
|---|---|---|---|---|---|---|
| 1 | `moon` | 月球 | moon | 0.165 | 1.85 | 1.000000 AU |
| 2 | `mercury` | 水星 | planet | 0.378 | 4.23 | 0.387098 AU |
| 3 | `venus` | 金星 | planet | 0.907 | 10.15 | 0.723332 AU |
| 4 | `mars` | 火星 | planet | 0.379 | 4.24 | 1.523679 AU |
| 5 | `jupiter` | 木星 | planet | 2.528 | 28.28 | 5.204400 AU |
| 6 | `saturn` | 土星 | planet | 1.065 | 11.91 | 9.582600 AU |
| 7 | `uranus` | 天王星 | planet | 0.886 | 9.91 | 19.218400 AU |
| 8 | `neptune` | 海王星 | planet | 1.140 | 12.75 | 30.110000 AU |
| 9 | `pluto` | 冥王星 | dwarf | 0.063 | 0.70 | 39.482000 AU |
| 10–21 | stellar ×12 | — | star/system/cluster/edge | 1.0（无固体表面） | 11.19 | 4.365–50,000 ly |
| 22–28 | cosmic ×7 | — | galaxy/cluster/edge | 1.0（无固体表面） | 11.19 | 163,000–46,500,000,000 ly |

---

## 5. 与 SPEC 的一致性 / 偏差记录

| 项 | 结论 |
|---|---|
| 站数 | SPEC 4.3 旧标题「26」与三组清单（9+12+7=28）、第 10 节验收矛盾；已与 Lead 确认按 **28** 实现，Lead 已把 SPEC 更新为 28（本次核对 SPEC 第 78 行已是 28 站）|
| 太阳系顺序 | 月球 → 水星 → 金星 → 火星 → 木星 → 土星 → 天王星 → 海王星 → 冥王星 ✔ |
| 轨道半长轴 | 9 个值与 SPEC 4.3 完全一致（`selftest` 逐项核对）✔ |
| 重力比 | 9 个值与 SPEC 4.3 完全一致（`selftest` 逐项核对）✔ |
| 银河系 12 站距离 | 与 SPEC 4.3 完全一致 ✔ |
| 宇宙 7 站距离 | 与 SPEC 4.3 完全一致 ✔ |
| 贴图 key | solar `globe_*`；stellar `star_<id>`；cosmic `gal_lmc/gal_smc/gal_andromeda/gal_triangulum/gal_virgo/gal_coma/gal_horizon`（最后一站 id 是 `observable_edge`，贴图 key 仍是 `gal_horizon`，与 Lead/engine 的命名约定对齐）✔ |
| `moon.firstLegKm` | 384,400 ✔ |
| 地球不在 STOPS | ✔（虚拟地球 `A.EARTH`；`A.segment(0).from` 返回 `{id:'earth', name:'地球'}`）|
| 成就 id | SPEC 4.4 要求的 10 条全在；另加 engine.js 已引用的 `a_ufo10`，共 11 条 ✔ |
| 偏差 1 | `alpha_cen` 的累计航程标签显示 `4.36 光年`（=`4.364998 ly` 的 2 位小数），而该站径向距离 `orbitalLY = 4.365`。两者分别是「路径长度」与「径向距离」，`docs/astronomy-notes.md` §7 已说明。|
| 偏差 2 | 气态/冰巨星重力比以 SPEC 值为准；NASA Fact Sheet 的赤道重力因参考面/自转效应与 SPEC 采用值略有出入（如木星 23.1 vs 24.79 m/s²），说明文档里已注明口径。|
| 偏差 3 | 无固体表面天体（恒星/星系/星系团/视界）重力比按契约统一取 1.0；`radiusKm` 对星系给近似物理尺度、对星系团/视界给 0（不适用），这些字段只作展示，渲染层不应当碰撞半径用。|

---

## 6. 给 Lead / engine 的集成提示

1. **id 已锁定**（engine.js 已按此实现，`selftest` 也覆盖）：
   - solar：`moon mercury venus mars jupiter saturn uranus neptune pluto`
   - stellar：`alpha_cen barnard wolf359 sirius eps_eri procyon tau_cet altair vega arcturus galactic_center galactic_edge`
   - cosmic：`lmc smc andromeda triangulum virgo coma observable_edge`
2. `A.STOPS` / `A.SEGMENTS` 长度都是 28，engine 遍历即可，不要硬编码。
3. 每站 `legDistanceKm` / `legDistanceLy` 都是**数值型且非空**（cosmic 段 `legDistanceKm` 约 1e23，仅用于显示/换算；精确值请用 ly 字段，见 `docs/astronomy-notes.md` §7.6）。engine.js `getLeg()` 的兜底逻辑（`typeof to.legDistanceKm === 'number'`）不会触发，直接走模块字段。
4. `A.legInfo(i)` 返回 `{index, from, to, unit, km, ly, label}` 以及 UI 可用的 `fromId/toId/fromName/toName/stage/stageName/totalLabel/launchSpeedKms/isFirst/isLast/indexInStage/isStageChange/distanceNote` 等。
5. `A.byId('earth')` 按契约返回 `null`；要地球对象用 `A.EARTH`（虚拟站，不参与 STOPS 计数/成就）。
6. `A.segment(0).from` 是虚拟地球站对象；`A.legDistance(null 或 'earth', stop)` 等价于「从地球出发」。
7. **发现但不属于我作用域的问题**（提醒，不改 engine.js）：`engine.js` 中 `finishLeg()` 里 `S.best = leg.km` 会混用单位——solar 段是 km，cosmic 段 `leg.km` 是 `4.4e23`（ly 换算来的），`best` 会变成天文数字；建议改用 `leg.real`（unit-aware）或分单位记录。`engine.js` 的 `fmtDist()` 已有 ly 分支，`G.best` 显示时注意不要拿 km 值走 km 分支。
8. 距离标签已经按游戏口径预计算（`38.44 万 km` / `1.60 光年` / `233.7 万光年` / `465 亿光年`），UI 优先用 `stop.legDistanceLabel` / `stop.totalDistanceLabel`，不要二次格式化。

---

## 7. 备注

- 数据的物理依据、公式、来源 URL、局限说明见 `docs/astronomy-notes.md`。
- 自检脚本未写入仓库（验证用临时文件）；交付物只有 §1 列出的三个文件。
- 如需调整站数/顺序，只需改 `src/astronomy.js` 的 `DATA` 数组与 `selftest()` 里的 `EXPECTED`/`EXP_*` 常量，其余计算与标签会自动重算。
