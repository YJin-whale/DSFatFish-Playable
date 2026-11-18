# 肥鱼跳宇宙 · 星尘远航 v6 规格（音频系统 / 上传音乐 / 律动角色 / 仓库更新）

> v6 增量：设置里的音频模块、内置两首歌、用户上传音乐、角色随节拍跳动、发射与飞行全程保持音频配置。
> 前置版本见 `docs/SPEC-v4.md`（实时太阳系等）、`docs/SPEC-v5.md`（通关重玩 / 无限模式 / 仓库化）。

## 1. 用户 v6 需求（验收清单）

1. **音频设置**：游戏内设置里可以**无极（连续）调整音乐音量**，另有音效音量；数值持久化，跨启动保留。
2. **内置两首歌**：插入用户提供的两段音频（罐装毕加索《Let Me Go（共创版）》、星落落oi《Let me go》），可在设置里播放/暂停/上一首/下一首、选择曲目。
3. **上传音乐模块**：用户可以上传自己想听的本地音频，放进播放列表；下次打开游戏仍可用（本地持久化，不上传服务器）。
4. **主题角色随韵律跳动**：音乐播放时，主角色（以及飞行中的角色/伙伴）会跟着节拍做 squash & stretch + 上下弹跳。
5. **发射及飞行过程保持原配置**：切换机库/发射台/飞行/结局等界面时，音乐不中断、音量/曲目/播放状态保持。
6. 保持单文件交付：`index.html` 双击即玩；内置音频以 data URI 内联（压缩到 96 kbps 以控制体积）。

## 2. 构建与资源

- 新增 `src/audio.js`（构建顺序：astronomy → **audio** → engine → render → ui）。
- `assets/audio/` 顶层放成品音频（`.mp3/.ogg/.wav/.m4a/.webm`），构建注入 `var SND = { key: dataURI }`；`assets/audio/raw/` 放用户给的原始未压缩文件（不内联、不入库）。
- 当前内置：
  - `bgm_canned_picasso` ← 罐装毕加索 - Let Me Go（共创版），原 4.87MB/2:04 → 96kbps 1.42MB
  - `bgm_xingluoluo` ← 星落落oi - Let me go，原 8.52MB/3:38 → 96kbps 2.50MB
  - `index.html` 约 8.7 MB（含音频 base64）。
- 版权：两首歌为**用户提供的第三方音乐**，仅本地/个人使用，不适用 MIT；公开分发前需自行取得授权。写入 `NOTICE.md`。

## 3. 存档契约（v6，`SAVE_KEY='fatfish_universe_save_v6'`，兼容迁移 v5/v4/v3/v2）

```js
{
  // ... v5 全部字段
  musicVol: 0.55,     // 音乐音量 0~1（连续浮点，无极）
  sfxVol: 0.85,       // 音效音量 0~1
  musicOn: true,      // 是否启用音乐（浏览器首次交互后自动开播）
  musicTrack: 'builtin:bgm_canned_picasso'  // 上次曲目 id：builtin:* 或 user:*
}
```

## 4. 音频模块契约（`src/audio.js`）

全局状态 `MUSIC`，关键导出函数（均挂到 `window.__FATFISH__` 便于 QA）：

```js
musicInit()                    // boot 时调用：建 <audio>、WebAudio 图（source→gain→analyser→out）、恢复上次曲目与音量、异步载入本地上传曲目
musicUnlock()                  // 首次交互解锁 AudioContext / 自动播放
musicPlay(id) / musicToggle() / musicNext(dir)
musicSetVolume(v) / musicSetSfxVolume(v)   // v 为 0~1 浮点（无极）
musicPickFiles()               // 打开系统文件选择框（上传音乐）
audioUploadFiles(fileList)     // 导入文件到 IndexedDB（store 'tracks'，keyPath id）
audioRemoveUpload(id)
audioUpdate(dt)                // 每帧：频谱分析 → MUSIC.level / bass / pulse / dance
musicState()                   // 调试/QA 用状态快照
musicImportTestBlob(name, sec) // QA 用：合成一段 WAV 导入（不弹文件框）
```

- 音频图：`MediaElementSource → 音乐 Gain → Analyser(fft 256) → destination`；`<audio loop>` 全局单例，切界面不重建、不暂停。
- 音量：连续值 0~1，UI 滑杆/滚轮无极调整；Gain = `v^1.4`；拖拽时延迟 0.35s 写存档。
- 律动：低频能量（前 14% bins）+ 能量突变检测 → `pulse`（0~1 衰减）；`dance = clamp(level*0.85 + bass*0.85 + pulse*0.75, 0, 1)` 再平滑；**分析器不可用时**（无音频设备/浏览器限制）用合成节拍兜底，保证角色仍会跟拍。
- 角色动画：`render.drawHero` 读取 `MUSIC.dance/pulse`，做上下弹跳 + 纵向 squash & stretch（幅度 ~4%，不喧宾夺主）。可传 `opts.dance` 覆盖。
- 自动播放：浏览器策略要求一次交互；boot 后监听第一次 `pointerdown/keydown/touchstart` 自动开播（`S.musicOn !== false` 时）。
- 上传持久化：IndexedDB `fatfish_audio_v1/tracks` 存 Blob，下次启动 `audioLoadUploads()` 恢复；单文件上限 48MB；支持 mp3/ogg/wav/m4a/webm。

## 5. 界面契约（`ui.js`）

- 设置页改为**双页签**：`♪ 音频设置`（默认）/ `⚙ 游戏设置`（原通关记录/再玩一次/无限模式/存档/清空）。
- 音频页：
  - 正在播放卡：曲名/作者 + `⏮ ⏯ ⏭`；
  - 「音乐音量（无极调节）」滑杆 + 百分比；「音效音量」滑杆；支持点击/拖动/滚轮（Shift 微调 0.005）；
  - 播放列表：内置 2 首 + 本地上传曲目；行内「播放」/「播放中」；上传曲目带 `✕` 删除；分页；
  - 「＋ 上传音乐文件」按钮（系统文件框）；也支持把文件拖进设置页窗口；
  - 页脚说明「只存本机 IndexedDB，不上传服务器」。
- 全局：左下角显示 `♪ 曲名 · 音量%`（窄屏隐藏避免与底部提示重叠）；快捷键 `M` 音乐开关、`N` 下一首；帮助页补充音频说明。
- 发射/飞行：不重建播放器、不重置音量；qa 断言跨界面 `playing` 与 `volume` 不变。

## 6. 调试 API / URL（QA 用）

`window.__FATFISH__` 新增：
`musicState() / musicToggle() / musicPlay(id) / musicNext() / setMusicVolume(v) / setSfxVolume(v) / musicUploadTest(name,sec) / musicUploadFileList(fileList) / removeUploadedMusic(id) / musicUnlock() / setSettingsTab('audio'|'game') / danceLevel() / musicDbCount()`（返回 Promise，重读 IndexedDB 中上传曲目数）；`state()` 新增 `audio`（musicState 快照，含 `fileInput` 是否已创建隐藏文件选择器）、`settingsTab`。

URL 参数新增：
`?music=off|on`、`?musicVol=0.42`、`?sfxVol=0.9`、`?tab=audio|game`（配合 `?screen=settings`）。

## 7. 验收口径（v6）

- 双击 `index.html` 可玩、无 JS 报错；内置两首歌可播放/切换/暂停，音量无极调整并持久化；
- 上传音乐后出现在列表、可播放、`musicDbCount()` ≥ 1，删除后恢复；
- 音乐播放时 `state().audio.dance > 0`，角色可见弹跳；切到发射台/飞行仍保持 `playing`、`volume`、`currentId`；
- 设置页桌面/移动端布局正常；帮助页出现音频说明；
- v4/v5 全部回归不退化（`tools/qa_v5_run.mjs` 50 场景）。

## 8. 交付状态（2026-11-18，已验收）

- [x] `src/audio.js`（音频引擎：BGM 单例 + WebAudio 图 + 上传 IndexedDB + 频谱律动）；构建顺序 astronomy → **audio** → engine → render → ui。
- [x] 两首内置曲入库：`assets/audio/bgm_canned_picasso.mp3`（1.42MB）、`assets/audio/bgm_xingluoluo.mp3`（2.50MB），96kbps 转码；原始文件在 `assets/audio/raw/`（13.4MB，**不入库**）。
- [x] 单文件 `index.html` v6.0.0：**9,089,288 B / 8.876 MB**（UX 修订后构建，mtime 2026-11-18 23:35:23），含音频 base64。
- [x] 设置页双页签：音频设置（正在播放 / 无极音量滑杆 + 滚轮微调 / 播放列表 / 上传 / 删除）+ 游戏设置（v5 的通关记录/新周目/无限模式/存档）。
- [x] 角色律动：`drawHero` 读取 `MUSIC.dance/pulse` 做弹跳 + squash & stretch（幅度约 9%~14% 弹跳、5.5% 纵向缩放，随节拍）。
- [x] 跨界面保持：title → launch → flight 全程 `playing / volume / currentId` 不变（QA 实测 volume=0.44、flight dance=0.624）。
- [x] 存档 v6（`fatfish_universe_save_v6`）兼容迁移 v5/v4/v3/v2；新增 `musicVol/sfxVol/musicOn/musicTrack`。
- [x] QA：`tools/qa_v6_run.mjs` 新增 18 场景全绿（pass 18 / fail 0 / pending 0 / warn 0，退出码 0），v5 基线 50 场景不退化（pass 50 / fail 0）。
  - 报告：`reports/qa-v6.md`、`reports/qa-v6-run.json`；截图 `reports/shots/v6qa_*.png`（14 张）。
  - 关键实测：无极音量连续 6 档 0.13/0.27/0.31/0.5/0.666/0.9；播放 dance 峰值 0.879；上传后曲目 3/上传 1/`musicDbCount()`=1，删除后归 0；跨启动持久化（重开 profile）uploaded=1、vol=0.37 通过。
- [x] 仓库：README v6 特性/截图/测试链接、NOTICE §7 音乐版权（两首第三方作品，非商业个人使用、不适用 MIT）、CHANGELOG [6.0.0]、.gitignore 排除 `assets/audio/raw/` 与 QA 临时 profile；tracked ≈ 34.5 MB / 141 files（无 LFS 需求）。

已知限制：
- 浏览器自动播放策略要求一次交互后才会自动开播（首次点击/按键后生效）；提供 `musicUnlock()` 调试接口便于 QA。
- 上传音乐只存在本机浏览器 IndexedDB，换设备/清缓存不保留；单文件限制 48MB。
- 内置两首为第三方版权音乐，仓库公开分发前需自行确认授权（见 NOTICE.md §7）。

### v6.0.0 修订（2026-11-18 晚，用户反馈）

- **问题**：通关后打开游戏，标题页主按钮「再玩一次」需要连点两次确认（第一次只弹 toast），容易被误认为无法开新游戏；新周目中途也没有「从地球重新开始」的入口。
- **修复**：
  - 单击主按钮 → 明确的新周目确认弹窗（保留项/重置项说明 + [保留成就与记录，开始新周目] / [清空全部存档，完全重来] / [取消]）；
  - 结局页、设置 → 游戏设置共用同一弹窗；设置条目改为「🔁 从地球重新开始（新周目）」，**任何时候**（不必先结束当前周目）可用；
  - 弹窗打开时拦截背景按钮与键盘（Esc/P 取消）；
  - 调试 API：`openNewCycleConfirm()` / `cancelConfirm()`，`state().confirmAction`。
- 提醒：若浏览器之前已经开着旧标签页，双击 `index.html` 只会切回旧页面，需刷新（Ctrl+F5）才加载新构建。
