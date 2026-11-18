# 肥鱼跳宇宙 · 星尘远航 v4（实时太阳系 / 角色成长 / 伙伴战斗）

> 单文件网页游戏。双击 `index.html` 即可开始，不需要安装任何东西。
> v3 说明见 `README-肥鱼跳宇宙-v3.md`，v4 增量规格见 `docs/SPEC-v4.md`。

---

## 一、怎么运行 / 怎么构建

- **直接玩**：双击 `index.html`（Chrome / Edge / 手机浏览器均可）。
- **改源码后重新构建**（改的是 `src/` 时）：
  ```powershell
  & "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe" build\build.py
  ```
  构建把 `src/astronomy.js → engine.js → render.js → ui.js`、`assets/tex/**`、`assets/chars/*.webp` 内联成单文件 `index.html`（当前 3438.9 KB）。
- **v4 交付物仍是单文件 `index.html`**（自包含，约 3.8 MB），可直接重新上传 WorkBuddy。

## 二、v4 按需求改了什么（对照用户 10 条）

| # | 用户要求 | v4 实现 |
|---|---|---|
| 1 | 太阳系八大行星按现实位置摆放 | `src/astronomy.js` 用 JPL J2000 轨道根数 + 世纪变率实时解算行星日心黄经；长按预演地图上 8 行星 + 冥王星按**当前真实黄经**摆放，轨道环仍按真实半长轴对数压缩。 |
| 2 | 实时监控太阳系、总里程随行星相对位置变化 | `A.planetState / A.solarPositions / A.liveSolarRoute`；机库与地图显示**观测时刻**、各行星黄经、**实时太阳系总航程**；太阳系航段距离改为两颗行星**当前真实位置三维弦长**（月球段固定 384,400 km）。2026-11-18 实测总航程 93.76 AU，2032-01 为 97.64 AU（相差 4.16%）。 |
| 3 | 非跳跃背景静态、跳跃时少量背景流星 | 标题/机库/发射台/商城/成就/改装/帮助等界面用 `drawSpaceBg(..., 'static')` 静态太空图；飞行中每 3.6–7.2 秒最多 1 道背景流星（`G.bgMeteors`），与飞行障碍陨石区分。 |
| 4 | 星辰币升级生命/护盾/加速度 | 新界面「角色改装」：生命值/护盾上限/加速度各 0–5 级，价格 120/160/100 起逐级翻倍；属性对出战角色生效（生命=3+升级，护盾上限=1+升级+GLM 加成，加速度 +10%/级）。 |
| 5 | 最多 2 名伙伴、可自动脱离反击 UFO | `S.companions` 两个槽位（Lv.3 解锁）；飞行中伙伴自动脱离编队飞向最近飞碟、发射友方弹丸、击毁后返回；HUD 显示「脱离反击中 ⚔」。 |
| 6 | 伙伴可携带护盾、数量无上限、贴图不重复 | 伙伴 `shields` 数组无上限；每层锅具按 6 种样式（铁锅/平底锅/砂锅/铜锅/蒸锅/小奶锅）轮换，环绕在伙伴身边显示。玩家护盾改为可叠加（上限 = 1 + 升级 + GLM）。 |
| 7 | 跳跃中退出不用回地球重来（存档） | 飞行中每 1.5 秒写一次续飞存档（progress/hp/fuel/护盾/伙伴护盾），暂停、切后台、`pagehide` 立即写；标题页显示「继续飞行 · 第 N 段（xx%）」，`?flight=1&progress=0.42` 可复现测试。抵达/失败自动清除。 |
| 8 | 银河系恒星同质化：不同颜色真实恒星贴图 | 10 颗恒星按**有效温度黑体色**生成写实贴图（`assets/tex/star_*.png`，256² RGBA），并补 `spectral/teffK`（G2V 5790K / M4V 3190K / M6V 2800K / A1V 9940K / K2V 5084K / F5IV 6530K / G8V 5344K / A7V 7550K / A0V 9600K / K1.5III 4286K）；太阳用 NASA SDO 真实影像、银心用 EHT Sgr A* 真实影像；银河系地图星点按光谱色着色 + 名字标注，抵达/飞行目标用各自贴图。 |
| 9 | 商城角色图不要大肥鱼换色 | 9 位角色全部用用户提供的 AI 立绘（DeepSeek 用 `hero.png`，其余 8 张去白底→300×400 透明 WebP），商城 3 页分页；ChatGPT/Claude/Gemini 为幼态版，Grok/Kimi/GLM/Qwen/MiniMax 暂用全身版（幼态图待用户确认后同名覆盖）。 |
| 10 | 击毁外星飞船掉落奖励 | 掉落表：星辰币 35% / 燃料 25% / 护盾 20% / 生命值 20%（新增 `hp` 拾取物，+1 HP，满血转星辰币）；击毁有爆炸、成就「飞船终结者」、`stats.ufoKills`。 |

### 其它 v4 变化

- 商城分页（9 角色 / 每页 3 位）+「角色改装」页签；机库新增「☉ 实时太阳系」读数、2 个伙伴槽位、改装入口。
- 飞行 HUD 增加：护盾 `×n/cap`、伙伴状态（数量/反击中/伙伴护盾数）、实时航段观测时刻。
- 新成就：`a_ufo_down`（飞船终结者）、`a_two_friends`（三鱼同行）、`a_upgrade`（改装完成）。
- 存档版本升到 `fatfish_universe_save_v4`，兼容迁移 v3（`partner` → `companions[0]`）。
- 版本号 `v4.0.0`。

## 三、实时太阳系数据说明（科学口径）

- **算法**：JPL "Approximate Positions of the Major Planets"（Standish）J2000 开普勒轨道根数 + 世纪变率 → 解偏近点角（牛顿迭代）→ 日心黄道 J2000 直角坐标；任意 ms 输入、按分钟缓存。
- **精度**：对 JPL DE421 参考值（2026-11-18）：最大黄经误差 **0.0738°**（土星）、最大日心距误差 **0.0416%**（木星）；2020–2035 采样最大 0.0741° / 0.1875%。参考值因本机网络无法直连 Horizons，用 DE421 本地计算 + 独立 VSOP87 实现交叉验证（差异 ≤0.005°），详见 `docs/astronomy-notes.md` §10。
- **航段距离**：太阳系第 1–8 段 = 两颗行星当前真实位置的三维弦长；第 0 段（地球→月球）= 384,400 km 固定值。总里程 = 9 段之和，随日期变化（2026-11-18 93.76 AU / 2032-01-01 97.64 AU）。
- **复现**：`?live=1` 把时钟固定到 2026-11-18T12:00:00Z；`?time=<ms>` 指定任意毫秒时间戳；`node build/check-astro.js` 通过 221 项自检。
- 声明：航段距离是"当前真实位置连线"，不是真实转移轨道（真实航线还受发射窗口/相位角影响），界面与帮助里都有注明。

## 四、恒星与行星贴图来源

- 行星：Solar System Scope（CC BY 4.0）等距柱状贴图 → 512² 正交球体 PNG；冥王星 NASA/JHUAPL/SwRI New Horizons PIA19952（公共领域）。
- 恒星（v4）：按有效温度黑体色 + 临边昏暗 + 米粒组织 + 日冕/星芒程序化重建；太阳用 NASA SDO/AIA 真实影像（公共领域）、银河系中心用 EHT Sgr A* 真实影像（CC BY 4.0，**Credit: EHT Collaboration**）。逐张来源/授权见 `assets/manifest-stars.json` 与 `reports/star-assets.md`。
- 星系：NASA/ESA 真实观测照片（仙女座、三角座、大麦哲伦云、小麦哲伦云）。
- 角色：用户提供的 8 张 AI 立绘 + `hero.png`；处理流水线与来源见 `assets/manifest-chars.json`、`reports/char-art.md`。

## 五、角色 / 伙伴 / 改装一览

| id | 名字 | 价格 | 被动 | 立绘状态 |
|---|---|---|---|---|
| deepseek | 深海小鲸娘 | 0 | 默认 | hero.png |
| chatgpt | 聊天酱 | 1200 | 星辰币 +10% | 幼态 ✅ |
| claude | 小星芒 | 1800 | 护盾无敌 +30% | 幼态 ✅ |
| gemini | 双星喵 | 2600 | 拾取范围 +25% | 幼态 ✅ |
| grok | 格萝克 | 2900 | 反击伤害 +50% | 全身（待幼态替换） |
| kimi | 月音酱 | 3200 | 燃料消耗 -20% | 全身（待幼态替换） |
| glm | 墨卷酱 | 3500 | 护盾上限 +1 | 全身（待幼态替换） |
| qwen | 千问酱 | 3800 | 星辰币 +15% | 全身（待幼态替换） |
| minimax | 小麦克 | 4100 | 加速度 +15% | 全身（待幼态替换） |

**幼态替换流程**（用户确认后同名覆盖即可）：
1. 按 `docs/chibi-generation-prompts.md` 在 genderswapai.com 生成 5 张幼态图（竖版 3:4、纯白底、全身）；
2. 覆盖 `assets/chars/raw/<id>.png`；
3. `python assets/chars/process_chars.py --only grok,kimi,glm,qwen,minimax`；
4. `python build/build.py` 重新构建。

## 六、自动化测试

- v4 回归（QA）：
  ```powershell
  $node = 'C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe'
  & $node tools/qa_v4_run.mjs
  ```
  报告：`reports/qa-v4-run.json` / `reports/qa-v4.md`，截图在 `reports/shots/v4qa_*.png`。
- 单场景（Chrome headless CDP，零依赖）：
  ```
  node tools/cdp_check.mjs --url "file:///C:/Users/admin/Desktop/FatFish-Playable/index.html?screen=shop&unlock=1&rich=1&lv=5" --scenario shop --wait-ms 1200 --shot reports/shots/shop.png --out reports/qa-shop.json
  ```
- 天文自检：`node build/check-astro.js`（221 项）。
- 游戏内调试接口（浏览器控制台）：`window.__FATFISH__`：
  `state() / goto(screen) / jumpTo(stopId) / setProgress(p) / setTime(ms) / liveInfo() / upgrade(id,key) / setCompanions([a,b]) / giveShield(n) / spawnUFO() / killUFO() / saveFlight() / resumeFlight() / setShopPage(n) / unlockAll() ...`
- URL 参数：`?screen=title|hangar|launch|flight|arrive|shop|upgrade|achv|help|ending|fail`、`?stop=moon`、`?progress=0.6`、`?zoom=0.9`、`?hold=1`、`?live=1`、`?time=<ms>`、`?flight=1&trip=2&progress=0.4`、`?resume=1`、`?unlock=1&rich=1&lv=5`。

## 七、文件结构

```
FatFish-Playable/
├─ index.html                 ← 最终交付：自包含单文件游戏（构建产物，勿手改）
├─ hero.png                   ← 默认角色深海小鲸娘
├─ src/
│  ├─ astronomy.js            ← 天文数据 + v4 实时行星位置 API（astro-live）
│  ├─ engine.js               ← 状态机/存档/续飞/飞行玩法/伙伴/升级/掉落/商城/成就/调试接口
│  ├─ render.js               ← 贴图/星球/恒星/角色/锅具/飞碟/背景流星/航线地图
│  ├─ ui.js                   ← 全部界面与输入（含角色改装、商城分页）
│  └─ index.template.html
├─ build/                     ← build.py、check-astro.js、astro 自检
├─ assets/
│  ├─ tex/                    ← 真实星球球体贴图 + v4 恒星贴图 + 星系照片
│  ├─ chars/                  ← 9 角色立绘（webp）+ 处理脚本 process_chars.py + 预览
│  └─ manifest-*.json
├─ tools/                     ← cdp_check.mjs（CDP 检查器）、qa_v4_run.mjs（v4 回归）
├─ docs/                      ← SPEC.md / SPEC-v4.md / astronomy-notes.md / chibi-generation-prompts.md
├─ reports/                   ← 各模块报告 + QA 截图
└─ README-肥鱼跳宇宙-v4.md
```

## 八、已知限制 / 下一步

1. **5 位角色幼态图待生成**：Grok / Kimi / GLM / Qwen / MiniMax 目前用用户提供的全身立绘，幼态替换流程见 §五（提示词已写好）。
2. **本机无法直连 JPL Horizons**：参考值用 DE421 + VSOP87 交叉验证；如以后能联网，按 `docs/astronomy-notes.md` §10.5 的 URL 模板刷新参考值即可。
3. 恒星贴图为 256² 程序化重建，凑近看分辨率有限；后续可换更高分辨率/真实观测图（放进 `assets/tex/star_*.png` 重新构建即生效）。
4. 续飞存档在浏览器 localStorage（单机、单浏览器），换设备/清缓存不保留；飞行中每 1.5s 存一次，极端崩溃最多丢 1.5 秒进度。
5. 伙伴反击为自动 AI，目前不带手动指令；护盾锅具样式 6 种循环使用。
6. 音频仍为简单合成音效，无背景音乐。
7. 本项目未接任何图像生成 API：角色幼态图需要用户按提示词在 genderswapai.com 生成后回填（见 §五）。

---

*改版：2026-11-18 · v4.0.0 · Lead + astro-live / char-art / star-art / qa-harness*
