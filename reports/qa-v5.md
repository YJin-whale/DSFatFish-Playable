# 肥鱼跳宇宙 v5 · 自动化回归报告（qa-harness，含 v4 基线）

**轮次标签**：v6.1-baseline

✅ **全部通过**

- 生成时间：2026-11-18T15:40:39.272Z（用时 269.0s）
- 构建产物：`C:\Users\admin\Desktop\FatFish-Playable\index.html`（8876.3 KB，mtime 2026-11-18T15:35:23.635Z）
- Node v24.21.0 / win32x64；Chrome：`C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`
- 场景 50 个：✅ pass 50 · ⏳ pending 0 · ⚠️ warn 0 · ❌ fail 0
- 退出码：**0**（0 = 无 fail；pending / warn 不算失败）

## 1. 能力探测（决定 pending 口径）

| 能力 | 结果 | 说明 |
|---|---|---|
| 版本 | 6.0.0 | engine VERSION |
| 实时天文 API（页面） | ✅ 已就绪 | state().live.live / legs=9 / totalAU>0 |
| 实时天文 API（src/astronomy.js） | ✅ 已就绪 | Node 侧独立交叉验证用 |
| star_* 恒星贴图 | ✅ 已就绪 | state().starTextures >= 10 |
| 9 角色立绘 | ✅ 已就绪 | charCount=9 且 charImages>=8 |
| setShopPage 调试 API | ✅ 可用 | 商城翻页断言用 |
| v5 调试 API + state 字段 | ✅ 已就绪 | clearGame/newCycle/startEndless/endlessInfo + cleared/clearCount/cycle/historyLen/charAch/endless |
| v5 界面（settings/records/endless） | ✅ 已就绪 | index.html 静态扫描 draw*Screen |
| v5 存档 key / URL 参数 | ✅ 已就绪 | fatfish_universe_save_v5 / ?cleared ?endless ?cycle |

## 1b. v5 需求验收分项

| v5 需求 | 覆盖场景 | 状态 |
|---|---|---|
| ① 通关后「再玩一次」保留通关历史与角色成就 | `v5-cleared-title`、`v5-clear-flow`、`v5-cycle-url` | ✅ pass |
| ① 通关历史记录（分页） | `v5-records` | ✅ pass |
| ① 角色成就档案（charAch） | `v5-records`、`v5-clear-flow` | ✅ pass |
| ② 通关解锁无限模式（标题页/入口） | `v5-cleared-title`、`v5-settings` | ✅ pass |
| ② 无限模式简报界面 | `v5-endless-brief` | ✅ pass |
| ② 无限模式开始 + 参数（敌多/无终点/UFO 上限） | `v5-endless-start`、`v5-endless-url` | ✅ pass |
| ② 无限模式成绩记录（endlessBest / 次数） | `v5-endless-fail` | ✅ pass |
| 记录 / 设置界面可用 | `v5-settings`、`v5-records` | ✅ pass |
| 存档迁移（v4 → v5 兼容） | `v5-migrate-write`、`v5-migrate-read` | ✅ pass |
| 移动端（390x844）v5 三场景 | `m-v5-settings`、`m-v5-records`、`m-v5-endless` | ✅ pass |
| v4 基线不回归（实时天文 / 商城 / 改装 / 飞行 / 续飞 / 伙伴 / 移动端） | 32 个 v4 场景 | ✅ pass |


## 2. 场景 × 断言总表

| # | 场景 | 分组 | 状态 | 断言（通过/待集成/失败） | 截图 | 用时 |
|---|---|---|---|---|---|---|
| 1 | 能力探测（调试 API / 贴图 / 立绘 / 实时天文 / v5 通关与无限模式） | caps | ✅ pass | 23/0/0 | [shots/v5qa_caps.png](shots/v5qa_caps.png) | 7.2s |
| 2 | 桌面 · 标题 | desktop | ✅ pass | 6/0/0 | [shots/v5qa_title.png](shots/v5qa_title.png) | 4.5s |
| 3 | 桌面 · 机库 | desktop | ✅ pass | 7/0/0 | [shots/v5qa_hangar.png](shots/v5qa_hangar.png) | 5.0s |
| 4 | 桌面 · 发射台 | desktop | ✅ pass | 8/0/0 | [shots/v5qa_launch.png](shots/v5qa_launch.png) | 4.5s |
| 5 | 桌面 · 实时太阳系地图（launch + hold + live） | desktop | ✅ pass | 14/0/0 | [shots/v5qa_launch-live-map.png](shots/v5qa_launch-live-map.png) | 4.9s |
| 6 | 桌面 · ?screen=solar 实时太阳系图 | desktop | ✅ pass | 13/0/0 | [shots/v5qa_solar-live.png](shots/v5qa_solar-live.png) | 4.9s |
| 7 | 桌面 · 另一观测时刻（time=1900000000000） | desktop | ✅ pass | 8/0/0 | [shots/v5qa_launch-live-time.png](shots/v5qa_launch-live-time.png) | 4.8s |
| 8 | 桌面 · 商城（默认第 1 页） | desktop | ✅ pass | 9/0/0 | [shots/v5qa_shop-p1.png](shots/v5qa_shop-p1.png) | 5.3s |
| 9 | 桌面 · 商城第 2 页（setShopPage(1)） | desktop | ✅ pass | 8/0/0 | [shots/v5qa_shop-p2.png](shots/v5qa_shop-p2.png) | 5.5s |
| 10 | 桌面 · 商城第 3 页（setShopPage(2)） | desktop | ✅ pass | 8/0/0 | [shots/v5qa_shop-p3.png](shots/v5qa_shop-p3.png) | 5.1s |
| 11 | 桌面 · 角色改装界面 | desktop | ✅ pass | 8/0/0 | [shots/v5qa_upgrade.png](shots/v5qa_upgrade.png) | 5.0s |
| 12 | 桌面 · 升级扣币并生效（chatgpt hp） | desktop | ✅ pass | 11/0/0 | [shots/v5qa_upgrade-action.png](shots/v5qa_upgrade-action.png) | 4.8s |
| 13 | 桌面 · 飞行（stop=moon progress=0.5） | desktop | ✅ pass | 12/0/0 | [shots/v5qa_flight-moon.png](shots/v5qa_flight-moon.png) | 5.3s |
| 14 | 桌面 · 飞行（stop=jupiter 实时航段） | desktop | ✅ pass | 10/0/0 | [shots/v5qa_flight-jupiter.png](shots/v5qa_flight-jupiter.png) | 5.9s |
| 15 | 桌面 · 恒星飞行（stop=sirius progress=0.7，银河贴图） | desktop | ✅ pass | 9/0/0 | [shots/v5qa_flight-sirius.png](shots/v5qa_flight-sirius.png) | 5.6s |
| 16 | 桌面 · 抵达（stop=mars） | desktop | ✅ pass | 6/0/0 | [shots/v5qa_arrive-mars.png](shots/v5qa_arrive-mars.png) | 5.2s |
| 17 | 桌面 · 结局 | desktop | ✅ pass | 5/0/0 | [shots/v5qa_ending.png](shots/v5qa_ending.png) | 5.2s |
| 18 | 桌面 · 帮助 | desktop | ✅ pass | 5/0/0 | [shots/v5qa_help.png](shots/v5qa_help.png) | 4.9s |
| 19 | 桌面 · 成就 | desktop | ✅ pass | 6/0/0 | [shots/v5qa_achv.png](shots/v5qa_achv.png) | 5.2s |
| 20 | 桌面 · 伙伴同行 + 自动反击击毁 UFO | feature | ✅ pass | 8/0/0 | [shots/v5qa_partners-ufo.png](shots/v5qa_partners-ufo.png) | 11.6s |
| 21 | 桌面 · 护盾叠加受 wokCap 约束 | feature | ✅ pass | 8/0/0 | [shots/v5qa_shield-cap.png](shots/v5qa_shield-cap.png) | 5.2s |
| 22 | 桌面 · 续飞（saveFlight → resumeFlight） | feature | ✅ pass | 12/0/0 | [shots/v5qa_resume-flight.png](shots/v5qa_resume-flight.png) | 5.2s |
| 23 | 持久化 1/3 · 飞行中存档（复用 profile） | persist | ✅ pass | 10/0/0 | [shots/v5qa_save-p1.png](shots/v5qa_save-p1.png) | 4.9s |
| 24 | 持久化 2/3 · 同一 profile 重开标题并续飞 | persist | ✅ pass | 11/0/0 | [shots/v5qa_save-p2.png](shots/v5qa_save-p2.png) | 5.2s |
| 25 | 持久化 3/3 · ?resume=1 URL 参数续飞 | persist | ✅ pass | 8/0/0 | [shots/v5qa_save-p3.png](shots/v5qa_save-p3.png) | 5.1s |
| 26 | 桌面 · ?flight=1 构造飞行中存档（标题页显示继续飞行） | persist | ✅ pass | 8/0/0 | [shots/v5qa_url-flight.png](shots/v5qa_url-flight.png) | 4.7s |
| 27 | 桌面 · 非飞行界面静态背景（无背景流星） | feature | ✅ pass | 7/0/0 | [shots/v5qa_bg-static.png](shots/v5qa_bg-static.png) | 5.2s |
| 28 | 桌面 · 飞行 8s 记录背景流星（仅记录） | feature | ✅ pass | 5/0/0 | [shots/v5qa_bg-meteors.png](shots/v5qa_bg-meteors.png) | 12.6s |
| 29 | v5 · 已通关标题页（?cleared=1，显示通关次数 / 无限模式入口） | v5 | ✅ pass | 18/0/0 | [shots/v5qa_v5-cleared-title.png](shots/v5qa_v5-cleared-title.png) | 5.2s |
| 30 | v5 · 多次通关 + 二周目 URL（?cleared=1&clears=2&cycle=2） | v5 | ✅ pass | 10/0/0 | [shots/v5qa_v5-cleared-multi.png](shots/v5qa_v5-cleared-multi.png) | 5.3s |
| 31 | v5 · 设置页（?screen=settings：再玩一次 / 无限模式 / 记录入口） | v5 | ✅ pass | 9/0/0 | [shots/v5qa_v5-settings.png](shots/v5qa_v5-settings.png) | 4.9s |
| 32 | v5 · 通关记录页（?screen=records：历史分页 / 角色成就档案） | v5 | ✅ pass | 13/0/0 | [shots/v5qa_v5-records.png](shots/v5qa_v5-records.png) | 5.5s |
| 33 | v5 · 通关流程（clearGame 记录 → newCycle 二周目，保留存档） | v5 | ✅ pass | 21/0/0 | [shots/v5qa_v5-clear-flow.png](shots/v5qa_v5-clear-flow.png) | 4.7s |
| 34 | v5 · 真实通关路径（stop=observable_edge + arriveNow → 记录通关） | v5 | ✅ pass | 11/0/0 | [shots/v5qa_v5-clear-arrive.png](shots/v5qa_v5-clear-arrive.png) | 5.7s |
| 35 | v5 · ?cycle=2 URL 参数（二周目标题页） | v5 | ✅ pass | 8/0/0 | [shots/v5qa_v5-cycle-url.png](shots/v5qa_v5-cycle-url.png) | 5.1s |
| 36 | v5 · 无限模式简报界面（?screen=endless，未开始） | v5 | ✅ pass | 10/0/0 | [shots/v5qa_v5-endless-brief.png](shots/v5qa_v5-endless-brief.png) | 4.7s |
| 37 | v5 · 无限模式开始（startEndless → flight，波次 / 刷怪 / 击毁 / 成就） | v5 | ✅ pass | 17/0/0 | [shots/v5qa_v5-endless-start.png](shots/v5qa_v5-endless-start.png) | 8.1s |
| 38 | v5 · ?endless=1 URL 参数直接进入无限模式飞行 | v5 | ✅ pass | 7/0/0 | [shots/v5qa_v5-endless-url.png](shots/v5qa_v5-endless-url.png) | 6.0s |
| 39 | v5 · 无限模式结束（生命归零 → 结果页 / 最佳成绩 / 次数+1） | v5 | ✅ pass | 12/0/0 | [shots/v5qa_v5-endless-fail.png](shots/v5qa_v5-endless-fail.png) | 12.3s |
| 40 | v5 · 存档迁移 1/2（写入 v4 旧 save key） | v5-persist | ✅ pass | 7/0/0 | [shots/v5qa_v5-migrate-write.png](shots/v5qa_v5-migrate-write.png) | 4.8s |
| 41 | v5 · 存档迁移 2/2（同 profile 重开，旧档被读取/迁移） | v5-persist | ✅ pass | 13/0/0 | [shots/v5qa_v5-migrate-read.png](shots/v5qa_v5-migrate-read.png) | 5.2s |
| 42 | 移动端 · 标题 | mobile | ✅ pass | 5/0/0 | [shots/v5qa_m-title.png](shots/v5qa_m-title.png) | 4.6s |
| 43 | 移动端 · 商城（窄屏列表） | mobile | ✅ pass | 7/0/0 | [shots/v5qa_m-shop.png](shots/v5qa_m-shop.png) | 4.5s |
| 44 | 移动端 · 角色改装 | mobile | ✅ pass | 6/0/0 | [shots/v5qa_m-upgrade.png](shots/v5qa_m-upgrade.png) | 4.6s |
| 45 | 移动端 · 飞行 | mobile | ✅ pass | 6/0/0 | [shots/v5qa_m-flight.png](shots/v5qa_m-flight.png) | 4.7s |
| 46 | 移动端 · 设置页 | mobile | ✅ pass | 6/0/0 | [shots/v5qa_m-v5-settings.png](shots/v5qa_m-v5-settings.png) | 4.6s |
| 47 | 移动端 · 通关记录页 | mobile | ✅ pass | 6/0/0 | [shots/v5qa_m-v5-records.png](shots/v5qa_m-v5-records.png) | 4.4s |
| 48 | 移动端 · 无限模式简报 | mobile | ✅ pass | 6/0/0 | [shots/v5qa_m-v5-endless.png](shots/v5qa_m-v5-endless.png) | 4.5s |
| 49 | 构建产物静态扫描（贴图 / 调试入口 / v4+v5 参数与界面 / 静态背景） | static | ✅ pass | 20/0/0 | — | — |
| 50 | 跨场景交叉断言（实时总航程 / 复现性 / v5 解锁链 / 全场报错） | cross | ✅ pass | 6/0/0 | — | — |

> 断言列格式：通过 / 待集成 / 失败；截图相对 `reports/`。

## 3. 逐场景断言明细

### ✅ 能力探测（调试 API / 贴图 / 立绘 / 实时天文 / v5 通关与无限模式） `caps`

- URL：`index.html?screen=title&unlock=1&live=1`
- 截图：`reports/shots/v5qa_caps.png`（像素方差 1579.2）
- cdp 报告：`reports/qa-v5-logs/caps.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1579.16 |  |
| 页面 = title | ✅ pass | title | title |  |
| f.version 以 4. / 5. 或 6. 开头 | ✅ pass | 4.x/5.x/6.x | 6.0.0 |  |
| v4 调试 API 齐备（state/liveInfo/setTime/upgrade/giveStardust/setCompanions/spawnUFO/killUFO/saveFlight/resumeFlight/giveShield/clearSave/unlockAll/setPrimary/setProgress） | ✅ pass | 全部 function | 全部齐备 |  |
| v5 调试 API 齐备（clearGame/newCycle/startEndless/endlessInfo） | ✅ pass | 全部 function | 全部齐备 |  |
| v5 state 字段齐备（cleared/clearCount/cycle/cycleCleared/historyLen/charAch/endlessBest/endless） | ✅ pass | 全部存在 | 全部存在 |  |
| v5 state 字段类型合理（clearCount/cycle/historyLen 数值，charAch/endless 对象） | ✅ pass | 类型合理 | {"clearCount":0,"cycle":1,"historyLen":0,"cleared":false} |  |
| v5 扩展 QA API（setCleared/endlessFinish/setEndlessTime/endlessSpawn/setHistoryPage） | ✅ pass | 全部 function | 全部齐备 |  |
| v5 附加 state 字段（canReplay/endlessUnlocked/endlessResult/historyPage/history） | ✅ pass | 全部存在 | 全部存在 |  |
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
- 截图：`reports/shots/v5qa_title.png`（像素方差 1576.3）
- cdp 报告：`reports/qa-v5-logs/title.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1576.32 |  |
| 页面 = title | ✅ pass | title | title |  |
| 版本号 4.x/5.x/6.x | ✅ pass | 4.x/5.x/6.x | 6.0.0 |  |

### ✅ 桌面 · 机库 `hangar`

- URL：`index.html?screen=hangar&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_hangar.png`（像素方差 1241.3）
- cdp 报告：`reports/qa-v5-logs/hangar.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1241.3 |  |
| 页面 = hangar | ✅ pass | hangar | hangar |  |
| 机库可见已拥有角色（owned >= 9） | ✅ pass | >=9 | 9 |  |
| ?lv=5 生效（pilotLv >= 5） | ✅ pass | >=5 | 6 |  |

### ✅ 桌面 · 发射台 `launch`

- URL：`index.html?screen=launch`
- 截图：`reports/shots/v5qa_launch.png`（像素方差 3747.3）
- cdp 报告：`reports/qa-v5-logs/launch.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 3747.28 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| 目标 = moon（首段） | ✅ pass | moon | moon |  |
| 首段固定 384400 km | ✅ pass | 384400 | 384400 |  |
| 航段距离文案非空 | ✅ pass | 非空 | 38.44 万 km |  |

### ✅ 桌面 · 实时太阳系地图（launch + hold + live） `launch-live-map`

- URL：`index.html?screen=launch&hold=1&live=1`
- 截图：`reports/shots/v5qa_launch-live-map.png`（像素方差 1031.5）
- cdp 报告：`reports/qa-v5-logs/launch-live-map.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1031.45 |  |
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
- 截图：`reports/shots/v5qa_solar-live.png`（像素方差 1039.5）
- cdp 报告：`reports/qa-v5-logs/solar-live.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1039.46 |  |
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
- 截图：`reports/shots/v5qa_launch-live-time.png`（像素方差 3747.6）
- cdp 报告：`reports/qa-v5-logs/launch-live-time.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 3747.64 |  |
| 页面 = launch | ✅ pass | launch | launch |  |
| ?time=1900000000000 覆盖固定时钟 | ✅ pass | 1900000000000 | 1900000000000 |  |
| state().live.live === true | ✅ pass | true | true |  |
| 该时刻实时总航程 totalAU > 0 | ✅ pass | >0 | 99.34779293282612 |  |

### ✅ 桌面 · 商城（默认第 1 页） `shop-p1`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_shop-p1.png`（像素方差 1003.8）
- cdp 报告：`reports/qa-v5-logs/shop-p1.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1003.84 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认第 1 页（shopPage = 0） | ✅ pass | 0 | 0 |  |
| 9 位角色 / 每页 3 张 = 3 页（shopPages = 3） | ✅ pass | 3 | 3 |  |
| charCount = 9 | ✅ pass | 9 | 9 |  |
| 角色立绘已加载（charImages >= 8） | ✅ pass | >=8 | 8 |  |

### ✅ 桌面 · 商城第 2 页（setShopPage(1)） `shop-p2`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_shop-p2.png`（像素方差 875.6）
- cdp 报告：`reports/qa-v5-logs/shop-p2.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 875.57 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认在第 1 页 | ✅ pass | 0 | 0 |  |
| 翻到第 2 页（setShopPage 生效） | ✅ pass | 1 | {"setReturn":1,"shopPage":1} |  |
| 页数 = 3 | ✅ pass | 3 | 3 |  |

### ✅ 桌面 · 商城第 3 页（setShopPage(2)） `shop-p3`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_shop-p3.png`（像素方差 852.1）
- cdp 报告：`reports/qa-v5-logs/shop-p3.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 852.14 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认在第 1 页 | ✅ pass | 0 | 0 |  |
| 翻到第 3 页（setShopPage 生效） | ✅ pass | 2 | {"setReturn":2,"shopPage":2} |  |
| 页数 = 3 | ✅ pass | 3 | 3 |  |

### ✅ 桌面 · 角色改装界面 `upgrade`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v5qa_upgrade.png`（像素方差 1118.9）
- cdp 报告：`reports/qa-v5-logs/upgrade.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1118.92 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| 可改装角色 9 位 | ✅ pass | 9 | 9 |  |
| state().upg 是对象 | ✅ pass | object | object |  |
| state().upgrades 含 maxHp/wokCap/accelMul | ✅ pass | maxHp/wokCap/accelMul | {"maxHp":4,"wokCap":1,"accelMul":1} |  |

### ✅ 桌面 · 升级扣币并生效（chatgpt hp） `upgrade-action`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v5qa_upgrade-action.png`（像素方差 1159.7）
- cdp 报告：`reports/qa-v5-logs/upgrade-action.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1159.66 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| unlockAll 后 owned 含 chatgpt | ✅ pass | true | true |  |
| 出战神切换为 chatgpt（setPrimary 生效） | ✅ pass | chatgpt | chatgpt |  |
| upgrade('chatgpt','hp') 返回 true | ✅ pass | true | true |  |
| 星辰币扣掉 hp 一级价格 120 | ✅ pass | -120 | -120 | before=100149 after=100029（已预先解锁 a_upgrade 排除成就奖励干扰） |
| state().upg.chatgpt.hp === 1 | ✅ pass | 1 | 1 | before=0 |
| state().upgrades.maxHp 增加 1 | ✅ pass | 5 | 5 |  |

### ✅ 桌面 · 飞行（stop=moon progress=0.5） `flight-moon`

- URL：`index.html?screen=flight&stop=moon&progress=0.5&live=1`
- 截图：`reports/shots/v5qa_flight-moon.png`（像素方差 828.1）
- cdp 报告：`reports/qa-v5-logs/flight-moon.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 828.12 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = moon | ✅ pass | moon | moon |  |
| 起点 = earth | ✅ pass | earth | earth |  |
| 月球段固定 384400 km | ✅ pass | 384400 | 384400 |  |
| 月球段 fixed（legLive = false） | ✅ pass | false | false |  |
| progress=0.5 生效（0.45~0.62） | ✅ pass | 0.45~0.62 | 0.5682 |  |
| maxHp = 3（deepseek 默认，pilotLv<5） | ✅ pass | 3 | 3 |  |
| 燃料 0~100 | ✅ pass | 0~100 | 97.87 |  |

### ✅ 桌面 · 飞行（stop=jupiter 实时航段） `flight-jupiter`

- URL：`index.html?screen=flight&stop=jupiter&live=1`
- 截图：`reports/shots/v5qa_flight-jupiter.png`（像素方差 704.3）
- cdp 报告：`reports/qa-v5-logs/flight-jupiter.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 704.25 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = jupiter | ✅ pass | jupiter | jupiter |  |
| 航段距离 > 0 | ✅ pass | >0 | 589582641.3313304 |  |
| 太阳系航段为实时测算（legLive = true） | ✅ pass | true | true |  |
| state().legKm 与 src/astronomy.js A.liveSolarLeg(idx) 一致（误差 <0.5%） | ✅ pass | 误差<0.5% | page=589582641.3km ref=589582641.3km 误差=0% |  |
| state().legKm 与 liveInfo().legs[idx].km 一致 | ✅ pass | {"idx":4,"km":589582641.3313304} | 589582641.3313304 |  |

### ✅ 桌面 · 恒星飞行（stop=sirius progress=0.7，银河贴图） `flight-sirius`

- URL：`index.html?screen=flight&stop=sirius&progress=0.7&live=1`
- 截图：`reports/shots/v5qa_flight-sirius.png`（像素方差 1891.6）
- cdp 报告：`reports/qa-v5-logs/flight-sirius.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1891.59 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = sirius（天狼星） | ✅ pass | sirius | sirius |  |
| 恒星航段距离 legLy > 0 | ✅ pass | >0 | 0.745000000000001 |  |
| progress=0.7 生效（0.66~0.80） | ✅ pass | 0.66~0.80 | 0.7559 |  |
| 航段文案含光年单位 | ✅ pass | 光年 | 0.75 光年 |  |

### ✅ 桌面 · 抵达（stop=mars） `arrive-mars`

- URL：`index.html?screen=arrive&stop=mars&unlock=1`
- 截图：`reports/shots/v5qa_arrive-mars.png`（像素方差 997.5）
- cdp 报告：`reports/qa-v5-logs/arrive-mars.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 997.47 |  |
| 页面 = arrive | ✅ pass | arrive | arrive |  |
| 星辰币非负 | ✅ pass | >=0 | 99999 |  |

### ✅ 桌面 · 结局 `ending`

- URL：`index.html?screen=ending&unlock=1`
- 截图：`reports/shots/v5qa_ending.png`（像素方差 1163.7）
- cdp 报告：`reports/qa-v5-logs/ending.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1163.69 |  |
| 页面 = ending | ✅ pass | ending | ending |  |

### ✅ 桌面 · 帮助 `help`

- URL：`index.html?screen=help`
- 截图：`reports/shots/v5qa_help.png`（像素方差 1376.4）
- cdp 报告：`reports/qa-v5-logs/help.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1376.36 |  |
| 页面 = help | ✅ pass | help | help |  |

### ✅ 桌面 · 成就 `achv`

- URL：`index.html?screen=achv&unlock=1&live=1`
- 截图：`reports/shots/v5qa_achv.png`（像素方差 422.4）
- cdp 报告：`reports/qa-v5-logs/achv.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 422.36 |  |
| 页面 = achv | ✅ pass | achv | achv |  |
| state().achievements 是数组 | ✅ pass | array | object |  |

### ✅ 桌面 · 伙伴同行 + 自动反击击毁 UFO `partners-ufo`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v5qa_partners-ufo.png`（像素方差 1244.2）
- cdp 报告：`reports/qa-v5-logs/partners-ufo.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 1244.23 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| setCompanions([chatgpt,claude]) 后随行伙伴 2 名 | ✅ pass | 2 | 2 |  |
| 伙伴自动反击击毁 UFO（ufoKills 增加）或 UFO 已离场（ufos=0） | ✅ pass | kills>0 | kills=1（尝试 1 次，4941ms） |  |
| 伙伴护盾数组存在（compShields 可持久化） | ✅ pass | 2 槽数组 | [0,0] |  |

### ✅ 桌面 · 护盾叠加受 wokCap 约束 `shield-cap`

- URL：`index.html?screen=flight&stop=moon&unlock=1&rich=1`
- 截图：`reports/shots/v5qa_shield-cap.png`（像素方差 618.9）
- cdp 报告：`reports/qa-v5-logs/shield-cap.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 618.86 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 护盾上限 wokCap >= 1 | ✅ pass | >=1 | 1 |  |
| giveShield(12) 后 wokCount <= wokCap | ✅ pass | <= 1 | 1 |  |
| 至少获得 1 层护盾（wokCount >= 1） | ✅ pass | >=1 | 1 |  |

### ✅ 桌面 · 续飞（saveFlight → resumeFlight） `resume-flight`

- URL：`index.html?screen=flight&stop=moon&progress=0.5&live=1`
- 截图：`reports/shots/v5qa_resume-flight.png`（像素方差 591.9）
- cdp 报告：`reports/qa-v5-logs/resume-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 591.87 |  |
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
- 截图：`reports/shots/v5qa_save-p1.png`（像素方差 773.8）
- cdp 报告：`reports/qa-v5-logs/save-p1.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 773.79 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| saveFlight() 返回 true | ✅ pass | true | true |  |
| state().flightSaved === true | ✅ pass | true | true |  |
| savedFlight.progress === 0.5 | ✅ pass | 0.5 | 0.5 |  |
| savedFlight.trip === 0 | ✅ pass | 0 | 0 |  |
| localStorage 已写入存档（当前 key 或兼容旧 key） | ✅ pass | >0 | {"v4Len":0,"v5Len":0,"v6Len":682} |  |

### ✅ 持久化 2/3 · 同一 profile 重开标题并续飞 `save-p2`

- URL：`index.html?screen=title`
- 截图：`reports/shots/v5qa_save-p2.png`（像素方差 828.7）
- cdp 报告：`reports/qa-v5-logs/save-p2.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 828.68 |  |
| 重开后默认在标题页 | ✅ pass | title | title |  |
| state().flightSaved === true（跨 run 持久化） | ✅ pass | true | true |  |
| savedFlight.progress ≈ 0.5（±0.05，上一轮落盘时可能有几百 ms 飞行推进） | ✅ pass | ≈0.5 | 0.5203 |  |
| savedFlight.trip = 0 | ✅ pass | 0 | 0 |  |
| resumeFlight() 返回 true | ✅ pass | true | true |  |
| 续飞后 screen === 'flight' | ✅ pass | flight | flight |  |
| 续飞后 progress 从 0.5 附近继续（0.48~0.60） | ✅ pass | 0.48~0.60 | 0.535 |  |

### ✅ 持久化 3/3 · ?resume=1 URL 参数续飞 `save-p3`

- URL：`index.html?resume=1`
- 截图：`reports/shots/v5qa_save-p3.png`（像素方差 916.5）
- cdp 报告：`reports/qa-v5-logs/save-p3.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 916.47 |  |
| ?resume=1 启动时读到存档（flightSaved=true） | ✅ pass | true | true |  |
| ?resume=1 直接进入飞行（screen === 'flight'） | ✅ pass | flight | flight |  |
| 启动时读到的存档进度 0.45~0.75（由上一轮飞行落盘） | ✅ pass | 0.45~0.75 | 0.6155 |  |
| 续飞后进度从存档值继续（+0~+0.12） | ✅ pass | +0~+0.12 | 0.0234 |  |

### ✅ 桌面 · ?flight=1 构造飞行中存档（标题页显示继续飞行） `url-flight`

- URL：`index.html?flight=1&progress=0.42`
- 截图：`reports/shots/v5qa_url-flight.png`（像素方差 1645.9）
- cdp 报告：`reports/qa-v5-logs/url-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1645.94 |  |
| 页面 = title | ✅ pass | title | title |  |
| ?flight=1 构造出飞行存档（flightSaved=true） | ✅ pass | true | true |  |
| savedFlight.progress ≈ 0.42 | ✅ pass | 0.42 | 0.42 |  |
| savedFlight.trip = 0 | ✅ pass | 0 | 0 |  |

### ✅ 桌面 · 非飞行界面静态背景（无背景流星） `bg-static`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v5qa_bg-static.png`（像素方差 1576.3）
- cdp 报告：`reports/qa-v5-logs/bg-static.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1576.26 |  |
| 页面 = title | ✅ pass | title | title |  |
| 标题页背景流星数 = 0（非飞行界面不出现流星） | ✅ pass | 0 | 0 |  |
| render 已实现 drawSpaceBg(t,warm,mode) 的 static 分支（构建产物静态扫描） | ✅ pass | drawSpaceBg(t,warm,mode) + >=4 处 static 调用 | {"hasSig":true,"staticBranches":8} |  |

### ✅ 桌面 · 飞行 8s 记录背景流星（仅记录） `bg-meteors`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v5qa_bg-meteors.png`（像素方差 811.6）
- cdp 报告：`reports/qa-v5-logs/bg-meteors.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 811.63 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 背景流星数（仅记录，随机 3.5~7s 最多 1 道） | ❌ info | undefined | {"max":1,"now":0,"seenSamples":5,"samples":36} | 飞行 8s 内每 200ms 采样，记录同时在场最大值（不设数量断言） |

### ✅ v5 · 已通关标题页（?cleared=1，显示通关次数 / 无限模式入口） `v5-cleared-title`

- URL：`index.html?cleared=1&screen=title`
- 截图：`reports/shots/v5qa_v5-cleared-title.png`（像素方差 1613.5）
- cdp 报告：`reports/qa-v5-logs/v5-cleared-title.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1613.51 |  |
| 页面 = title | ✅ pass | title | title |  |
| state().cleared === true（?cleared=1 构造已通关存档） | ✅ pass | true | true |  |
| state().clearCount >= 1 | ✅ pass | >=1 | 1 |  |
| state().historyLen >= 1（通关历史可查） | ✅ pass | >=1 | 2 |  |
| state().history 是数组且条目含 mode/primary | ✅ pass | 数组+条目 | {"mode":"story","primary":"deepseek","cycle":1} |  |
| state().cycle >= 1 | ✅ pass | >=1 | 1 |  |
| state().canReplay === true（可「再玩一次」） | ✅ pass | true | true |  |
| state().charAch 是对象（角色成就档案） | ✅ pass | object | object |  |
| charAch 有角色档案数据（>=1 个角色） | ✅ pass | >=1 | 1 |  |
| charAch 值类型符合 SPEC（SPEC-v5 §2：{achId:true} 嵌套对象） | ✅ pass | 嵌套对象 | 符合 SPEC |  |
| state().endlessUnlocked === true（无限模式已解锁） | ✅ pass | true | true |  |
| 无限模式入口可用（startEndless / endlessInfo 为函数） | ✅ pass | function/function | {"startEndless":"function","endlessInfo":"function"} |  |
| 通关解锁无限模式（endlessBest 成绩字段可读 / 已解锁） | ✅ pass | endlessBest 对象 | {"seconds":95,"kills":63,"coins":1450,"iso":"2026-11-18 21:40","char":"deepseek","cycle":1} |  |
| 标题页通关态已实现（静态扫描：已通关 / 再玩一次 文案） | ✅ pass | 通关态文案/字段 | 存在 |  |

### ✅ v5 · 多次通关 + 二周目 URL（?cleared=1&clears=2&cycle=2） `v5-cleared-multi`

- URL：`index.html?cleared=1&clears=2&cycle=2&screen=title`
- 截图：`reports/shots/v5qa_v5-cleared-multi.png`（像素方差 1613.5）
- cdp 报告：`reports/qa-v5-logs/v5-cleared-multi.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1613.45 |  |
| 页面 = title | ✅ pass | title | title |  |
| ?clears=2 构造 closeCount >= 2 的通关记录 | ✅ pass | >=2 | 2 |  |
| 通关历史 >= 2 条（多条记录可查） | ✅ pass | >=2 | 2 |  |
| ?cycle=2 生效（state().cycle === 2） | ✅ pass | 2 | 2 |  |
| cleared 仍为 true | ✅ pass | true | true |  |
| canReplay / endlessUnlocked 均为 true | ✅ pass | true/true | {"canReplay":true,"endlessUnlocked":true} |  |

### ✅ v5 · 设置页（?screen=settings：再玩一次 / 无限模式 / 记录入口） `v5-settings`

- URL：`index.html?cleared=1&screen=settings`
- 截图：`reports/shots/v5qa_v5-settings.png`（像素方差 950.6）
- cdp 报告：`reports/qa-v5-logs/v5-settings.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 950.6 |  |
| 页面 = settings | ✅ pass | settings | settings |  |
| 设置界面已实现（静态扫描 drawSettingsScreen） | ✅ pass | drawSettingsScreen | 存在 |  |
| 设置页有「再玩一次」入口（newCycle API 可用） | ✅ pass | function | function |  |
| 设置页有「无限模式」入口（startEndless API 可用） | ✅ pass | function | function |  |
| 设置页有「通关记录」入口（静态扫描记录入口/records 跳转） | ✅ pass | records 入口 + 界面 | 存在 |  |

### ✅ v5 · 通关记录页（?screen=records：历史分页 / 角色成就档案） `v5-records`

- URL：`index.html?cleared=1&screen=records`
- 截图：`reports/shots/v5qa_v5-records.png`（像素方差 974.4）
- cdp 报告：`reports/qa-v5-logs/v5-records.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 974.35 |  |
| 页面 = records | ✅ pass | records | records |  |
| 记录界面已实现（静态扫描 drawRecordsScreen） | ✅ pass | drawRecordsScreen | 存在 |  |
| clearGame()/newCycle()/goto(records) 不抛异常 | ✅ pass | 无异常 | 无 |  |
| clearGame+newCycle 交替累积 >=6 条通关历史（每页 5 条 → 至少 2 页） | ✅ pass | >=6 | 8 |  |
| clearCount 随通关记录增长（>=6） | ✅ pass | >=6 | 7 |  |
| 角色成就档案 charAch 非空 | ✅ pass | >=1 | 1 |  |
| 历史条目含 mode/primary/cycle/ufoKills/pilotLv 字段 | ✅ pass | mode/primary/cycle/ufoKills/pilotLv | {"mode":"story","primary":"deepseek","cycle":7,"achievements":0,"ufoKills":0,"pilotLv":1} |  |
| 记录分页可翻（setHistoryPage(n) → state().historyPage = n，每页 5 条） | ✅ pass | historyPage=1 且 >=2 页 | {"historyPageBefore":0,"pageAfter":1,"pages":null,"historyLen":8} |  |
| 进入记录页默认第 1 页（historyPage = 0） | ✅ pass | 0 | 0 |  |

### ✅ v5 · 通关流程（clearGame 记录 → newCycle 二周目，保留存档） `v5-clear-flow`

- URL：`index.html?screen=title&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_v5-clear-flow.png`（像素方差 4611.7）
- cdp 报告：`reports/qa-v5-logs/v5-clear-flow.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 4611.73 |  |
| clearGame()/newCycle() 不抛异常 | ✅ pass | 无异常 | 无 |  |
| clearGame() 返回 {ok:true, clearCount, historyLen, cleared:true} | ✅ pass | {ok,clearCount,historyLen,cleared} | {"ok":true,"clearCount":1,"historyLen":1,"cleared":true} |  |
| clearGame() 后 clearCount = before + 1 | ✅ pass | 1 | 1 |  |
| clearGame() 后 historyLen = before + 1 | ✅ pass | 1 | 1 |  |
| clearGame() 后 cleared === true | ✅ pass | true | true |  |
| clearGame() 后 cycleCleared === true（防重复记录） | ✅ pass | true | true |  |
| newCycle() 后 cycle = 当前 + 1 | ✅ pass | 2 | 2 |  |
| newCycle() 后 trip = 0（回到起点） | ✅ pass | 0 | 0 |  |
| newCycle() 后 cycleCleared = false（新周目可再次记录） | ✅ pass | false | false |  |
| newCycle() 后 cleared 仍为 true | ✅ pass | true | true |  |
| newCycle() 后通关历史不变 | ✅ pass | 1 | 1 |  |
| newCycle() 后角色保留（owned 数不变） | ✅ pass | 9 | 9 |  |
| newCycle() 后改装保留（chatgpt.hp 不变） | ✅ pass | 1 | 1 |  |
| newCycle() 后成就保留（数量不减且含 a_wok） | ✅ pass | 数量不减 + a_wok | {"achLen":4,"hasWok":true} |  |
| newCycle() 后出战神保留（chatgpt） | ✅ pass | chatgpt | chatgpt |  |
| newCycle() 后星辰币保留（不减；通关/周目成就可能额外 +150） | ✅ pass | >= before | {"before":100179,"after":100479} |  |
| newCycle() 后角色成就档案保留（chatgpt 档案仍在） | ✅ pass | 含 chatgpt | {"deepseek":{"a_wok":true},"chatgpt":{"a_upgrade":true,"a_clear":true,"a_ngplus":true}} |  |

### ✅ v5 · 真实通关路径（stop=observable_edge + arriveNow → 记录通关） `v5-clear-arrive`

- URL：`index.html?screen=flight&stop=observable_edge&unlock=1&live=1`
- 截图：`reports/shots/v5qa_v5-clear-arrive.png`（像素方差 979.6）
- cdp 报告：`reports/qa-v5-logs/v5-clear-arrive.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 979.55 |  |
| 通关后进入抵达/终章界面（arrive 或 ending） | ✅ pass | arrive/ending | arrive |  |
| arriveNow() 返回真值 | ✅ pass | true | true |  |
| 抵达最后一站后 cleared === true | ✅ pass | true | true |  |
| clearCount = 1（首次通关） | ✅ pass | 1 | 1 |  |
| historyLen = 1 且记录含 mode/primary | ✅ pass | 1 条历史 | {"historyLen":1,"history0":{"mode":"story","cycle":1,"primary":"deepseek"}} |  |
| canReplay === true（可再玩一次） | ✅ pass | true | true |  |
| 通关成就 a_clear 已解锁 | ✅ pass | a_clear | ["a_cosmic_edge","a_clear"] |  |

### ✅ v5 · ?cycle=2 URL 参数（二周目标题页） `v5-cycle-url`

- URL：`index.html?cleared=1&cycle=2&screen=title`
- 截图：`reports/shots/v5qa_v5-cycle-url.png`（像素方差 1613.3）
- cdp 报告：`reports/qa-v5-logs/v5-cycle-url.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1613.31 |  |
| 页面 = title | ✅ pass | title | title |  |
| ?cycle=2 使 state().cycle === 2 | ✅ pass | 2 | 2 |  |
| ?cleared=1&cycle=2 同时生效（cleared === true） | ✅ pass | true | true |  |
| 二周目仍保留通关历史（historyLen >= 1） | ✅ pass | >=1 | 2 |  |

### ✅ v5 · 无限模式简报界面（?screen=endless，未开始） `v5-endless-brief`

- URL：`index.html?cleared=1&screen=endless`
- 截图：`reports/shots/v5qa_v5-endless-brief.png`（像素方差 681.9）
- cdp 报告：`reports/qa-v5-logs/v5-endless-brief.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 681.88 |  |
| 页面 = endless | ✅ pass | endless | endless |  |
| 无限模式界面已实现（静态扫描 drawEndlessScreen） | ✅ pass | drawEndlessScreen | 存在 |  |
| 通关后无限模式已解锁（cleared === true） | ✅ pass | true | true |  |
| 简报界面未在飞行中（state().endless === null） | ✅ pass | null/未开始 | null |  |
| endlessInfo() 未开局时为空（null 或 active=false） | ✅ pass | null | null |  |
| endlessBest 最佳成绩可读（含 seconds/kills/coins） | ✅ pass | {seconds,kills,coins} | {"seconds":95,"kills":63,"coins":1450,"iso":"2026-11-18 21:40","char":"deepseek","cycle":1} |  |

### ✅ v5 · 无限模式开始（startEndless → flight，波次 / 刷怪 / 击毁 / 成就） `v5-endless-start`

- URL：`index.html?cleared=1&screen=endless`
- 截图：`reports/shots/v5qa_v5-endless-start.png`（像素方差 752）
- cdp 报告：`reports/qa-v5-logs/v5-endless-start.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 752.04 |  |
| 开始后进入飞行（screen0 = screen1 = flight） | ✅ pass | flight/flight | flight/flight |  |
| startEndless() 不抛异常 | ✅ pass | 无异常 | 无 |  |
| startEndless() 返回 true | ✅ pass | true | true |  |
| 飞行中 state().endless 对象存在（无限模式激活） | ✅ pass | endless 对象 | {"seconds":0,"mmss":"00:00","kills":0,"wave":1,"coins":0} |  |
| state().endless 含 seconds/kills/wave/coins | ✅ pass | {seconds,kills,wave,coins} | {"seconds":0,"mmss":"00:00","kills":0,"wave":1,"coins":0} |  |
| endlessInfo() 返回本局成绩对象（seconds/kills/wave） | ✅ pass | 成绩对象 | {"seconds":0,"mmss":"00:00","kills":0,"wave":1,"coins":0} |  |
| startEndless() 后 endlessRuns +1 | ✅ pass | 1 | 1 |  |
| 无限模式无终点（progress 保持 0） | ✅ pass | 0 | 0 |  |
| 生存 45s → 波次 >= 3（每 20s 一档） | ✅ pass | seconds>=45 且 wave>=3 | {"seconds":45,"mmss":"00:45","kills":0,"wave":3,"coins":0} |  |
| 生存 105s → 波次 >= 6（难度递增） | ✅ pass | wave>=6 | {"seconds":105,"mmss":"01:45","kills":0,"wave":6,"coins":0} |  |
| 存活 60s 成就 a_endless60 即时解锁（无限模式飞行中） | ✅ pass | a_endless60 | ["a_clear","a_endless","a_endless60"] |  |
| 无限模式敌人极多（endlessSpawn(8)/spawnUFO×8 后 ufos >= 6） | ✅ pass | >=6 | 8 |  |
| killUFO() 后击毁数增长（全局 ufoKills 与 endlessInfo().kills） | ✅ pass | 全局与 endless 计数都增长 | {"global":"0→8","endless":"0→8","apiKilled":8} |  |
| 击毁掉落（本局星辰币 / 掉落件数；状态未暴露件数则记录金币与击毁） | ❌ info | undefined | {"coins0":150,"coins1":450,"endlessCoins":"0→0","kills":8,"wave":6,"apiKilled":8,"achievements":["a_clear","a_endless","a_endless60","a_ufo_down"]} | 掉落件数未在 state/endlessInfo 中直接暴露，记录本局分数变化作为掉落证据 |

### ✅ v5 · ?endless=1 URL 参数直接进入无限模式飞行 `v5-endless-url`

- URL：`index.html?cleared=1&endless=1`
- 截图：`reports/shots/v5qa_v5-endless-url.png`（像素方差 830.9）
- cdp 报告：`reports/qa-v5-logs/v5-endless-url.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 830.85 |  |
| ?endless=1 进入飞行（screen = flight） | ✅ pass | flight | flight |  |
| ?endless=1 直接进入无限模式（state().endless 对象存在） | ✅ pass | endless 对象 | {"seconds":2,"mmss":"00:02","kills":0,"wave":1,"coins":0} |  |
| endlessInfo() 返回本局成绩对象 | ✅ pass | 成绩对象 | {"seconds":2,"mmss":"00:02","kills":0,"wave":1,"coins":0} |  |
| 无限模式开局 UFO 生成中（ufos >= 1 或很快生成，仅记录） | ❌ info | undefined | 0 | 开局 UFO 数（随机时刻采样） |

### ✅ v5 · 无限模式结束（生命归零 → 结果页 / 最佳成绩 / 次数+1） `v5-endless-fail`

- URL：`index.html?cleared=1&screen=endless`
- 截图：`reports/shots/v5qa_v5-endless-fail.png`（像素方差 605.7）
- cdp 报告：`reports/qa-v5-logs/v5-endless-fail.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 605.7 |  |
| 生命归零后回到无限模式结果页（screen === endless） | ✅ pass | endless | endless |  |
| 结束后退出本局（state().endless === null 且 endlessInfo() 为空） | ✅ pass | null/null | {"endless":null,"info":null} |  |
| endlessResult 含本局成绩与 best（seconds/kills/coins/isBest） | ✅ pass | {seconds,kills,coins,isBest} | {"seconds":124,"kills":11,"coins":0,"wave":7,"isBest":true,"best":{"seconds":124,"kills":63,"coins":1450,"iso":"2026-11-18 23:39"},"pilot":"deepseek","companions":[]} |  |
| 打出更好成绩时刷新 endlessBest / isBest=true | ✅ pass | endlessBest 刷新 或 result.isBest=true | {"before":{"seconds":95,"kills":63,"coins":1450,"iso":"2026-11-18 21:40","char":"deepseek","cycle":1},"after":{"seconds":124,"kills":63,"coins":1450,"iso":"2026-11-18 23:39","char":"deepseek","cycle":1},"isBest":true,"pe… |  |
| endlessBest 单调不减（不会被打得更差的成绩覆盖） | ✅ pass | 单调不减 / 新纪录 | {"before":{"seconds":95,"kills":63,"coins":1450,"iso":"2026-11-18 21:40","char":"deepseek","cycle":1},"after":{"seconds":124,"kills":63,"coins":1450,"iso":"2026-11-18 23:39","char":"deepseek","cycle":1}} |  |
| endlessBest 含 seconds/kills/coins | ✅ pass | seconds/kills/coins | {"seconds":124,"kills":63,"coins":1450,"iso":"2026-11-18 23:39","char":"deepseek","cycle":1} |  |
| 本次无限模式计入次数（endlessRuns >= before+1） | ✅ pass | >= before+1 | {"before":0,"after":1} |  |
| 无限模式成就已记录（a_endless + 存活 60s 的 a_endless60） | ✅ pass | a_endless+a_endless60 | 齐全 |  |
| 用 setHp(1)+hit() 触发失败（尝试次数，仅记录） | ❌ info | undefined | {"hits":1,"loops":1,"peakSeconds":124,"killed":11} | 失败前命中次数与存活时长 |

### ✅ v5 · 存档迁移 1/2（写入 v4 旧 save key） `v5-migrate-write`

- URL：`index.html?screen=title`
- 截图：`reports/shots/v5qa_v5-migrate-write.png`（像素方差 1574.6）
- cdp 报告：`reports/qa-v5-logs/v5-migrate-write.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1574.63 |  |
| 页面 = title | ✅ pass | title | title |  |
| 已写入 fatfish_universe_save_v4 | ✅ pass | 写入成功 | {"v4Len":374} |  |
| 测试前当前/旧存档 key 已清空（保持旧档） | ✅ pass | false | {"v5Present":false,"v6Present":false} |  |

### ✅ v5 · 存档迁移 2/2（同 profile 重开，旧档被读取/迁移） `v5-migrate-read`

- URL：`index.html?screen=title&live=1`
- 截图：`reports/shots/v5qa_v5-migrate-read.png`（像素方差 1615.7）
- cdp 报告：`reports/qa-v5-logs/v5-migrate-read.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1615.7 |  |
| 页面 = title | ✅ pass | title | title |  |
| 旧档星辰币迁移（4321） | ✅ pass | 4321 | 4321 |  |
| 旧档出战神迁移（chatgpt） | ✅ pass | chatgpt | chatgpt |  |
| 旧档角色迁移（deepseek/chatgpt/claude） | ✅ pass | 3 个角色 | 齐全 |  |
| 旧档改装迁移（chatgpt hp=2 / shield=1） | ✅ pass | {"hp":2,"shield":1} | {"hp":2,"shield":1} |  |
| 旧档成就迁移（含 a_wok / a_mars） | ✅ pass | a_wok+a_mars | 齐全 |  |
| v4 旧档读入后新字段补默认（cleared=false / cycle=1 / historyLen=0） | ✅ pass | {"cleared":false,"cycle":1,"historyLen":0} | {"cleared":false,"cycle":1,"historyLen":0} |  |
| 旧档读入后立即写回当前存档 key（boot 时 v5/v6 key 已存在） | ✅ pass | v5 或 v6 key >0 | {"v5AtBoot":0,"v6AtBoot":609} |  |
| 触发一次 persist 后仍写回当前存档 key（v5/v6） | ✅ pass | v5 或 v6 key >0 | {"v5Len":0,"v6Len":609,"persistErr":null} |  |
| 旧 v4 key 仍保留（不破坏回退） | ❌ info | undefined | 374 | 旧存档长度（保留即可，非强制） |

### ✅ 移动端 · 标题 `m-title`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v5qa_m-title.png`（像素方差 1671）
- cdp 报告：`reports/qa-v5-logs/m-title.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1671 |  |
| 页面 = title | ✅ pass | title | title |  |

### ✅ 移动端 · 商城（窄屏列表） `m-shop`

- URL：`index.html?screen=shop&unlock=1&rich=1&lv=5`
- 截图：`reports/shots/v5qa_m-shop.png`（像素方差 1449.6）
- cdp 报告：`reports/qa-v5-logs/m-shop.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1449.57 |  |
| 页面 = shop | ✅ pass | shop | shop |  |
| 默认第 1 页 | ✅ pass | 0 | 0 |  |
| 9 位角色 | ✅ pass | 9 | 9 |  |

### ✅ 移动端 · 角色改装 `m-upgrade`

- URL：`index.html?screen=upgrade&unlock=1&rich=1`
- 截图：`reports/shots/v5qa_m-upgrade.png`（像素方差 1417.9）
- cdp 报告：`reports/qa-v5-logs/m-upgrade.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1417.87 |  |
| 页面 = upgrade | ✅ pass | upgrade | upgrade |  |
| 9 位角色 | ✅ pass | 9 | 9 |  |

### ✅ 移动端 · 飞行 `m-flight`

- URL：`index.html?screen=flight&stop=moon&live=1`
- 截图：`reports/shots/v5qa_m-flight.png`（像素方差 673.1）
- cdp 报告：`reports/qa-v5-logs/m-flight.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 673.06 |  |
| 页面 = flight | ✅ pass | flight | flight |  |
| 目标 = moon | ✅ pass | moon | moon |  |

### ✅ 移动端 · 设置页 `m-v5-settings`

- URL：`index.html?cleared=1&screen=settings`
- 截图：`reports/shots/v5qa_m-v5-settings.png`（像素方差 1207）
- cdp 报告：`reports/qa-v5-logs/m-v5-settings.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 1206.98 |  |
| 页面 = settings | ✅ pass | settings | settings |  |
| 设置界面已实现（静态扫描 drawSettingsScreen） | ✅ pass | drawSettingsScreen | 存在 |  |

### ✅ 移动端 · 通关记录页 `m-v5-records`

- URL：`index.html?cleared=1&screen=records`
- 截图：`reports/shots/v5qa_m-v5-records.png`（像素方差 933.2）
- cdp 报告：`reports/qa-v5-logs/m-v5-records.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 933.18 |  |
| 页面 = records | ✅ pass | records | records |  |
| 记录界面已实现 + 有历史数据 | ✅ pass | 界面 + historyLen>=1 | {"drawRecordsScreen":true,"historyLen":2} |  |

### ✅ 移动端 · 无限模式简报 `m-v5-endless`

- URL：`index.html?cleared=1&screen=endless`
- 截图：`reports/shots/v5qa_m-v5-endless.png`（像素方差 941.5）
- cdp 报告：`reports/qa-v5-logs/m-v5-endless.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 100） | ✅ pass | > 100 | 941.45 |  |
| 页面 = endless | ✅ pass | endless | endless |  |
| 无限模式界面已实现 + 已解锁 | ✅ pass | 界面 + cleared=true | {"drawEndlessScreen":true,"cleared":true} |  |

### ✅ 构建产物静态扫描（贴图 / 调试入口 / v4+v5 参数与界面 / 静态背景） `static`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| index.html 内 VERSION = '4.x' / '5.x' / '6.x' | ✅ pass | 4.x/5.x/6.x | 6.0.0 |  |
| CHARS 注入 8 位新角色立绘（deepseek 用 hero） | ✅ pass | 8 | 8 |  |
| TEX 注入 hero（deepseek 立绘） | ✅ pass | 存在 | 存在 |  |
| TEX 注入 star_* 恒星贴图 >= 10 张 | ✅ pass | >=10 | 13 |  |
| 构建含 setShopPage 调试入口 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 live=1（固定实时时钟） | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 time=<ms> | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 flight=1 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 resume=1 | ✅ pass | 存在 | 存在 |  |
| v4 URL 参数 screen=upgrade|solar | ✅ pass | 存在 | {"solar":true,"upgrade":true} |  |
| drawSpaceBg(t,warm,mode) 静态背景分支 + >=4 处 static 调用 | ✅ pass | 实现 | {"modeParam":true,"staticCalls":8} |  |
| 太阳系地图使用 A.solarPositions 真实黄经 | ✅ pass | 存在 | 存在 |  |
| 兼容读取 v4 存档 key（fatfish_universe_save_v4） | ✅ pass | 存在 | 存在 |  |
| v5 存档 key = fatfish_universe_save_v5 | ✅ pass | 存在 | 存在 |  |
| v5 界面：settings / records / endless 三个绘制函数 | ✅ pass | drawSettingsScreen/drawRecordsScreen/drawEndlessScreen | {"settings":true,"records":true,"endless":true} |  |
| v5 调试 API：clearGame/newCycle/startEndless/endlessInfo | ✅ pass | 全部存在 | ["clearGame:true","newCycle:true","startEndless:true","endlessInfo:true"] |  |
| v5 URL 参数 ?cleared=1 | ✅ pass | 存在 | 存在 |  |
| v5 URL 参数 ?endless=1 | ✅ pass | 存在 | 存在 |  |
| v5 URL 参数 ?cycle=<n> | ✅ pass | 存在 | 存在 |  |
| v5 URL 参数 screen=records|settings|endless | ✅ pass | 三个分支存在 | {"records":true,"settings":true,"endless":true} |  |

### ✅ 跨场景交叉断言（实时总航程 / 复现性 / v5 解锁链 / 全场报错） `cross`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| ?live=1 与 ?live=1&time=1900000000000 的实时总航程不同 | ✅ pass | 两个时刻总航程不同 | {"liveA":14026385403.8,"liveB":14862218281.5} |  |
| 固定 ?live=1 观测时刻可复现（两次运行总航程一致） | ✅ pass | 两次一致 | {"probe":14026385403.8,"run":14026385403.8} |  |
| 全部场景 console.error / 未捕获异常 = 0 | ✅ pass | 0 个场景报错 | 0 |  |
| 无 fail 场景（pending / warn 不算失败） | ✅ pass | 0 | 0 |  |
| v5 跨场景：已通关标题页（cleared=true）→ startEndless 后 state().endless 激活 | ✅ pass | cleared=true → endless 激活 | {"cleared":true,"endless":{"seconds":0,"mmss":"00:00","kills":0,"wave":1,"coins":0}} |  |
| v5 跨场景：clearGame() 累积通关历史（流程场景 ≥1 条、记录场景 ≥6 条） | ✅ pass | flow>=1 / records>=6 | {"flowHistory":1,"recordsHistory":8} |  |

## 4. 失败清单（代码 bug，Lead 要修）

无 🎉

## 5. 待集成清单（pending，等 Lead 最终构建后复跑）

无

## 6. 警告（warn，不算失败）

无

## 7. 复跑方式

```powershell
& "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe" tools/qa_v5_run.mjs
# 只跑部分场景：
& "...\node.exe" tools/qa_v5_run.mjs --only=v5-cleared-title,v5-clear-flow,v5-endless-start
# 带轮次标签：
& "...\node.exe" tools/qa_v5_run.mjs --label=final
```

> 产物：`reports/qa-v5-run.json`（机器可读）、`reports/qa-v5.md`（本文件）、`reports/shots/v5qa_*.png`、`reports/qa-v5-logs/*.json`。
> v4 回归脚本 `tools/qa_v4_run.mjs` 保留不动，历史报告 `reports/qa-v4-run.json` / `qa-v4.md` 不受影响。
