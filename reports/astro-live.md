# v4 实时太阳系天文数据 · 交付报告（astro-live）

> 项目：肥鱼跳宇宙 · 星尘远航 v4（`C:\Users\admin\Desktop\FatFish-Playable`）
> 任务：共享任务 `task-1` —— 按 `docs/SPEC-v4.md` 第 3 节实现实时太阳系位置 API
> 负责人：teammate `astro-live`
> 日期：2026-11-18
> 状态：**已完成**（`A.selftest() = []`，`node build/check-astro.js` 退出码 0；`index.html` 需 Lead 重新构建后生效）

---

## 1. 结论摘要

| 验收项 | 结果 |
|---|---|
| `A.selftest()` | **`[]`（0 个错误）** |
| `node build\check-astro.js` | **通过 221 项 / 失败 0 项，退出码 0** |
| 2026-11-18T00:00:00Z 行星黄经 vs JPL 参考 | 最大误差 **0.0738°（土星）** ≤ 0.1° ✅ |
| 2026-11-18T00:00:00Z 日心距 vs JPL 参考 | 最大相对误差 **0.0416%（木星）** ≤ 0.3% ✅ |
| 2020–2035 全区间（64 时刻 × 9 行星） | 最大黄经误差 **0.0741°**、最大日心距误差 **0.1875%** ✅ |
| 实时太阳系总里程（2026-11-18） | **14,024,055,480.791 km = 93.745021 AU**（> 0） |
| 总里程随时间变化 | 2032-01-01 = 14,606,926,790.613 km；差 **582,871,309.823 km（4.156%）** ✅ |
| v3 兼容 | v3 全部导出保留；`A.STOPS[*].legDistanceKm` 等静态字段未改，v3 自检项全过 ✅ |
| 恒星去同质化数据 | 10 颗恒星站补 `spectral` / `teffK`，值可断言的表写入源码与 docs ✅ |

---

## 2. 改动文件（均在本人写作用域内）

| 文件 | 改动 |
|---|---|
| `src/astronomy.js` | 新增 v4 实时行星位置段（JPL J2000 根数表 + 开普勒求解 + 缓存）；新增 7 个 API 与 `PLANET_IDS/PLANET_ELEMENTS/LIVE_REFERENCE/EARTH_MOON_KM` 导出；10 颗恒星站补 `spectral/teffK`；`selftest()` 增加 v4 断言；`A.VERSION` 1.0.0 → 1.1.0；头部注释补 v4 契约。v3 代码与数据未删改。 |
| `build/check-astro.js` | 重写为带断言的 node 自检：v3 基础 28 站 + v4 API + 2026-11-18 参考对照表 + 9 段实时里程 + 日期变化 + 恒星光谱表；任一断言失败退出码 1。用 `new Function(src + 'return A;')()` 载入模块（避免 strict 模式下 `eval` 拿不到 `var A`）。 |
| `docs/astronomy-notes.md` | 追加 **§10「v4 实时行星位置」**（10.1 动机与改动边界、10.2 算法、10.3 UTC→TT、10.4 根数表与来源复核、10.5 参考值与精度校验、10.6 实测算例、10.7 恒星光谱型/有效温度、10.8 复现与自检、10.9 已知限制）；更新文件头与 §9 自检覆盖说明。 |
| `reports/astro-live.md` | 本报告。 |

**未改动**：`src/engine.js`、`src/render.js`、`src/ui.js`、`src/index.template.html`、`index.html`、`build/build.py`、`assets/**`（Lead/其他 teammate 作用域）。**未运行** `build/build.py`。

---

## 3. 交付 API 清单（ES5，无 DOM，浏览器 `<script>` 与 node 均可执行）

```js
// 单行星状态：JPL "Keplerian Elements for Approximate Positions of the Major Planets"
// J2000 根数 + 世纪变率 → 日心黄道 J2000 直角坐标（AU，太阳在原点）
A.planetState(id, ms)
// → { id, x, y, z, rAU, lonDeg, latDeg, ms } | null
//   id: 'mercury'|'venus'|'earth'|'mars'|'jupiter'|'saturn'|'uranus'|'neptune'|'pluto'
//   lonDeg 已归一化到 0..360；latDeg ∈ [-90, 90]；rAU = √(x²+y²+z²)

A.solarPositions(ms)
// → { earth:{...}, mercury:{...}, venus:{...}, mars:{...}, jupiter:{...}, saturn:{...},
//     uranus:{...}, neptune:{...}, pluto:{...}, sun:{x:0,y:0,z:0}, _ms, _iso }

A.liveLegKm(fromId, toId, ms)     // → 数值 km；'moon' 按地球位置处理；未知 id → null
A.liveSolarLeg(index, ms)        // index = A.STOPS 下标 0..8
// → { index, fromId, toId, km, au, fixed, note } | null
//   index 0：地球→月球固定 384,400 km，fixed:true；其余 8 段为实时三维弦长，fixed:false

A.liveSolarRoute(ms)
// → { legs:[liveSolarLeg×9], totalKm, totalAU, ms, iso }

A.formatUTC(ms)                   // → 'YYYY-MM-DD HH:mm:ss UTC'
A.nowMs()                         // → Date.now()；外部可覆盖（QA 固定时钟）
```

附带导出（供 QA/文档/引擎核对）：`A.PLANET_IDS`（9 项，含 earth）、`A.PLANET_ELEMENTS`（根数表）、`A.LIVE_REFERENCE`（固定时刻参考值与 J2000 参考值/来源说明）、`A.EARTH_MOON_KM = 384400`。

实现要点：
- 同一 `ms` 结果幂等：内部按**精确 ms** 缓存 9 颗行星位置；`planetState` 每次返回副本。
- 时间系统：`ms` 视为 UTC，`JDE = ms/86400000 + 2440587.5 + 69.184/86400`（TT−UTC=69.184 s，2017–2035 无闰秒假设，对水星黄经影响 0.003°）。
- 开普勒方程牛顿迭代，初值 `E₀ = M + e·sinM`，阈值 `1e-13 rad`。
- 根数表来源与数值见 `docs/astronomy-notes.md` §10.4（JPL SSD Table 1 / Standish 8.10.2，1800–2050，J2000 历元；Earth 行是地月质心 EMBary）。

---

## 4. 实测：2026-11-18T00:00:00Z 的 9 段距离与总里程

`ms = Date.UTC(2026, 10, 18, 0, 0, 0) = 1794960000000`，由 `A.liveSolarRoute(ms)` 实际运行输出：

| # | 航段 | km | AU | 类型 |
|---|---|---|---|---|
| 0 | 地球 → 月球 | 384,400.000 | 0.002570 | 固定 384,400 km |
| 1 | 月球（按地球位置）→ 水星 | 138,147,450.365 | 0.923459 | 实时弦长 |
| 2 | 水星 → 金星 | 88,708,400.443 | 0.592979 | 实时弦长 |
| 3 | 金星 → 火星 | 170,059,886.454 | 1.136780 | 实时弦长 |
| 4 | 火星 → 木星 | 590,106,005.504 | 3.944615 | 实时弦长 |
| 5 | 木星 → 土星 | 1,955,309,080.229 | 13.070434 | 实时弦长 |
| 6 | 土星 → 天王星 | 2,290,449,322.072 | 15.310708 | 实时弦长 |
| 7 | 天王星 → 海王星 | 3,942,367,970.519 | 26.353102 | 实时弦长 |
| 8 | 海王星 → 冥王星 | 4,848,522,965.206 | 32.410374 | 实时弦长 |
| — | **totalKm / totalAU** | **14,024,055,480.791** | **93.745021** | `A.liveSolarRoute` |

- QA 固定时刻 `?live=1`（引擎把时钟固定为 **2026-11-18T12:00:00Z**）：`totalKm = 14,026,385,403.788 km`、`totalAU = 93.760595`；9 段分别为 384,400 / 140,106,177.856 / 90,351,818.823 / 169,186,876.460 / 589,582,641.331 / 1,955,497,548.487 / 2,290,166,459.554 / 3,942,498,843.929 / 4,848,610,637.348 km。
- 对比 2032-01-01T00:00:00Z：`totalKm = 14,606,926,790.613 km`（97.641275 AU），差 `582,871,309.823 km`（4.156%）。自检断言「差 > 1 亿 km 且相对差 > 0.5%」。
- 逐年（每年 11-18T00:00:00Z）totalKm 在 14.02e9–15.15e9 km 间变化，明细表见 `docs/astronomy-notes.md` §10.6。
- 与 v3 静态规则对照：v3 太阳系段合计 5,940,587,328.57 km（39.710374 AU）——两者物理含义不同（半长轴差 vs 当前三维弦长），v3 字段仅作离线基准，未改动。

---

## 5. 与 JPL 参考值的误差（2026-11-18T00:00:00Z）

参考值来源：**JPL DE421 开发星历**本地计算（`skyfield` + `de421.bsp`，黄道 J2000 旋转；地球取地月质心）。详细说明见 §7。

| 行星 | 实算黄经 | 参考黄经 | Δ黄经 | 实算日心距 AU | 参考日心距 AU | Δ日心距 |
|---|---|---|---|---|---|---|
| 水星 | 124.127905° | 124.133216° | −0.0053° | 0.324928364 | 0.324934404 | −0.0019% |
| 金星 | 70.228433° | 70.228494° | −0.0001° | 0.720967561 | 0.720974740 | −0.0010% |
| 地球 | 55.278185° | 55.279642° | −0.0015° | 0.988624070 | 0.988644467 | −0.0021% |
| 火星 | 108.431500° | 108.434740° | −0.0032° | 1.611684186 | 1.611760214 | −0.0047% |
| 木星 | 134.970759° | 134.946366° | +0.0244° | 5.320052637 | 5.322264581 | −0.0416% |
| 土星 | 12.519409° | 12.445633° | **+0.0738°** | 9.420551669 | 9.420066385 | +0.0052% |
| 天王星 | 63.202356° | 63.202403° | −0.00005° | 19.427344046 | 19.432564342 | −0.0269% |
| 海王星 | 2.930254° | 2.938974° | −0.0087° | 29.876535141 | 29.876918202 | −0.0013% |
| 冥王星 | 304.417282° | 304.423460° | −0.0062° | 35.647631248 | 35.643600231 | +0.0113% |

- 最大黄经误差 **0.0738°（土星）**、最大日心距误差 **0.0416%（木星）**，均在 SPEC 容差（0.1° / 0.3%）内。
- 2020–2035 每季度采样（64 个时刻）全区间最大：黄经 **0.0741°（土星）**、日心距 **0.1875%（土星）**，同样达标（明细表见 docs §10.5）。
- J2000 历元一致性：`A.planetState('earth', 2000-01-01T12:00:00Z)` 黄经 100.38100° / r 0.98330742 AU；DE421 地月质心 100.380172° / 0.983309967 AU，差 0.0008° / 2.6e-6。
- 交叉验证：用独立实现 `astronomy-engine`（VSOP87）在 2026-11-18 计算同一组位置，与 DE421 参考值相差 ≤ 0.005°，说明参考值与坐标系旋转正确（误差来自 JPL 近似根数本身，而非实现 bug）。

---

## 6. 恒星站 `spectral` / `teffK`

| 站点 | spectral | teffK | 站点 | spectral | teffK |
|---|---|---|---|---|---|
| `alpha_cen` | G2V | 5790 | `procyon` | F5IV | 6530 |
| `barnard` | M4V | 3190 | `tau_cet` | G8V | 5344 |
| `wolf359` | M6V | 2800 | `altair` | A7V | 7550 |
| `sirius` | A1V | 9940 | `vega` | A0V | 9600 |
| `eps_eri` | K2V | 5084 | `arcturus` | K1.5III | 4286 |

来源：SIMBAD（<http://simbad.u-strasbg.fr/simbad/>）与 Wikipedia 各星条目；有效温度取常用文献值（±几十 K 差异属文献口径，游戏只用于配色/贴图选择，不参与轨道与航段计算）。`A.selftest()` 断言值与 MKK 格式正则 `^[OBAFGKM][0-9](\.[0-9])?(III|II|IV|I|V)$`。

---

## 7. 参考值取数说明（Horizons 不可达与退化方案）

任务书要求「参考值必须真的去取：可用 web 工具或 PowerShell 调 Horizons API；若网络取不到，改用 JPL 表中算法在 J2000 历元的一致性 + 公开近似值做断言，并在报告里说明」。本机的实际情况：

1. **Horizons API 直连失败**：`ssd.jpl.nasa.gov`（137.78.251.144:443）TCP 连接超时（`curl` 21 s → HTTP 000；`Invoke-WebRequest` 同样超时），不是 DNS 问题。
2. **公共代理也失败**：`api.allorigins.win` 返回 522（其边缘节点也连不上 JPL origin）、`api.cors.lol` 返回 429、`api.codetabs.com` 超时；`web.archive.org`、`r.jina.ai` 在本机同样不可达。
3. **可达的 JPL 同源数据**：
   - JPL 根数表原文件的公开镜像（ASU）成功取回并逐字核对：`http://oss.mars.asu.edu/svn/krc/tags/archive_2011_10_14/run/standish.tab`（= Standish Table 8.10.2 = `p_elem_t1.txt`，文件头注明"Also at: http://ssd.jpl.nasa.gov/txt/p_elem_t1.txt"）。
   - 通过 PyPI 清华镜像安装 `skyfield` + `skyfield-data`（后者自带 **JPL DE421** `de421.bsp`），在本机计算任意时刻的日心黄道 J2000 位置。DE421 与 Horizons 服务端常见 DE440/441 属同一 JPL 星历族，2020–2035 对这些行星的差异在亚角秒量级。
4. **结论**：参考值取 JPL DE421 本地计算值，并在 `A.LIVE_REFERENCE`、`A.selftest()` 与 docs 中注明来源；同时保留「J2000 历元一致性」断言（`A.LIVE_REFERENCE.j2000`）。若后续网络可访问 Horizons，用 docs §10.5 的 URL 模板刷新 `LIVE_REFERENCE` 并重跑 `check-astro.js` 即可，代码无需改动。

参考值计算脚本（本地临时脚本，未进仓库）核心逻辑：
```python
import skyfield_data, os
from skyfield.api import load
ts = load.timescale()
eph = load(os.path.join(skyfield_data.get_skyfield_data_path(), 'de421.bsp'))
t = ts.utc(2026, 11, 18, 0, 0, 0)
body = eph['mars']              # 行星用 '* barycenter'，地球用 'earth barycenter'（与根数表 EMBary 对齐）
x, y, z = (body - eph['sun']).at(t).position.au
# 再用 J2000 平黄赤交角 23.4392911° 旋转到黄道，得到 lon/rAU（与 A.planetState 同坐标系）
```

---

## 8. 验收命令与输出（本人已跑通）

```powershell
$node = 'C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe'
& $node build\check-astro.js
```

实际输出（节选）：

```text
== v3 基础数据 ==
== v4 实时太阳系 API ==
== 固定时刻 2026-11-18T00:00:00Z 对 JPL 参考值（...）
  planet     lonDeg(算)  lonDeg(参考)   Δlon°      rAU(算)      rAU(参考)    Δr%
  mercury     124.127905    124.133216  -0.005311   0.324928364   0.324934404  -0.00186
  venus        70.228433     70.228494  -0.000061   0.720967561   0.720974740  -0.00100
  earth        55.278185     55.279642  -0.001457   0.988624070   0.988644467  -0.00206
  mars        108.431500    108.434740  -0.003240   1.611684186   1.611760214  -0.00472
  jupiter     134.970759    134.946366   0.024393   5.320052637   5.322264581  -0.04156
  saturn       12.519409     12.445633   0.073776   9.420551669   9.420066385   0.00515
  uranus       63.202356     63.202403  -0.000047  19.427344046  19.432564342  -0.02686
  neptune       2.930254      2.938974  -0.008720  29.876535141  29.876918202  -0.00128
  pluto       304.417282    304.423460  -0.006178  35.647631248  35.643600231   0.01131
  最大黄经误差：0.07378°（saturn）；最大日心距误差：0.04156%（jupiter）
  J2000 历元地球：lon 100.38100°（参考 100.380172°），r 0.98330742 AU（参考 0.983309967 AU）
...
== 实时太阳系 9 段（2026-11-18 00:00:00 UTC） ==
  [0] earth→moon                     384400.0 km      0.002570 AU  (fixed)
  [1] moon→mercury                138147450.4 km      0.923459 AU
  ...
  [8] neptune→pluto              4848522965.2 km     32.410374 AU
== 实时总里程与日期变化 ==
  2026-11-18：totalKm = 14024055480.791 km（93.745021 AU）
  2032-01-01：totalKm = 14606926790.613 km（97.641275 AU）
  差值 = 582871309.823 km（4.156%）
== 总结 ==
  通过 221 项，失败 0 项
  OK：src/astronomy.js v4 自检全部通过
```

模块级自检：

```powershell
& $node -e "var fs=require('fs');var A=new Function(fs.readFileSync('src/astronomy.js','utf8')+'\nreturn A;')(); console.log(JSON.stringify(A.selftest()));"
# 输出：[]
```

---

## 9. 给 Lead / QA 的集成说明

- 我只改了自己的 4 个文件，**没有动** engine/render/ui、`build/build.py`、`index.html`、assets；也**没有运行** `build/build.py`。`index.html` 仍是旧构建产物，需要 Lead 重新 build 后实时 API 才会进游戏。
- 引擎侧（已存在，无需我改）：`engine.js` 的 `buildSolarNow()` 已经在调 `A.solarPositions/liveSolarLeg/liveSolarRoute`，`render.js` 的 `solarMapPositions()` 用 `pos[id].lonDeg`，`ui.js` 读 `leg.live/fixed/obsIso`；字段与我的返回结构一致。
- 建议 QA 断言：
  - `?live=1` 时 `__FATFISH__.liveInfo()` 的 `totalKm ≈ 14,026,385,403.788`、`totalAU ≈ 93.760595`、`iso === '2026-11-18 12:00:00 UTC'`；
  - 太阳系地图上各行星黄经与 `A.solarPositions(Date.UTC(2026,10,18,12))[id].lonDeg` 一致（`state().live.planets`）；
  - 不同固定时刻（如再加一个 `?time=2032-01-01T00:00:00Z`）总里程明显不同（14.02e9 vs 14.61e9 km）。
- 注意 `?live=1` 的固定时刻是 **2026-11-18T12:00:00Z**（engine 里写死），不是自检用的 00:00，两者数值都已在本报告给出，避免对不上。

---

## 10. 风险 / 未完成项

1. **Horizons 直采未完成**（网络阻断）：参考值改用 JPL DE421 本地星历，已做 2020–2035 全区间校验与独立 VSOP87 交叉验证；如网络恢复，可用 docs §10.5 的模板刷新参考值，属小工作量。
2. **土星/木星误差接近容差上限**：0.074° / 0.024°（2026-11-18），全区间土星最大 0.0741°。这是 JPL 近似根数法固有精度，SPEC 容差 0.1° 内但余量不大；若未来要求更准需换 VSOP87 或完整 DE 星历（体积/性能代价大，不在本任务范围）。
3. **`index.html` 未重建**：按作用域要求未跑 build.py；集成后需 Lead/QA 重跑 `?live=1` 场景确认渲染层读数。
4. **月球段仍为固定值**：按 SPEC 规定不做实时地月距离；若 QA 期待 `liveLegKm('earth','moon') = 384400` 需注意契约原文是「'moon' 按地球位置处理」，本实现按字面返回 **0 km**（固定 384,400 只在 `liveSolarLeg(0)` / `liveSolarRoute.legs[0]` 中体现）。此点已在 docs §10.8/§10.9 写明。
5. **`A.nowMs` 被覆盖后的行为**：外部覆盖（QA 固定时钟）后，省略 `ms` 的实时 API 会跟随覆盖值；显式传 `ms` 时不受影响（engine 目前总是显式传）。selftest 在 `A.nowMs` 未被覆盖时才做系统时间比较，避免 QA 固定时钟导致自检假失败。
