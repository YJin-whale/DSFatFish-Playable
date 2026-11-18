# 天文数据说明 · `docs/astronomy-notes.md`

> 对应实现：`src/astronomy.js`（暴露全局 `A`）
> 对应规格：`docs/SPEC.md` 第 4 节（v3）；v4 增量见 `docs/SPEC-v4.md` 第 3 节
> 负责人：astro-data（v3 静态数据）；v4 实时行星位置由 astro-live 维护（见 §10）
> 目的：把 `A.STOPS` 里每一个距离、重力比、半径的**测算依据与来源**写清楚，并解释游戏所用「航段距离」规则的物理含义与局限。
> 验收记录：`reports/astro-live.md`；node 自检：`build/check-astro.js`

---

## 1. 基本常量与单位

| 常量 | 值 | 定义 / 来源 |
|---|---|---|
| 天文单位 `AU_KM` | 149,597,870.7 km | IAU 2012 年 B2 号决议定义 1 AU = 149,597,870,700 m（精确值）。<https://www.iau.org/static/resolutions/IAU2012_English.pdf> |
| 光年 `LY_KM` | 9,460,730,472,580.8 km | 1 儒略年（365.25 d）× 真空光速 299,792.458 km/s，即光在 1 儒略年内走过的距离。<https://science.nasa.gov/exoplanets/what-is-a-light-year/> |
| 地球标准重力 `EARTH_G` | 9.80665 m/s² | 标准重力加速度（ISO 80000-3 / CGPM 定义值），作为重力比的分母。 |
| 地球第二宇宙速度 `EARTH_ESCAPE_KMS` | 11.186 km/s | 地球表面逃逸速度，作为「起跳基础速度」的基准值（NASA Planetary Fact Sheet 取整 11.2 km/s）。<https://nssdc.gsfc.nasa.gov/planetary/factsheet/> |
| 太阳系外缘 `SOLAR_EDGE_LY` | 0.00063 ly ≈ 39.84 AU | 游戏设定的「太阳系出口」工程近似值（见 §2.4）。 |
| 秒差距换算 | 1 pc = 3.2615638 ly | 视差距离公式：`d[pc] = 1 / ϖ[″]`，`d[ly] = 3.2615638 / ϖ[″]`。 |

所有数值单位换算都只使用上述常量，`selftest()` 会核对常量本身以及每条航段与常量的一致性。

---

## 2. 航段距离规则：物理含义与局限

游戏需要在界面与「预演航线」上展示每段航程，但不需要（也不应该）做真实轨道积分。因此 SPEC 4.3 规定了一套**站点间隔**规则。它不是飞行器真实航迹，而是「两个天体在太阳系/银河系中的径向间隔」。三条规则如下：

### 2.1 地球 → 月球：384,400 km

地月平均距离（半长轴）为 384,400 km。月球轨道是椭圆，近地点约 363,300 km、远地点约 405,500 km，游戏取平均值。
来源：NASA Moon Fact Sheet <https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html>

### 2.2 太阳系其余站点：轨道半长轴之差

```
legKm = |orbitalAU(prev) − orbitalAU(cur)| × AU_KM
```

- 物理含义：两条**共面、近圆**轨道在「近日点方向对齐」时的径向间隔，也就是这两个轨道半径的差；可以理解为「从一条轨道跳到另一条轨道至少要跨过的径向距离」。
- 局限（写在这里，避免 UI 误导玩家）：
  1. **不包含相位角**：真实两颗行星的距离随各自公转相位变化，最近时约 `|a₂−a₁|`，最远时可达 `a₁+a₂`。例如地球与火星最近约 0.52 AU、最远约 2.52 AU，而游戏按站点顺序取的是「相邻站点半长轴差」，与真实会合无关。
  2. **不包含偏心率与倾角**：真实轨道是椭圆且有轨道倾角，最近距离要用轨道根数数值求解。
  3. **不是转移轨道长度**：真正从一条轨道飞到另一条轨道要走霍曼转移或更复杂的转移轨道。以地球→火星为例，霍曼转移沿半椭圆弧飞行，弧长约 3.9 AU，而两者的轨道半长轴之差只有 0.524 AU——**差了约 7.5 倍**。所以本作把 leg 当作「关卡进度距离」，不用于任何轨道力学计算。
  4. **月球之后还要「跳回内圈」**：按 SPEC 的顺序，月球（a≈1 AU）之后是水星（0.387 AU），再回到金星、火星……这是一条先向内、再向外的折线。因此太阳系段累计航程（5.9406e9 km，即 39.710374 AU）并不等于「地球到冥王星」的径向距离（38.482 AU），它更长，因为路线有折返。这是 SPEC 规定的顺序与规则导致的，不是计算错误。

轨道半长轴取自 NASA NSSDC Planetary Fact Sheet 的 `Distance from Sun`（该表注明该值即半长轴 mean distance / semi-major axis）：
<https://nssdc.gsfc.nasa.gov/planetary/factsheet/>（数值与 SPEC 4.3 给定值一致，见 §3 表）

### 2.3 银河系 / 可观测宇宙段：径向距离差

```
legLy = |orbitalLY(prev) − orbitalLY(cur)|
legKm = legLy × LY_KM
```

- 物理含义：两个目标「到太阳的径向距离之差」。例如巴纳德星 5.963 ly、天狼星 8.601 ly，径向差 2.638 ly。
- 局限：**忽略天球方向角**。两个天体真实的直线距离是
  `d = √(d₁² + d₂² − 2·d₁·d₂·cos θ)`（θ 为两天体的角距离）。
  径向差 `|d₂−d₁|` 只是真实距离在「同一视线方向」上的下界；两颗星若在天球上相隔很远，真实距离会明显更大。本作没有为每站建三维坐标，故统一采用径向差。
- 这条规则有一个好性质：从太阳系外缘开始的径向差**逐段可望远镜求和**，累计到「可观测宇宙视界」时恰好等于 46.5 Gly（见 §2.4）。这也是 SPEC 选用它的原因：数值可核对、累计航程有明确终点。
- 首站从太阳系外缘 `0.00063 ly`（≈39.84 AU）起算，而不是从 0 起算：SPEC 4.3 规定「银河系段从太阳/太阳系外缘 0.00063 ly 起算」。这个值略大于冥王星轨道远日距的一半、约等于轨道半长轴 39.48 AU 的量级，是「离开太阳系」的合理近似。

### 2.4 累计航程与终点

- solar 段按 km 累加，stellar/cosmic 段按 ly 累加；跨段时用 `LY_KM` 换算，避免 `1e23 km` 级别的大数反复相加造成精度损耗。
- 太阳系段总长：**5,940,587,328.57 km ≈ 59.41 亿 km**。其中「轨道半长轴差」部分合计 39.707804 AU（5,940,202,928.6 km），加上地月段 384,400 km（≈0.00257 AU），合计 39.710374 AU。
- 银河系段总长：50,000 − 0.00063 ≈ **49,999.99937 ly**（从太阳系外缘到银河系边缘）。
- 宇宙段总长：46,500,000,000 − 50,000 = **46,499,950,000 ly**。
- 终点累计：`太阳段(0.00062792 ly) + 49,999.99937 + 46,499,950,000 ≈ 46,500,000,000 ly`，即 **465 亿光年**，界面显示 `465 亿光年`。`selftest()` 会校验终点累计与 465 亿光年的误差 < 1e-9（相对）。

---

## 3. 太阳系 9 站

| # | id | 中文名 | 轨道半长轴（AU） | 重力比 | 表面重力（约） | 航段（按规则） |
|---|---|---|---|---|---|---|
| 1 | `moon` | 月球 | 1.000000（随地球） | 0.165 | 1.62 m/s² | 地月平均 384,400 km |
| 2 | `mercury` | 水星 | 0.387098 | 0.378 | 3.71 m/s² | \|0.387098−1.000000\| AU |
| 3 | `venus` | 金星 | 0.723332 | 0.907 | 8.90 m/s² | \|0.723332−0.387098\| AU |
| 4 | `mars` | 火星 | 1.523679 | 0.379 | 3.72 m/s² | \|1.523679−0.723332\| AU |
| 5 | `jupiter` | 木星 | 5.2044 | 2.528 | 24.79 m/s²（1 bar） | \|5.2044−1.523679\| AU |
| 6 | `saturn` | 土星 | 9.5826 | 1.065 | 10.44 m/s²（1 bar） | \|9.5826−5.2044\| AU |
| 7 | `uranus` | 天王星 | 19.2184 | 0.886 | 8.69 m/s²（1 bar） | \|19.2184−9.5826\| AU |
| 8 | `neptune` | 海王星 | 30.11 | 1.140 | 11.18 m/s²（1 bar） | \|30.11−19.2184\| AU |
| 9 | `pluto` | 冥王星 | 39.482 | 0.063 | 0.62 m/s² | \|39.482−30.11\| AU |

- **来源**：NASA NSSDCA Planetary Fact Sheet（Metric）<https://nssdc.gsfc.nasa.gov/planetary/factsheet/>；月球另见 NASA Moon Fact Sheet <https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html>。数值与 SPEC 4.3 完全一致。
- **重力比口径**：`gravityRatio = 表面重力 ÷ 9.80665`。气态/冰巨星的「表面」取 1 bar 气压参考面，这类数值在不同资料里会因参考面、自转离心效应不同而略有差异（例如 NASA Fact Sheet 的木星取 23.1 m/s²，而常用参考值 1 bar 层为 24.79 m/s²）。**本项目以 SPEC 4.3 给定的重力比为准**（它对应 24.79 / 10.44 / 8.69 / 11.18 m/s² 这一组常用值），说明文字只做近似解释，不参与计算。
- 冥王星在 2006 年被 IAU 重新定义为矮行星，`kind` 记为 `dwarf`；月球 `kind` 为 `moon`，其余为 `planet`。

---

## 4. 银河系 12 站（视差距离）

**测距方法**：这些目标都在几百光年内，主要靠**三角视差**——地球绕太阳运动使恒星在天球上画出小椭圆，测出视差角 ϖ（角秒）后 `d[pc] = 1/ϖ`，再乘 3.2615638 得到光年数。依巴谷（Hipparcos）与盖亚（Gaia）任务的星表是主要数据来源；Gaia DR3 对近邻亮星的视差精度可达零点几到几毫角秒，相应距离误差在 0.01–0.1 光年量级。

| # | id | 中文名 | 距太阳（ly） | 航段（= 与上一站径向差，ly） | 说明 |
|---|---|---|---|---|---|
| 10 | `alpha_cen` | 半人马座α | 4.365 | 4.365 − 0.00063 = 4.36437 | 三合星系统；比邻星约 4.24 ly |
| 11 | `barnard` | 巴纳德星 | 5.963 | 1.598 | 红矮星，自行最快 |
| 12 | `wolf359` | 沃尔夫359 | 7.856 | 1.893 | 红矮星、耀星 |
| 13 | `sirius` | 天狼星 | 8.601 | 0.745 | 双星（A + 白矮星 B） |
| 14 | `eps_eri` | 波江座ε | 10.475 | 1.874 | 年轻类太阳恒星，有尘埃盘 |
| 15 | `procyon` | 南河三 | 11.462 | 0.987 | 双星（A + 白矮星 B） |
| 16 | `tau_cet` | 天仓五 | 11.912 | 0.450 | 类太阳恒星，有行星候选体 |
| 17 | `altair` | 牛郎星 | 16.73 | 4.818 | 自转极快、明显扁球 |
| 18 | `vega` | 织女星 | 25.04 | 8.310 | 曾是星等零点；未来极星 |
| 19 | `arcturus` | 大角星 | 36.7 | 11.660 | 橙红巨星，半径约 25 R☉ |
| 20 | `galactic_center` | 银河系中心 | 26000 | 25963.3 | 银心核球，含人马座 A* |
| 21 | `galactic_edge` | 银河系边缘 | 50000 | 24000 | 银盘半径约 15 kpc ≈ 5 万 ly |

- **来源**：SPEC 4.3 给定值（与 Hipparcos / Gaia / RECONS 等近邻星表一致）；Gaia 数据存档 <https://gea.esac.esa.int/archive/>，依巴谷任务 <https://www.cosmos.esa.int/web/hipparcos>，近邻星研究联盟 RECONS <http://www.recons.org/>。
- 半人马座α 的 4.365 ly 是 AB 双星系统的常用距离；比邻星（Proxima Centauri）约 4.24 ly。本作按 SPEC 采用 4.365。
- 银河系中心 26,000 ly 与银盘半径 50,000 ly 取常用近似值（银心约 8 kpc，银盘半径约 15 kpc），用于游戏尺度展示。来源：NASA Science Universe <https://science.nasa.gov/universe/overview/>。

---

## 5. 可观测宇宙 7 站

**测距方法简述**：
- 近邻星系（大/小麦哲伦云、仙女座、三角座）：造父变星周光关系、红巨星分支顶端（TRGB）、造父/天琴座 RR 星等标准烛光，以及 HST 观测的食双星等，交叉校准。
- 星系团（室女座、后发座）：成员星系的红移与团内速度弥散、面亮度涨落、Ia 型超新星校准，取哈勃常数换算成距离。
- 可观测宇宙视界：由宇宙学参数（Planck 2018）计算得到的**共动距离**（comoving distance），不是光在 138 亿年里走的直线距离——宇宙在膨胀，所以「可观测半径」约 46.5 Gly，大于宇宙年龄 × 光速。

| # | id | 中文名 | 距太阳（ly） | 航段（径向差，ly） | 来源 |
|---|---|---|---|---|---|
| 22 | `lmc` | 大麦哲伦云 | 163,000 | 113,000 | NASA/IPAC NED |
| 23 | `smc` | 小麦哲伦云 | 200,000 | 37,000 | NASA/IPAC NED |
| 24 | `andromeda` | 仙女座星系 | 2,537,000 | 2,337,000 | NASA/IPAC NED |
| 25 | `triangulum` | 三角座星系 | 2,730,000 | 193,000 | NASA/IPAC NED |
| 26 | `virgo` | 室女座星系团 | 53,800,000 | 51,070,000 | NASA/IPAC NED |
| 27 | `coma` | 后发座星系团 | 321,000,000 | 267,200,000 | NASA/IPAC NED |
| 28 | `observable_edge` | 可观测宇宙视界 | 46,500,000,000 | 46,179,000,000 | Planck 2018 / NASA Science |

- **来源**：NASA/IPAC Extragalactic Database（星系/星系团距离）<https://ned.ipac.caltech.edu/>；Planck 2018 results VI（宇宙学参数）<https://doi.org/10.1051/0004-6361/201833910>；NASA Science Universe Overview <https://science.nasa.gov/universe/overview/>。
- **46.5 Gly 的说明**：常用口径为「可观测宇宙半径约 465 亿光年」。Planck 2018 参数算出的共动半径在 46.1–46.5 Gly 之间（取决于参数集与计算口径），SPEC 4.3 取 46.5 Gly，本实现按 SPEC 采用 46.5。宇宙年龄约 138 亿年，两者差值来自空间膨胀。
- 大/小麦哲伦云、仙女座、三角座的距离都是「到太阳（银河系）的距离」，不是到银河系中心的距离——这与 `orbitalLY` 字段「距太阳距离」的定义一致。

---

## 6. 每条航段的最终数值

28 条航段的完整数值表、累计航程、起跳速度表见 `reports/astro-data.md`（由 `src/astronomy.js` 实际运行输出，未手工抄写）。这里只给校验结论：

- `A.STOPS.length = 28`（太阳系 9 + 银河系 12 + 宇宙 7）。
- `A.selftest() = []`。
- 太阳系段累计 `A.STOPS[8].totalDistanceKm ≈ 5.9406e9 km`（59.41 亿 km）。
- 终点 `A.STOPS[27].totalDistanceLy = 46,500,000,000 ly`（465 亿光年）。
- 银河系段首段 = `4.365 − 0.00063 = 4.36437 ly`。

---

## 7. 与 SPEC 的差异 / 取舍记录

1. **站数 26 → 28**：SPEC 4.3 旧标题写「共 26 站」，但同节三组清单（9 + 12 + 7）与第 10 节验收清单均为 28 站。已与 Lead 确认「26」是陈旧数字，SPEC 已更新为 28，本实现按 28 站。
2. **半人马座α 的累计数值显示 4.36 光年**：该站的 `orbitalLY = 4.365`，但 `totalDistanceLabel` 是「从地球出发的累计路径」= 太阳段(0.00062792 ly) + (4.365 − 0.00063) ≈ 4.364998 ly，按 2 位小数显示为 4.36。径向距离本身在 `orbitalLY` 字段里是 4.365，两者不是同一个量（路径长度 vs 径向距离），文档与 UI 说明里不要混用。
3. **气态/冰巨星重力比口径**：见 §3，取 SPEC 给定值，NASA Fact Sheet 的赤道重力因参考面不同略有出入。
4. **无固体表面天体的重力比**：恒星、星系、星系团、视界按契约统一取 `gravityRatio = 1.0`，`gravityNote` 注明「无固体表面」。真实恒星表面重力各不相同（如半人马座α A 约 20 g），但不参与游戏起跳计算。
5. **半径字段**：恒星/系统给真实平均半径；星系给近似盘面/有效半径（`radiusKm` 数量级 1e16–1e18 km）；星系团、银心、银边、视界没有单一「半径」，记为 0，并在 `gravityNote` 注明不适用。
6. **大数精度**：宇宙段 `legDistanceKm` 可达 4.4e23 km，超出 JS 安全整数范围（2^53 ≈ 9e15），只有 15–16 位有效数字，**仅用于显示/换算，不应用于精确比较**；需要精确值请用 ly 字段（都在 1e11 以内，double 可精确表示整数）。
7. **`radiusKm` 对渲染只作参考**：游戏渲染层不应把星系/星团半径当碰撞半径使用。

---

## 8. 参考来源清单

1. NASA NSSDCA, *Planetary Fact Sheet - Metric*：<https://nssdc.gsfc.nasa.gov/planetary/factsheet/>
2. NASA NSSDCA, *Planetary Fact Sheet Notes*（说明 Distance from Sun 即半长轴、Gravity 参考面等）：<https://nssdc.gsfc.nasa.gov/planetary/factsheet/planetfact_notes.html>
3. NASA NSSDCA, *Moon Fact Sheet*：<https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html>
4. IAU, *2012 Resolution B2*（AU 精确定义）：<https://www.iau.org/static/resolutions/IAU2012_English.pdf>
5. NASA Science, *What is a light-year?*：<https://science.nasa.gov/exoplanets/what-is-a-light-year/>
6. NASA Science, *Universe Overview*：<https://science.nasa.gov/universe/overview/>
7. ESA, *Gaia Archive*（天体测量视差）：<https://gea.esac.esa.int/archive/>
8. ESA, *Hipparcos*：<https://www.cosmos.esa.int/web/hipparcos>
9. RECONS（Research Consortium on Nearby Stars）：<http://www.recons.org/>
10. NASA/IPAC, *Extragalactic Database (NED)*：<https://ned.ipac.caltech.edu/>
11. Planck Collaboration, *Planck 2018 results VI: Cosmological parameters*, A&A 641, A6：<https://doi.org/10.1051/0004-6361/201833910>

---

## 9. 复现与校验

```powershell
# node 下 eval 模块并跑自检（HTML 里由构建脚本内联，不需要 node）
$node = "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe"
& $node -e "var fs=require('fs');eval(fs.readFileSync('src/astronomy.js','utf8'));console.log(A.STOPS.length, A.selftest());"
# 期望输出：28 []
```

`A.selftest()` 覆盖：常量、层级、28 站顺序与分段数量、字段完整性、贴图 key、单位、轨道字段、重力比、距离与「轨道半长轴差 / 径向差」规则的一致性、累计单调性、`segment()`/`legInfo()`/`legDistance()`/`cumulative()`/`indexOf()`/`byId()`/`stageOf()`/`launchSpeedKms()`/`fmtNumber()`/`fmtDistance()` 的返回值、成就 id 与站点挂载关系、虚拟地球站。v4 起还覆盖 §10 的实时行星 API（见 §10.8）。

---

## 10. v4 实时行星位置（`A.planetState` / `A.liveSolarRoute` 等）

> 契约：`docs/SPEC-v4.md` 第 3 节
> 实现：`src/astronomy.js` 的「v4 实时行星位置」段（`A.VERSION = '1.1.0'`）
> 自检：`A.selftest()`、`build/check-astro.js`；验收记录：`reports/astro-live.md`

### 10.1 为什么不再用「轨道半长轴之差」

v3 的太阳系航段距离 = `|a₂ − a₁| × AU_KM`（§2.2），物理含义是两条共面近圆轨道在「近日点方向对齐」时的径向间隔，**不含相位角**：真实两颗行星的距离随公转相位在 `|a₂−a₁|`（最近）到 `a₁+a₂`（最远）之间变化。例如地球与火星最近约 0.52 AU、最远约 2.52 AU，而 v3 固定取 0.524 AU，无法体现「今天火星在哪」。

v4 验收要求「行星按当前真实黄经摆放」「总里程随真实行星相对位置变化」（SPEC-v4 §1.1、§1.2、§10），所以太阳系 8 段改为**观测时刻两颗行星三维位置之间的弦长**：

```
legKm(t) = | r_from(t) − r_to(t) | × AU_KM
```

其中 `r(t)` 是行星在**日心黄道 J2000 直角坐标系**中的位置（AU，x 指向 J2000 春分点，z 指向黄北极）。第 0 段（地球→月球）仍是固定 384,400 km（`fixed:true`，月球位置按地球处理）；其余 8 段随观测时刻实时变化。

**改动边界**：`A.STOPS[i].legDistanceKm / legDistanceLy / totalDistanceKm` 等 v3 静态字段一律不动，仍按「半长轴差 / 径向差」计算，作为离线基准与旧档兼容；界面与实时数值改读 `A.liveSolarLeg(index, ms)`、`A.liveSolarRoute(ms)`、`A.solarPositions(ms)`。v3 的 `A.selftest()` 里那些「距离与静态规则一致」的断言继续通过，说明两套数据没有互相污染。

### 10.2 算法：JPL 开普勒根数 → 任意时刻日心黄道坐标

数据源为 JPL Solar System Dynamics 的 **"Keplerian Elements for Approximate Positions of the Major Planets"**（E. M. Standish），Table 1（1800 AD – 2050 AD）。给定观测时刻 `ms`（Unix 毫秒，UTC）后：

```text
JD_UTC = ms / 86400000 + 2440587.5            （Unix 纪元 = JD 2440587.5）
JDE    = JD_UTC + 69.184 / 86400              （TT = UTC + 69.184 s，见 §10.3）
T      = (JDE − 2451545.0) / 36525            （儒略世纪；T = 0 即 J2000.0）

a = a₀ + ȧT     e = e₀ + ėT     I = I₀ + İT
L = L₀ + L̇T     ϖ = ϖ₀ + ϖ̇T     Ω = Ω₀ + Ω̇T

ω = ϖ − Ω                                     （近点幅角 = 近日点黄经 − 升交点黄经）
M = L − ϖ                                     （平近点角；先归一化到 −180°..180°）
M = E − e·sinE                                （开普勒方程，弧度；牛顿迭代：
                                               初值 E₀ = M + e·sinM，收敛阈值 1e-13 rad）

x′ = a(cosE − e)          y′ = a·√(1−e²)·sinE          z′ = 0      （轨道平面内坐标）

x = (cosω cosΩ − sinω sinΩ cosI)·x′ + (−sinω cosΩ − cosω sinΩ cosI)·y′
y = (cosω sinΩ + sinω cosΩ cosI)·x′ + (−sinω sinΩ + cosω cosΩ cosI)·y′
z = (sinω sinI)·x′ + (cosω sinI)·y′

r   = √(x² + y² + z²)                          （日心距，AU）
lon = atan2(y, x) 归一化到 0..360°             （日心黄经，度）
lat = atan2(z, √(x² + y²))                     （日心黄纬，度）
```

实现细节（`src/astronomy.js`）：
- 牛顿迭代最多 100 次，`|ΔE| < 1e-13 rad` 即停；9 颗行星全算一遍在本机 < 1 ms，同一 `ms` 内部缓存，因此 `planetState / solarPositions / liveSolarLeg / liveSolarRoute` 对同一时刻严格幂等。
- `lonDeg` 用 `norm360()` 转成 0..360（负数会被补 360），不会出现 −179.9° 这种值。
- 输入 id 大小写不敏感；`liveLegKm` 里 `'moon'` 按地球位置处理；无法识别的 id 返回 `null`。
- `A.nowMs()` 默认 `Date.now()`，外部可覆盖（例如 QA 固定时钟）；所有实时 API 省略 `ms` 时走 `A.nowMs()`。

### 10.3 时间系统：UTC → TT

- 输入 `ms` 是 Unix 毫秒（UTC）。开普勒根数的时间自变量是 TT（≈TDB），两者差 `TT − UTC = 32.184 s + (TAI − UTC)`。
- 2017-01-01 起 `TAI − UTC = 37 s`，2017–2035 预期不再加闰秒，因此取常数 **69.184 s**（2026 / 2032 都适用）。换算成天 = 8.008e-4 d。
- 影响量级：水星一天走约 4.09°，69 s 只对应 **0.0033°**，远小于本表 0.07° 的近似误差，所以这个近似不会压低精度；但它让 2026/2032 的参考值对齐更干净。
- 真正无法预测的是未来闰秒/ΔT（UT1−TAI），2035 年前不超过几秒，同样可忽略。

### 10.4 根数表与来源

**Table 1（1800 AD – 2050 AD）**，参考系：J2000 平黄道与春分点；历元 J2000.0（JD 2451545.0 TDB）。变率单位：`a [AU/世纪]`、`e [1/世纪]`、角度 `[°/世纪]`。表中「Earth」一行是**地月质心 EMBary**（JPL 原表也如此），与地心位置在 2026 年相差 < 0.002°（月球绕地月质心运动的投影），游戏可忽略。

```text
             a (AU)          e            I (°)          L (°)         ϖ (°)          Ω (°)
Mercury   0.38709927   0.20563593    7.00497902   252.25032350   77.45779628   48.33076593
  rates   0.00000037   0.00001906   -0.00594749 149472.67411175   0.16047689   -0.12534081
Venus     0.72333566   0.00677672    3.39467605   181.97909950  131.60246718   76.67984255
  rates   0.00000390  -0.00004107   -0.00078890  58517.81538729    0.00268329   -0.27769418
Earth     1.00000261   0.01671123   -0.00001531   100.46457166  102.93768193    0.0
  rates   0.00000562  -0.00004392   -0.01294668  35999.37244981    0.32327364    0.0
Mars      1.52371034   0.09339410    1.84969142    -4.55343205  -23.94362959   49.55953891
  rates   0.00001847   0.00007882   -0.00813131  19140.30268499    0.44441088   -0.29257343
Jupiter   5.20288700   0.04838624    1.30439695    34.39644051   14.72847983  100.47390909
  rates  -0.00011607  -0.00013253   -0.00183714   3034.74612775    0.21252668    0.20469106
Saturn    9.53667594   0.05386179    2.48599187    49.95424423   92.59887831  113.66242448
  rates  -0.00125060  -0.00050991    0.00193609   1222.49362201   -0.41897216   -0.28867794
Uranus   19.18916464   0.04725744    0.77263783   313.23810451  170.95427630   74.01692503
  rates  -0.00196176  -0.00004397   -0.00242939    428.48202785    0.40805281    0.04240589
Neptune  30.06992276   0.00859048    1.77004347   -55.12002969   44.96476227  131.78422574
  rates   0.00026291   0.00005105    0.00035372    218.45945325   -0.32241464   -0.00508664
Pluto    39.48211675   0.24882730   17.14001206   238.92903833  224.06891629  110.30393684
  rates  -0.00031596   0.00005170    0.00004818    145.20780515   -0.04062942   -0.01183482
```

- 官方页面：<https://ssd.jpl.nasa.gov/planets/approx_pos.html>；原始数据文件：<https://ssd.jpl.nasa.gov/txt/p_elem_t1.txt>；论文/讲义出处：E. M. Standish, *Keplerian Elements for Approximate Positions of the Major Planets*, Table 8.10.2（IAU Commission 4, XSChap8.pdf）。
- **复核路径**：本机网络无法直连 `ssd.jpl.nasa.gov`（TCP 连接超时，见 §10.5），因此根数表数值逐字取自 JPL 自己发布的同一份文件 `standish.tab` 的公开镜像：
  <http://oss.mars.asu.edu/svn/krc/tags/archive_2011_10_14/run/standish.tab>
  （文件头部注明 "From: http://iau-comm4.jpl.nasa.gov/XSChap8.pdf, Table 8.10.2 ... Also at: http://ssd.jpl.nasa.gov/txt/p_elem_t1.txt"）。
- 这套根数是**近似拟合**，不是数值积分：1800–2050 内日心黄经误差从几角秒到约 0.1°（木星、土星最大），对游戏「按当前真实黄经摆放」完全够用；2020–2035 的实测误差见 §10.5。

### 10.5 参考值与精度校验

**参考值来源：JPL DE421 开发星历（本地计算）**。`ssd.jpl.nasa.gov` 的 Horizons API 在本机网络不可达（`curl` 21 s 连接超时，HTTP 000；经 `api.allorigins.win` / `api.cors.lol` 等公共代理也是 522/429 失败），按任务书允许的退化方案，参考值改为 **JPL DE421**（与 Horizons 服务端同属 JPL DE 星历族）在本机计算：PyPI 清华镜像安装 `skyfield` + `skyfield-data`（后者自带 `de421.bsp`），用 `skyfield` 把 ICRF 直角坐标按 J2000 平黄赤交角 23.4392911° 旋转到 J2000 黄道。DE421 与 Horizons 常用的 DE440/441 在 2020–2035 对这些行星的位置差在亚角秒量级，远小于本近似算法的 0.07° 误差。另用独立实现 **astronomy-engine**（VSOP87 级数，npm/jsDelivr）交叉验证 2026-11-18 位置：两者（DE421 与 VSOP87）彼此相差 ≤ 0.005°。

固定时刻 `2026-11-18T00:00:00Z` 的参考值与实算值（`ms = 1794960000000`）：

| 行星 | 实算黄经 (°) | 参考黄经 (°) | Δ黄经 (°) | 实算日心距 (AU) | 参考日心距 (AU) | Δ日心距 |
|---|---|---|---|---|---|---|
| 水星 mercury | 124.127905 | 124.133216 | −0.005311 | 0.324928364 | 0.324934404 | −0.0019% |
| 金星 venus | 70.228433 | 70.228494 | −0.000061 | 0.720967561 | 0.720974740 | −0.0010% |
| 地球 earth（地月质心） | 55.278185 | 55.279642 | −0.001457 | 0.988624070 | 0.988644467 | −0.0021% |
| 火星 mars | 108.431500 | 108.434740 | −0.003240 | 1.611684186 | 1.611760214 | −0.0047% |
| 木星 jupiter | 134.970759 | 134.946366 | +0.024393 | 5.320052637 | 5.322264581 | −0.0416% |
| 土星 saturn | 12.519409 | 12.445633 | +0.073776 | 9.420551669 | 9.420066385 | +0.0052% |
| 天王星 uranus | 63.202356 | 63.202403 | −0.000047 | 19.427344046 | 19.432564342 | −0.0269% |
| 海王星 neptune | 2.930254 | 2.938974 | −0.008720 | 29.876535141 | 29.876918202 | −0.0013% |
| 冥王星 pluto | 304.417282 | 304.423460 | −0.006178 | 35.647631248 | 35.643600231 | +0.0113% |

- 最大误差：**黄经 0.0738°（土星）**，**日心距 0.0416%（木星）**，满足 SPEC-v4「黄经 ≤0.1°、日心距 ≤0.3%」。
- `A.selftest()` 对这张表逐项断言（黄经 ≤0.1°、日心距 ≤0.3%）；`build/check-astro.js` 打印完整对照表。
- **2020–2035 全区间校验**：以 DE421 生成 2020-01 至 2035-10 每季度一个时刻（64 个采样点）× 9 颗行星，与本实现对比，最大误差：

| 行星 | 最大 Δ黄经 (°) | 最大 Δ日心距 | 出现时刻（黄经 / 日心距最大处） |
|---|---|---|---|
| 水星 | 0.0051 | 0.0031% | 2022-10-01 |
| 金星 | 0.0067 | 0.0056% | 2021-10-01 |
| 地球 | 0.0058 | 0.0050% | 2029-07-01 |
| 火星 | 0.0177 | 0.0168% | 2026-04-01 |
| 木星 | 0.0715 | 0.0616% | 2023-04-01 |
| 土星 | **0.0741** | **0.1875%** | 2026-04-01 / 2020-04-01 |
| 天王星 | 0.0302 | 0.0400% | 2021-01-01 |
| 海王星 | 0.0143 | 0.0284% | 2020-01-01 |
| 冥王星 | 0.0143 | 0.0218% | 2023-10-01 |

  全区间最大黄经误差 0.0741°、最大日心距误差 0.1875%，均在 SPEC 容差内（土星、木星是这套近似根数的固有误差，不是实现错误）。
- **J2000 历元一致性**：`A.planetState('earth', Date.UTC(2000,0,1,12,0,0))` 得黄经 100.38100°、日心距 0.98330742 AU；DE421 地月质心参考值 100.380172° / 0.983309967 AU，差 0.0008° / 2.6e-6，说明根数表的历元与坐标系对齐正确（`A.selftest()` 断言黄经差 ≤0.02°、距离相对差 ≤0.1%）。
- 复现参考值的方法：`python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple skyfield skyfield-data`，然后用 `skyfield` 读 `de421.bsp`，对 `(planet_barycenter − sun).at(ts.utc(...)).position.au` 做上述黄道旋转；具体脚本与输出见 `reports/astro-live.md`。
- 若将来网络可以访问 Horizons，可用下列查询刷新参考值（`COMMAND` 编码见注释）：

```text
https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='499'&CENTER='500@10'
  &MAKE_EPHEM='YES'&EPHEM_TYPE='VECTORS'&START_TIME='2026-11-18'&STOP_TIME='2026-11-18%2000:01'
  &STEP_SIZE='1d'&VEC_TABLE='2'&REF_PLANE='ECLIPTIC'&REF_SYSTEM='J2000'&OUT_UNITS='AU-D'
```

  `COMMAND`：199 水星、299 金星、399 地球（地心；算法用 3 = 地月质心更一致）、499 火星、599 木星、699 土星、799 天王星、899 海王星、999 冥王星；`CENTER='500@10'` 是太阳中心。返回 `$$SOE` 段里的 X/Y/Z（AU）即 J2000 黄道坐标，可换算黄经/日心距。

### 10.6 实测算例：2026-11-18 的 8 段距离与总里程

`2026-11-18T00:00:00Z`（`ms = 1794960000000`）由 `A.liveSolarRoute(ms)` 实际运行输出：

| # | 航段 | 距离 (km) | 距离 (AU) | 备注 |
|---|---|---|---|---|
| 0 | 地球 → 月球 | 384,400.000 | 0.002570 | 固定值，`fixed:true` |
| 1 | 月球（按地球）→ 水星 | 138,147,450.365 | 0.923459 | 实时弦长 |
| 2 | 水星 → 金星 | 88,708,400.443 | 0.592979 | 实时弦长 |
| 3 | 金星 → 火星 | 170,059,886.454 | 1.136780 | 实时弦长 |
| 4 | 火星 → 木星 | 590,106,005.504 | 3.944615 | 实时弦长 |
| 5 | 木星 → 土星 | 1,955,309,080.229 | 13.070434 | 实时弦长 |
| 6 | 土星 → 天王星 | 2,290,449,322.072 | 15.310708 | 实时弦长 |
| 7 | 天王星 → 海王星 | 3,942,367,970.519 | 26.353102 | 实时弦长 |
| 8 | 海王星 → 冥王星 | 4,848,522,965.206 | 32.410374 | 实时弦长 |
| — | **合计（totalKm）** | **14,024,055,480.791** | **93.745021** | `A.liveSolarRoute(ms).totalKm` |

对比：v3 静态规则（半长轴差）太阳系段合计 5,940,587,328.57 km（39.710374 AU）。实时弦长合计 93.745 AU 明显更大，因为相邻行星真实位置大多不在同一条径向线上（这正是 v3 规则忽略的相位角）；两者是不同物理量，不能互相校验，只能并列展示（v3 字段仅作离线基准）。

**总里程随日期变化**（每年 11-18T00:00:00Z，`A.liveSolarRoute`）：

| 日期 | totalKm | totalAU |
|---|---|---|
| 2026-11-18 | 14,024,055,480.791 | 93.745021 |
| 2027-11-18 | 14,486,562,142.307 | 96.836687 |
| 2028-11-18 | 14,376,585,907.599 | 96.101541 |
| 2029-11-18 | 14,594,365,287.934 | 97.557306 |
| 2030-11-18 | 14,644,817,376.023 | 97.894558 |
| 2031-11-18 | 14,512,610,947.215 | 97.010812 |
| 2032-11-18 | 14,863,919,853.399 | 99.359167 |
| 2033-11-18 | 14,520,746,010.907 | 97.065192 |
| 2034-11-18 | 15,147,879,397.210 | 101.257320 |
| 2035-11-18 | 14,688,612,103.886 | 98.187307 |

- **2026-11-18 vs 2032-01-01**（自检断言用的日期对）：`14,024,055,480.791 km` vs `14,606,926,790.613 km`，差 **582,871,309.823 km（4.156%）**。`A.selftest()` 断言两者差 > 1 亿 km 且相对差 > 0.5%，证明总里程确实随真实相对位置变化。
- **QA 固定时刻 `?live=1`**（引擎把时钟固定在 `2026-11-18T12:00:00Z`）：`A.liveSolarRoute` 得 `totalKm = 14,026,385,403.788 km`、`totalAU = 93.760595`，可用于 `__FATFISH__.liveInfo()` / 截图断言。
- 界面显示口径：`A.solarPositions(ms)[id].lonDeg` 是行星当前真实黄经；`A.liveSolarRoute(ms).totalAU/totalKm` 是「当前 9 段连线总里程」，两者同源（同一 `ms` 缓存），QA 可用同一时刻交叉核对。

### 10.7 恒星站的 `spectral` / `teffK`

v4 给银河系 10 颗真实恒星补了光谱型与有效温度（渲染层按光谱型/黑体色温区分贴图与颜色，SPEC-v4 §1.7 / §6）：

| 站点 id | 恒星 | spectral | teffK | 说明 / 来源 |
|---|---|---|---|---|
| `alpha_cen` | 半人马座α | G2V | 5790 | α Cen A，系统取最亮主星；SIMBAD / Wikipedia |
| `barnard` | 巴纳德星 | M4V | 3190 | 红矮星；SIMBAD（GJ 699）/ Wikipedia |
| `wolf359` | 沃尔夫359 | M6V | 2800 | 红矮星 / 耀星；SIMBAD / Wikipedia |
| `sirius` | 天狼星 | A1V | 9940 | 天狼星 A（A1V）；SIMBAD / Wikipedia |
| `eps_eri` | 波江座ε | K2V | 5084 | 年轻类太阳恒星；SIMBAD / Wikipedia |
| `procyon` | 南河三 | F5IV | 6530 | 南河三 A（F5IV–V，取 F5IV）；SIMBAD / Wikipedia |
| `tau_cet` | 天仓五 | G8V | 5344 | 类太阳恒星；SIMBAD / Wikipedia |
| `altair` | 牛郎星 | A7V | 7550 | 快速自转的 A 型星；SIMBAD / Wikipedia |
| `vega` | 织女星 | A0V | 9600 | 曾是星等零点；SIMBAD / Wikipedia |
| `arcturus` | 大角星 | K1.5III | 4286 | 橙红巨星；SIMBAD / Wikipedia |

- 来源：SIMBAD 天体查询服务 <http://simbad.u-strasbg.fr/simbad/>、Wikipedia 各星条目（如 <https://en.wikipedia.org/wiki/Alpha_Centauri>、<https://en.wikipedia.org/wiki/Sirius>）。有效温度取常用文献值（不同文献 ±几十 K，游戏只用于配色，不参与轨道/航段计算）。
- `A.selftest()` 断言这 10 站的 `spectral` 字符串（含 MKK 格式正则）与 `teffK` 数值，并检查范围 2000–12000 K；`build/check-astro.js` 逐站打印。
- 注意：`alpha_cen` 是 `kind:'system'`（三合星），表中给的是最亮成员 α Cen A；`galactic_center` / `galactic_edge` 不是单颗恒星，没有 `spectral/teffK` 字段，渲染层按 `stop.color` 程序化处理。

### 10.8 复现与自检

```powershell
# 1) node 自检（打印 v3 基础 + v4 API + 2026-11-18 对照表 + 9 段里程 + 恒星光谱表）
$node = "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe"
& $node build\check-astro.js
# 期望：总结 221 项通过 0 失败，退出码 0

# 2) 模块级自检（浏览器 console 或 node 都可）
& $node -e "var fs=require('fs');var A=new Function(fs.readFileSync('src/astronomy.js','utf8')+'\nreturn A;')(); console.log(A.selftest());"
# 期望：[]

# 3) 手工查看实时数据（node）
& $node -e "var fs=require('fs');var A=new Function(fs.readFileSync('src/astronomy.js','utf8')+'\nreturn A;')(); var ms=Date.UTC(2026,10,18,0,0,0); console.log(A.formatUTC(ms), A.solarPositions(ms).earth); console.log(A.liveSolarRoute(ms).totalKm);"

# 4) 浏览器 console（游戏 index.html 加载后）
#    A.formatUTC(Date.UTC(2026,10,18,0,0,0))        -> '2026-11-18 00:00:00 UTC'
#    A.solarPositions(Date.UTC(2026,10,18)).earth   -> {id:'earth', x, y, z, rAU, lonDeg, latDeg, ms}
#    A.liveSolarRoute(Date.UTC(2026,10,18)).totalKm -> 14024055480.79...
```

`A.selftest()` 的 v4 断言包括：7 个新 API 存在且为函数；根数表 9 行星 × 12 个数完整；同一 `ms` 幂等（`planetState` / `solarPositions` / `liveSolarRoute` 两次结果全等）；2026-11-18 的 9 颗行星黄经 ≤0.1°、日心距 ≤0.3%；J2000 历元地球黄经/日心距对 DE421；地月第 0 段固定 384,400 km 且 `fixed:true`；`liveLegKm` 对称、`moon` 按地球、未知 id 返回 `null`；9 段航段与 `liveSolarRoute` 求和一致；总里程 > 0 且 2026-11 与 2032-01 差异显著；`formatUTC` 格式；`nowMs` 可覆盖；10 颗恒星 `spectral/teffK` 值与格式。

### 10.9 已知限制与风险

1. **近似根数法的固有误差**：土星、木星在 2020–2035 的黄经误差可达 0.07°（表见 §10.5）。这在 SPEC 容差内，但如果未来要求「行星在屏幕上与真实天象逐角秒对齐」，需要换用 VSOP87/DE 星历级数（体积和 CPU 成本都会上升）。
2. **地球用**地月质心**根数**：与地心差 < 0.002°，对游戏无感；若未来要显示「地球在太阳系中的精确位置」，可再叠加月球质心偏移（需要月球根数，当前未做）。
3. **月球段固定值**：384,400 km 是平均值，真实地月距离在 363,300–405,500 km 间变化；第 0 段按 SPEC 保持固定，不做实时弦长。
4. **未来闰秒/ΔT**：时间换算用常数 69.184 s，2035 年后若加闰秒会有 ≤ 几秒误差，对应行星黄经 < 0.001°，可忽略；但 3000 年尺度的长期仿真不适用本表（Table 1 仅 1800–2050）。
5. **参考值不是 Horizons 直采**：本机网络不可达，改用 JPL DE421 本地计算（详见 §10.5）；若 Lead 侧网络可访问 Horizons，建议用 §10.5 的 URL 模板刷新一遍 `LIVE_REFERENCE` 常量并重跑 `check-astro.js`。
6. **渲染一致性**：`render.js` 只读 `solarPositions` 与 `liveSolarRoute`；`engine.js` 对第 0 段单独用 `firstLegKm`、其余太阳系段用 `liveSolarLeg`，所以本模块不需要改 engine 侧逻辑；任何 UI 数值断言应以同一 `ms` 调用本模块为准，避免「UI 时钟与模块时钟不同步」的假差异。

