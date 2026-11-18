# 肥鱼跳宇宙 v3 · 最终 QA 报告

> **结论：34/34 场景全部通过。** 0 console error、0 未捕获异常、0 资源加载失败、0 断言失败。
> 被测构建：`index.html` SHA256 = `794CDF8CC15ACEA73A101ED8186CBDCE49625E6F1C6DF2AB912F2CB1C07CE0F6`，2,809,746 bytes（Lead 确认的冻结版），测试期间文件哈希稳定未变。
> 测试时间：2026-11-18 19:51–19:55（Asia/Shanghai），全量耗时 190.7 s。

---

## 1. 被测构建与环境

| 项 | 值 |
|---|---|
| 构建文件 | `C:\Users\admin\Desktop\FatFish-Playable\index.html` |
| 大小 / SHA256 | 2,809,746 bytes / `794CDF8C…07CE0F6`（运行时前后一致，未在测试中被改动） |
| 构建时间 | 2026-11-18 19:48（src/engine.js 19:44:04 → 构建 19:44:06，之后 Lead 冻结） |
| 调试 API | `window.__FATFISH__`（state/goto/jumpTo/setProgress/arriveNow/unlockAll/buy/partner/setPartner/hold/release/giveWok/spawnUFO/setHp/unlock/hit） |
| Node | v24.21.0（`C:\Users\admin\.dsh\...\node\bin\node.exe`） |
| Chrome | 156.0.8078.74 headless=new，CDP Protocol 1.3 |
| 测试工具 | `tools/cdp_check.mjs`（零依赖 CDP，`docs/qa-harness.md`）＋ `tools/qa_final_run.ps1`（批量执行器） |
| 视口 | 桌面 1280×800；移动端 390×844；横屏 844×390（DPR=1） |

> 哈希沿革说明：Lead 早前报过 `8342909F…`（2,809,631 B）是上一次构建；之后又改了一次（新增 `debugHit`、E2E 脚本自初始化），当前冻结版为 `794CDF8C…`。**本报告全部 34 项均在 794C… 上重跑**，旧数据未混入。

---

## 2. 方法

1. **加载与报错收集**：headless Chrome 打开 `file:///…/index.html?<参数>`，收集 `Runtime.consoleAPICalled` / `Runtime.exceptionThrown` / `Log.entryAdded` / `Network.loadingFailed`；未捕获异常一律判失败，`console.error`/资源失败默认判失败。
2. **状态断言**：通过 `Runtime.evaluate` 读 `window.__FATFISH__.state()` 做精确断言（screen / trip / current / target / legUnit / srcGravity / baseSpeedKms / zoom / owned / partner / stardust / achievements / localStorage）。
3. **E2E**：用 Lead 提供的 `build/e2e_hold.js`、`build/e2e_moon.js`，向 canvas 派发真实 `PointerEvent` 完成长按→飞行→抵达→再起跳全流程（脚本已带自初始化）。
4. **截图非空白**：页面 canvas `getImageData` 方差 + Node 侧 PNG 解码方差双检（阈值 5）；smoke 场景强制检查。
5. **每轮全新临时 profile**，结束强制清理 Chrome 进程树与临时目录；存档验证采用 Lead 指定的单页面内 `localStorage` 读回口径。

批量脚本一条命令跑完全部：`powershell -NoProfile -ExecutionPolicy Bypass -File tools/qa_final_run.ps1`
（脚本为 UTF-8 with BOM，兼容 Windows PowerShell 5.1；产物见 §9。）

---

## 3. 全场景结果总表（34 项）

| # | 场景 | URL / 额外参数 | 关键断言 | 结果 | 耗时 | 截图方差 | 截图 |
|---|---|---|---|---|---|---|---|
| 1 | smoke | 无（新 profile） | `screen=title`、`__FATFISH__` 存在、canvas/截图非空白 | ✅ | 3.9s | 1442.55 | `final-smoke.png` |
| 2 | title | `?screen=title` | `screen=title` | ✅ | 4.0s | 1443.24 | `final-title.png` |
| 3 | hangar | `?screen=hangar` | `screen=hangar` | ✅ | 3.9s | 1169.77 | `final-hangar.png` |
| 4 | shop | `?screen=shop&rich=1&lv=3` | `screen=shop`、`stardust=9999`、`pilotLv=3` | ✅ | 3.7s | 1301.78 | `final-shop.png` |
| 5 | achv | `?screen=achv` | `screen=achv` | ✅ | 4.0s | 395.06 | `final-achv.png` |
| 6 | help | `?screen=help` | `screen=help` | ✅ | 3.9s | 1032.55 | `final-help.png` |
| 7 | fail | `?screen=fail` | `screen=fail` | ✅ | 3.9s | 574.48 | `final-fail.png` |
| 8 | paused | `?screen=paused` | `screen=paused` | ✅ | 3.9s | 522.92 | `final-paused.png` |
| 9 | ending | `?screen=ending` | `screen=ending` | ✅ | 4.0s | 937.28 | `final-ending.png` |
| 10 | launch | `?screen=launch` | `screen=launch`、`current=earth`、`target=moon`、`baseSpeedKms=11.186` | ✅ | 4.0s | 3751.32 | `final-launch.png` |
| 11 | launch-zoom | `?screen=launch&zoom=0.96` | `zoom.p>0.9` | ✅ | 4.1s | 879.35 | `final-launch-zoom.png` |
| 12 | launch-galaxy | `?stop=alpha_cen&screen=launch` | `target=alpha_cen`、`legUnit=ly` | ✅ | 4.1s | 2870.18 | `final-launch-galaxy.png` |
| 13 | launch-universe | `?stop=lmc&screen=launch` | `target=lmc`、`legUnit=ly` | ✅ | 4.0s | 765.46 | `final-launch-universe.png` |
| 14 | launch-galaxy-zoom | `?stop=alpha_cen&screen=launch&zoom=0.96` | `zoom.p>0.9` | ✅ | 4.1s | 741.00 | `final-launch-galaxy-zoom.png` |
| 15 | launch-universe-zoom | `?stop=lmc&screen=launch&zoom=0.96` | `zoom.p>0.9` | ✅ | 4.1s | 799.59 | `final-launch-universe-zoom.png` |
| 16 | flight | `?screen=flight&progress=0.5` | `screen=flight`、`legUnit=km`、`progress∈(0.4,0.75)` | ✅ | 4.3s | 826.88 | `final-flight.png` |
| 17 | flight-ly | `?stop=alpha_cen&screen=flight&progress=0.5` | `legUnit=ly`、`target=alpha_cen` | ✅ | 4.3s | 1288.67 | `final-flight-ly.png` |
| 18 | flight-galaxy | `?stop=triangulum&screen=flight&progress=0.7` | `target=triangulum`、`progress>0.6` | ✅ | 4.3s | 899.02 | `final-flight-galaxy.png` |
| 19 | e2e-hold | 无参数 + `build/e2e_hold.js` | `afterHoldScreen=flight`、`afterArriveScreen=arrive`、`trip=1`、成就含 `a_one_small_step` | ✅ | 11.0s | 1218.79 | `final-e2e-hold.png` |
| 20 | e2e-moon | 无参数 + `build/e2e_moon.js` | `screen=flight`、`current=moon`、`target=mercury`、`srcGravity=0.165`、`baseSpeedKms∈[1.8,1.9]` | ✅ | 16.5s | 717.89 | `final-e2e-moon.png` |
| 21 | arrive-moon | `?stop=moon&screen=arrive` | `screen=arrive`、`current=moon`、`trip=1` | ✅ | 3.9s | 1124.29 | `final-arrive-moon.png` |
| 22 | arrive-mars | `?stop=mars&screen=arrive` | `current=mars` | ✅ | 4.0s | 987.01 | `final-arrive-mars.png` |
| 23 | arrive-andromeda | `?stop=andromeda&screen=arrive` | `current=andromeda` | ✅ | 3.8s | 954.51 | `final-arrive-andromeda.png` |
| 24 | arrive-edge | `?stop=observable_edge&screen=arrive` | `current=observable_edge`、`trip=28` | ✅ | 3.9s | 1093.20 | `final-arrive-edge.png` |
| 25 | shop-buy | `?screen=shop&rich=1&lv=3` + `buy('chatgpt')`/`buy('claude')`/`partner('chatgpt')` | `owned` 含两者、`partner=chatgpt`、`stardust=6999`（9999−1200−1800） | ✅ | 4.0s | 1234.93 | `final-shop-buy.png` |
| 26 | ending-final | `?screen=flight` + `jumpTo('observable_edge')`→`arriveNow()`→`goto('ending')` | 抵达 `trip=28` → `screen=ending` | ✅ | 4.2s | 860.57 | `final-ending-final.png` |
| 27 | m-title | `?screen=title` + 390×844 触摸模拟 | `screen=title` | ✅ | 3.6s | 1525.63 | `final-m-title.png` |
| 28 | m-launch | `?screen=launch` + 390×844 | `screen=launch` | ✅ | 3.6s | 3825.54 | `final-m-launch.png` |
| 29 | m-flight | `?screen=flight&progress=0.5` + 390×844 | `screen=flight` | ✅ | 3.6s | 962.22 | `final-m-flight.png` |
| 30 | m-shop | `?screen=shop&rich=1&lv=3` + 390×844 | `screen=shop` | ✅ | 3.7s | 1639.06 | `final-m-shop.png` |
| 31 | m-arrive | `?stop=moon&screen=arrive` + 390×844 | `screen=arrive` | ✅ | 3.7s | 1230.80 | `final-m-arrive.png` |
| 32 | l-hangar | `?screen=hangar` + 844×390 横屏 | `screen=hangar` | ✅ | 3.7s | 1203.29 | `final-l-hangar.png` |
| 33 | l-flight | `?screen=flight&progress=0.5` + 844×390 | `screen=flight` | ✅ | 3.8s | 983.48 | `final-l-flight.png` |
| 34 | save-verify | `?screen=flight` + `arriveNow()` + 读 `localStorage` | `saved.trip=1`、`saved.achievements` 含 `a_one_small_step` | ✅ | 3.8s | 872.60 | `final-save-verify.png` |

**40 条断言全部为真，34 个场景退出码均为 0。** 详细机器可读数据见 `reports/qa-final-summary.json`（含每场景完整 `evalResult`），逐场控制台输出见 `reports/qa-final-logs/*.log`。

---

## 4. 关键数据核验

| 验证项 | 期望（SPEC / 需求） | 实测 |
|---|---|---|
| 地球起跳基础速度 | 11.186 km/s（二宇宙速度） | **11.186** ✅ |
| 地球→月球航段 | 384,400 km | **38.44 万 km**，`legKm=384400` ✅ |
| 月面重力 / 起跳速度 | 重力 0.165；速度 ≈1.845 km/s | **0.165 / 1.84569 km/s** ✅ |
| 月球→水星航段 | 约 9,168.9 万 km | **9168.88 万 km** ✅ |
| 火星重力比（抵达页断言背景） | 0.907 | `srcGravity=0.907` ✅ |
| 银河系段单位与首站 | ly；半人马座α 4.365 ly | **4.36 光年**，`legUnit=ly` ✅ |
| 宇宙段距离 | 大麦哲伦云 16.3 万 ly；仙女座 253.7 万 ly；视界 465 亿 ly | **11.3 万 l.y.（从银河边缘起算）、233.7 万光年、461.79 亿光年** ✅ |
| 站点总数 / 终章 | 28 站，抵达视界即终章 | **trip=28、`screen=ending`** ✅ |
| 航程尺满量程（截图） | 随航段增长，满量程数值变化 | 地→月 **38.4 万 km**；月→水星 **1000.0 万 km** ✅ |
| 长按预演结果 | 进 flight、进度推进、抵达触发成就 | `afterHoldScreen=flight`、`afterArriveScreen=arrive`、`trip=1`、成就 `a_one_small_step`、星尘 322 ✅ |
| 商城扣费/拥有/伙伴 | 1200+1800 扣减；owned 含两者；partner=chatgpt | `9999 → 6999`、`owned=[deepseek,chatgpt,claude]`、`partner=chatgpt`、`primary=claude` ✅ |
| 存档落盘 | `fatfish_universe_save_v3` 中 trip=1、成就已保存 | `rawLen=277`、`savedTrip=1`、`savedAch=[a_one_small_step]` ✅ |

E2E 细节（来自 evalResult 原始返回）：

```jsonc
// e2e-hold：真实长按 3.6s → 起飞 → setProgress(0.93) → 自动抵达月球
{"afterHoldScreen":"flight","afterHoldProgress":0.0221,
 "afterArriveScreen":"arrive","trip":1,
 "achievements":["a_one_small_step"],"stardust":322}

// e2e-moon：地球→月球→点“从月球再次起跳”→长按再次起飞
{"leg1":{"screen":"flight","label":"38.44 万 km","baseSpeed":11.186},
 "arrivedMoon":{"screen":"arrive","trip":1,"ach":["a_one_small_step"]},
 "launchFromMoon":{"screen":"launch","current":"moon","target":"mercury",
                   "legLabel":"9168.88 万 km","srcGravity":0.165,"baseSpeed":1.84569},
 "flightFromMoon":{"screen":"flight","current":"moon","target":"mercury",
                   "srcGravity":0.165,"baseSpeed":1.84569}}
```

---

## 5. 截图视觉自查（8 张，含 Lead 要求的 4 张必查）

| 截图 | 观察结论 |
|---|---|
| `final-title.png` | 星空 + **真实地球卫星影像贴图**（非洲/欧洲清晰）＋月球贴图＋金鱼娘立绘＋按钮组，非空白/非全黑 ✅ |
| `final-flight.png` | **真实月球贴图**（环形山）＋ HUD（23.02 万 km、基础速度 11.19 km/s、3 心、燃料条）＋右侧航程尺（38.4 万→0 刻度、59.9% 标记）＋外星飞船/收集物 ✅ |
| `final-arrive-moon.png` | **真实月面贴图**大图＋抵达面板（航段 38.44 万 km、重力 16.5%、冷知识、+140 星辰币、下一站水星 9168.88 万 km）＋「从月球再次起跳」按钮 ✅ |
| `final-launch-zoom.png` | **太阳系航线预演全景**：太阳＋八大行星真实贴图＋公转轨道＋白色虚线贴地航线（预测航道：地球→月球 38.44 万 km、基础速度 11.19 km/s）✅ |
| `final-launch-galaxy-zoom.png` | **银河系全景**：银河旋臂＋恒星分布＋白色虚线「冥王星→半人马座α 4.36 光年、0.70 km/s」✅ |
| `final-launch-universe-zoom.png` | **可观测宇宙全景**：宇宙视界圆＋星系团分布（真实星系图）＋白色虚线「银河系边缘→大麦哲伦云 11.3 万光年」✅ |
| `final-arrive-andromeda.png` | **真实仙女座星系照片**（红外/伪彩盘面）＋抵达面板（233.7 万光年、与银河系 45 亿年后相撞冷知识）✅ |
| `final-e2e-moon.png` | 月→水星飞行：基础速度 **1.85 km/s**、航段 9168.88 万 km、航程尺满量程 **1000.0 万 km**、3.5% 进度、月球贴图与星空 ✅ |

结论：所有抽查截图均**有真实天体贴图、UI 文字可读、无空白/全黑**；移动端与横屏截图（390×844 / 844×390）布局无溢出、主按钮可见。

---

## 6. 错误汇总

| 指标 | 结果 |
|---|---|
| console.error / console.assert | **0** |
| 未捕获异常（Runtime.exceptionThrown） | **0** |
| Log error | **0** |
| 资源加载失败（含 file:// 缺失贴图） | **0** |
| 导航/加载超时 | **0** |
| 断言失败 | **0** |
| 截图空白判定失败 | **0** |
| 截图方差范围（阈值 5） | 395.06 – 3825.54（远高于阈值） |
| smoke 画面方差 | canvas **1441.44** / 截图 **1442.55** |
| 非 0 退出场景 | **0 / 34** |

**最终一轮无任何失败项，故无失败控制台原文需要粘贴。** 历史失败记录见下节。

---

## 7. 历史失败与处置（透明记录）

**① 第一轮 e2e-hold / e2e-moon 失败（旧版 E2E 脚本，无自初始化）**
被测文件当时已在冻结版 `794C…`，但 `build/e2e_*.js` 还是旧版：脚本假设起始在 launch 界面，实际停在 title，长按打在标题页所以无反应。失败断言原文：

```
[assert] 断言 #1 为假：window.__FATFISH__.state().screen === 'arrive'（值=false）
[assert] 断言 #2 为假：window.__FATFISH__.state().trip === 1（值=false）
[assert] 断言 #3 为假：window.__FATFISH__.state().achievements.indexOf('a_one_small_step') >= 0（值=false）
（e2e-moon 同类 5 条，evalResult 显示 leg1.screen="title"、baseSpeed=11.186）
```
Lead 已确认是脚本自初始化缺失、非游戏 bug；更新脚本后重跑 **全部通过**（见 §3 #19/#20）。

**② 存档两轮 profile 复用失败**
`save-run2` 出现 `[harness] Error: CDP WebSocket 连接失败：(无详细信息)` —— 同一 `--user-data-dir` 二次启动时 profile 锁/调试端口竞争。按 Lead 指定的**单页面内读 localStorage** 口径改为 `save-verify`，**通过**（savedTrip=1、成就已落盘）。

**③ 构建哈希沿革**
上述第一轮全量 31/34 通过时，被测文件已是 `794CDF8C…`（`stableDuringRun=true`）；后续收到 Lead 更新说明后，用新脚本 + 新存档口径**全量重跑 34 项，全部通过**。本报告数据全部来自最后一次全量运行（19:51–19:55，同一 SHA256）。

---

## 8. 已知限制与残余风险

1. **环境差异**：headless Chrome 156 + `file://` 直开，与真实双击浏览器/WorkBuddy 线上环境仍有差异（字体、GPU 合成、音频设备）；移动端是 390×844 视口 + 触摸事件模拟，**不是真机**。
2. **路径覆盖**：多数场景用 URL 参数 + `__FATFISH__` 调试 API 直达界面；真实用户交互路径只覆盖了 E2E 的长按/点击两处。真实首次游玩流程（点按钮逐屏进入）未逐步点击验证。
3. **随机元素**：UFO/星辰币/星空为随机生成，同场景截图逐次不同（方差 ±10 左右波动属正常）；截图只做「非空白 + 视觉抽查」，不做像素级回归。
4. **音频**：headless 静音，音效未验听感。
5. **未覆盖**：长时间挂机内存泄漏、真机触屏手势（双指/滑动）、服务器部署与跨域、断网重连、双人伙伴同时飞行的画面（`partner` 状态已断言，未单独截飞行图）。
6. **存档验证口径**：单页面内读回 localStorage（Lead 指定），未验证「关浏览器后再开」的冷启动读取；但因 `loadSave()` 逻辑与写入同一 key，风险极低。
7. 每轮使用全新临时 profile，测试不会污染本机存档；结束时 Chrome 进程树与临时目录均已清理（已核验无残留）。

---

## 9. 产物清单

| 路径 | 数量 | 说明 |
|---|---|---|
| `reports/qa-final-*.json` | 34 | 每场景完整报告（errors/logs/evalResult/assertions/screenshotStats/args） |
| `reports/qa-final-summary.json` | 1 | 总汇总（34 项通过率、耗时、哈希、每场景 evalResult 摘要） |
| `reports/shots/final-*.png` | 34（21.6 MB） | 各场景截图，1280×800 / 390×844 / 844×390 |
| `reports/qa-final-logs/*.log` | 34 | 各场景控制台原文（cdp_check 输出） |
| `tools/qa_final_run.ps1` | 1 | 批量执行器（本报告全部数据由它生成） |
| `tools/cdp_check.mjs` | 1 | CDP 检查工具（含本次新增的优雅关闭 Chrome，便于 localStorage 落盘场景） |

---

## 10. 复现

```powershell
Set-Location 'C:\Users\admin\Desktop\FatFish-Playable'
# 全量 34 项（约 3 分钟）
powershell -NoProfile -ExecutionPolicy Bypass -File tools\qa_final_run.ps1

# 单场景示例（商城购买）
$node = 'C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe'
& $node tools/cdp_check.mjs `
  --url "file:///C:/Users/admin/Desktop/FatFish-Playable/index.html?screen=shop&rich=1&lv=3" `
  --scenario load --wait-ms 2000 `
  --eval "(() => { const f = window.__FATFISH__; f.buy('chatgpt'); f.buy('claude'); f.partner('chatgpt'); return f.state(); })()" `
  --assert "window.__FATFISH__.state().stardust === 6999" `
  --shot reports/shots/check-shop.png --out reports/qa-check-shop.json
```

---

*报告生成：qa-harness ｜ 2026-11-18 ｜ 被测版本 v3.0.0（页面右下角版本标记一致）*
