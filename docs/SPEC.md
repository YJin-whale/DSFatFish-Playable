# 肥鱼跳宇宙 · 星尘远航 — 改版工程规格（v3）

> **v4 说明**：v4（2026-11-18）的增量需求、新契约与验收口径见 `docs/SPEC-v4.md`；
> **v5 说明**：v5 的通关重玩 / 历史记录 / 无限模式 / 仓库化见 `docs/SPEC-v5.md`；
> **v6 说明**：v6 的音频系统（无极音量 / 内置曲目 / 上传音乐 / 律动角色）见 `docs/SPEC-v6.md`。
> 本文档保留为 v3 规格与历史基线；其中被 v4/v5/v6 覆盖的部分以对应 SPEC 与 `README.md` 为准。

> 本文件是 v3 全体协作者（Lead / teammates）的唯一事实来源。
> 游戏目录：`C:\Users\admin\Desktop\FatFish-Playable`
> 线上地址（用户提供，与本地原始 index.html 一致）：https://fatfish-jump-universe.app.workbuddy.host/?sharecode=OBDYU6QNS7

## 0. 背景与目标

原版是单文件 canvas 小游戏（1026 行 JS）：按住 W 无脑爬升，在 100/180/320/1500… km 处按高度解锁天体，画面程序绘制。
用户要求改成「从地球出发 → 月球 → 太阳系各行星 → 冥王星 → 银河系 → 可观测宇宙边缘」的**星际跳跃冒险**，并加入真实天文距离、月面二次起跳、重力比例速度、长按缩放到本层级全景 + 白色虚线航线预测、外星飞船攻击、护盾铁锅、动态航程尺、成就、商城与双人同行。

原始文件已备份：`index_original_backup.html`。**最终交付物仍然是单文件 `index.html`**（自包含，双击可玩，可重新上传 WorkBuddy）。源文件拆分在 `src/`，构建脚本把 JS + 贴图 base64 内联成 `index.html`。

## 1. 用户需求拆解（验收清单）

1. **月球贴图**：月球用网络下载的真实月面照片/贴图；所有降落天体都用真实星球影像贴图（非纯色渐变）。
2. **月球成就**：抵达月球弹出成就「我的一小步，大肥鱼们的一大步」；月球成为新的跳跃点可再次起跳；起跳基础速度按当地重力/地球重力比例；航段距离严格按真实天文距离测算并在界面展示；右下角航程尺长度固定，但满量程数值随航程增长，角色标记按比例**向下**重定位（缩放变大时）。
3. **外星飞船**：飞行过程中随机出现外星飞船攻击玩家（弹幕），玩家可躲避。
4. **角色形象**：默认角色为 DeepSeek 金鱼娘（现有 hero.png，用户昵称“大肥鱼”）；获得护盾时头顶出现一口铁锅；护盾最多 1 个，不叠加。商城新增 ChatGPT、Claude 的幼态拟人角色（风格与默认角色一致）。
5. **长按起飞预演**：起跳界面长按角色 → 背景连续缩小到能看见整个当前层级（太阳系 / 银河系 / 可观测宇宙）→ 显示严格天体力学/几何推算的白色虚线飞行路线 → 完成瞬间切回长按前界面 → 进入可操作的躲避/收集飞行。太阳系最后落点为冥王星；飞出太阳系后同样机制缩小到银河系，落点换成其他恒星系；最后飞出可观测宇宙。
6. **商城 + 伙伴**：星辰币购买角色；可选两个已拥有角色同时跳跃（伙伴同行）；角色等级到一定程度解锁其他功能（本轮只做入口占位，不展开）。

## 2. 目录与文件所有权（写作用域，避免冲突）

| 路径 | 负责人 | 说明 |
|---|---|---|
| `index.html` | Lead（构建脚本生成） | 最终单文件交付物，**不要手改** |
| `index_original_backup.html` | Lead | 原始版本备份 |
| `src/astronomy.js` | **astro-data** | 纯数据 + 纯函数，无 DOM |
| `src/engine.js` `src/render.js` `src/ui.js` `src/index.template.html` `build/build.py` | Lead | 游戏核心 / 渲染 / 界面 / 构建 |
| `assets/tex/**` | **planet-assets** | 真实星球贴图、球体渲染 PNG、背景图 |
| `assets/chars/**` | **char-art** | ChatGPT / Claude 幼态拟人角色 PNG |
| `tools/**` | **qa-harness** | 无依赖 CDP 测试工具 |
| `docs/**` | 各自 + Lead | 规格 / 数据说明 |
| `reports/**` | 各自 | 交付报告 |

只写自己作用域内的文件。需要改别人的文件 → 给 Lead 发消息。

## 3. 线程分工

- **Lead**：架构、`engine.js`/`render.js`/`ui.js`、构建、集成、最终验收。
- **planet-assets**：下载真实星球贴图 → 生成透明背景球体 PNG（带真实光照/晨昏线）→ 写 `assets/manifest-textures.json`。
- **astro-data**：`src/astronomy.js`（天体、真实距离、重力比、成就、阶段数据 + 自检）。
- **char-art**：ChatGPT / Claude 幼态拟人角色立绘（与 hero.png 风格一致，透明背景）。
- **qa-harness**：Chrome headless CDP 测试工具 + 截图/报错采集；最终对成品做回归。

## 4. `src/astronomy.js` 契约（astro-data 必须严格实现）

普通 ES5 IIFE，**不依赖任何外部库/DOM**，浏览器和 node 下都能 `eval` 执行；最终暴露全局 `A`：

```js
var A = (function(){
  'use strict';
  // ... 
  return { /* 见下 */ };
})();
```

### 4.1 常量

```js
AU_KM = 149597870.7          // 1 天文单位
LY_KM = 9460730472580.8      // 1 光年
EARTH_G = 9.80665            // m/s²
EARTH_ESCAPE_KMS = 11.186    // 地球第二宇宙速度 km/s，作为“起跳基础速度”基准
```

### 4.2 `A.STAGES`（3 个层级，按顺序）

```js
[
 { id:'solar',   name:'太阳系',       short:'太阳系',   unit:'km',  mapType:'solar'   },
 { id:'stellar', name:'银河系',       short:'银河系',   unit:'ly',  mapType:'galaxy'  },
 { id:'cosmic',  name:'可观测宇宙',   short:'宇宙',     unit:'ly',  mapType:'universe'}
]
```

### 4.3 `A.STOPS`（按航行顺序的落点数组，共 28 站 = 太阳系 9 + 银河系 12 + 宇宙 7，地球为出发点不列入）

字段（全部必填，数值来源写在 `src`/`note`）：

```js
{
  id:'moon',              // 小写英文稳定 id
  name:'月球',            // 中文名
  en:'Moon',              // 英文名
  stage:'solar',          // solar | stellar | cosmic
  kind:'moon'|'planet'|'dwarf'|'star'|'system'|'galaxy'|'cluster'|'edge',
  orbitalAU: 1.0,         // 绕太阳轨道半长轴（AU，solar 必填；其他可为 0）
  orbitalLY: 0,           // 距太阳距离（ly，stellar/cosmic 必填；solar 可为 0）
  radiusKm: 1737.4,       // 天体平均半径（可选但建议给）
  gravityRatio: 0.165,    // 表面重力/地球重力（无固体表面用 1.0 并注明）
  gravityNote: '月球表面重力 1.62 m/s²，约为地球的 16.5%',
  texture:'globe_moon',   // 贴图 key，与 assets 文件名对应（见第 5 节）
  color:'#D9DEEA',        // 主题色（UI/占位）
  desc:'一句话介绍',
  fact:'一条真实天文冷知识',
  achievement:{ id:'a_one_small_step', title:'我的一小步，大肥鱼们的一大步', text:'...' }, // 可无
  firstLegKm: 384400,     // 仅 moon：地月平均距离 km
  distanceNote:'地月平均距离 384,400 km'
}
```

**航段距离规则（写进代码与注释，界面要能解释）**：
- 月球：`384400 km`（地月平均距离）。
- 其余 solar 站：与前一站的平均轨道间距 `|orbitalAU(prev) - orbitalAU(cur)| × AU_KM`（地球起点 orbitalAU=1；即两条轨道共线时的最近距离，注释说明“按轨道半长轴之差测算”）。
- stellar/cosmic 站：与前一站的径向距离差 `|orbitalLY(prev) - orbitalLY(cur)| × LY_KM`；首站从太阳系边缘（银河系段从太阳/太阳系外缘 0.00063 ly 起算）开始，注释说明。
- 每站提供 `legDistanceKm`、`legDistanceLy`、`legDistanceLabel`（人类可读，如 `「38.44 万 km」`、`「1.60 光年」`、`「233.7 万光年」`）、`totalDistanceLabel`（从地球累计）。
- 提供 `A.segment(index)` 返回 `{from, to, legKm, legLy, unit}`；`A.legInfo(i)`。

**太阳系顺序**（must）：月球 → 水星 → 金星 → 火星 → 木星 → 土星 → 天王星 → 海王星 → 冥王星。
轨道半长轴（AU）：水星 0.387098、金星 0.723332、地球 1.000000、火星 1.523679、木星 5.2044、土星 9.5826、天王星 19.2184、海王星 30.11、冥王星 39.482。
重力比：月球 0.165、水星 0.378、金星 0.907、火星 0.379、木星 2.528、土星 1.065、天王星 0.886、海王星 1.140、冥王星 0.063。

**银河系段**（距太阳，ly）：半人马座α 4.365、巴纳德星 5.963、沃尔夫359 7.856、天狼星 8.601、波江座ε 10.475、南河三 11.462、天仓五 11.912、牛郎星 16.73、织女星 25.04、大角星 36.7、银河系中心 26000、银河系边缘 50000。
**宇宙段**（距太阳，ly）：大麦哲伦云 163000、小麦哲伦云 200000、仙女座星系 2537000、三角座星系 2730000、室女座星系团 53800000、后发座星系团 321000000、可观测宇宙视界 46500000000。

贴图 key 分配：
- solar 9 站：`globe_moon/mercury/venus/mars/jupiter/saturn/uranus/neptune/pluto`
- stellar 12 站：无单独照片 → `star_<id>`（渲染层程序化绘制），但需给 `texture` 字段值 `star_alpha_cen` 等
- cosmic 7 站：`gal_lmc / gal_smc / gal_andromeda / gal_triangulum / gal_virgo / gal_coma / gal_horizon`，其中 `gal_andromeda`、`gal_triangulum` 若有真实图片使用 assets 提供的，否则程序化。

### 4.4 `A.ACHIEVEMENTS`

数组，至少包含：
```js
{ id:'a_one_small_step', title:'我的一小步，大肥鱼们的一大步', desc:'首次登陆月球', icon:'🌕' }
```
另加：首次抵达火星 / 木星 / 冥王星 / 冲出太阳系（抵达半人马座α）/ 抵达银河系边缘 / 抵达可观测宇宙视界 / 首次获得铁锅护盾 `a_wok` / 双人同行 `a_partner` / 收集 50 枚星辰币 `a_rich`。字段：`id,title,desc,icon`。

### 4.5 辅助函数

```js
A.fmtNumber(n)                  // 1234567 -> '1,234,567'
A.fmtDistance(km, opts)         // km -> '38.44 万 km' / '1.5 亿 km' / '4.37 光年'
A.fmtKelvin? 不需要
A.legDistance(fromStopOrEarth, toStop)  // 返回 {km, ly, unit, label}
A.cumulative(stop)              // 累计航程 label
A.indexOf(id)                   // 在 A.STOPS 中的索引
A.byId(id)                      // 按 id 取 stop
A.stageOf(index)                // 'solar'|'stellar'|'cosmic'
A.launchSpeedKms(gravityRatio)  // 11.186 * gravityRatio，保留两位
A.selftest()                    // 返回 [] 或 错误字符串数组；校验：站数、顺序、单调性、单位、数据完整性、距离数值与外部常量一致
```

### 4.6 验收

- `node` 环境下 eval 可执行，`A.selftest()` 返回 `[]`。
- 注释与 `docs/astronomy-notes.md` 写清每个距离的测算依据与来源（NASA Planetary Fact Sheet、IAU 半长轴、视差距离等）。
- 数据必须与本文档第 4.3 节一致；如发现文档中的数据有误，先给 Lead 发消息确认。

## 5. 贴图资产契约（planet-assets）

输出目录 `assets/tex/`：

- `raw/`：下载的原始等距柱状贴图（equirectangular jpg，不删，便于重建）。
- `globe_<id>.png`：**512×512 RGBA**，透明背景，正射球体：圆内按经纬采样原始贴图 + 晨昏线/明暗 + 边缘大气蓝光；圆外透明。id = moon/mercury/venus/mars/jupiter/saturn/uranus/neptune/pluto/sun。
- `bg_milkyway.jpg`：≥1024×512 的银河星空背景（可来自 `2k_stars_milky_way.jpg` 裁剪/压缩）。
- `gal_andromeda.jpg`、`gal_triangulum.jpg`、`gal_lmc.jpg`、`gal_smc.jpg`：真实星系照片（若来源不可达可留空并在报告说明，渲染层会用程序化兜底）。
- `assets/manifest-textures.json`：每张图 `{key,file,w,h,source,url,license,note}`。
- 体积：单张 globe PNG 建议 ≤ 120 KB；总 assets ≤ 4 MB。用 `C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe`（已装 Pillow/numpy）。
- 必须逐张读回校验：尺寸、透明通道、球体非空（非全透明像素占比 20%~80%），并在 `reports/planet-assets.md` 记录。
- 授权：Solar System Scope 贴图 CC BY 4.0，需在游戏「关于/署名」里注明来源；NASA/ESA 图像注明来源与公共领域/授权。

## 6. 角色美术契约（char-art）

- 默认角色 `hero.png`（296×394，透明底，DeepSeek 金鱼娘）。
- 交付 `assets/chars/chatgpt.png`、`assets/chars/claude.png`：**296×394 或同比例**、透明背景、幼态 Q 版、与 hero.png 同一画风（粗描边、赛璐璐上色、大眼、Q 版比例），分别体现 ChatGPT（青绿色系、耳机/麦克风、对话气泡元素）与 Claude（橙桃色系、星芒/星号发饰、暖色点缀）。
- 优先尝试网络搜集符合授权的图（记录来源/授权）；找不到可商用/可再分发的高质量图时，**以 hero.png 为基底做高质量调色 + 配饰重绘**（保证风格一致），并在报告里说明。
- 交付 `assets/manifest-chars.json` + `reports/char-art.md`（含来源、处理步骤、预览路径）。
- 运行时若缺图，渲染层会用 `ctx.filter hue-rotate` + 配饰程序化兜底，所以**不要改 hero.png**。

## 7. 测试工具契约（qa-harness）

- `tools/cdp_check.mjs`：无第三方依赖（Node 24 内置 fetch/WebSocket），启动本机 Chrome headless（路径 `C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`），通过 CDP：
  - 打开 `file:///...index.html?<query>`；
  - 收集 `Runtime.consoleAPICalled`、`Runtime.exceptionThrown`、`Log.entryAdded`；
  - 可执行任意 JS（`Runtime.evaluate`）读取 `window.__FATFISH__` 状态；
  - 可截图 `Page.captureScreenshot` 存 `reports/shots/*.png`；
  - 输出 JSON 报告并以非 0 退出码表示失败。
- CLI 例：`node tools/cdp_check.mjs --url "file:///C:/.../index.html" --scenario smoke --out reports/qa-smoke.json`
- 先对 `index_original_backup.html` 做一次基线 smoke（能加载、无 JS 报错、截图非空），证明工具本身可用。
- 最终对改版 `index.html` 跑场景：title/hangar/launchpad/flight/arrival/shop/achievement/partner/zoom-preview，各出截图 + 状态断言。
- 报告 `reports/qa-*.md`，失败截图 + 控制台报错原文。

## 8. 构建与集成（Lead）

- `build/build.py`：读 `src/index.template.html`，按顺序拼接 `src/astronomy.js` → `src/engine.js` → `src/render.js` → `src/ui.js`，注入 `TEX`（assets 图片 → base64 data URI，键名同文件名去扩展名）+ `CHARS` + 版本号，输出 `index.html`。
- 构建后自动跑 `node tools/cdp_check.mjs` 的 smoke 场景（Lead 手动执行）。
- 游戏需在没有 assets（只有代码）时也能运行（程序化兜底贴图），构建把真实贴图带上。

## 9. 全局调试 API（Lead 实现，qa 用）

`window.__FATFISH__ = { version, state(), goto(screen), jumpTo(stopId), debug:{...} }`，字符串参数通过 URL query 也能触发（如 `?screen=shop`、`?stop=moon`、`?autoplay=1`）。qa 依赖此接口。

## 10. 验收口径

- 双击 `index.html` 可玩、无 JS 报错；
- 月球降落 + 成就触发 + 从月球再起跳；
- 长按预演 → 缩放 → 白色虚线轨迹 → 切回 → 飞行；
- 右下角航程尺满量程增长 + 标记下移；
- UFO 攻击、铁锅护盾（最多 1）、双角色同行；
- 商城可买/ChatGPT/Claude 角色；伙伴可选择两个角色；
- 太阳系 9 站 → 银河系 12 站 → 宇宙 7 站完整可通到「可观测宇宙视界」；
- 移动端触屏可玩，横竖屏自适应。
