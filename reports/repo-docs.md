# repo-docs 交付报告 · GitHub 仓库化整理（v5 / v6）

- 任务：共享任务 `task-5`「GitHub 仓库化整理（README/LICENSE/NOTICE/gitignore/CHANGELOG/Pages）」
- 负责人：**repo-docs**
- 日期：2026-11-18（五阶段：仓库骨架 → v5 最终构建补截图 → v6 音频版仓库更新 → v6 QA 全绿收尾 → **v6.0.0 内 UX 修订同步**）
- 工作目录：`FatFish-Playable`（本机无 `git` 命令，所有体积为按 `.gitignore` 规则脚本模拟求和）
- 写作用域：`README.md`、`LICENSE`、`NOTICE.md`、`.gitignore`、`.gitattributes`、
  `CHANGELOG.md`、`.github/**`、`docs/screenshots/**`、`reports/repo-docs.md`
- **未改动**：`src/**`、`index.html`、`build/build.py`、`assets/**` 素材本体、`docs/SPEC*.md`、
  `docs/astronomy-notes.md`、`docs/chibi-generation-prompts.md`、
  `README-肥鱼跳宇宙-v3.md`、`README-肥鱼跳宇宙-v4.md`。
- **验收对象（最终）**：v6.0.0（含 UX 修订）`index.html` = **9,089,288 B / 8.876 MB**，
  `VERSION = '6.0.0'`，mtime **2026-11-18 23:35:23**，sha256 前缀 **`b20bf9c7`**。
  历史对照：v6 初版 9,087,183 B / sha `fb9c1c0b` / mtime 23:09:00；v5 = 3,561,747 B / mtime 22:19:02。
- **v6.0.0 UX 修订（同版本内）**：新周目 / 清空存档改为**明确确认弹窗**（保留成就开始新周目 /
  清空全部存档完全重来 / 取消，Esc 可关；弹窗拦截背景按钮与键盘）；设置页入口改为
  「🔁 从地球重新开始（新周目）」且**任何时候**可用。受影响截图：`10-settings`、`11-cleared-title`
  重拍，新增 `16-newcycle-confirm`。
- **QA 状态（最终，Lead 确认）**：v6 音频 **18/18 pass**（label=`final-uxfix`）、
  v5 基线 **50/50 pass**（label=`v6.1-baseline`），fail 0 / pending 0 / warn 0，退出码 0；
  报告 `reports/qa-v6.md`（40.0 KB）与 `reports/qa-v6-run.json`（79.7 KB）已覆盖为最新。

## 1. 编写依据（先读后写）

| 文件 | 用途 |
|---|---|
| `docs/SPEC-v6.md` | v6 增量需求、存档 v6、音频模块契约、界面与 URL 契约 |
| `reports/qa-v6.md` / `qa-v6-run.json` / `tools/qa_v6_run.mjs` | v6 验收口径、关键实测值（音量 / dance / 上传 / 跨界面保持）、场景清单 |
| `src/audio.js`（头部注释 + 导出） | 音频引擎实现事实：全局单例 `<audio>`、WebAudio 图、IndexedDB、`musicImportTestBlob` |
| `src/ui.js`（`applyUrlParams`、设置页） | v6 URL 参数实际支持：`?tab=audio`、`?musicVol`、`?sfxVol`、`?music=off|on` |
| `src/engine.js`（`__FATFISH__`） | v6 调试 API 实际名称：`musicUploadTest / musicUnlock / danceLevel / musicDbCount` |
| `docs/SPEC-v5.md`、`reports/qa-v5.md`、`tools/qa_v5_run.mjs` | v5 契约与 50 场景基线（v6 回归基线） |
| `reports/qa-v4.md`、`README-肥鱼跳宇宙-v4.md` | v4 历史验收口径 |
| `assets/manifest-*.json`、`reports/star-assets.md`、`reports/char-art.md` | 素材逐张来源与授权（NOTICE §3–§6） |
| `assets/audio/`、`assets/audio/raw/` | 两首成品 mp3 体积与来源（NOTICE §7）；raw 需 gitignore |
| `build/build.py` | 构建输入（`assets/tex`、`assets/chars`、`assets/audio` 顶层 + `hero.png`；`raw/` 不参与） |
| `tools/cdp_check.mjs` | 截图 / QA 命令（`--mobile`、`--eval`、视口参数；Chrome 带 `--autoplay-policy=no-user-gesture-required`） |

## 2. 交付清单（最终）

| # | 文件 | 内容 | 状态 |
|---|---|---|---|
| 1 | `README.md` | GitHub 首页：英文 2 句简介 + 中文定位 + 6 个静态徽章（**v6.0.0**）+ 主截图 + 特性（含**音频系统 v6**、**新周目确认弹窗 UX 修订**、v5 全量、8.7 MB 单文件）+ 截图墙 **16 张**（v5 新界面 4 张 + 新周目确认大图 +「音频系统（v6）」4 张）+ 玩法操作（含 `M`/`N`、新周目确认）+ 快速开始（构建链含 `audio.js`/`assets/audio`）+ 自动化测试（**qa_v6_run + v5 基线全绿结论 + 关键实测摘录**、qa_v4_run、cdp_check、天文自检）+ 调试 API/URL 参数（v4–v6）+ 项目树 + 技术栈（5 个 JS 模块 / WebAudio / IndexedDB）+ 素材来源 + 已知限制 + Pages 部署 + License + 版本文档 + 致谢 | ✅ 完成 |
| 2 | `LICENSE` | MIT（2026，FatFish-Playable contributors）+ 素材授权分离（含内置音乐：版权归原权利人、非商业、再分发需授权） | ✅ 完成 |
| 3 | `NOTICE.md` | §1 代码 / §2 天文数据 / §3 行星贴图 / §4 星系照片 / §5 恒星贴图（**Credit: EHT Collaboration**）/ §6 角色立绘（默认角色 CC BY-NC-SA 4.0）/ **§7 音乐（两首第三方曲目 + 用户上传音乐）** / §8 字体与音效 / §9 合规速查（含音乐两行） | ✅ 完成 |
| 4 | `.gitignore` | Python 缓存 / 系统杂项 / QA 临时产物（截图、逐场景 JSON、cdp 日志、Chrome profile、`tools/_*` 探针）/ 构建中间产物 / **`assets/audio/raw/`** / 根目录 v3 遗留 / 打包文件；保留 `assets/*/raw/` 源素材与 `assets/audio/*.mp3` 成品 | ✅ 完成 |
| 5 | `.gitattributes` | `* text=auto eol=lf` + 文本类型显式声明（`.ps1` CRLF）+ 图片/音频/字体/压缩包 binary + `index.html` linguist 标记 | ✅ 完成 |
| 6 | `CHANGELOG.md` | Keep a Changelog：**[6.0.0]**（音频引擎/无极音量/两首内置曲/上传模块/律动/跨界面保持/双页签/存档 v6/8.7MB/构建顺序/**新周目确认弹窗 UX 修订**）、[5.0.0]、[4.0.0]、[3.0.0]，日期均 2026-11-18 | ✅ 完成 |
| 7 | `docs/screenshots/` | **16 张 v6.0.0 实拍截图**（11 张重拍 + 4 张音频主题 + 1 张新周目确认弹窗；`10/11` 因 UX 修订重拍；webp，单张 19.9–48.1 KB，合计 **624.3 KB**） | ✅ 完成 |
| 8 | `.github/workflows/pages.yml` | GitHub Actions 静态 Pages（checkout → configure-pages → upload-pages-artifact 根目录 → deploy-pages）；README 有启用步骤 | ✅ 完成 |
| 9 | `reports/repo-docs.md` | 本文件（最终交付记录） | ✅ 完成 |

> `docs/SPEC-v6.md`、`src/audio.js`、`index.html`、`assets/audio/` 均属 Lead / qa-harness 作用域，本次只读不改。

## 3. `.gitignore` 依据（最终）

模拟规则后：**tracked ≈ 34.88 MB / 149 files**，**排除 ≈ 273.99 MB / 915 files**。

| 忽略规则 | 代表路径 | 排除体积 | 依据 |
|---|---|---|---|
| `reports/shots/` | v4 / v5 / v6 / 终验各轮 QA 截图（303 张） | 194.89 MB | 每轮 QA 截图输出，可重跑 `tools/qa_v*_run.mjs` 重建；仓库只留精选 `docs/screenshots/` |
| `assets/tex/_build/` | 贴图编码试验 / 预览 / 下载原图缓存（203 个） | 61.81 MB | 贴图流水线中间产物，成品在 `assets/tex/*.png` / `*.jpg` |
| `assets/audio/raw/` | 用户提供的两首原始 mp3（5.1 MB + 8.9 MB） | 13.39 MB | 原始大文件不内联、不提交；96 kbps 成品 `assets/audio/*.mp3`（3.93 MB）**保留跟踪** |
| 根目录 `layer-*.png`、`preview-*.png`、`layers-overview.png`、`index_original_backup.html` | 10 个 v3 开发期遗留文件 | 2.43 MB | 分层调试图与改版前备份，不参与当前构建 |
| `reports/qa-*.json`（`!qa-v4/v5/v6-run.json`） | 258 个逐场景 cdp 日志 / 截图报告 | 0.78 MB | 一场景一个临时 JSON；只保留三份汇总机读报告 |
| `reports/qa-*-logs/`、`reports/_qa*/` | v4/v5/v6 的 cdp 日志与 headless Chrome profile（130 个） | 0.45 MB（profile 运行时另计 5 MB 级） | QA 运行缓存，可重跑生成 |
| `tools/_*` | `_probe_v5_*.js`、`_qa_v6_static_scan.mjs`（4 个） | 0.01 MB | 以下划线开头的一次性探针 / 静态扫描脚本（文件头自述「可删」）；正式执行器 `tools/qa_v*_run.mjs` 保留 |
| `build/*.png`、`build/bg_milkyway.jpg` | 构建兜底贴图 | 0.23 MB | 仅当 `assets/tex/` 缺图时才被 `build.py` 使用 |
| `__pycache__/`、`*.pyc`、`Thumbs.db`、`.DS_Store`、`*.zip`、`*.log` 等 | 缓存 / 系统 / 打包 / 日志 | ~0 | 与本机环境绑定，不应入库 |
| `assets/chars/raw/chibi_drafts/` | 幼态图草稿 | 0（当前不存在） | 预留：用户确认后同名覆盖 `raw/<id>.png` 才进构建 |

**保留跟踪的素材源文件**：`assets/tex/raw/`（6.81 MB）、`assets/chars/raw/`（9.63 MB）、
`assets/audio/*.mp3`（3.93 MB，两首成品）。

## 4. 截图清单（`docs/screenshots/`，全部来自 v6.0.0 最终构建）

压缩方式：Pillow 12.3.0，LANCZOS（桌面 1280×800 / 手机 390×844 保持原尺寸），
WebP `quality=82 / method=6`，**全部单张 19.9–48.1 KB（限值 300 KB）**，合计 **624.3 KB / 16 张**。
全部截图右下角水印为 **v6.0.0**，与最终构建（sha256 `b20bf9c7`，含 UX 修订）一致。

| 文件名 | 源截图（`reports/shots/`） | 页面（query） | 体积 | README 位置 |
|---|---|---|---|---|
| `01-title.webp` | `v6qa_title.png` | `?screen=title&unlock=1&lv=5` | 43.4 KB | 页首主图 |
| `02-solar-map.webp` | `v6qa_launch-live-map.png` | `?screen=launch&stop=neptune&hold=1&live=1` | 48.1 KB | 实时太阳系地图 |
| `03-flight-partners.webp` | `v6qa_partners-ufo.png` | `?screen=flight&stop=moon&live=1` + eval `setCompanions(['chatgpt','claude']);setHp(9);spawnUFO()` | 47.7 KB | 飞行 + 伙伴反击 |
| `04-shop.webp` | `v6qa_shop-p1.png` | `?screen=shop&unlock=1&rich=1&lv=5` | 46.0 KB | 商城 9 角色 |
| `05-upgrade.webp` | `v6qa_upgrade.png` | `?screen=upgrade&unlock=1&rich=1&lv=5` | 47.9 KB | 角色改装 |
| `06-arrive-sirius.webp` | `v6qa_arrive-sirius.png` | `?screen=arrive&stop=sirius&unlock=1&rich=1&lv=5` | 36.3 KB | 抵达天狼星 |
| `07-mobile-title.webp` | `v6qa_m-title.png` | 标题页 + `--mobile --width 390 --height 844` | 21.5 KB | 手机端标题 |
| `08-endless.webp` | `v6qa_endless.png` | `?screen=endless&cleared=1` | 29.5 KB | v5 无限模式简报 |
| `09-records.webp` | `v6qa_records.png` | `?screen=records&cleared=1&clears=2&unlock=1&lv=5` | 43.0 KB | v5 通关记录 + 角色档案 |
| `10-settings.webp` | `v6qa_settings.png`（UX 修订后重拍） | `?screen=settings&cleared=1&tab=game` | 37.5 KB | v5 游戏设置页（双页签；「从地球重新开始」） |
| `11-cleared-title.webp` | `v6qa_cleared-title.png`（UX 修订后重拍） | `?screen=title&cleared=1&clears=2&cycle=2&unlock=1&lv=5` | 46.2 KB | 通关后标题页（主按钮「▶ 开始新周目」） |
| `12-audio-settings.webp` | `v6qa_audio-settings.png` | `?screen=settings&tab=audio&musicVol=0.55` + eval `musicUnlock();musicPlay('builtin:bgm_canned_picasso')` 等 2.2 s | 36.5 KB | v6 音频设置（播放中） |
| `13-audio-upload.webp` | `v6qa_audio-upload.png` | 同上页 + eval `musicUploadTest('测试节拍',2)` 等 2 s | 37.1 KB | v6 上传列表（共 3 首） |
| `14-audio-mobile.webp` | `v6qa_audio-mobile.png` | 音频页 + `--mobile --width 390 --height 844` + 播放 | 19.9 KB | v6 移动端音频页 |
| `15-dance-title.webp` | `v6qa_dance-title.png` | `?screen=title&unlock=1&lv=5` + eval 播放并等 2.8 s（角色跟拍、左下 ♪） | 43.5 KB | v6 角色律动 |
| `16-newcycle-confirm.webp` | `v6qa_newcycle-confirm.png` | `?cleared=1&clears=2&cycle=2` + eval `openNewCycleConfirm()` 等 0.45 s | 40.5 KB | v6.0.0 UX 修订：新周目确认弹窗 |

- 采集命令：`node tools/cdp_check.mjs --url "<index.html 文件协议 URL>?<query>"
  --scenario v6-<id> --wait-ms 800~2500 --shot reports/shots/v6qa_<id>.png --out reports/qa-v6-shot-<id>.json`
  （音乐场景用异步 `--eval` 内 `await sleep(...)` 等播放 / 分析器稳态；移动端加 `--mobile --width 390 --height 844`；
  新周目弹窗用 `--eval` 打开后等 0.45 s 让弹窗渲染再截图）。
- 播放态验证：12 显示「Let Me Go（共创版）— 罐装毕加索 / 播放中 / 55% / 85%」；
  13 显示「测试节拍 · 本地上传 / 播放中 / 共 3 首（内置 2）」；15 左下角「♪ Let Me Go（共创版）· 55%」且角色弹跳。
- UX 修订验证：10 游戏设置页显示「🔁 从地球重新开始（新周目）· 任何时候都可以从地球重新出发」；
  11 主按钮「▶ 开始新周目（保留成就与记录）」；16 弹窗「开始新周目？」含保留 / 重置说明、
  「保留成就与记录，开始新周目」「清空全部存档，完全重来」「取消」三键，背景按钮被压暗。
- 源 PNG 在 v6 复跑 QA 后会被覆盖，重压缩即可再生；压缩参数记录在本节与体积行。

## 5. 体积核算（最终 tracked）

| 类别 | 体积 | 文件数 | 说明 |
|---|---|---|---|
| `assets/` | 23.41 MB | 82 | 贴图成品 1.91 MB + `tex/raw` 6.81 MB + 角色 1.0 MB + `chars/raw` 9.63 MB + **`audio/*.mp3` 3.93 MB** + manifest |
| `index.html` | 8.876 MB | 1 | v6.0.0（含 UX 修订）自包含构建产物（9,089,288 B / sha `b20bf9c7`，含两首内置音乐 base64） |
| `reports/` | 1.09 MB | 16 | 各模块 md + `qa-v4/v5/v6.md` + 三份 run.json + `star-contact-sheet.png` |
| `docs/` | 0.71 MB | 22 | SPEC ×4 + astronomy-notes + chibi-prompts + `screenshots/` ×16（624.3 KB） |
| `tools/` | 0.36 MB | 5 | `cdp_check.mjs`、`qa_v4/v5/v6_run.mjs`、`qa_final_run.ps1` |
| `src/` | 0.33 MB | 6 | v6 源码（含 `audio.js`） |
| `hero.png` | 0.19 MB | 1 | 默认角色立绘 |
| `build/` | 0.03 MB | 7 | `build.py`、`check-astro.js`、stub、e2e 脚本 |
| 根目录文档/配置 | 0.08 MB | 7 | README / CHANGELOG / NOTICE / LICENSE / .gitignore / .gitattributes / 历史 README |
| **合计** | **≈ 34.88 MB** | **149** | 在用户目标「≈36 MB」内；无需 Git LFS（最大单文件 `index.html` 8.876 MB < 100 MB） |

> 排除量：**273.99 MB / 915 files**（reports/shots 194.89 MB、assets/tex/_build 61.81 MB、
> `assets/audio/raw` 13.39 MB 为主）。
> 版本对比：v5 tracked 25.10 MB / 137 files → v6 tracked 34.88 MB / 149 files
> （+ `index.html` 5.31 MB、+ 音频成品 3.93 MB、+ QA 报告与 v6 工具 ~0.21 MB、+ 5 张截图 ~0.19 MB，
> 其中 UX 修订带来 `index.html` +2 KB 与 3 张截图增改）。

## 6. 自检记录（最终）

| 检查 | 方法 | 结果 |
|---|---|---|
| 交付文件相对链接与图片路径 | 正则提取 8 个交付文件的相对链接 / `src`，逐一 `os.path.exists` | ✅ **52 个链接全部存在**（含 `reports/qa-v6.md`、`docs/SPEC-v6.md`、16 张截图） |
| 本机绝对路径 / 环境泄漏 | 8 个交付文件逐行扫描盘符路径、用户目录、运行环境目录、file 协议 | ✅ **0 命中** |
| README 图片引用与目录对账 | 16 个 `docs/screenshots/*.webp` 引用 ↔ 目录 | ✅ **16/16 一致**（无缺失、无未引用） |
| 截图格式与体积 | 读 RIFF/WEBP magic + 字节数 | ✅ 16/16 合法 WebP，19.9–48.1 KB（合计 624.3 KB） |
| README 目录（TOC）锚点 | GitHub slug 规则 ↔ 实际 `##` 标题 | ✅ 13/13 命中 |
| v6 验收结论一致性 | README 声明 ↔ `qa-v6.md` / `qa-v6-run.json`（18 场景 + v5 基线 50 场景，exit 0） | ✅ 一致（最终报告 label=`final-uxfix` / `v6.1-baseline`，已覆盖为最新） |
| v6.0.0 UX 修订一致性 | README / CHANGELOG 描述 ↔ `10`/`11`/`16` 截图实际文案 | ✅ 一致（弹窗三键 + Esc/取消，设置页「从地球重新开始」） |
| gitignore 不含成品音频、raw 已排除 | 规则核对 + 模拟 | ✅ `assets/audio/*.mp3` 跟踪（3.93 MB）、`assets/audio/raw/` 排除（13.39 MB） |
| tracked 体积 | 脚本模拟 `.gitignore` 全量求和 | ✅ 34.88 MB / 149 files（排除 273.99 MB / 915 files） |
| 本机 `git` | `git --version` | ❌ 本机未安装 git → 提交动作由 Lead 在装好 git 的环境执行 |

## 7. QA 结果摘要（写进 README 的依据）

| 项 | 值 | 来源 |
|---|---|---|
| v6 音频场景 | 18 个：pass 18 / pending 0 / warn 0 / fail 0，退出码 0（label=`final-uxfix`） | `reports/qa-v6.md` |
| v5 基线 | 50 个：pass 50 / fail 0，构建 sha256 与当前一致（label=`v6.1-baseline`） | `reports/qa-v6.md` §1 |
| 内置曲目 | 2 首（Let Me Go（共创版） / Let me go） | `caps` |
| URL 音量 | `?musicVol=0.42` / `?sfxVol=0.9` 生效并落盘 | `settings-url-volume` |
| 无极滑杆 | 连续 6 档：0.13 / 0.27 / 0.31 / 0.5 / 0.666 / 0.9 | `settings-slider` |
| 播放律动 | `danceLevel()` 峰值 0.879（200 ms 出数；level 0.15 / bass 0.507） | `play` |
| 跨界面保持 | title → launch → flight：playing=true / volume=0.44 / 曲目不变；飞行中 dance 0.624 | `cross-keep` |
| 上传 / 删除 | 列表 3 首（内置 2）/ 上传 1；`musicDbCount()=1`；删除后归 0 | `upload-add` / `upload-remove` |
| 跨启动持久化 | 重开 profile 后 uploaded=1 / vol=0.37 / db=1 | `persist-read` |
| 移动端 | 390×844 音频页 sliders=2 / volume=0.66 | `m-audio-settings` |

> **v6.0.0 UX 修订（同版本内修复）**：标题页主按钮 / 结局页 / 设置页入口统一改为「开始新周目？」确认弹窗
> （保留成就与记录开始新周目 / 清空全部存档完全重来 / 取消，Esc 可关；弹窗拦截背景按钮与键盘）；
> 设置页条目改为「🔁 从地球重新开始（新周目）」，任何时候可用。受影响的 10/11 截图已重拍，
> 并新增 16 号弹窗截图。最终回归已用同一构建（sha `b20bf9c7`）跑完：
> **v6 音频 18/18（`final-uxfix`）+ v5 基线 50/50（`v6.1-baseline`）全绿，fail 0，exit 0。**

## 8. 待补项

1. **无阻塞项**：v6 仓库化交付完毕，可直接提交 GitHub。
2. **角色幼态图**（非阻塞、历史项）：Grok / Kimi / GLM / Qwen / MiniMax 五张幼态图待用户确认后
   同名覆盖 `assets/chars/raw/<id>.png` 并重跑处理脚本 + 构建；README「已知限制」与 NOTICE 表述已兼容。
3. **`docs/SPEC-v5.md` / `SPEC-v6.md` §交付状态勾选** 属 Lead 作用域，本次未改 SPEC 文档。

## 9. 提交建议（给 Lead，装好 git 的环境执行）

```bash
cd FatFish-Playable
git init -b main
git add -A
git status --short          # 应约 149 个文件、≈35 MB；不应出现 reports/shots、assets/audio/raw、assets/tex/_build
git commit -m "feat: 肥鱼跳宇宙 v6.0.0 音频版 —— 内置 BGM/无极音量/本地上传/角色律动，新周目确认弹窗 UX 修订；仓库整理（README/NOTICE/CHANGELOG/16 截图/Pages）"
git remote add origin https://github.com/<用户名>/FatFish-Playable.git
git push -u origin main
```

- push 前确认：`index.html` = **9,089,288 B / 8.876 MB**，sha256 `b20bf9c7…`，VERSION 6.0.0；
  `assets/audio/` 顶层只有两首成品 mp3（3.93 MB），`assets/audio/raw/` 未入库；
  `docs/screenshots/` 恰好 16 张 webp（624.3 KB）。
- push 后到 **Settings → Pages → Source: GitHub Actions** 启用 Pages（静态站点直接发布根目录，
  8.876 MB 入口页 + assets 共约 35 MB，远低于 Pages 上限）。
- 若 GitHub 提示单文件过大：`index.html` 8.876 MB 远低于 100 MB 限制；真正的大文件
  （`reports/shots` 194 MB、`assets/tex/_build` 62 MB、`assets/audio/raw` 13.4 MB）都已在 `.gitignore`。
