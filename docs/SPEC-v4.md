# 肥鱼跳宇宙 · 星尘远航 v4 工程规格（太阳系实时化 / 角色成长 / 伙伴战斗）

> 本文件是 v4 全体协作者的唯一事实来源。v3 的规格见 `docs/SPEC.md`，v4 只描述增量与新契约。
> 游戏目录：`C:\Users\admin\Desktop\FatFish-Playable`
> 构建：`python build/build.py`（源文件 `src/*.js` → 单文件 `index.html`；`index.html` 为构建产物，禁止手改）
> 运行时：Python `C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe`（Pillow/numpy 可用）；Node `...\dependencies\node\bin\node.exe`；Chrome `C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`

## 1. 用户 v4 需求（验收清单）

1. **太阳系八大行星按真实位置摆放**：太阳系地图上 8 颗行星（+冥王星）必须按“当前真实黄经/位置”摆放，而不是均匀圆弧。
2. **实时监控真实太阳系**：界面能显示观测时刻与各行星当前方位；太阳系航段总里程随真实行星相对位置变化（不再用轨道半长轴之差）。
3. **背景**：未跳跃时（标题/机库/发射台/商城等）背景为静态太空图；跳跃飞行中可有少量陨石划过背景（不喧宾夺主）。
4. **星辰币升级角色属性**：生命值、护盾值、加速度三项可花星辰币升级。
5. **伙伴（最多 2 名）**：已出战角色外，最多携带 2 名伙伴一起发射；伙伴可自动脱离主角攻击外星飞船；伙伴可携带护盾（无上限、贴图不重复）。
6. **存档防丢失**：飞行途中退出，下次可从“当前航段 + 已飞进度”继续，不用回地球重来。
7. **银河系阶段恒星去同质化**：10 颗真实恒星使用不同颜色/形态的恒星贴图（按光谱型/有效温度），银河系地图与抵达画面都要体现；可用的官方网站/艺术家模拟真实星图作贴图，并在署名中注明来源。
8. **商城角色图**：不再是大肥鱼换色。现有 8 位 AI 拟人角色 + 默认深海小鲸娘共 9 位，用用户提供的立绘（ChatGPT/Claude/Grok/Gemini/Kimi/GLM/Qwen/MiniMax）。其中 Grok/Kimi/GLM/Qwen/MiniMax 的幼态形象后续由用户确认后替换（文件名不变，替换即生效）。
9. **击毁外星飞船掉落**：护盾、星辰币、燃料、生命值点。
10. **星程/数值科学化**：航段距离、总里程、观测时刻、行星方位必须可解释、可复现；数据来源写进 docs。

## 2. 写作用域（防止冲突）

| 路径 | 负责人 | 说明 |
|---|---|---|
| `src/astronomy.js`、`build/check-astro.js`、`docs/astronomy-notes.md`、`reports/astro-live.md` | **astro-live** | 实时行星位置 API 与自检 |
| `assets/chars/**`、`docs/chibi-generation-prompts.md`、`reports/char-art.md` | **char-art** | 9 角色立绘处理、幼态提示词 |
| `assets/tex/star_*.png`、`assets/tex/raw/star/**`、`assets/manifest-stars.json`、`reports/star-assets.md` | **star-art** | 恒星贴图 |
| `src/engine.js`、`src/render.js`、`src/ui.js`、`build/build.py`、`docs/SPEC-v4.md`、`docs/SPEC.md`、`README-肥鱼跳宇宙-v3.md`、`index.html` | **Lead** | 玩法/渲染/界面/构建/集成 |
| `tools/**`、`reports/qa-*`、`reports/shots/**` | **qa-harness** | 自动化回归 |

只写自己作用域内的文件；需要改别人的文件先给 Lead 发消息。

## 3. `src/astronomy.js` 新增契约（astro-live 必须严格实现）

保持 v3 已有导出（`A.STOPS/A.ACHIEVEMENTS/A.segment/A.legInfo/selftest/...`）不破坏，`A.selftest()` 仍须返回 `[]`。
新增（ES5，无 DOM，浏览器/node 均可执行）：

```js
// 1. 单行星状态：JPL “Keplerian Elements for Approximate Positions of the Major Planets”
//    J2000 轨道根数 + 世纪变率 → 任意时刻日心黄道直角坐标（J2000 黄道，AU）
A.planetState(id, ms)            // id: 'mercury'|'venus'|'earth'|'mars'|'jupiter'|'saturn'|'uranus'|'neptune'|'pluto'
                                 // 返回 { id, x, y, z, rAU, lonDeg, latDeg, ms }
A.solarPositions(ms)             // { earth:{...}, mercury:{...}, ..., pluto:{...}, sun:{x:0,y:0,z:0}, _ms, _iso }
// 2. 实时航段：太阳能段按两点当前真实位置的三维弦长；index 0（地球→月球）固定 384400 km
A.liveLegKm(fromId, toId, ms)    // 'moon' 按地球位置处理；返回 km（数值）
A.liveSolarLeg(index, ms)        // index = A.STOPS 下标（0..8）；返回
                                 // { index, fromId, toId, km, au, fixed, note }
A.liveSolarRoute(ms)             // 太阳系 9 段：{ legs:[liveSolarLeg...], totalKm, totalAU, ms, iso }
// 3. 时间工具
A.formatUTC(ms)                  // 'YYYY-MM-DD HH:mm:ss UTC'
A.nowMs()                        // 允许被外部覆盖的当前时间（默认 Date.now()）
```

约定：
- 月球段固定 384,400 km（地月平均距离），`fixed:true`；其余 8 段为实时弦长。
- 所有实时函数对同一 ms 必须返回一致结果（内部可缓存到分钟）；不得改变 `A.STOPS` 里的静态 `legDistanceKm` 字段（保留作离线基准）。
- 精度要求：行星位置与 JPL Horizons 对比，2020–2035 年内黄经误差 ≤ 0.1°，地日距误差 ≤ 0.3%（近似根数法正常水平）。用它算出的航段距离必须写进自检断言。
- 给 10 颗恒星站补 `spectral`（如 `'G2V'`）、`teffK`（有效温度，K）字段，数据来源 SIMBAD/Wikipedia，写注释与来源。
- `A.selftest()` 增加：实时 API 存在性、同一 ms 幂等、固定日期（2026-11-18T00:00:00Z）对 JPL Horizons 参考值的断言、总里程正值、8 段随日期变化（对比 2026-11 与 2032-01 的 totalKm 不同）。
- `docs/astronomy-notes.md` 追加 v4 章节：算法、根数表来源（JPL SSD https://ssd.jpl.nasa.gov/planets/approx_pos.html）、精度、与 v3 半长轴差法的区别、实时总里程如何随日期变化、如何复现（给一段 node 代码）。

## 4. 存档契约（v4，`SAVE_KEY='fatfish_universe_save_v4'`，兼容迁移 v3）

```js
{
  stardust, best, runs, trip, achievements, pilotXp, pilotLv, muted, firstRun,
  stats: { coins, ufoDodged, fail, wokBreak, legs, ufoKills },
  owned: ['deepseek', ...],           // 9 个角色
  primary: 'deepseek',
  companions: ['', ''],               // 最多 2 个伙伴，空串表示未携带
  upg: { '<charId>': { hp:0, shield:0, accel:0 } },   // 0..5 级
  flight: null | {                    // 飞行中自动存档（续飞用）
    trip, progress, runCoins, hp, maxHp, fuel, wokCount,
    savedAt, savedIso
  }
}
```
- v3 的 `partner` 迁移为 `companions[0]`；`upg` 缺省补 0。
- 飞行中每 ~1.5s 写一次 `flight`（localStorage），暂停/切后台/`pagehide` 立即写；抵达或失败时清空。
- 标题主按钮：`flight` 存在时显示“继续飞行 · 第 N 段（xx%）”，点击恢复该航段进度直接进入飞行；机库/发射台不受影响。

## 5. 角色、升级与伙伴（engine 实现，UI 契约）

### 5.1 CHARACTERS（9 位，engine 数组，顺序即商城顺序）

| id | 名字 | en | 价格 | 主题色 | 被动 |
|---|---|---|---|---|---|
| deepseek | 深海小鲸娘 | DeepSeek | 0 | #5AA9FF | 默认 |
| chatgpt | 聊天酱 | ChatGPT | 1200 | #10A37F | 星辰币 +10% |
| claude | 小星芒 | Claude | 1800 | #D97757 | 护盾无敌时间 +30% |
| gemini | 双星喵 | Gemini | 2600 | #A88BFF | 拾取范围 +25% |
| grok | 格萝克 | Grok | 2900 | #C9A227 | 反击伤害 +50% |
| kimi | 月音酱 | Kimi | 3200 | #8FB8FF | 燃料消耗 -20% |
| glm | 墨卷酱 | GLM | 3500 | #6E7B9A | 护盾上限 +1 |
| qwen | 千问酱 | Qwen | 3800 | #4A6BD8 | 星辰币 +15% |
| minimax | 小麦克 | MiniMax | 4100 | #FF8A5B | 加速度 +15% |

商城宽屏每页 3 张卡（分页 ‹ ›），窄屏纵向列表可翻页；卡片数据来自 `S.owned/primary/companions`。

### 5.2 升级（`S.upg[charId]`）
- 三项：`hp`（生命值）/`shield`（护盾上限）/`accel`（加速度），每项 0..5 级。
- 价格（星辰币）：hp `[120,240,480,960,1920]`；shield `[160,320,640,1280,2560]`；accel `[100,200,400,800,1600]`。
- 效果（仅对出战角色生效）：
  - `maxHp = 3 + upg.hp + (pilotLv>=5 ? 1 : 0)`
  - `wokCap = 1 + upg.shield + (pilot==='glm' ? 1 : 0)`（护盾可收集多个，受上限约束；伙伴不占此上限）
  - `accelMult = (1 + 0.10*upg.accel) * (pilot==='minimax' ? 1.15 : 1)`
- UI：新界面 `upgrade`（角色改装）：已拥有角色横向切换，三项等级点 + 当前效果 + 升级价格 + “升级”按钮；入口在商城/机库。
- debug API：`upgrade(charId, key)`（直接升一级，扣币，供 QA）、`giveStardust(n)`。

### 5.3 伙伴（最多 2 名）
- `S.companions` 两个槽位；商城卡片按钮：`伙伴 1` / `伙伴 2` / `取消`（不能与出战角色相同，不能重复；`pilotLv>=3` 解锁）。
- 飞行中：伙伴跟随阵型（左后/右后），有独立 `mode:'follow'|'attack'`。
- **自动反击**：场上有 UFO 且冷却到时，最近 UFO 的伙伴脱离编队 → 飞向 UFO → 发射友方弹丸（`G.friendBullets`）→ 命中扣 UFO 血 → 返回编队；每名伙伴独立冷却 1.6~2.6s。
- UFO 血量 3（grok 在场/出战则伤害 ×1.5，向上取整），击毁：爆炸粒子 + 掉落奖励 + `stats.ufoKills++` + 成就 `a_ufo_down`。
- **伙伴护盾**：伙伴可无限携带（`comp.shields` 数组）；拾取护盾时若伙伴未满员，30% 概率分配给伙伴（否则给玩家，玩家受 `wokCap` 限制）；伙伴护盾按顺序使用不同锅具贴图（`wokStyle` 0..N 循环，至少 4 种：铁锅/砂锅/平底锅/铜锅），不重复同一贴图连排。
- 掉落表（击毁 UFO）：星辰币 35% / 燃料 25% / 护盾 20% / 生命值 20%；生命值拾取 `kind:'hp'`，`+1 HP`（不超过 maxHp）。

### 5.4 飞船只 HUD 与飞行数值
- 玩家可持有多个护盾：`G.wokCount`（0..wokCap），受击消耗 1 个；HUD 显示 `🍳 ×n`，护盾碎裂动效沿用。
- 加速度用 `accelMult`；燃料消耗用 `kimi` 被动 ×0.8。
- 伙伴攻击在 HUD 顶部有提示（“伙伴自动反击中”）。

## 6. 渲染契约（render.js）

- `drawSpaceBg(t, warm)`：新增第三参 `mode`：`'static'` 时背景完全静态（固定星空/照片，不旋转不漂移），用于所有非飞行界面；`'flight'` 时保留动态星空 + 背景流星（少量）。
- 背景流星：`G.bgMeteors`，飞行中每 3.5~7s 最多 1 道，斜向划过，细长尾迹，alpha≤0.5；不得与飞行障碍（陨石）混淆。
- 恒星：stellar 站若有 `star_<id>` 贴图，抵达/飞行目标/银河地图用贴图 + 光晕；否则按 `stop.color` 程序化。银河地图所有恒星点按 `stop.color` 着色（不再全白）。
- 太阳系地图：`solarMapPositions()` 改为使用 `A.solarPositions(nowMs)` 的真实黄经（径向按轨道半长轴对数压缩，仅显示用）；轨道环保留；地球/月球用地球真实位置 + 月球偏移；界面显示“观测时刻 + 实时总航程”。虚线路径改为当前节点间连线（标注“实时位置连线，非转移轨道”）。
- 商城/机库/飞行角色立绘：使用 `CHARS[<id>]` 贴图（构建注入 `assets/chars/<id>.webp`）；缺图时保留色相兜底。
- 锅具样式：`drawWok(cx,cy,size,rot,alpha,style)` 支持 4+ 种锅型（默认为铁锅）。

## 7. 恒星贴图契约（star-art）

- 输出 `assets/tex/star_<id>.png`（`<id>` = astronomy.js 的 stellar 站 id），256×256 RGBA 透明底，星空/照片类可 512×512。
- 必交付：`star_alpha_cen/barnard/wolf359/sirius/eps_eri/procyon/tau_cet/altair/vega/arcturus.png`，可选 `star_galactic_center.png`（EHT Sgr A* 真实图像，CC BY 4.0，注明来源）、`star_galactic_edge.png`、`star_sun.png`（NASA SDO 太阳真实影像）。
- 每张：按有效温度黑体色温 → sRGB 主色；临边昏暗、米粒组织/表面纹理、日冕光晕、点花纹（衍射星芒可有可无）；巨星光晕更大（大角星 K1.5III）。
- 若有真实观测图像且授权允许（NASA/ESA/ESO 公共领域或 CC BY），优先用真实图像做底，注明来源与授权。
- `assets/manifest-stars.json`：每张 `{key,file,w,h,source,url,license,note,spectral,teffK}`；`reports/star-assets.md` 记录处理与校验（尺寸、透明通道、非空像素比例、体积）。

## 8. 角色美术契约（char-art）

- 用户提供 8 张立绘（附件目录，映射见下），复制到 `assets/chars/raw/` 存档后再处理：
  - ChatGPT `2bac4838...`（白发龙角、调色盘画笔，幼态）
  - Claude `6452189e...`（橙发向日葵，幼态）
  - Grok `b0af75fa...`（金发双马尾吸血鬼、巨斧，全身）
  - Gemini `9f23ed43...`（紫发猫娘、星星，幼态）
  - Kimi `9d67b670...`（银白蓝发、长笛礼服，全身）
  - GLM `85890b3b...`（黑发狼耳、GLM 书本，全身）
  - Qwen `176dea0b...`（蓝发汉服、折扇，全身）
  - MiniMax `d326f0c8...`（橙发记者、麦克风，全身）
- 去白底（边缘泛洪，保留白色服装内部）、裁切内容、透明化、统一画布 300×400（等比居中，底部对齐）、输出 `assets/chars/<id>.webp`（质量 80~88，单张 ≤ 90KB）+ `assets/chars/preview_compare.png`。
- `assets/manifest-chars.json` + `reports/char-art.md`（来源、处理步骤、尺寸、体积、预览）。
- 不改 `hero.png`；Grok/Kimi/GLM/Qwen/MiniMax 的幼态替换图后续同名覆盖。
- 另写 `docs/chibi-generation-prompts.md`：为 5 位缺幼态形象的角色写可直接粘贴到 genderswapai.com（GenderSwapAI）的中文提示词 + 参考图使用说明（参考图用 ChatGPT/Claude/Gemini 三张幼态图定画风，用角色全身立绘定要素），每张单独一节，含“两/三头身、粗描边、赛璐璐、白底、全身、正面”等画风约束。

## 9. QA 验收（qa-harness）

`window.__FATFISH__` 新增：`setTime(ms)`（覆盖实时时钟）、`liveInfo()`、`upgrade(id,key)`、`giveStardust(n)`、`setCompanions([a,b])`、`spawnUFO()`、`killUFO()`、`saveFlight()`、`resumeFlight()`、`setShield(n)`、`state()` 扩展字段（`live:{iso,totalAU,totalKm,legs}`, `upg`, `companions`, `wokCount`, `flightSaved` 等）。
URL 参数新增：`?live=1`（固定实时时钟到 2026-11-18T12:00:00Z 便于断言）、`?screen=upgrade|solar`、`?flight=1`（构造飞行中存档）。
必须覆盖场景：title/hangar/launch/flight/arrive/shop(9 角色分页)/upgrade/achv/help/ending、实时太阳系地图（行星黄经与 astronomy 计算一致）、续飞存档（重载后恢复进度）、伙伴反击击毁 UFO 掉落、护盾叠加上限、背景静态/流星、9 角色立绘加载。每场景截图 + JSON 断言，最终 `reports/qa-v4-*.json`，失败退出码非 0。

## 10. 验收口径（v4）

- 双击 `index.html` 可玩、无 JS 报错，单文件自包含；
- 太阳系地图行星按当前真实位置摆放，观测时刻/实时总航程可见，不同日期总里程不同（`?live=1` 固定时间可复现）；
- 飞行中退出→重进→“继续飞行”从原进度恢复；
- 星辰币可升级 hp/shield/accel，数值在飞行/界面生效；
- 最多 2 名伙伴同行、自动脱离反击 UFO、击毁掉落 4 类奖励；
- 银河 10 颗恒星颜色/贴图各异，地图与抵达画面体现；
- 商城 9 位角色立绘互不相同（不再换色），分页可用；
- 非飞行界面静态背景；飞行中少量背景流星；
- 移动端触屏可玩。

## 11. 交付状态（2026-11-18，已验收）

| 项 | 状态 | 证据 |
|---|---|---|
| 实时太阳系 API（astro-live） | ✅ 完成 | `node build/check-astro.js` 221 项通过；`A.selftest()=[]`；`reports/astro-live.md` |
| 9 角色立绘（char-art） | ✅ 完成（5 位幼态待替换） | `assets/chars/*.webp` 8 张 + `hero.png`；`preview_compare.png`；`reports/char-art.md`；幼态提示词 `docs/chibi-generation-prompts.md` |
| 10+ 恒星贴图（star-art） | ✅ 完成 | `assets/tex/star_*.png`（10 恒星 + sun + galactic_center + galactic_edge）；`assets/manifest-stars.json`；`reports/star-assets.md` |
| 游戏逻辑/界面/构建（Lead） | ✅ 完成 | `README-肥鱼跳宇宙-v4.md`；`index.html` v4.0.0 单文件（3438.9 KB） |
| 自动化回归（qa-harness） | ✅ 34/34 通过 | `reports/qa-v4.md`、`reports/qa-v4-run.json`、`reports/shots/v4qa_*.png` |
| 幼态图生成（5 位） | ⏳ 等用户确认 | 本机无图像生成通道、无法登录 genderswapai.com；提示词已写好，用户生成后同名覆盖 → 处理脚本 → build |

验收实测（QA，2026-11-18）：34 场景 pass 34 / fail 0 / pending 0；实时总航程 93.760595 AU（2026-11-18T12:00Z）与 99.347793 AU（2030-03-17）不同且可复现；天狼星/大角星飞行贴图正常；商城 3 页 9 立绘；伙伴反击 6s 内击毁 UFO；续飞跨 run 持久化通过；移动端 4 场景通过。
