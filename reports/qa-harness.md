# QA 测试工具说明 · `tools/cdp_check.mjs`

> 负责人：qa-harness ｜ 状态：**可用，原版基线已通过** ｜ 最后更新：2026-11-18

零第三方依赖的 Chrome headless CDP 检查器。用 Node 24 内置的 `fetch` + `WebSocket` 直连
DevTools Protocol，完成「启动 Chrome → 打开页面 → 收集报错 → 执行断言/取值 → 截图 → 输出 JSON → 按成败设退出码」。

本文件说明怎么用、报告长什么样、判定口径和已知限制；基线数据在 `reports/qa-baseline.json`。

---

## 1. 交付物

| 文件 | 说明 |
|---|---|
| `tools/cdp_check.mjs` | 检查器本体（单文件，约 1500 行，无依赖） |
| `reports/qa-baseline.json` | 原版 `index_original_backup.html` 的 smoke 基线报告 |
| `reports/shots/original.png` | 原版基线截图（1280×800） |
| `reports/qa-harness.md` | 本文件 |

环境（已实测）：

- Node：`C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe`（v24.21.0）
- Chrome：`C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`（156.0.8078.74）
- 工作目录：`C:\Users\admin\Desktop\FatFish-Playable`（命令都在这里执行）

---

## 2. 快速开始

### 2.1 跑原版基线（复现）

```powershell
Set-Location 'C:\Users\admin\Desktop\FatFish-Playable'
$node = 'C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe'

& $node tools/cdp_check.mjs `
  --url "file:///C:/Users/admin/Desktop/FatFish-Playable/index_original_backup.html" `
  --scenario smoke --wait-ms 2000 `
  --shot reports/shots/original.png --out reports/qa-baseline.json
# 正常输出最后一行：✅ OK smoke | 3.2s | errors=0 | ... | canvasVariance=1255.64 截图方差=1254.86
```

### 2.2 跑改版回归（示例）

```powershell
$url = "file:///C:/Users/admin/Desktop/FatFish-Playable/index.html"

# 场景名会自动拼 ?screen=<name>（URL 没 query 时），并截图 + 断言游戏内状态
& $node tools/cdp_check.mjs --url $url `
  --scenario shop --wait-ms 2500 `
  --shot reports/shots/shop.png --out reports/qa-shop.json `
  --assert "window.__FATFISH__ && window.__FATFISH__.state().screen === 'shop'"

# 需要其它 query 时直接写全（URL 带 query 就不会再自动拼）
& $node tools/cdp_check.mjs --url "$url?stop=moon&autoplay=1" `
  --scenario arrival --wait-ms 3000 `
  --shot reports/shots/arrival.png --out reports/qa-arrival.json `
  --eval "window.__FATFISH__.state()" `
  --assert "window.__FATFISH__.state().screen === 'arrival'"
```

### 2.3 一批场景批量跑（PowerShell 模板）

```powershell
$url = "file:///C:/Users/admin/Desktop/FatFish-Playable/index.html"
$scenes = 'title','hangar','launchpad','flight','arrival','shop','achievement','partner','zoom-preview'
$fails = @()
foreach ($s in $scenes) {
  & $node tools/cdp_check.mjs --url $url --scenario $s --wait-ms 2500 `
    --shot "reports/shots/$s.png" --out "reports/qa-$s.json"
  if ($LASTEXITCODE -ne 0) { $fails += $s }
}
if ($fails.Count) { "失败场景：$($fails -join ', ')" } else { '全部通过' }
```

> 别在循环里写 `$node` 变量名冲突：PowerShell 里 `$node` 和 `$null` 不冲突，可放心用；
> 若要串成一行可改成 `$n = '...node.exe'`。

### 2.4 移动端视口

```powershell
& $node tools/cdp_check.mjs --url $url --scenario smoke --wait-ms 2000 `
  --mobile --width 390 --height 844 `
  --shot reports/shots/mobile.png --out reports/qa-mobile.json
```

---

## 3. CLI 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--url <url\|path>` | 必填 | `http(s)://`、`file:///` 原样使用；其他按本地路径转 `file://`（不存在直接报错） |
| `--scenario <name>` | `smoke` | 内置 `smoke`（加载→等 2s→截图→像素方差非空白检查）、`load`（只加载截图）。其他名字=自定义场景，URL 无 query 时自动追加 `?screen=<name>` |
| `--wait-ms <n>` | smoke 2000，其他 3000 | `readyState === 'complete'` 之后再等的毫秒数 |
| `--timeout-ms <n>` | 60000 | 整轮总超时，到点强杀 Chrome、落盘失败报告、exit 1 |
| `--shot <path>` | `reports/shots/<scenario>.png` | 截图路径（自动建目录） |
| `--no-shot` | 关 | 不截图 |
| `--out <path>` | `reports/qa-<scenario>.json` | JSON 报告路径 |
| `--eval "<js>"` | 无 | `Runtime.evaluate({awaitPromise:true, returnByValue:true})`，可重复；1 条→`evalResult` 是值本身，多条→数组 |
| `--eval-file <path>` | 无 | 从文件读 JS 当 `--eval`（长脚本用） |
| `--assert "<js>"` | 无 | 可重复；求值为假即失败（exit 1），结果记入 `assertions[]` |
| `--allow-console-errors` | 关 | `console.error` / `console.assert` / `Log` 的 error 不判失败（**未捕获异常仍判失败**） |
| `--allow-network-errors` | 关 | 资源加载失败不判失败 |
| `--var-threshold <num>` | `5` | 空白判定：亮度方差 ≤ 阈值视为空白（0–255 亮度尺度） |
| `--width` / `--height` | 1280×800 | 视口（`Emulation.setDeviceMetricsOverride`，截图尺寸同此） |
| `--mobile` | 关 | 移动端模拟（视口 + 触摸模拟） |
| `--chrome <path>` | 自动找 | 也可用环境变量 `FATFISH_CHROME` / `CHROME_PATH` |
| `--user-data-dir <path>` | 临时目录 | 复用 profile（不删除）；默认每轮新建临时目录并在结束时删掉 → **存档/进度类测试请复用** |
| `--keep-chrome` | 关 | 不杀 Chrome、不删 profile（排障用） |
| `--verbose` | 关 | 打印每条 CDP 事件 |
| `--help` | — | 帮助 |

退出码：`0` 通过；`1` 测试失败（含超时、页面报错、断言失败、环境错误）；`2` 命令行参数解析错误。

---

## 4. JSON 报告字段

```jsonc
{
  "ok": true,                    // 总判定：无 errors 且未超时
  "tool": "cdp_check.mjs", "toolVersion": 1,
  "scenario": "smoke",
  "url": "file:///...",          // 实际打开的 URL（含自动追加的 query）
  "title": "肥鱼跳宇宙 · 星尘远航",
  "startedAt": "...", "finishedAt": "...", "durationMs": 3232,
  "viewport": { "width": 1280, "height": 800, "mobile": false },
  "chrome": { "path": "...", "browser": "Chrome/156...", "protocolVersion": "1.3" },
  "errors": [                    // 失败原因列表（决定 exit code）
    { "kind": "exception", "message": "...", "url": "...", "line": 123, "column": 4, "stack": [...] },
    { "kind": "console.error", "message": "..." },
    { "kind": "log.error", "message": "..." },
    { "kind": "network", "message": "资源加载失败：<url> → net::ERR_FILE_NOT_FOUND" },
    { "kind": "blank-canvas", "message": "canvas 像素方差 ... ≤ 阈值 ..." },
    { "kind": "assert", "message": "断言 #1 为假：..." },
    { "kind": "eval", "message": "--eval 第 1 条执行失败：..." },
    { "kind": "timeout", "message": "整轮超时（60000ms），强制结束" }
  ],
  "logs": [                      // 全部 console / 异常 / Log 条目（不区分是否失败）
    { "source": "console", "type": "log", "text": "loaded ok", "url": null, "line": null }
  ],
  "warnings": [ ... ],           // 不判失败但值得注意：自定义场景、对话框、PNG 解码失败等
  "networkFailures": [           // Network.loadingFailed 原始条目
    { "url": "...", "errorText": "net::ERR_FILE_NOT_FOUND", "type": "Image", "canceled": false }
  ],
  "evalResult": null,            // --eval 结果（无 --eval 时 null）
  "assertions": [ { "index": 1, "expression": "...", "ok": true, "value": true } ],
  "checks": {
    "consoleErrorCount": 0, "exceptionCount": 0, "networkFailureCount": 0,
    "loadTimedOut": false, "readyState": "complete",
    "varThreshold": 5, "blankCheck": true,
    "canvasVariance": 1255.64,      // 页面 canvas 亮度方差（smoke 探针）
    "screenshotVariance": 1254.86   // 截图 PNG 亮度方差（内置 PNG 解码算的）
  },
  "screenshot": "C:\\...\\reports\\shots\\original.png",  // 绝对路径，null=没截
  "screenshotStats": { "width": 1280, "height": 800, "bytes": 229958, "variance": 1254.86, ... },
  "exitCode": 0,
  "node": "v24.21.0",
  "cmdline": ["--url", "...", "--scenario", "smoke"],   // 原样命令行，便于复现
  "args": { ... }                  // 解析后的参数
}
```

错误 kind 全集：`console.error` / `console.assert` / `exception` / `log.error` / `network` /
`blank-canvas` / `blank-screenshot` / `navigate` / `load-timeout` / `probe` / `eval` / `assert` /
`crash` / `timeout` / `harness` / `uncaught` / `signal`。

---

## 5. 判定口径

**算失败**（exit 1）：
1. `Runtime.exceptionThrown`（未捕获异常）—— 永远失败，`--allow-console-errors` 也救不了；
2. `console.error` / `console.assert` / `Log.entryAdded(level=error)` —— 除非 `--allow-console-errors`；
3. `Network.loadingFailed` 且 `canceled !== true` —— 除非 `--allow-network-errors`；
4. smoke / 自定义场景的空白判定（仅 `smoke` 开启）：canvas 或截图的亮度方差 ≤ `--var-threshold`；
5. `--assert` 为假、`--eval` 抛异常、导航失败、`readyState` 超时未 complete、整轮超时。

**只记录不判失败**：`warnings[]`（自定义场景提示、`alert/confirm` 对话框、PNG 解码失败等）、`logs[]` 全量。

**非空白怎么算**：两条腿，都过才算过。

- canvas：页面内 `getImageData` 采样（最多 20 万像素）算亮度方差 + `toDataURL().length`；
- 截图：Node 侧用内置最小 PNG 解码器（`zlib.inflateSync` + 逐行反滤波，支持 8bit 灰度/RGB/RGBA，
  即 Chrome 截图的实际格式）算亮度方差。

两条腿的意义不同：canvas 方差低 = 游戏没画东西；截图为空白 = 没合成到屏幕上（canvas 隐藏/被盖住/尺寸 0）。
所以两个都查。原版基线两项都 ~1255，阈值 5 留了 250 倍余量，画面只有一点点内容也能过。

---

## 6. 实现要点（排障时看）

- **启动**：`--headless=new --remote-debugging-port=0 --user-data-dir=<临时目录>` + `--no-first-run
  --disable-gpu --no-sandbox --allow-file-access-from-files --remote-allow-origins=*`（后两个是 file:// 读像素
  和新版 Chrome 允许外部 WebSocket 的关键）。调试地址从 stderr 的 `DevTools listening on ws://...` 解析，
  失败则读 `<user-data-dir>\DevToolsActivePort` 兜底。
- **CDP**：browser 级 WebSocket → `Target.createTarget(about:blank)` → `Target.attachToTarget(flatten:true)`
  拿 sessionId → 逐条 `sessionId` 发命令。不依赖 `/json/new`（新版 Chrome 要求 PUT，容易踩坑）。
- **等加载**：`Page.navigate` 后轮询 `document.readyState === 'complete'`（避免 load 事件早于监听器的竞态），
  再按 `--wait-ms` 等 rAF/动画稳定。
- **PNG 解码**：只支持非隔行、8bit、colorType 0/2/4/6；解不了记 `warnings`，不影响 canvas 那条腿。
- **清理**：正常结束、异常、信号、超时 watchdog 四条路径都会 `taskkill /pid <pid> /T /F` 杀整棵 Chrome 进程树
  并重试删除临时 profile；已实测无残留进程/目录。

---

## 7. 已知限制

1. **只覆盖无头 Chrome**（本机 Windows Chrome 156）。`--mobile` 是视口+触摸模拟，不是真机；
   触屏手势/软键盘行为拿不到，真机问题需要人工验。
2. **不做输入模拟**：无 `--key`/`--click`。需要按键/长按的流程用 `--eval` 在页面里派发事件
   （`new KeyboardEvent(...)`、`canvas.dispatchEvent(...)`），或让 Lead 在 `__FATFISH__.debug` 里暴露
   直达接口后断言状态。长按预演这类时序逻辑，最稳的是加 debug 接口而不是硬模拟鼠标。
3. **单 canvas**：探针只测 `document.querySelector('canvas')`（第一个）。原版就一个 `#game`；
   若改版用多 canvas 且主画面不是第一个，需给 `--eval` 自己指定。
4. **WebGL 兜底**：若 canvas 是 WebGL 且 `preserveDrawingBuffer:false`，`getImageData`/`toDataURL` 拿不到像素，
   探针记 `canvas.error`，此时只靠截图方差判空白（不额外判失败）。
5. **截图只截视口**（`captureBeyondViewport:false`）。视口 1280×800，超出部分不截；长页面用 `--height` 加高。
6. **每轮全新 profile**：localStorage 默认是空的、结束即删。测「存档保留/商城已购」要用 `--user-data-dir`
   复用同一个目录，并自己清理其中状态。
7. **报告里的路径是绝对路径**（`screenshot`、`screenshotStats.path`），直接点开可用；写文档引用时注意。
8. **重复计错**：资源 404 会同时出 `network` 和 `log.error` 两条（Chrome 两个域都报），`errors` 按
   「kind+message+url+line」去重，跨类不去重 —— 看总数时别被吓到。
9. **首帧时机依赖机器负载**：headless 下 rAF 正常跑，但动画进度和 `--wait-ms` 不严格对应；
   对具体数值有要求的断言，宁可读 `__FATFISH__.state()` 而不是截图比像素。
10. **不联网**：所有页面都从本地加载，网络失败仅指本地文件缺失（`net::ERR_FILE_NOT_FOUND`）之类。

---

## 8. 基线结果（2026-11-18）

命令见 2.1。结果：**通过（exit 0）**。

| 项目 | 值 |
|---|---|
| 页面 | `file:///C:/Users/admin/Desktop/FatFish-Playable/index_original_backup.html` |
| 标题 | 肥鱼跳宇宙 · 星尘远航 |
| `readyState` | complete |
| console 错误 / 未捕获异常 | 0 / 0 |
| 资源加载失败 | 0 |
| canvas 亮度方差 | 1255.64（阈值 5） |
| 截图亮度方差 | 1254.86 |
| 截图 | `reports/shots/original.png`，1280×800，229,958 B |
| 用时 | 3.23 s |

截图内容：天空渐变 + 云 + DeepSeek 金鱼娘立绘 +「开始试飞」按钮 + 底部操作说明，与原版一致。

---

## 9. 工具自测记录（证明失败口径也没问题）

| 用例 | 命令要点 | 预期 | 实测 |
|---|---|---|---|
| 原版基线 | `--scenario smoke` | exit 0，无错误 | ✅ exit 0 |
| 自定义场景 + query | `--scenario shop`（URL 无 query） | 自动打开 `?screen=shop` | ✅ url 含 `?screen=shop`，exit 0 |
| `--eval` + `--assert` | `--eval "({...})" --assert "!!document.querySelector('canvas')"` | 取值进 `evalResult`，断言 ok | ✅ 两项都正确 |
| console.error | `--eval "console.error('故意报错'); 42"` | exit 1，`errors[0].kind=console.error` | ✅ |
| 同上 + 放行 | 加 `--allow-console-errors` | exit 0 | ✅ |
| eval 抛异常 | `--eval "throw new Error('故意异常')"` | exit 1 | ✅ |
| 本地路径不存在 | `--url no_such_file.html` | exit 1，`kind=harness` | ✅ |
| 缺资源页面 | 临时 HTML 引 `missing_texture.png` | exit 1，`network` + `log.error` | ✅ 捕获 `ERR_FILE_NOT_FOUND` |
| 移动端视口 | `--mobile --width 390 --height 844` | 截图 390×844、无错误 | ✅ 方差 2729.29，exit 0 |
| 超时兜底 | `--timeout-ms 1500 --wait-ms 5000` | exit 1，报告 `kind=timeout`，无残留进程 | ✅ |
| 清理 | 每轮结束查 `chrome.exe` 命令行含 `fatfish-cdp`、`%TEMP%\fatfish-cdp-*` | 无残留 | ✅ 全部干净 |

---

## 10. 进阶用法

**读游戏状态做详细断言**（推荐配合 `__FATFISH__`）：

```powershell
& $node tools/cdp_check.mjs --url $url --scenario flight --wait-ms 3000 `
  --shot reports/shots/flight.png --out reports/qa-flight.json `
  --eval "JSON.stringify(window.__FATFISH__.state())" `
  --assert "window.__FATFISH__.state().screen === 'flight'"
```

**长脚本用 `--eval-file`**：把断言/取值写进 `.mjs` 片段文件（内容就是一条表达式，可直接用 IIFE）。
**调试工具本身**：`--verbose` 看 CDP 事件流；`--keep-chrome` 留下 Chrome 和 profile 用 DevTools 手动看页面。
