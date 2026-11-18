# 肥鱼跳宇宙 v4 · 自动化回归报告（qa-harness）

**轮次标签**：final2

✅ **全部通过**

- 生成时间：2026-11-18T13:33:55.145Z（用时 160.1s）
- 构建产物：`C:\Users\admin\Desktop\FatFish-Playable\index.html`（3438.9 KB，mtime 2026-11-18T13:30:42.902Z）
- Node v24.21.0 / win32x64；Chrome：`C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`
- 场景 34 个：✅ pass 34 · ⏳ pending 0 · ⚠️ warn 0 · ❌ fail 0
- 退出码：**0**（0 = 无 fail；pending / warn 不算失败）

## 1. 能力探测（决定 pending 口径）

| 能力 | 结果 | 说明 |
|---|---|---|
| 版本 | 4.0.0 | engine VERSION |
| 实时天文 API（页面） | ✅ 已就绪 | state().live.live / legs=9 / totalAU>0 |
| 实时天文 API（src/astronomy.js） | ✅ 已就绪 | Node 侧独立交叉验证用 |
| star_* 恒星贴图 | ✅ 已就绪 | state().starTextures >= 10 |
| 9 角色立绘 | ✅ 已就绪 | charCount=9 且 charImages>=8 |
| setShopPage 调试 API | ✅ 可用 | 商城翻页断言用 |

## 2. 场景 × 断言总表

| # | 场景 | 分组 | 状态 | 断言（通过/待集成/失败） | 截图 | 用时 |
|---|---|---|---|---|---|---|
| 1 | 能力探测（调试 API / 贴图 / 立绘 / 实时天文） | caps | ✅ pass | 18/0/0 | [shots/v4qa_caps.png](shots/v4qa_caps.png) | 6.8s |
| 2 | 桌面 · 标题 | desktop | ✅ pass | 6/0/0 | [shots/v4qa_title.png](shots/v4qa_title.png) | 4.5s |
| 3 | 桌面 · 机库 | desktop | ✅ pass | 7/0/0 | [shots/v4qa_hangar.png](shots/v4qa_hangar.png) | 4.5s |
| 4 | 桌面 · 发射台 | desktop | ✅ pass | 8/0/0 | [shots/v4qa_launch.png](shots/v4qa_launch.png) | 4.2s |
| 5 | 桌面 · 实时太阳系地图（launch + hold + live） | desktop | ✅ pass | 14/0/0 | [shots/v4qa_launch-live-map.png](shots/v4qa_launch-live-map.png) | 4.6s |
| 6 | 桌面 · ?screen=solar 实时太阳系图 | desktop | ✅ pass | 13/0/0 | [shots/v4qa_solar-live.png](shots/v4qa_solar-live.png) | 4.7s |
| 7 | 桌面 · 另一观测时刻（time=1900000000000） | desktop | ✅ pass | 8/0/0 | [shots/v4qa_launch-live-time.png](shots/v4qa_launch-live-time.png) | 4.2s |
| 8 | 桌面 · 商城（默认第 1 页） | desktop | ✅ pass | 9/0/0 | [shots/v4qa_shop-p1.png](shots/v4qa_shop-p1.png) | 4.4s |
| 9 | 桌面 · 商城第 2 页（setShopPage(1)） | desktop | ✅ pass | 8/0/0 | [shots/v4qa_shop-p2.png](shots/v4qa_shop-p2.png) | 4.5s |
| 10 | 桌面 · 商城第 3 页（setShopPage(2)） | desktop | ✅ pass | 8/0/0 | [shots/v4qa_shop-p3.png](shots/v4qa_shop-p3.png) | 4.4s |
| 11 | 桌面 · 角色改装界面 | desktop | ✅ pass | 8/0/0 | [shots/v4qa_upgrade.png](shots/v4qa_upgrade.png) | 4.4s |
| 12 | 桌面 · 升级扣币并生效（chatgpt hp） | desktop | ✅ pass | 11/0/0 | [shots/v4qa_upgrade-action.png](shots/v4qa_upgrade-action.png) | 4.3s |
| 13 | 桌面 · 飞行（stop=moon progress=0.5） | desktop | ✅ pass | 12/0/0 | [shots/v4qa_flight-moon.png](shots/v4qa_flight-moon.png) | 4.6s |
| 14 | 桌面 · 飞行（stop=jupiter 实时航段） | desktop | ✅ pass | 10/0/0 | [shots/v4qa_flight-jupiter.png](shots/v4qa_flight-jupiter.png) | 4.8s |
| 15 | 桌面 · 恒星飞行（stop=sirius progress=0.7，银河贴图） | desktop | ✅ pass | 9/0/0 | [shots/v4qa_flight-sirius.png](shots/v4qa_flight-sirius.png) | 4.8s |
| 16 | 桌面 · 抵达（stop=mars） | desktop | ✅ pass | 6/0/0 | [shots/v4qa_arrive-mars.png](shots/v4qa_arrive-mars.png) | 4.5s |
| 17 | 桌面 · 结局 | desktop | ✅ pass | 5/0/0 | [shots/v4qa_ending.png](shots/v4qa_ending.png) | 4.6s |
| 18 | 桌面 · 帮助 | desktop | ✅ pass | 5/0/0 | [shots/v4qa_help.png](shots/v4qa_help.png) | 4.4s |
| 19 | 桌面 · 成就 | desktop | ✅ pass | 6/0/0 | [shots/v4qa_achv.png](shots/v4qa_achv.png) | 4.4s |
| 20 | 桌面 · 伙伴同行 + 自动反击击毁 UFO | feature | ✅ pass | 8/0/0 | [shots/v4qa_partners-ufo.png](shots/v4qa_partners-ufo.png) | 11.5s |
| 21 | 桌面 · 护盾叠加受 wokCap 约束 | feature | ✅ pass | 8/0/0 | [shots/v4qa_shield-cap.png](shots/v4qa_shield-cap.png) | 4.5s |
| 22 | 桌面 · 续飞（saveFlight → resumeFlight） | feature | ✅ pass | 12/0/0 | [shots/v4qa_resume-flight.png](shots/v4qa_resume-flight.png) | 4.5s |
| 23 | 持久化 1/3 · 飞行中存档（复用 profile） | persist | ✅ pass | 10/0/0 | [shots/v4qa_save-p1.png](shots/v4qa_save-p1.png) | 4.3s |
| 24 | 持久化 2/3 · 同一 profile 重开标题并续飞 | persist | ✅ pass | 11/0/0 | [shots/v4qa_save-p2.png](shots/v4qa_save-p2.png) | 4.7s |
| 25 | 持久化 3/3 · ?resume=1 URL 参数续飞 | persist | ✅ pass | 8/0/0 | [shots/v4qa_save-p3.png](shots/v4qa_save-p3.png) | 4.8s |
| 26 | 桌面 · ?flight=1 构造飞行中存档（标题页显示继续飞行） | persist | ✅ pass | 8/0/0 | [shots/v4qa_url-flight.png](shots/v4qa_url-flight.png) | 4.3s |
| 27 | 桌面 · 非飞行界面静态背景（无背景流星） | feature | ✅ pass | 7/0/0 | [shots/v4qa_bg-static.png](shots/v4qa_bg-static.png) | 4.6s |
| 28 | 桌面 · 飞行 8s 记录背景流星（仅记录） | feature | ✅ pass | 5/0/0 | [shots/v4qa_bg-meteors.png](shots/v4qa_bg-meteors.png) | 11.9s |
| 29 | 移动端 · 标题 | mobile | ✅ pass | 5/0/0 | [shots/v4qa_m-title.png](shots/v4qa_m-title.png) | 4.2s |
| 30 | 移动端 · 商城（窄屏列表） | mobile | ✅ pass | 7/0/0 | [shots/v4qa_m-shop.png](shots/v4qa_m-shop.png) | 4.2s |
| 31 | 移动端 · 角色改装 | mobile | ✅ pass | 6/0/0 | [shots/v4qa_m-upgrade.png](shots/v4qa_m-upgrade.png) | 4.2s |
| 32 | 移动端 · 飞行 | mobile | ✅ pass | 6/0/0 | [shots/v4qa_m-flight.png](shots/v4qa_m-flight.png) | 4.3s |
| 33 | 构建产物静态扫描（贴图 / 调试入口 / v4 参数 / 静态背景） | static | ✅ pass | 13/0/0 | — | — |
| 34 | 跨场景交叉断言（实时总航程 / 复现性 / 全场报错） | cross | ✅ pass | 4/0/0 | — | — |

> 断言列格式：通过 / 待集成 / 失败；截图相对 `reports/`。

## 3. 逐场景断言明细

### ✅ 能力探测（调试 API / 贴图 / 立绘 / 实时天文） `caps`

- URL：`index.html?screen=title&unlock=1&live=1`
- 截图：`reports/shots/v4qa_caps.png`（像素方差 1448.4）
- cdp 报告：`reports/qa-v4-logs/caps.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1448.42 |  |
| 页面 = title | ✅ pass | title | title |  |
| f.version 以 4. 开头 | ✅ pass | 4.x | 4.0.0 |  |
| 调试 API 齐备（state/liveInfo/setTime/upgrade/giveStardust/setCompanions/spawnUFO/killUFO/saveFlight/resumeFlight/giveShield/clearSave/unlockAll/setPrimary/setProgress） | ✅ pass | 全部 function | 全部齐备 |  |
| setShopPage(n) 存在（v4 商城分页 QA 入口） | ✅ pass | function | function |  |
| CHARACTERS = 9 位角色（state().charCount） | ✅ pass | 9 | 9 |  |
| 8 位新角色立绘已加载（state().charImages >= 8，deepseek 用 hero） | ✅ pass | >=8 | 8 |  |
| unlockAll 后 state().owned 含 9 个角色 id | ✅ pass | 9 个 id | 9 个 |  |
| star_* 恒星贴图 >= 10（state().starTextures） | ✅ pass | >=10 | 13 |  |
| state().live.live === true（实时天文已接入） | ✅ pass | true | true |  |
| liveInfo().legs 共 9 段（实时总航程可算） | ✅ pass | 9 | 9 |  |
| state().live.totalAU > 0 | ✅ pass | >0 | 93.76059524213221 |  |
| state().live.planets 共 9 颗行星 | ✅ pass | 9 | 9 |  |
| ?live=1 固定观测时刻 = 2026-11-18T12:00:00Z | ✅ pass | 1795003200000 | 1795003200000 | clockMs=1795003200000 |
| 观测时刻可显示（state().live.iso 非空） | ✅ pass | 含日期的观测时刻 | 2026-11-18 12:00:00 UTC |  |
| SPEC §9 的 setShield(n)（仅记录，giveShield 已可用） | ❌ info | undefined | {"giveShield":"function"} | SPEC 写的是 setShield，engine 实际提供 giveShield |

### ✅ 桌面 · 标题 `title`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v4qa_title.png`（像素方差 1442.9）
- cdp 报告：`reports/qa-v4-logs/title.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1442.93 |  |
| 页面 = title | ✅ pass | title | title |  |
| 版本号 4.x | ✅ pass | 4.x | 4.0.0 |  |

### ✅ 桌面 · 机库 `hangar`

- URL：`index.html?screen=hangar&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v4qa_hangar.png`（像素方差 1239.2）
- cdp 报告：`reports/qa-v4-logs/hangar.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1239.23 |  |
| 页面 = hangar | ✅ pass | hangar | hangar |  |
| 机库可见已拥有角色（owned >= 9） | ✅ pass | >=9 | 9 |  |
| ?lv=5 生效（pilotLv >= 5） | ✅ pass | >=5 | 6 |  |

### ✅ 桌面 · 发射台 `launch`

- URL：`index.html?screen=launch`
- 截图：`reports/shots/v4qa_launch.png`（像素方差 3751.6）
- cdp 报告：`reports/qa-v4-logs/launch.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 3751.58 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| 目标 = moon（首段） | ✅ pass | moon | moon |  |
| 首段固定 384400 km | ✅ pass | 384400 | 384400 |  |
| 航段距离文案非空 | ✅ pass | 非空 | 38.44 万 km |  |

### ✅ 桌面 · 实时太阳系地图（launch + hold + live） `launch-live-map`

- URL：`index.html?screen=launch&hold=1&live=1`
- 截图：`reports/shots/v4qa_launch-live-map.png`（像素方差 1033.8）
- cdp 报告：`reports/qa-v4-logs/launch-live-map.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1033.78 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| hold=1 使缩放停在实时地图（zoom.p >= 0.8） | ✅ pass | >=0.8 | 0.86 |  |
| ?live=1 固定时钟 | ✅ pass | 1795003200000 | 1795003200000 |  |
| state().live.live === true | ✅ pass | true | true |  |
| 实时行星 9 颗（state().live.planets.length = 9） | ✅ pass | 9 | 9 |  |
| 实时总航程 totalAU > 0 | ✅ pass | >0 | 93.76059524213221 |  |
| liveInfo().legs 共 9 段 | ✅ pass | 9 | 9 |  |
| 第 0 段（地球→月球）固定 384400 km 且 fixed=true | ✅ pass | 384400/fixed | {"km":384400,"fixed":true} |  |
| 第 1 段实时弦长 km > 0 | ✅ pass | >0 | 140106177.85552102 |  |
| 行星黄经与 src/astronomy.js 计算一致（误差 <= 0.1°） | ✅ pass | 全部 <=0.1° | 最大 mercury 0° |  |

### ✅ 桌面 · ?screen=solar 实时太阳系图 `solar-live`

- URL：`index.html?screen=solar&live=1`
- 截图：`reports/shots/v4qa_solar-live.png`（像素方差 1038.7）
- cdp 报告：`reports/qa-v4-logs/solar-live.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1038.72 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| screen=solar 打开放大的太阳系地图（zoom.p >= 0.85） | ✅ pass | >=0.85 | 0.9 |  |
| state().live.live === true | ✅ pass | true | true |  |
| 实时行星 9 颗（state().live.planets.length = 9） | ✅ pass | 9 | 9 |  |
| 实时总航程 totalAU > 0 | ✅ pass | >0 | 93.76059524213221 |  |
| liveInfo().legs 共 9 段 | ✅ pass | 9 | 9 |  |
| 第 0 段（地球→月球）固定 384400 km 且 fixed=true | ✅ pass | 384400/fixed | {"km":384400,"fixed":true} |  |
| 第 1 段实时弦长 km > 0 | ✅ pass | >0 | 140106177.85552102 |  |
| 行星黄经与 src/astronomy.js 计算一致（误差 <= 0.1°） | ✅ pass | 全部 <=0.1° | 最大 mercury 0° |  |

### ✅ 桌面 · 另一观测时刻（time=1900000000000） `launch-live-time`

- URL：`index.html?screen=launch&live=1&time=1900000000000`
- 截图：`reports/shots/v4qa_launch-live-time.png`（像素方差 3751.6）
- cdp 报告：`reports/qa-v4-logs/launch-live-time.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 3751.58 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| ?time=1900000000000 覆盖固定时钟 | ✅ pass | 1900000000000 | 1900000000000 |  |
| state().live.live === true | ✅ pass | true | true |  |
| 该时刻实时总航程 totalAU > 0 | ✅ pass | >0 | 99.34779293282612 |  |

### ✅ 桌面 · 商城（默认第 1 页） `shop-p1`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v4qa_shop-p1.png`（像素方差 1001.7）
- cdp 报告：`reports/qa-v4-logs/shop-p1.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1001.72 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认第 1 页（shopPage = 0） | ✅ pass | 0 | 0 |  |
| 9 位角色 / 每页 3 张 = 3 页（shopPages = 3） | ✅ pass | 3 | 3 |  |
| charCount = 9 | ✅ pass | 9 | 9 |  |
| 角色立绘已加载（charImages >= 8） | ✅ pass | >=8 | 8 |  |

### ✅ 桌面 · 商城第 2 页（setShopPage(1)） `shop-p2`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v4qa_shop-p2.png`（像素方差 873.4）
- cdp 报告：`reports/qa-v4-logs/shop-p2.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 873.42 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认在第 1 页 | ✅ pass | 0 | 0 |  |
| 翻到第 2 页（setShopPage 生效） | ✅ pass | 1 | {"setReturn":1,"shopPage":1} |  |
| 页数 = 3 | ✅ pass | 3 | 3 |  |

### ✅ 桌面 · 商城第 3 页（setShopPage(2)） `shop-p3`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v4qa_shop-p3.png`（像素方差 850）
- cdp 报告：`reports/qa-v4-logs/shop-p3.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 849.96 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认在第 1 页 | ✅ pass | 0 | 0 |  |
| 翻到第 3 页（setShopPage 生效） | ✅ pass | 2 | {"setReturn":2,"shopPage":2} |  |
| 页数 = 3 | ✅ pass | 3 | 3 |  |

### ✅ 桌面 · 角色改装界面 `upgrade`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v4qa_upgrade.png`（像素方差 1116.9）
- cdp 报告：`reports/qa-v4-logs/upgrade.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1116.94 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| 可改装角色 9 位 | ✅ pass | 9 | 9 |  |
| state().upg 是对象 | ✅ pass | object | object |  |
| state().upgrades 含 maxHp/wokCap/accelMul | ✅ pass | maxHp/wokCap/accelMul | {"maxHp":4,"wokCap":1,"accelMul":1} |  |

### ✅ 桌面 · 升级扣币并生效（chatgpt hp） `upgrade-action`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v4qa_upgrade-action.png`（像素方差 1154）
- cdp 报告：`reports/qa-v4-logs/upgrade-action.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1153.99 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| unlockAll 后 owned 含 chatgpt | ✅ pass | true | true |  |
| 出战神切换为 chatgpt（setPrimary 生效） | ✅ pass | chatgpt | chatgpt |  |
| upgrade('chatgpt','hp') 返回 true | ✅ pass | true | true |  |
| 星辰币扣掉 hp 一级价格 120 | ✅ pass | -120 | -120 | before=100149 after=100029（已预先解锁 a_upgrade 排除成就奖励干扰） |
| state().upg.chatgpt.hp === 1 | ✅ pass | 1 | 1 | before=0 |
| state().upgrades.maxHp 增加 1 | ✅ pass | 5 | 5 |  |

### ✅ 桌面 · 飞行（stop=moon progress=0.5） `flight-moon`

- URL：`index.html?screen=flight&stop=moon&progress=0.5&live=1`
- 截图：`reports/shots/v4qa_flight-moon.png`（像素方差 817.6）
- cdp 报告：`reports/qa-v4-logs/flight-moon.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 817.64 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = moon | ✅ pass | moon | moon |  |
| 起点 = earth | ✅ pass | earth | earth |  |
| 月球段固定 384400 km | ✅ pass | 384400 | 384400 |  |
| 月球段 fixed（legLive = false） | ✅ pass | false | false |  |
| progress=0.5 生效（0.45~0.62） | ✅ pass | 0.45~0.62 | 0.5608 |  |
| maxHp = 3（deepseek 默认，pilotLv<5） | ✅ pass | 3 | 3 |  |
| 燃料 0~100 | ✅ pass | 0~100 | 98.1 |  |

### ✅ 桌面 · 飞行（stop=jupiter 实时航段） `flight-jupiter`

- URL：`index.html?screen=flight&stop=jupiter&live=1`
- 截图：`reports/shots/v4qa_flight-jupiter.png`（像素方差 691.6）
- cdp 报告：`reports/qa-v4-logs/flight-jupiter.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 691.56 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = jupiter | ✅ pass | jupiter | jupiter |  |
| 航段距离 > 0 | ✅ pass | >0 | 589582641.3313304 |  |
| 太阳系航段为实时测算（legLive = true） | ✅ pass | true | true |  |
| state().legKm 与 src/astronomy.js A.liveSolarLeg(idx) 一致（误差 <0.5%） | ✅ pass | 误差<0.5% | page=589582641.3km ref=589582641.3km 误差=0% |  |
| state().legKm 与 liveInfo().legs[idx].km 一致 | ✅ pass | {"idx":4,"km":589582641.3313304} | 589582641.3313304 |  |

### ✅ 桌面 · 恒星飞行（stop=sirius progress=0.7，银河贴图） `flight-sirius`

- URL：`index.html?screen=flight&stop=sirius&progress=0.7&live=1`
- 截图：`reports/shots/v4qa_flight-sirius.png`（像素方差 1853.4）
- cdp 报告：`reports/qa-v4-logs/flight-sirius.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1853.39 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = sirius（天狼星） | ✅ pass | sirius | sirius |  |
| 恒星航段距离 legLy > 0 | ✅ pass | >0 | 0.745000000000001 |  |
| progress=0.7 生效（0.66~0.80） | ✅ pass | 0.66~0.80 | 0.7503 |  |
| 航段文案含光年单位 | ✅ pass | 光年 | 0.75 光年 |  |

### ✅ 桌面 · 抵达（stop=mars） `arrive-mars`

- URL：`index.html?screen=arrive&stop=mars&unlock=1`
- 截图：`reports/shots/v4qa_arrive-mars.png`（像素方差 996.6）
- cdp 报告：`reports/qa-v4-logs/arrive-mars.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 996.55 |  |
| 页面 = arrive | ✅ pass | arrive | arrive |  |
| 星辰币非负 | ✅ pass | >=0 | 99999 |  |

### ✅ 桌面 · 结局 `ending`

- URL：`index.html?screen=ending&unlock=1`
- 截图：`reports/shots/v4qa_ending.png`（像素方差 975.4）
- cdp 报告：`reports/qa-v4-logs/ending.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 975.39 |  |
| 页面 = ending | ✅ pass | ending | ending |  |

### ✅ 桌面 · 帮助 `help`

- URL：`index.html?screen=help`
- 截图：`reports/shots/v4qa_help.png`（像素方差 1217）
- cdp 报告：`reports/qa-v4-logs/help.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1217.01 |  |
| 页面 = help | ✅ pass | help | help |  |

### ✅ 桌面 · 成就 `achv`

- URL：`index.html?screen=achv&unlock=1&live=1`
- 截图：`reports/shots/v4qa_achv.png`（像素方差 424.1）
- cdp 报告：`reports/qa-v4-logs/achv.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 424.13 |  |
| 页面 = achv | ✅ pass | achv | achv |  |
| state().achievements 是数组 | ✅ pass | array | object |  |

### ✅ 桌面 · 伙伴同行 + 自动反击击毁 UFO `partners-ufo`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v4qa_partners-ufo.png`（像素方差 1092.9）
- cdp 报告：`reports/qa-v4-logs/partners-ufo.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 1092.92 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| setCompanions([chatgpt,claude]) 后随行伙伴 2 名 | ✅ pass | 2 | 2 |  |
| 伙伴自动反击击毁 UFO（ufoKills 增加）或 UFO 已离场（ufos=0） | ✅ pass | kills>0 | kills=1（尝试 1 次，5742ms） |  |
| 伙伴护盾数组存在（compShields 可持久化） | ✅ pass | 2 槽数组 | [0,0] |  |

### ✅ 桌面 · 护盾叠加受 wokCap 约束 `shield-cap`

- URL：`index.html?screen=flight&stop=moon&unlock=1&rich=1`
- 截图：`reports/shots/v4qa_shield-cap.png`（像素方差 615.4）
- cdp 报告：`reports/qa-v4-logs/shield-cap.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 615.44 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 护盾上限 wokCap >= 1 | ✅ pass | >=1 | 1 |  |
| giveShield(12) 后 wokCount <= wokCap | ✅ pass | <= 1 | 1 |  |
| 至少获得 1 层护盾（wokCount >= 1） | ✅ pass | >=1 | 1 |  |

### ✅ 桌面 · 续飞（saveFlight → resumeFlight） `resume-flight`

- URL：`index.html?screen=flight&stop=moon&progress=0.5&live=1`
- 截图：`reports/shots/v4qa_resume-flight.png`（像素方差 589.5）
- cdp 报告：`reports/qa-v4-logs/resume-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 589.48 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| saveFlight() 返回 true | ✅ pass | true | true |  |
| state().flightSaved === true | ✅ pass | true | true |  |
| state().savedFlight.progress 接近 0.5（±0.02） | ✅ pass | ≈0.5 | 0.5 |  |
| savedFlight.trip = 0（第 1 段） | ✅ pass | 0 | 0 |  |
| resumeFlight() 返回 true | ✅ pass | true | true |  |
| resumeFlight() 后 screen === 'flight' | ✅ pass | flight | flight |  |
| 恢复后 progress 保持 0.5（±0.02） | ✅ pass | ≈0.5 | 0.5 |  |

### ✅ 持久化 1/3 · 飞行中存档（复用 profile） `save-p1`

- URL：`index.html?screen=flight&stop=moon&progress=0.5`
- 截图：`reports/shots/v4qa_save-p1.png`（像素方差 781.8）
- cdp 报告：`reports/qa-v4-logs/save-p1.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 781.8 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| saveFlight() 返回 true | ✅ pass | true | true |  |
| state().flightSaved === true | ✅ pass | true | true |  |
| savedFlight.progress === 0.5 | ✅ pass | 0.5 | 0.5 |  |
| savedFlight.trip === 0 | ✅ pass | 0 | 0 |  |
| localStorage 已写入 fatfish_universe_save_v4 | ✅ pass | >0 | 459 |  |

### ✅ 持久化 2/3 · 同一 profile 重开标题并续飞 `save-p2`

- URL：`index.html?screen=title`
- 截图：`reports/shots/v4qa_save-p2.png`（像素方差 834.5）
- cdp 报告：`reports/qa-v4-logs/save-p2.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 834.5 |  |
| 重开后默认在标题页 | ✅ pass | title | title |  |
| state().flightSaved === true（跨 run 持久化） | ✅ pass | true | true |  |
| savedFlight.progress ≈ 0.5（±0.05，上一轮落盘时可能有几百 ms 飞行推进） | ✅ pass | ≈0.5 | 0.5172 |  |
| savedFlight.trip = 0 | ✅ pass | 0 | 0 |  |
| resumeFlight() 返回 true | ✅ pass | true | true |  |
| 续飞后 screen === 'flight' | ✅ pass | flight | flight |  |
| 续飞后 progress 从 0.5 附近继续（0.48~0.60） | ✅ pass | 0.48~0.60 | 0.5313 |  |

### ✅ 持久化 3/3 · ?resume=1 URL 参数续飞 `save-p3`

- URL：`index.html?resume=1`
- 截图：`reports/shots/v4qa_save-p3.png`（像素方差 897.1）
- cdp 报告：`reports/qa-v4-logs/save-p3.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 897.12 |  |
| ?resume=1 启动时读到存档（flightSaved=true） | ✅ pass | true | true |  |
| ?resume=1 直接进入飞行（screen === 'flight'） | ✅ pass | flight | flight |  |
| 启动时读到的存档进度 0.45~0.75（由上一轮飞行落盘） | ✅ pass | 0.45~0.75 | 0.6038 |  |
| 续飞后进度从存档值继续（+0~+0.12） | ✅ pass | +0~+0.12 | 0.0166 |  |

### ✅ 桌面 · ?flight=1 构造飞行中存档（标题页显示继续飞行） `url-flight`

- URL：`index.html?flight=1&progress=0.42`
- 截图：`reports/shots/v4qa_url-flight.png`（像素方差 1512.9）
- cdp 报告：`reports/qa-v4-logs/url-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1512.93 |  |
| 页面 = title | ✅ pass | title | title |  |
| ?flight=1 构造出飞行存档（flightSaved=true） | ✅ pass | true | true |  |
| savedFlight.progress ≈ 0.42 | ✅ pass | 0.42 | 0.42 |  |
| savedFlight.trip = 0 | ✅ pass | 0 | 0 |  |

### ✅ 桌面 · 非飞行界面静态背景（无背景流星） `bg-static`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v4qa_bg-static.png`（像素方差 1442.9）
- cdp 报告：`reports/qa-v4-logs/bg-static.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1442.92 |  |
| 页面 = title | ✅ pass | title | title |  |
| 标题页背景流星数 = 0（非飞行界面不出现流星） | ✅ pass | 0 | 0 |  |
| render 已实现 drawSpaceBg(t,warm,mode) 的 static 分支（构建产物静态扫描） | ✅ pass | drawSpaceBg(t,warm,mode) + >=4 处 static 调用 | {"hasSig":true,"staticBranches":5} |  |

### ✅ 桌面 · 飞行 8s 记录背景流星（仅记录） `bg-meteors`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v4qa_bg-meteors.png`（像素方差 834.5）
- cdp 报告：`reports/qa-v4-logs/bg-meteors.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 834.48 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 背景流星数（仅记录，随机 3.5~7s 最多 1 道） | ❌ info | undefined | {"max":1,"now":0,"seenSamples":8,"samples":38} | 飞行 8s 内每 200ms 采样，记录同时在场最大值（不设数量断言） |

### ✅ 移动端 · 标题 `m-title`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v4qa_m-title.png`（像素方差 1588.8）
- cdp 报告：`reports/qa-v4-logs/m-title.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1588.82 |  |
| 页面 = title | ✅ pass | title | title |  |

### ✅ 移动端 · 商城（窄屏列表） `m-shop`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v4qa_m-shop.png`（像素方差 1539.7）
- cdp 报告：`reports/qa-v4-logs/m-shop.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1539.73 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认第 1 页 | ✅ pass | 0 | 0 |  |
| 9 位角色 | ✅ pass | 9 | 9 |  |

### ✅ 移动端 · 角色改装 `m-upgrade`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v4qa_m-upgrade.png`（像素方差 1485.6）
- cdp 报告：`reports/qa-v4-logs/m-upgrade.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1485.6 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| 9 位角色 | ✅ pass | 9 | 9 |  |

### ✅ 移动端 · 飞行 `m-flight`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v4qa_m-flight.png`（像素方差 736）
- cdp 报告：`reports/qa-v4-logs/m-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 736.02 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = moon | ✅ pass | moon | moon |  |

### ✅ 构建产物静态扫描（贴图 / 调试入口 / v4 参数 / 静态背景） `static`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| index.html 内 VERSION = '4.x' | ✅ pass | 4.x | 4.0.0 |  |
| CHARS 注入 8 位新角色立绘（deepseek 用 hero） | ✅ pass | 8 | 8 |  |
| TEX 注入 hero（deepseek 立绘） | ✅ pass | 存在 | 存在 |  |
| TEX 注入 star_* 恒星贴图 >= 10 张 | ✅ pass | >=10 | 13 |  |
| 构建含 setShopPage 调试入口 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 live=1（固定实时时钟） | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 time=<ms> | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 flight=1 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 resume=1 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 screen=upgrade|solar | ✅ pass | 存在 | {"solar":true,"upgrade":true} |  |
| drawSpaceBg(t,warm,mode) 静态背景分支 + >=4 处 static 调用 | ✅ pass | 实现 | {"modeParam":true,"staticCalls":5} |  |
| 太阳系地图使用 A.solarPositions 真实黄经 | ✅ pass | 存在 | 存在 |  |
| 存档 key = fatfish_universe_save_v4 | ✅ pass | 存在 | 存在 |  |

### ✅ 跨场景交叉断言（实时总航程 / 复现性 / 全场报错） `cross`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| ?live=1 与 ?live=1&time=1900000000000 的实时总航程不同 | ✅ pass | 两个时刻总航程不同 | {"liveA":14026385403.8,"liveB":14862218281.5} |  |
| 固定 ?live=1 观测时刻可复现（两次运行总航程一致） | ✅ pass | 两次一致 | {"probe":14026385403.8,"run":14026385403.8} |  |
| 全部场景 console.error / 未捕获异常 = 0 | ✅ pass | 0 个场景报错 | 0 |  |
| 无 fail 场景（pending / warn 不算失败） | ✅ pass | 0 | 0 |  |

## 4. 失败清单（代码 bug，Lead 要修）

无 🎉

## 5. 待集成清单（pending，等 Lead 最终构建后复跑）

无

## 6. 警告（warn，不算失败）

无

## 7. 复跑方式

```powershell
& "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe" tools/qa_v4_run.mjs
# 只跑部分场景：
& "...\node.exe" tools/qa_v4_run.mjs --only=title,shop-p1,upgrade-action
# 带轮次标签：
& "...\node.exe" tools/qa_v4_run.mjs --label=final
```

> 产物：`reports/qa-v4-run.json`（机器可读）、`reports/qa-v4.md`（本文件）、`reports/shots/v4qa_*.png`、`reports/qa-v4-logs/*.json`。
