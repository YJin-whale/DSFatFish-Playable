# 肥鱼跳宇宙 v6 · 音频回归报告（qa-harness）

**轮次标签**：final-uxfix

✅ **全部通过**

- 生成时间：2026-11-18T15:42:33.524Z（用时 109.4s）
- 构建产物：`C:\Users\admin\Desktop\FatFish-Playable\index.html`（8.67 MB / 9089288 B，mtime 2026-11-18T15:35:23.635Z，sha256 `b20bf9c75e248065…`）
- Node v24.21.0 / win32x64；Chrome：`C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe`
- 场景 18 个：✅ pass 18 · ⏳ pending 0 · ⚠️ warn 0 · ❌ fail 0
- 退出码：**0**（0 = 无 fail；pending / warn 不算失败）

## 1. v5 基线（50 场景不退化）

| 项 | 值 |
|---|---|
| 轮次标签 | v6.1-baseline |
| 生成时间 | 2026-11-18T15:40:39.272Z |
| 场景 | 50 个：pass 50 / pending 0 / warn 0 / **fail 0** |
| 退出码 | 0 |
| 基线构建 | 9089288 B / mtime 2026-11-18T15:35:23.635Z |
| 与当前构建一致 | ✅ 一致 |


## 2. 关键实测值（音量 / 曲目 / dance / 上传 / 跨界面保持）

| 项目 | 实测值 | 来源场景 | 备注 |
|---|---|---|---|
| VERSION | 6.0.0 | `caps` |  |
| 内置曲目 / 曲目总数 | 2 首内置 / 2 首列表 | `caps` |  |
| 内置曲目 | Let Me Go（共创版） / Let me go | `caps` |  |
| URL 音量 ?musicVol=0.42 | 0.42 | `settings-url-volume` |  |
| URL 音效 ?sfxVol=0.9 | 0.9 | `settings-url-volume` |  |
| URL 音量落盘 | 0.42 / 0.9 | `settings-url-volume` |  |
| audioSliderApply('musicVol',0.27) | 0.27 | `settings-slider` |  |
| 连续 6 档音量实测 | 0.13 / 0.27 / 0.31 / 0.5 / 0.666 / 0.9 | `settings-slider` |  |
| setMusicVolume(0.31) / setSfxVolume(0.9) | 0.31 / 0.9 | `settings-slider` |  |
| 播放状态 | playing=true / current=Let Me Go（共创版） | `play` |  |
| danceLevel()（analyser 出数耗时） | 0.9（200ms） | `play` | level=0.176 bass=0.573 pulse=0.943 |
| 播放 error | （空，无解码/播放报错） | `play` |  |
| musicToggle() 暂停 / 恢复 | playing=false → 恢复后 true | `pause` |  |
| musicNext() 切歌 | Let Me Go（共创版） → Let me go | `next-track` |  |
| 内置曲2 名称 | Let me go / 星落落oi | `next-track` |  |
| 跨界面 playing|volume | title true|0.44 → launch true|0.44 → flight true|0.44（screen=flight） | `cross-keep` |  |
| 飞行中 danceLevel() | 0.649 | `cross-keep` |  |
| 上传后曲目数 / 上传数 | 3 / 1 | `upload-add` | id=user:test:1795016515315 |
| musicDbCount()（重读 IndexedDB） | 1 | `upload-add` |  |
| 上传曲目播放 danceLevel() | 0.009 | `upload-add` |  |
| 删除后 uploadedCount / dbCount | 0 / 0 | `upload-remove` |  |
| 跨启动持久化（写入轮） | uploaded=1 / vol=0.37 / savedTrack=user:test:1795016528495 | `persist-write` |  |
| 跨启动持久化（重开轮） | uploaded=1 / trackCount=3 / vol=0.37 / db=1 | `persist-read` |  |
| 移动端 390x844 音频页 | sliders=2 / volume=0.66 / viewport=390x844 | `m-audio-settings` |  |
| 移动端播放 danceLevel() | 0.361 | `m-play` |  |

> 音频解码/播放异常时，场景断言里会直接贴 `state().audio.error` 原文（见「失败清单」）。

## 3. 场景 × 断言总表

| # | 场景 | 分组 | 状态 | 断言（通过/待定/失败） | 截图 | 用时 |
|---|---|---|---|---|---|---|
| 1 | 能力探测（v6 音频调试 API / 状态 / 内置曲目 / 存档骨架） | caps | ✅ pass | 16/0/0 | [shots/v6qa_caps.png](shots/v6qa_caps.png) | 7.1s |
| 2 | 设置 · 音频页（双页签 / 正在播放卡 / 无极滑杆 / 播放列表） | settings | ✅ pass | 10/0/0 | [shots/v6qa_settings-audio.png](shots/v6qa_settings-audio.png) | 5.3s |
| 3 | 设置 · 音频页 + URL 音量（?musicVol=0.42&sfxVol=0.9） | settings | ✅ pass | 10/0/0 | [shots/v6qa_settings-url-volume.png](shots/v6qa_settings-url-volume.png) | 5.0s |
| 4 | 设置 · 无极音量（audioSliderApply 0.27 / 连续多档 / setMusicVolume / setSfxVolume / 落盘） | settings | ✅ pass | 11/0/0 | [shots/v6qa_settings-slider.png](shots/v6qa_settings-slider.png) | 7.8s |
| 5 | 播放 · musicUnlock + musicPlay(内置曲1) → playing/dance/analyser | play | ✅ pass | 12/0/0 | [shots/v6qa_play.png](shots/v6qa_play.png) | 5.8s |
| 6 | 暂停 · musicToggle() 暂停 / 再 toggle 恢复 | play | ✅ pass | 9/0/0 | [shots/v6qa_pause.png](shots/v6qa_pause.png) | 9.2s |
| 7 | URL · ?music=off 不自动播放（musicUnlock 也不开播） | play | ✅ pass | 9/0/0 | [shots/v6qa_music-off.png](shots/v6qa_music-off.png) | 6.7s |
| 8 | 切歌 · musicNext() 换曲 / 内置曲2 currentName 含「Let me go」 | play | ✅ pass | 11/0/0 | [shots/v6qa_next-track.png](shots/v6qa_next-track.png) | 9.8s |
| 9 | 跨界面保持 · title → launch → flight（musicVol=0.44，播放/音量/曲目不变） | play | ✅ pass | 11/0/0 | [shots/v6qa_cross-keep.png](shots/v6qa_cross-keep.png) | 10.5s |
| 10 | 上传 · musicUploadTest 导入合成 WAV → 列表 +1 / IndexedDB 读回 / 自动播放 | upload | ✅ pass | 15/0/0 | [shots/v6qa_upload-add.png](shots/v6qa_upload-add.png) | 6.2s |
| 11 | 删除 · removeUploadedMusic(id) → 列表/IndexedDB 恢复，切回内置曲目继续播 | upload | ✅ pass | 11/0/0 | [shots/v6qa_upload-remove.png](shots/v6qa_upload-remove.png) | 6.8s |
| 12 | 跨启动持久化① · 写：上传曲目 + 音量 0.37/0.62 存进 profile | persist | ✅ pass | 7/0/0 | — | 7.0s |
| 13 | 跨启动持久化② · 读：同一 profile 重开 → 上传曲目/音量还在 | persist | ✅ pass | 11/0/0 | — | 5.6s |
| 14 | 移动端 390x844 · 设置音频页 | mobile | ✅ pass | 10/0/0 | [shots/v6qa_m-audio-settings.png](shots/v6qa_m-audio-settings.png) | 5.5s |
| 15 | 移动端 390x844 · 播放状态（dance / 曲目） | mobile | ✅ pass | 10/0/0 | [shots/v6qa_m-play.png](shots/v6qa_m-play.png) | 5.1s |
| 16 | 帮助页 · 音频说明（截图；文案静态扫描在 static 场景） | desktop | ✅ pass | 7/0/0 | [shots/v6qa_help.png](shots/v6qa_help.png) | 5.5s |
| 17 | 构建产物静态扫描（内置音乐 / 音频模块 / IndexedDB / 帮助文案 / URL 参数） | static | ✅ pass | 13/0/0 | — | — |
| 18 | 跨场景交叉断言（v5 基线不退化 / 全场景 0 console error / 构建稳定） | cross | ✅ pass | 5/0/0 | — | — |

> 断言列格式：通过 / 待定 / 失败；截图相对 `reports/`。pending 为环境限制（如 `--user-data-dir` 复用偶发 websocket 失败），不算代码 bug。

## 4. 逐场景断言明细

### ✅ 能力探测（v6 音频调试 API / 状态 / 内置曲目 / 存档骨架） `caps`

- URL：`index.html?screen=title&unlock=1`
- 截图：`reports/shots/v6qa_caps.png`（像素方差 1582.1）
- cdp 报告：`reports/qa-v6-logs/caps.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1582.06 |  |
| 页面 = title | ✅ pass | title | title |  |
| VERSION = '6.0.0' | ✅ pass | 6.0.0 | 6.0.0 |  |
| state().audio 存在（musicState 快照） | ✅ pass | object | object |  |
| state().audio.ready = true | ✅ pass | true | true |  |
| 内置曲目 >= 2（trackCount>=2 且 builtinCount=2） | ✅ pass | trackCount>=2 / builtinCount=2 | trackCount=2 builtinCount=2 |  |
| 两首内置曲目 id/名称都在列表里（罐装毕加索 / 星落落oi） | ✅ pass | builtin:bgm_canned_picasso + builtin:bgm_xingluoluo | Let Me Go（共创版） / Let me go |  |
| v6 音频调试 API 齐备（musicState/musicPlay/musicToggle/musicNext/setMusicVolume/setSfxVolume/musicUnlock/danceLevel/musicUploadTest/musicDbCount/audioSliderApply/settingsTabs…） | ✅ pass | 全部 function | 全部齐备 |  |
| 未解锁前不自动播放（playing=false）且无错误 | ✅ pass | playing=false / error="" | playing=false error= |  |
| 默认曲目是内置曲目（currentId 以 builtin: 开头） | ✅ pass | builtin:* | builtin:bgm_canned_picasso |  |
| 上传入口就绪（隐藏 file input 已创建，musicPickFiles 可用） | ✅ pass | true | true |  |
| 干净 profile 下 uploadedCount = 0（每场景临时 profile） | ✅ pass | 0 | 0 |  |
| 存档 key fatfish_universe_save_v6 存在且含音乐字段 | ✅ pass | fatfish_universe_save_v6 含 musicVol/sfxVol/musicOn/musicTrack | 字段 musicVol,sfxVol,musicOn,musicTrack |  |
| 首次启动默认音量落盘 musicVol≈0.55 / sfxVol≈0.85（info） | ℹ️ info | 0.55 / 0.85 | musicVol=0.55 sfxVol=0.85 musicOn=true musicTrack=builtin:bgm_canned_picasso | 默认值口径（SPEC-v6 §3） |

<details><summary>evalResult 原始值</summary>

```json
{
 "version": "6.0.0",
 "screen": "title",
 "settingsTab": "audio",
 "audio": {
  "ready": true,
  "playing": false,
  "unlocked": false,
  "currentId": "builtin:bgm_canned_picasso",
  "currentName": "Let Me Go（共创版）",
  "currentArtist": "罐装毕加索",
  "volume": 0.55,
  "sfxVolume": 0.85,
  "level": 0,
  "bass": 0,
  "pulse": 0,
  "dance": 0,
  "trackCount": 2,
  "builtinCount": 2,
  "uploadedCount": 0,
  "uploadsLoaded": true,
  "dbReady": true,
  "fileInput": true,
  "error": "",
  "tracks": [
   {
    "id": "builtin:bgm_canned_picasso",
    "name": "Let Me Go（共创版）",
    "artist": "罐装毕加索",
    "kind": "builtin"
   },
   {
    "id": "builtin:bgm_xingluoluo",
    "name": "Let me go",
    "artist": "星落落oi",
    "kind": "builtin"
   }
  ]
 },
 "api": {
  "musicState": "function",
  "musicToggle": "function",
  "musicPlay": "function",
  "musicNext": "function",
  "setMusicVolume": "function",
  "setSfxVolume": "function",
  "musicUploadTest": "function",
  "removeUploadedMusic": "function",
  "musicUnlock": "function",
  "setSettingsTab": "function",
  "danceLevel": "function",
  "musicDbCount": "function",
  "audioSliderApply": "function",
  "settingsTabs": "function"
 },
 "saveKeys": [
  "fatfish_universe_save_v6"
 ],
 "saveErr": "",
 "save": {
  "musicVol": 0.55,
  "sfxVol": 0.85,
  "musicOn": true,
  "musicTrack": "builtin:bgm_canned_picasso"
 }
}
```
</details>

### ✅ 设置 · 音频页（双页签 / 正在播放卡 / 无极滑杆 / 播放列表） `settings-audio`

- URL：`index.html?screen=settings&tab=audio`
- 截图：`reports/shots/v6qa_settings-audio.png`（像素方差 950.6）
- cdp 报告：`reports/qa-v6-logs/settings-audio.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 950.6 |  |
| 页面 = settings | ✅ pass | settings | settings |  |
| ?tab=audio 生效（settingsTab='audio'） | ✅ pass | audio | audio |  |
| settingsTabs().sliders >= 2（音乐 + 音效两条滑杆已绘制） | ✅ pass | >=2 | 2 |  |
| state().audio.ready = true | ✅ pass | true | true |  |
| 列表含 2 首内置曲目 | ✅ pass | >=2 / 2 | trackCount=2 |  |
| 播放列表两项内置曲目都在（id 完整） | ✅ pass | builtin:bgm_canned_picasso + builtin:bgm_xingluoluo | builtin:bgm_canned_picasso,builtin:bgm_xingluoluo |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "settings",
 "settingsTab": "audio",
 "sliders": 2,
 "audio": {
  "ready": true,
  "playing": false,
  "volume": 0.55,
  "sfxVolume": 0.85,
  "trackCount": 2,
  "builtinCount": 2,
  "uploadedCount": 0,
  "currentId": "builtin:bgm_canned_picasso",
  "currentName": "Let Me Go（共创版）",
  "error": "",
  "tracks": [
   {
    "id": "builtin:bgm_canned_picasso",
    "name": "Let Me Go（共创版）",
    "kind": "builtin"
   },
   {
    "id": "builtin:bgm_xingluoluo",
    "name": "Let me go",
    "kind": "builtin"
   }
  ]
 }
}
```
</details>

### ✅ 设置 · 音频页 + URL 音量（?musicVol=0.42&sfxVol=0.9） `settings-url-volume`

- URL：`index.html?screen=settings&tab=audio&musicVol=0.42&sfxVol=0.9`
- 截图：`reports/shots/v6qa_settings-url-volume.png`（像素方差 940.1）
- cdp 报告：`reports/qa-v6-logs/settings-url-volume.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 940.14 |  |
| 页面 = settings | ✅ pass | settings | settings |  |
| settingsTab='audio' | ✅ pass | audio | audio |  |
| state().audio.volume ≈ 0.42（?musicVol） | ✅ pass | 0.42 | 0.42 |  |
| state().audio.sfxVolume ≈ 0.9（?sfxVol） | ✅ pass | 0.9 | 0.9 |  |
| settingsTabs().sliders >= 2 | ✅ pass | >=2 | 2 |  |
| URL 音量已写入存档（save.musicVol≈0.42 / sfxVol≈0.9） | ✅ pass | 0.42 / 0.9 | 0.42 / 0.9 |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "settings",
 "tab": "audio",
 "sliders": 2,
 "volume": 0.42,
 "sfxVolume": 0.9,
 "ready": true,
 "saved": {
  "musicVol": 0.42,
  "sfxVol": 0.9
 }
}
```
</details>

### ✅ 设置 · 无极音量（audioSliderApply 0.27 / 连续多档 / setMusicVolume / setSfxVolume / 落盘） `settings-slider`

- URL：`index.html?screen=settings&tab=audio`
- 截图：`reports/shots/v6qa_settings-slider.png`（像素方差 923.2）
- cdp 报告：`reports/qa-v6-logs/settings-slider.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 923.16 |  |
| settingsTabs().sliders >= 2（音乐/音效两条无极滑杆） | ✅ pass | >=2 | 2 |  |
| audioSliderApply('musicVol', 0.27) → volume≈0.27 | ✅ pass | 0.27 | 0.27 |  |
| 连续多档音量逐个命中（0.13/0.27/0.31/0.5/0.666/0.9，无极非量化） | ✅ pass | 6 档全部命中且互不相同 | uniq=6 [0.13, 0.27, 0.31, 0.5, 0.666, 0.9] |  |
| setMusicVolume(0.31) → volume≈0.31（返回 0.31） | ✅ pass | 0.31 | 0.31 (ret 0.31) |  |
| setSfxVolume(0.9) → sfxVolume≈0.9 | ✅ pass | 0.9 | 0.9 |  |
| setSettingsTab('game') / 'audio' 双页签切换生效 | ✅ pass | game → audio | game → audio |  |
| 音量延迟落盘（save.musicVol≈0.31 / sfxVol≈0.9） | ✅ pass | 0.31 / 0.9 | 0.31 / 0.9 |  |
| 初始音量已恢复（info） | ℹ️ info | 恢复值 | 0.55 | settings 页初始音量 |

<details><summary>evalResult 原始值</summary>

```json
{
 "before": 0.55,
 "series": [
  0.13,
  0.27,
  0.31,
  0.5,
  0.666,
  0.9
 ],
 "got": [
  0.13,
  0.27,
  0.31,
  0.5,
  0.666,
  0.9
 ],
 "vol27": 0.27,
 "vol31": 0.31,
 "ret31": 0.31,
 "sfx": 0.9,
 "retSfx": 0.9,
 "setTabGame": "game",
 "tabsGame": {
  "tab": "game",
  "sliders": 2
 },
 "tabsAudio": {
  "tab": "audio",
  "sliders": 2
 },
 "saved": {
  "musicVol": 0.31,
  "sfxVol": 0.9
 }
}
```
</details>

### ✅ 播放 · musicUnlock + musicPlay(内置曲1) → playing/dance/analyser `play`

- URL：`index.html?screen=title&musicVol=0.5`
- 截图：`reports/shots/v6qa_play.png`（像素方差 1583.9）
- cdp 报告：`reports/qa-v6-logs/play.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1583.88 |  |
| 页面 = title | ✅ pass | title | title |  |
| musicUnlock() 后 state().audio.unlocked = true | ✅ pass | true | true |  |
| musicPlay() 后 playing = true | ✅ pass | true | true |  |
| currentId = builtin:bgm_canned_picasso（罐装毕加索） | ✅ pass | builtin:bgm_canned_picasso | builtin:bgm_canned_picasso |  |
| currentName 含「Let Me Go」（罐装毕加索 - Let Me Go（共创版）） | ✅ pass | 含 Let Me Go | Let Me Go（共创版） / 罐装毕加索 |  |
| danceLevel() > 0（角色随节拍跳动，等 1.5~2.5s analyser 出数） | ✅ pass | >0 | dance=0.9（200ms 出数, level=0.176 bass=0.573） |  |
| state().audio.error 为空（无解码/播放报错） | ✅ pass | error="" | error="" |  |
| ?musicVol=0.5 生效（volume≈0.5） | ✅ pass | 0.5 | 0.5 |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "title",
 "unlockedBefore": false,
 "unlockedAfter": true,
 "playRet": true,
 "playing": true,
 "currentId": "builtin:bgm_canned_picasso",
 "currentName": "Let Me Go（共创版）",
 "currentArtist": "罐装毕加索",
 "volume": 0.5,
 "sfxVolume": 0.85,
 "trackCount": 2,
 "builtinCount": 2,
 "dance": 0.9,
 "danceAtMs": 200,
 "level": 0.176,
 "bass": 0.573,
 "pulse": 0.943,
 "error": ""
}
```
</details>

### ✅ 暂停 · musicToggle() 暂停 / 再 toggle 恢复 `pause`

- URL：`index.html?screen=title`
- 截图：`reports/shots/v6qa_pause.png`（像素方差 1581.6）
- cdp 报告：`reports/qa-v6-logs/pause.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1581.63 |  |
| 播放中（前置条件） | ✅ pass | true | true |  |
| musicToggle() 后 playing = false | ✅ pass | false | false |  |
| 暂停后 danceLevel() = 0（角色停止跳动） | ✅ pass | 0 | 0 |  |
| 再 musicToggle() 后恢复播放（playing = true） | ✅ pass | true | true |  |
| 暂停/恢复全程无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "before": {
  "playing": true,
  "currentId": "builtin:bgm_canned_picasso",
  "dance": 1
 },
 "toggled": false,
 "after": {
  "playing": false,
  "error": "",
  "dance": 0
 },
 "toggledBack": true,
 "resumed": {
  "playing": true,
  "currentId": "builtin:bgm_canned_picasso",
  "error": ""
 }
}
```
</details>

### ✅ URL · ?music=off 不自动播放（musicUnlock 也不开播） `music-off`

- URL：`index.html?screen=title&music=off`
- 截图：`reports/shots/v6qa_music-off.png`（像素方差 1580.5）
- cdp 报告：`reports/qa-v6-logs/music-off.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1580.49 |  |
| ?music=off 下 musicUnlock() 后 playing = false | ✅ pass | false | false |  |
| 存档 musicOn = false | ✅ pass | false | false |  |
| 音频模块仍就绪（ready=true，曲目已载入） | ✅ pass | ready=true / trackCount>=2 | ready=true trackCount=2 |  |
| danceLevel() = 0（无音乐时不跳动） | ✅ pass | 0 | 0 |  |
| 无音频错误（静音是主动配置，不是播放失败） | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "playing": false,
 "ready": true,
 "unlocked": true,
 "trackCount": 2,
 "dance": 0,
 "error": "",
 "musicOn": false,
 "musicTrack": "builtin:bgm_canned_picasso"
}
```
</details>

### ✅ 切歌 · musicNext() 换曲 / 内置曲2 currentName 含「Let me go」 `next-track`

- URL：`index.html?screen=title&musicVol=0.5`
- 截图：`reports/shots/v6qa_next-track.png`（像素方差 1580.6）
- cdp 报告：`reports/qa-v6-logs/next-track.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1580.61 |  |
| musicNext() 后 currentId 变化 | ✅ pass | 不同 id | builtin:bgm_canned_picasso → builtin:bgm_xingluoluo |  |
| musicNext() 切到内置曲2（builtin:bgm_xingluoluo） | ✅ pass | builtin:bgm_xingluoluo | builtin:bgm_xingluoluo |  |
| 切歌后 currentName 含「Let me go」（星落落oi - Let me go） | ✅ pass | 含 Let me go | Let me go / 星落落oi |  |
| 切歌后仍然 playing = true | ✅ pass | true | true |  |
| 内置曲1 名称含「Let Me Go」（罐装毕加索） | ✅ pass | 含 Let Me Go | Let Me Go（共创版） |  |
| musicPlay(内置曲2) 后 currentName = Let me go | ✅ pass | 含 Let me go | Let me go / 星落落oi |  |
| 切歌全程无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "before": {
  "id": "builtin:bgm_canned_picasso",
  "name": "Let Me Go（共创版）",
  "playing": true
 },
 "nextRet": true,
 "next": {
  "id": "builtin:bgm_xingluoluo",
  "name": "Let me go",
  "artist": "星落落oi",
  "playing": true,
  "error": ""
 },
 "picassoName": "Let Me Go（共创版）",
 "xing": {
  "id": "builtin:bgm_xingluoluo",
  "name": "Let me go",
  "artist": "星落落oi",
  "playing": true
 }
}
```
</details>

### ✅ 跨界面保持 · title → launch → flight（musicVol=0.44，播放/音量/曲目不变） `cross-keep`

- URL：`index.html?screen=title&musicVol=0.44`
- 截图：`reports/shots/v6qa_cross-keep.png`（像素方差 732.4）
- cdp 报告：`reports/qa-v6-logs/cross-keep.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 732.36 |  |
| title 先播起来（前置条件：playing + volume≈0.44） | ✅ pass | playing=true / 0.44 | true / 0.44 |  |
| goto(launch) 后 playing / volume 不变 | ✅ pass | playing=true / 0.44 / screen=launch | true / 0.44 / launch |  |
| startFlight() 后 playing / volume 不变（飞行中音乐不中断） | ✅ pass | playing=true / 0.44 / screen=flight | true / 0.44 / flight |  |
| 三步 currentId 一致（不切歌不重建播放器） | ✅ pass | 三步相同 | builtin:bgm_canned_picasso → builtin:bgm_canned_picasso → builtin:bgm_canned_picasso |  |
| 飞行中 danceLevel() > 0（角色/伙伴随节拍跳动） | ✅ pass | >0 | 0.649 |  |
| 飞行确实开始（screen=flight） | ✅ pass | flight | flight |  |
| 全程无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "title": {
  "screen": "title",
  "playing": true,
  "volume": 0.44,
  "currentId": "builtin:bgm_canned_picasso",
  "error": ""
 },
 "launch": {
  "screen": "launch",
  "playing": true,
  "volume": 0.44,
  "currentId": "builtin:bgm_canned_picasso",
  "error": ""
 },
 "flight": {
  "screen": "flight",
  "playing": true,
  "volume": 0.44,
  "currentId": "builtin:bgm_canned_picasso",
  "error": ""
 },
 "flightDance": 0.649,
 "flightHp": 3,
 "flightProgress": 0.07547943750000002,
 "flightScreen": "flight",
 "trackCount": 2
}
```
</details>

### ✅ 上传 · musicUploadTest 导入合成 WAV → 列表 +1 / IndexedDB 读回 / 自动播放 `upload-add`

- URL：`index.html?screen=settings&tab=audio&musicVol=0.23&sfxVol=0.4`
- 截图：`reports/shots/v6qa_upload-add.png`（像素方差 807.4）
- cdp 报告：`reports/qa-v6-logs/upload-add.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 807.4 |  |
| musicUploadTest() 返回 user: test 曲目 id | ✅ pass | user:* | user:test:1795016515315 |  |
| 上传后 trackCount +1 | ✅ pass | +1 | 2 → 3 |  |
| uploadedCount >= 1 | ✅ pass | >=1 | 1 |  |
| 上传后自动播放（playing = true） | ✅ pass | true | true |  |
| currentId = 上传曲目 id | ✅ pass | = testId | user:test:1795016515315 |  |
| 播放列表里有「QA 测试曲」（kind=user / 作者=本地上传） | ✅ pass | name=QA 测试曲 / kind=user | QA 测试曲 / 本地上传 (user:test:1795016515315) |  |
| musicDbCount() 重新读 IndexedDB >= 1 | ✅ pass | >=1 | 1 |  |
| 上传曲目播放时 danceLevel() > 0（analyser 工作） | ✅ pass | >0 | 0.009 |  |
| 停在音频设置页（截图含上传曲目行） | ✅ pass | settings/audio/sliders>=2 | settings/audio/sliders=2 |  |
| ?musicVol=0.23 / ?sfxVol=0.4 保持 | ✅ pass | 0.23 / 0.4 | 0.23 / 0.4 |  |
| 无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "before": {
  "trackCount": 2,
  "uploadedCount": 0
 },
 "testId": "user:test:1795016515315",
 "after": {
  "trackCount": 3,
  "uploadedCount": 1,
  "currentId": "user:test:1795016515315",
  "playing": true,
  "volume": 0.23,
  "sfxVolume": 0.4,
  "uploadsLoaded": true,
  "dbReady": true,
  "error": ""
 },
 "dbCount": 1,
 "dance": 0.009,
 "tracks": [
  {
   "id": "builtin:bgm_canned_picasso",
   "name": "Let Me Go（共创版）",
   "artist": "罐装毕加索",
   "kind": "builtin"
  },
  {
   "id": "builtin:bgm_xingluoluo",
   "name": "Let me go",
   "artist": "星落落oi",
   "kind": "builtin"
  },
  {
   "id": "user:test:1795016515315",
   "name": "QA 测试曲",
   "artist": "本地上传",
   "kind": "user"
  }
 ],
 "screen": "settings",
 "tab": "audio",
 "sliders": 2
}
```
</details>

### ✅ 删除 · removeUploadedMusic(id) → 列表/IndexedDB 恢复，切回内置曲目继续播 `upload-remove`

- URL：`index.html?screen=settings&tab=audio`
- 截图：`reports/shots/v6qa_upload-remove.png`（像素方差 994.6）
- cdp 报告：`reports/qa-v6-logs/upload-remove.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 994.61 |  |
| 前置：上传后 uploadedCount = before+1 | ✅ pass | +1 | 0 → 1 |  |
| removeUploadedMusic(id) 返回 true | ✅ pass | true | true |  |
| 删除后 uploadedCount 恢复原值 | ✅ pass | 0 | 0 |  |
| 删除后 trackCount 恢复原值（回到 2 首内置） | ✅ pass | 2 | 2 |  |
| musicDbCount() 重新读 IndexedDB 也恢复（删除落库） | ✅ pass | 0 | 0 |  |
| 删除当前曲目后回落到内置曲目并继续播放 | ✅ pass | builtin:* / playing=true | builtin:bgm_canned_picasso / playing=true |  |
| 删除全程无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "before": {
  "uploadedCount": 0,
  "trackCount": 2
 },
 "id": "user:test:1795016521514",
 "mid": {
  "uploadedCount": 1,
  "trackCount": 3,
  "currentId": "user:test:1795016521514",
  "playing": true
 },
 "removed": true,
 "after": {
  "uploadedCount": 0,
  "trackCount": 2,
  "currentId": "builtin:bgm_canned_picasso",
  "playing": true,
  "error": ""
 },
 "dbAfter": 0,
 "tracks": [
  {
   "id": "builtin:bgm_canned_picasso",
   "name": "Let Me Go（共创版）",
   "artist": "罐装毕加索",
   "kind": "builtin"
  },
  {
   "id": "builtin:bgm_xingluoluo",
   "name": "Let me go",
   "artist": "星落落oi",
   "kind": "builtin"
  }
 ]
}
```
</details>

### ✅ 跨启动持久化① · 写：上传曲目 + 音量 0.37/0.62 存进 profile `persist-write`

- URL：`index.html?screen=settings&tab=audio`
- cdp 报告：`reports/qa-v6-logs/persist-write.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 写入轮 uploadedCount >= 1 | ✅ pass | >=1 | 1 |  |
| 写入轮 volume≈0.37 / sfx≈0.62 | ✅ pass | 0.37 / 0.62 | 0.37 / 0.62 |  |
| 存档已落盘（savedVol≈0.37 / savedTrack=上传 id） | ✅ pass | 0.37 / user:* | 0.37 / user:test:1795016528495 |  |
| 写入轮 musicDbCount() >= 1 | ✅ pass | >=1 | 1 |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "id": "user:test:1795016528495",
 "uploadedCount": 1,
 "trackCount": 3,
 "volume": 0.37,
 "sfxVolume": 0.62,
 "savedVol": 0.37,
 "savedSfx": 0.62,
 "savedOn": true,
 "savedTrack": "user:test:1795016528495",
 "db": 1,
 "tracks": [
  {
   "id": "builtin:bgm_canned_picasso",
   "name": "Let Me Go（共创版）",
   "artist": "罐装毕加索",
   "kind": "builtin"
  },
  {
   "id": "builtin:bgm_xingluoluo",
   "name": "Let me go",
   "artist": "星落落oi",
   "kind": "builtin"
  },
  {
   "id": "user:test:1795016528495",
   "name": "QA 跨启动曲",
   "artist": "本地上传",
   "kind": "user"
  }
 ]
}
```
</details>

### ✅ 跨启动持久化② · 读：同一 profile 重开 → 上传曲目/音量还在 `persist-read`

- URL：`index.html?screen=settings&tab=audio`
- cdp 报告：`reports/qa-v6-logs/persist-read.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 重开后 uploadedCount >= 1（IndexedDB 跨启动恢复） | ✅ pass | >=1 | 1 |  |
| 重开后 musicDbCount() >= 1 | ✅ pass | >=1 | 1 |  |
| 重开后 trackCount >= 3（2 内置 + 上传） | ✅ pass | >=3 | 3 |  |
| 重开后音量保持 volume≈0.37（存档持久化） | ✅ pass | 0.37 | 0.37 |  |
| 重开后 sfxVolume≈0.62 | ✅ pass | 0.62 | 0.62 |  |
| localStorage 存档仍是中写轮写入的值（musicTrack=上传 id） | ✅ pass | 0.37 / user:* | 0.37 / user:test:1795016528495 |  |
| 播放列表含「QA 跨启动曲」 | ✅ pass | name=QA 跨启动曲 | user:test:1795016528495 |  |
| 恢复后无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "uploadedCount": 1,
 "trackCount": 3,
 "volume": 0.37,
 "sfxVolume": 0.62,
 "uploadsLoaded": true,
 "dbReady": true,
 "db": 1,
 "currentId": "user:test:1795016528495",
 "currentName": "QA 跨启动曲",
 "error": "",
 "savedVol": 0.37,
 "savedSfx": 0.62,
 "savedTrack": "user:test:1795016528495",
 "tracks": [
  {
   "id": "builtin:bgm_canned_picasso",
   "name": "Let Me Go（共创版）",
   "artist": "罐装毕加索",
   "kind": "builtin"
  },
  {
   "id": "builtin:bgm_xingluoluo",
   "name": "Let me go",
   "artist": "星落落oi",
   "kind": "builtin"
  },
  {
   "id": "user:test:1795016528495",
   "name": "QA 跨启动曲",
   "artist": "本地上传",
   "kind": "user"
  }
 ]
}
```
</details>

### ✅ 移动端 390x844 · 设置音频页 `m-audio-settings`

- URL：`index.html?screen=settings&tab=audio&musicVol=0.66`
- 截图：`reports/shots/v6qa_m-audio-settings.png`（像素方差 1223）
- cdp 报告：`reports/qa-v6-logs/m-audio-settings.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 1223 |  |
| 页面 = settings | ✅ pass | settings | settings |  |
| settingsTab='audio' | ✅ pass | audio | audio |  |
| 移动端滑杆 >= 2（无极滑杆已绘制） | ✅ pass | >=2 | 2 |  |
| ?musicVol=0.66 生效 | ✅ pass | 0.66 | 0.66 |  |
| 视口 = 390x844 | ✅ pass | 390x844 | 390x844 |  |
| 音频模块就绪 | ✅ pass | ready=true | ready=true trackCount=2 |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "settings",
 "tab": "audio",
 "sliders": 2,
 "volume": 0.66,
 "ready": true,
 "trackCount": 2,
 "vw": 390,
 "vh": 844
}
```
</details>

### ✅ 移动端 390x844 · 播放状态（dance / 曲目） `m-play`

- URL：`index.html?screen=title&musicVol=0.66`
- 截图：`reports/shots/v6qa_m-play.png`（像素方差 1668.4）
- cdp 报告：`reports/qa-v6-logs/m-play.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 60） | ✅ pass | > 60 | 1668.42 |  |
| 页面 = title | ✅ pass | title | title |  |
| 移动端播放中 | ✅ pass | true | true |  |
| danceLevel() > 0 | ✅ pass | >0 | dance=0.361（300ms） |  |
| ?musicVol=0.66 生效 | ✅ pass | 0.66 | 0.66 |  |
| 视口 = 390x844 | ✅ pass | 390x844 | 390x844 |  |
| 无音频错误 | ✅ pass | error="" |  |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "title",
 "playing": true,
 "currentId": "builtin:bgm_canned_picasso",
 "currentName": "Let Me Go（共创版）",
 "volume": 0.66,
 "dance": 0.361,
 "danceAtMs": 300,
 "error": "",
 "vw": 390,
 "vh": 844
}
```
</details>

### ✅ 帮助页 · 音频说明（截图；文案静态扫描在 static 场景） `help`

- URL：`index.html?screen=help`
- 截图：`reports/shots/v6qa_help.png`（像素方差 1376.4）
- cdp 报告：`reports/qa-v6-logs/help.json`

| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| 页面加载完成（readyState = complete） | ✅ pass | complete | complete |  |
| console.error / 未捕获异常 = 0 | ✅ pass | 0/0 | 0/0 |  |
| 资源加载失败 = 0 | ✅ pass | 0 | 0 |  |
| 截图存在且非空白（方差 > 80） | ✅ pass | > 80 | 1376.36 |  |
| 页面 = help | ✅ pass | help | help |  |
| 版本号 6.x | ✅ pass | 6.x | 6.0.0 |  |
| 帮助页下音频模块仍就绪 | ✅ pass | ready=true | ready=true trackCount=2 |  |

<details><summary>evalResult 原始值</summary>

```json
{
 "screen": "help",
 "version": "6.0.0",
 "audioReady": true,
 "trackCount": 2
}
```
</details>

### ✅ 构建产物静态扫描（内置音乐 / 音频模块 / IndexedDB / 帮助文案 / URL 参数） `static`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| index.html 内 data:audio/mpeg;base64 >= 2（两首内置曲目内联） | ✅ pass | >=2 | 3 |  |
| SND 表含两首内置曲目 key（bgm_canned_picasso / bgm_xingluoluo） | ✅ pass | 2 个 key | 2 个齐备 |  |
| 构建产物 VERSION = '6.0.0' | ✅ pass | 6.0.0 | 6.0.0 |  |
| 存档 key fatfish_universe_save_v6 | ✅ pass | 'fatfish_universe_save_v6' | 存在 |  |
| src/audio.js 关键函数全部编译进构建产物（musicInit/musicUnlock/musicPlay/…/audioUpdate） | ✅ pass | 17 个 function | 全部存在 |  |
| ui/engine 音频挂点（滑杆绘制 / 设置页 / 调试 API） | ✅ pass | 12 个 | 全部存在 |  |
| IndexedDB 契约（fatfish_audio_v1 / tracks / 48MB 上限） | ✅ pass | 库名 + store + 上限 | 全部存在 |  |
| 音量映射 Gain = v^1.4（SPEC-v6 §4） | ✅ pass | v^1.4 | 存在 |  |
| WebAudio 分析器 fftSize = 256（律动分析） | ✅ pass | createAnalyser + fftSize=256 | 存在 |  |
| 分析器不可用时的合成节拍兜底（MUSIC.silentT > 0.5 分支） | ✅ pass | 兜底分支存在 | 存在 |  |
| 帮助页/设置页音频说明文案（无极 / 上传 / IndexedDB / 飞行保持） | ✅ pass | 无极 / 上传自己喜欢的音乐 / IndexedDB / 发射与飞行全程不中断 | 4 段齐备 |  |
| v6 URL 参数（?music=off / ?musicVol / ?sfxVol / ?tab） | ✅ pass | 4 个参数 | 全部存在 |  |
| index.html 体积符合 SPEC-v6（约 8.7MB，含两首内置音乐） | ✅ pass | 8.0~9.8 MB | 8.67 MB |  |
| 构建产物信息（info） | ℹ️ info | — | 9089288 B / mtime 2026-11-18T15:35:23.635Z / sha256 b20bf9c75e248065… |  |

### ✅ 跨场景交叉断言（v5 基线不退化 / 全场景 0 console error / 构建稳定） `cross`


| 断言 | 状态 | 期望 | 实际 | 备注 |
|---|---|---|---|---|
| v5 基线 50 场景（label=v6.1-baseline） | ✅ pass | 50 | 50 |  |
| v5 基线 0 fail（v4/v5 功能不退化） | ✅ pass | fail=0 | pass=50 pending=0 warn=0 fail=0 |  |
| v5 基线跑的是当前最终构建（bytes + mtime 一致） | ✅ pass | 9089288 B / 2026-11-18T15:35:23.635Z | 9089288 B / 2026-11-18T15:35:23.635Z |  |
| 全部音频场景 console.error / 未捕获异常 = 0 | ✅ pass | 0 个场景有错 | 16 个场景全 0 |  |
| 跑测期间 index.html 未被改动（结果对应同一构建） | ✅ pass | 9089288 B / 2026-11-18T15:35:23.635Z | 9089288 B / 2026-11-18T15:35:23.635Z |  |
| 环境限制场景（pending，不影响验收判定） | ℹ️ info | — | 无 | --user-data-dir 复用 profile 偶发 CDP/WebSocket 失败（Lead 实测）；同页 IndexedDB 读回已由 upload-add 覆盖 |
| v6 音频场景数（info） | ℹ️ info | — | 16 个真实场景 + static + cross |  |

## 5. 失败清单（代码 bug，Lead 要修）

无 🎉

## 6. 待定 / 警告（环境限制，非代码 bug）

无

## 7. 复跑命令

```bash
# 1) v5 基线（50 场景不退化；产出 reports/qa-v5-run.json 作本报告 v5 基线一栏）
node tools/qa_v5_run.mjs --label=v6-baseline

# 2) v6 音频全量
node tools/qa_v6_run.mjs --label=final

# 单个场景（排查用）
node tools/qa_v6_run.mjs --only=play

# 直接复现某个 URL（cdp_check 自带 --autoplay-policy=no-user-gesture-required / --mute-audio）
node tools/cdp_check.mjs --url "file:///<工作目录>/index.html?screen=settings&tab=audio&musicVol=0.42&sfxVol=0.9" \
  --scenario repro --wait-ms 2000 --shot reports/shots/repro.png --out reports/qa-v6-logs/repro.json
```

## 8. 口径与环境限制说明

- 判定口径：pass / fail / pending / warn；**pending / warn 不算失败**，退出码只看 fail。
- 音频场景均为独立临时 Chrome profile（`cdp_check.mjs` 默认行为），因此每个场景的 `uploadedCount` 从 0 起算；`musicUploadTest()` 的 WAV 只写当前实例的 IndexedDB。
- 跨启动持久化（persist-write / persist-read）复用 `reports/_qa-v6-profile`：本机偶发 `CDP WebSocket 连接失败`（Lead 实测），已自动重试 3 次；仍失败则记 pending 并在「待定」里注明，不判代码 bug。同页面内 IndexedDB 读回由 `upload-add` 的 `musicDbCount()` 覆盖。
- `state().audio.error` 非空时会直接贴原文；音频解码/播放失败按 fail 处理。
- 纯 canvas 绘制，UI 文案无法 DOM 读取：帮助页/设置页音频文案用 `index.html` 静态扫描（static 场景）+ 截图双重覆盖。
- v5 基线跑测对 `tools/qa_v5_run.mjs` 做了**仅断言口径**的适配（qa-audio 改，不改功能代码）：① 版本号断言接受 `6.x`（v6 构建 VERSION=6.0.0 属预期）；② 存档断言接受当前 `fatfish_universe_save_v6` key（v6 SPEC §3）；③ 迁移场景写入 v4 旧档时同时清空 v6 当前 key，才能构造出「只有旧档」的 profile。功能断言与场景均未删改。
- 本报告不修改 `src/**` / `index.html` / `build.py` / `assets/**` / `docs/**`；仅写 `tools/**`、`reports/**`。

---

_由 `tools/qa_v6_run.mjs` 生成；v24.21.0 / win32x64；构建 sha256 `b20bf9c75e248065a620ed96d49a1acce5783ea26241f02258a9e805c5e4b9f6`_
