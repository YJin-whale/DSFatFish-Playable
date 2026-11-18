# Changelog

本项目（**肥鱼跳宇宙 · 星尘远航 / FatFish-Playable**）的所有重要变更记录在此文件。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循
[语义化版本](https://semver.org/lang/zh-CN/)。所有版本都在同一天（2026-11-18）
按需求迭代交付，版本号与游戏内 `VERSION` 常量一致。

## [6.0.0] - 2026-11-18

「音频系统 / 上传音乐 / 律动角色」。v6 需求与契约见 [`docs/SPEC-v6.md`](docs/SPEC-v6.md)。

### Added

- **音频引擎**（`src/audio.js`）：全局单例 `<audio>` + WebAudio 图
  （MediaElementSource → 音乐增益 → Analyser → 输出），切界面不重建、不暂停；
  音乐 / 音效音量均为 **0–1 连续值（无极调节）**，滑杆拖动、滚轮微调（Shift 0.005），
  数值写入存档（`musicVol` / `sfxVol`）。
- **两首内置曲目**：罐装毕加索《Let Me Go（共创版）》、星落落oi《Let me go》，
  统一压到 96 kbps 内联进单文件；设置里可播放 / 暂停 / 上一首 / 下一首 / 直接选曲。
- **上传本地音乐**：设置页「＋ 上传音乐文件」或把文件拖进窗口即可导入
  （mp3 / ogg / wav / m4a / webm，单文件 ≤ 48 MB），存入浏览器 **IndexedDB**
  （`fatfish_audio_v1/tracks`），**不上传服务器**、下次打开仍在，可逐首删除。
- **角色随节拍跳动**：每帧分析频谱（低频能量 + 能量突变 → `pulse`）得到 `dance`，
  主角色与飞行中的角色 / 伙伴做上下弹跳 + 纵向 squash & stretch（幅度 ~4%）；
  分析器不可用时用合成节拍兜底，保证角色仍会跟拍。
- **跨界面保持**：机库 / 发射台 / 飞行 / 结局切换时音乐不中断，曲目、播放状态与音量保持；
  左下角显示「♪ 曲名 · 音量%」；`M` 音乐开关、`N` 下一首。
- 设置页改为**双页签**：「♪ 音频设置」（默认）/「⚙ 游戏设置」。
- 存档 v6（`SAVE_KEY = fatfish_universe_save_v6`，兼容迁移 v5 / v4 / v3 / v2）：
  `musicVol / sfxVol / musicOn / musicTrack`。
- 调试 API：`musicState() / musicPlay(id) / musicToggle() / musicNext() /
  setMusicVolume(v) / setSfxVolume(v) / musicUploadTest(name,sec) / musicUnlock() /
  setSettingsTab('audio'|'game') / danceLevel() / musicDbCount()`；
  URL 参数 `?music=off|on`、`?musicVol=0.42`、`?sfxVol=0.9`、`?tab=audio|game`。
- `docs/SPEC-v6.md`（v6 规格与音频契约）。

### Changed

- `index.html` 单文件从约 3.4 MB 增至 **8.876 MB（9,089,288 B）**
  （含两首 96 kbps 内置音乐的 base64）。
- 构建顺序变为 `astronomy → audio → engine → render → ui`；`assets/audio/*.mp3` 注入
  `var SND = { key: dataURI }`，`assets/audio/raw/` 原始大文件不内联、不入库。
- 帮助页补充音频说明；设置页入口与 `O`（设置）/ `K`（通关记录）快捷键保持不变，
  音频页为默认页签。
- **新周目 / 清空存档改为明确确认弹窗**（v6.0.0 内 UX 修订）：单击标题页主按钮、结局页
  「再玩一次」或设置页入口统一弹出「开始新周目？」对话框——写明保留什么（成就 / 角色 / 改装 /
  通关记录 / 无限模式纪录）与重置什么（当前航程），提供「▶ 保留成就与记录，开始新周目」
  「清空全部存档，完全重来」「取消」三个明确选项（Esc 可关）；设置页条目改为
  「🔁 从地球重新开始（新周目）」，**任何时候**都能从地球重开（不必先通关完当前周目）；
  弹窗打开时拦截背景按钮与键盘，避免误触。

## [5.0.0] - 2026-11-18

「通关重玩 / 无限模式 / 仓库化」。v5 需求与契约见 [`docs/SPEC-v5.md`](docs/SPEC-v5.md)。

### Added

- **通关重玩**：完成 28 站后可「再玩一次」开新周目（`cycle + 1`），保留星辰币、
  已购角色、角色改装、成就、通关历史、无限模式成绩；当前周目新达成的成就单独记录。
- **通关历史记录界面**（`records`）：记录每一次通关的时间、模式（剧情 / 无限）、
  出战角色、同行伙伴、本次新达成成就、击毁飞船数、飞行员等级与星辰币；
  每页 5 条、支持翻页，最新在前，最多保留 50 条。
- **角色成就档案**：按角色记录「用这个角色达成过哪些成就」，在记录界面查看。
- **无限模式**（`endless`）：通关一次后解锁。同屏飞碟从 6 架起步、每 20 秒 +1 档
  （封顶 9 架），生成间隔 1.1–2.4 s；护盾掉落权重 ×0.35（降到 35%）、
  燃料拾取回复降到 18（普通 36）、燃料消耗 ×1.15、星辰币收益 ×1.8、
  击毁掉落 3–5 件（普通 2–3 件）。结算记录存活秒数 / 击毁数 / 本局星辰币，
  并保存历史最好成绩。
- **设置界面**（`settings`）：音效开关、通关记录入口、再玩一次（二次确认）、
  无限模式入口、清空存档（二次确认）。
- 新成就：`a_endless`（首次进入无限模式）、`a_endless60`（无限模式存活 60 s）、
  `a_endless100`（无限模式击毁 100 架）。
- 结局页新增「再玩一次 / 无限模式 / 通关记录」按钮；标题页右上角新增 ⚙ 设置入口，
  状态行显示「已通关 ×N · 无限模式已解锁」。
- 存档 v5（`SAVE_KEY = fatfish_universe_save_v5`，兼容迁移 v4 / v3 / v2）：
  `cleared / clearCount / cycle / cycleCleared / history / charAch / runAch /
  endlessBest / endlessRuns`。
- 调试 API：`clearGame() / newCycle() / startEndless() / endlessInfo()`；
  URL 参数 `?cleared=1`、`?screen=records|settings|endless`、`?endless=1`、`?cycle=2`。
- **仓库化**：新增根 `README.md`、`LICENSE`（代码 MIT）、`NOTICE.md`（素材逐项授权）、
  `.gitignore`、`.gitattributes`、`CHANGELOG.md`、`docs/screenshots/` 精选截图与
  GitHub Pages 部署工作流 `.github/workflows/pages.yml`；本仓库自此可直接提交 GitHub。

### Changed

- 抵达最后一站时记录通关（`cycleCleared` 防止重复写入），到达面板显示「★ 通关！」与通关次数。
- 无限模式飞行 HUD 改为显示「存活 mm:ss · 波次 W · 击毁 N · 本局 +星辰币」，
  隐藏章节进度条与航程尺。
- 无限模式不写续飞存档：中途退出视为放弃本局，不记录成绩。

## [4.0.0] - 2026-11-18

「实时太阳系 / 角色成长 / 伙伴战斗」。v4 需求与契约见 [`docs/SPEC-v4.md`](docs/SPEC-v4.md)。

### Added

- **实时太阳系**：`src/astronomy.js` 新增 `planetState / solarPositions /
  liveLegKm / liveSolarLeg / liveSolarRoute / formatUTC`，用 JPL《Approximate
  Positions of the Major Planets》的 J2000 轨道根数 + 世纪变率实时解算行星日心黄经。
- 太阳系地图按行星**当前真实黄经**摆放（不再是均匀圆弧），机库 / 地图显示观测时刻、
  各行星方位与**实时太阳系总航程**；新增 `?live=1`（固定 2026-11-18T12:00:00Z）与
  `?time=<ms>` 复现参数。
- **角色改装界面**：生命值 / 护盾上限 / 操控加速度各 0–5 级（120 / 160 / 100 星辰币起逐级翻倍）。
- **伙伴系统**：最多携带 2 名伙伴（Lv.3 解锁）；飞行中自动脱离编队反击外星飞船，
  伙伴护盾无上限、锅具样式 6 种轮换不重复。
- **飞行续存**：飞行中每 1.5 秒写续飞存档，暂停 / 切后台 / `pagehide` 立即落盘；
  标题页显示「继续飞行 · 第 N 段（xx%）」，`?flight=1`、`?resume=1` 可复现。
- 商城扩到 **9 位 AI 拟人角色**（3 页分页），全部使用用户提供的独立立绘。
- 恒星去同质化：10 颗恒星按有效温度黑体色 **程序化重建贴图**（256² RGBA），
  太阳用 NASA SDO/AIA 真实影像、银河系中心用 EHT Sgr A* 真实影像；
  星系照片（仙女座 / 三角座 / 大麦哲伦云 / 小麦哲伦云）来自 NASA/ESA。
- UFO 掉落奖励表：星辰币 / 燃料 / 护盾 / 生命值；新成就 `a_ufo_down`（飞船终结者）、
  `a_two_friends`（三鱼同行）、`a_upgrade`（改装完成）。
- 非飞行界面（标题 / 机库 / 发射台 / 商城等）改为**静态**太空背景，飞行中才有少量背景流星。
- 调试 API：`upgrade() / setCompanions() / spawnUFO() / killUFO() / saveFlight() /
  resumeFlight() / giveShield() / setShopPage()` 等。

### Changed

- 太阳系航段距离从「轨道半长轴之差」改为**两颗行星当前真实位置的三维弦长**
  （月球段固定 384,400 km）；2026-11-18 实测总航程 93.76 AU。
- 护盾从「最多 1 个、不叠加」改为**可叠加**（上限 = 1 + 改装等级 + 角色加成）。
- 商城角色立绘从 v3 的「大肥鱼换色」改为用户提供的 8 张独立 AI 立绘。
- 存档升级为 `fatfish_universe_save_v4`（兼容迁移 v3，`partner` → `companions[0]`）；
  `VERSION = '4.0.0'`。

## [3.0.0] - 2026-11-18

「星际跳跃改版」：把原版「按住 W 无脑爬升」的单文件小游戏改造成从地球出发、
直到可观测宇宙边缘的 28 站星际跳跃冒险。v3 规格见 [`docs/SPEC.md`](docs/SPEC.md)，
版本说明见 [`README-肥鱼跳宇宙-v3.md`](README-肥鱼跳宇宙-v3.md)。

### Added

- **28 站真实航程**：太阳系 9 站（月球 → 水星 → … → 冥王星）+ 银河系 12 站 +
  可观测宇宙 7 站，每段距离来自真实天文数据并可在界面查看。
- **真实星球贴图**：月球、水星、金星、火星、木星、土星、天王星、海王星、冥王星
  使用真实影像生成的球体贴图（Solar System Scope / NASA）。
- 月球成就「我的一小步，大肥鱼们的一大步」，月球可作为新跳跃点再次起跳。
- 起跳基础速度按**当地重力 / 地球重力比**换算（地球 11.186 km/s 基准）。
- **长按预演**：发射台长按角色（或按住空格）→ 背景缩小到当前层级全景 →
  白色虚线预测航线 → 瞬间切回 → 进入可操作的躲避 / 收集飞行。
- 飞行途中随机出现**外星飞船**并发射弹幕；护盾为头顶铁锅，受击旋转飞出。
- 动态**航程尺**：像素长度固定、满量程按 1/2/5 档增长、标记按比例下移。
- 星际商城（初始为 3 位角色）+ 双人同行 + 飞行员等级解锁。
- 单文件构建脚本 `build/build.py`：把 `src/*.js` 与 `assets/` 贴图 base64 内联成
  自包含 `index.html`（双击即玩，无任何运行时依赖）。
