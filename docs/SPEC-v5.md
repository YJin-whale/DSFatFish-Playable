# 肥鱼跳宇宙 · 星尘远航 v5 规格（通关重玩 / 无限模式 / GitHub 仓库化）

> v5 增量需求与契约。v3 见 `docs/SPEC.md`，v4 见 `docs/SPEC-v4.md`。
> 验收与交付状态见 `docs/SPEC-v5.md` 第 6 节；GitHub 仓库整理见根目录 `README.md`、`LICENSE`、`NOTICE.md`、`.gitignore`。

## 1. 用户 v5 需求（验收清单）

1. **通关后可「再玩一次」**：完成 28 站（进入终章）后，标题页/结局页可选择开新周目；保留已通关历史记录与已解锁成就（包括「使用某个角色时达成的成就」）。
2. **通关历史记录**：记录每一次通关：时间、模式、出战角色、同行伙伴、该次新达成的成就、击毁飞船数、飞行员等级等；独立界面可查看（分页）。
3. **角色成就档案**：每个角色单独记录「用这个角色达成过哪些成就」，可在记录界面查看。
4. **通关后解锁「无限模式」**：敌人数量非常多；防御道具（护盾）掉落降低；燃料回复降低；星辰币收益提升；每击败一个敌人掉落更多装备。
5. **无限模式成绩**：记录最好成绩（存活秒数/击毁数/星辰币），显示在无限模式界面与通关记录里。
6. **文档与仓库整理**：所有文件可提交 GitHub：根 README、许可证、素材授权 NOTICE、.gitignore、CHANGELOG、截图目录、GitHub Pages 部署工作流；不把本机运行环境路径、QA 临时产物、开发中间文件提交进去。

## 2. 存档契约（v5，`SAVE_KEY='fatfish_universe_save_v5'`，兼容迁移 v4/v3/v2）

在 v4 字段基础上新增：

```js
{
  // ... v4 全部字段
  cleared: false,          // 是否通关过（任一周目/模式）
  clearCount: 0,           // 通关次数
  cycle: 1,                // 周目序号（再玩一次 +1）
  cycleCleared: false,     // 当前周目是否已记录通关（防重复记录）
  history: [],             // 通关记录，最新在前，最多 50 条
  charAch: {},             // { charId: { achId: true } } 每个角色达成的成就
  runAch: [],              // 当前周目新达成的成就 id（开新周目清空）
  endlessBest: null,       // { seconds, kills, coins, iso, char }
  endlessRuns: 0           // 无限模式游玩次数
}
```

通关记录条目（`history[i]`）：

```js
{
  id: <ms>, iso: 'YYYY-MM-DD HH:mm', mode: 'story'|'endless',
  primary: 'chatgpt', primaryName: '聊天酱',
  companions: ['claude','kimi'],       // 角色 id
  achievements: ['a_mars','a_ufo_down'], // 本次新达成
  ufoKills: 12, pilotLv: 6, stardust: 2345,
  cycle: 2,
  seconds: 0, kills: 0                 // 仅 endless 有意义
}
```

- 兼容：v4 存档读入时 `cleared` 等补默认；旧 `partner`→`companions[0]` 迁移逻辑保留。
- `unlockAch()` 同时写 `runAch`（本周期新增）与 `charAch[S.primary][id]`（角色档案）。
- 通关判定：抵达最后一站（`S.trip >= A.STOPS.length`）时记录一次；`cycleCleared` 防重复。
- 开新周目：`S.trip=0, cycleCleared=false, runAch=[], cycle++, flight=null`；保留星辰币/角色/改装/成就/历史/无限模式成绩/cleared。

## 3. 无限模式契约

- **解锁**：`S.cleared === true`（通关过一次）。标题页/设置页/结局页显示入口，未解锁时置灰并提示。
- **进入**：`startEndless()` → 简报界面（`screen='endless'`）→ 开始 → `screen='flight'`，`G.endless.active=true`。
- **飞行参数**（相对普通飞行）：
  - 飞碟同时存在上限 `6`（普通 2），生成间隔 1.1~2.4s（普通 5.0~8.5s），弹幕间隔 ×0.6、弹速 ×1.1；
  - 护盾拾取权重 ×0.35（防御道具降低）；
  - 燃料拾取回复 18（普通 36），燃料消耗 ×1.15；
  - 星辰币收益 ×1.8；
  - 击毁 UFO 掉落件数 3~5（普通 2~3）；
  - 无终点：`progressRate=0`，不触发 `finishLeg`；`G.progress` 保持 0。
- **难度递增**：每 20 秒一档（wave），飞碟生成间隔再 ×0.88、上限 +1（封顶 9）、弹幕更快。
- **结束**：生命归零 → `screen='endless'` 结果显示：存活秒数、击毁数、本局星辰币、是否刷新纪录；写 `S.endlessBest`、`S.endlessRuns++`。
- **最佳纪录口径**：`S.endlessBest` 的存活秒数 / 击毁数 / 星辰币三项分项取历史最大值（任一项提高即 `isBest=true` 并刷新，其余项保留原纪录）；结果页显示合并后的最佳纪录。
- **成就**：`a_endless`（首次进入，进入时解锁）、`a_endless60`（无限模式存活满 60 秒，**游戏中即时解锁**）、`a_endless100`（累计击毁 100 艘，即时解锁）。
- **不参与续飞存档**：无限模式不写 `S.flight`；中途退出视为放弃本局（不记录成绩）。
- **HUD**：显示 `∞ 无限模式 · 存活 mm:ss · 波次 W · 击毁 N · 本局 +coins`；隐藏章节进度条与航程尺，显示难度标尺（可选）。

## 4. 界面契约（ui.js）

- 新界面：
  - `settings`（设置）：音效开关、通关记录入口、再玩一次（需通关+二次确认）、无限模式入口、清空存档（二次确认）、返回。
  - `records`（通关记录）：历史记录分页（每页 5 条，‹ › 翻页），每条显示模式/时间/角色/伙伴/新成就/战绩；角色成就档案（按角色显示达成数）；无限模式最佳成绩。
  - `endless`（无限模式简报 + 结果）：未解锁时显示锁定说明；结果态显示本局成绩与最佳纪录。
- 标题页：右上角新增 `⚙` 进设置；`S.cleared && 当前周目已通关` 时主按钮变「再玩一次（保留成就与记录）」（二次确认）；状态行显示「已通关 ×N · 无限模式已解锁」。
- 结局页：新增「再玩一次」「无限模式」「通关记录」按钮（保留回到标题）。
- 暂停界面（无限模式）：显示本局存活/击毁，「退出无限模式」→ 结果页（不记录未完成局）或标题。
- 到达最终站：面板显示「★ 通关！」与通关次数；按钮改为进入终章。

## 5. 调试 API / URL（QA 用）

`window.__FATFISH__` 新增：
`clearGame()`（模拟通关记录）、`newCycle()`、`startEndless()`、`endlessInfo()`（返回 `{active,seconds,kills,coins,wave,best}`）、`state()` 扩展 `cleared / clearCount / cycle / cycleCleared / canReplay / historyLen / history / charAch / charAchCounts / endlessUnlocked / endlessBest / endlessRuns / endless / endlessResult / historyPage`。

> `state().charAch` 与存档同构：`{ charId: { achId: true } }`；`state().charAchCounts` 是每个角色的成就计数（便于 QA 断言）。

URL 参数新增：`?cleared=1`（构造已通关存档，含 1~2 条历史与无限模式解锁）、`?screen=records|settings|endless`、`?endless=1`（直接进入无限模式飞行）、`?cycle=2`。

## 6. 交付状态（2026-11-18）

- [x] engine/render/ui 实现 + 构建通过（`index.html` v5.0.0 单文件，约 3.5 MB）
  - 存档 v5（`fatfish_universe_save_v5`，兼容迁移 v4/v3/v2，迁移后立即写回 v5 key）
  - 通关判定 / 历史记录（最多 50 条）/ 角色成就档案 / 新周目 / 无限模式 / 设置与记录界面
  - 调试 API：`clearGame / setCleared / newCycle / startEndless / endlessInfo / endlessFinish / setEndlessTime / endlessSpawn / setHistoryPage`
  - URL：`?cleared=1&clears=N&cycle=N`、`?screen=records|settings|endless`、`?endless=1`
- [x] QA v5 回归全绿（新增 clear/records/newcycle/endless/settings/migration 场景）
  - 最终构建 `index.html` v5.0.0（3479.1 KB，mtime 2026-11-18 22:53:09）
  - `node tools/qa_v5_run.mjs --label=final`：**50 场景 pass 50 / fail 0 / pending 0 / warn 0，退出码 0**
  - 覆盖：v4 全部基线（实时天文/商城/改装/飞行/续飞/伙伴/移动端）+ v5 通关记录、真实通关路径、新周目、设置、记录页、无限模式简报/开始/?endless=1/结束、存档迁移、构建产物静态扫描、跨场景交叉断言
  - 报告：`reports/qa-v5.md` / `reports/qa-v5-run.json`；截图 `reports/shots/v5qa_*.png`
- [x] README / LICENSE / NOTICE / .gitignore / .gitattributes / CHANGELOG / docs/screenshots / Pages workflow（repo-docs 交付）
  - `docs/screenshots/` 11 张 v5.0.0 实拍 WebP（合计 437.1 KB）；tracked 预计约 25 MB / 137 files（无 LFS 需求）
- [x] `docs/SPEC-v5.md` 验收记录（本文件）

已知口径：
- 无限模式不写续飞存档；中途退出视为放弃本局（不记录成绩），结束/失败才写 `endlessBest` 与 `endlessRuns`。
- 无限模式的星辰币在结算时全额入账；主线星辰币/角色/改装/成就与新周目共享同一存档。
- 通关历史按"记录一次通关"计：普通周目在抵达最后一站时记录；开新周目后 `cycleCleared` 重置，避免重复记录。
