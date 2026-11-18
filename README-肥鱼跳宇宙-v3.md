# 肥鱼跳宇宙 · 星尘远航 v3（星际跳跃改版）

> 单文件网页游戏。双击 `index.html` 即可开始，不需要安装任何东西。
> 线上地址原版：https://fatfish-jump-universe.app.workbuddy.host/?sharecode=OBDYU6QNS7
> 本目录里的 `index.html` 是改版后的可部署版本（自包含，贴图和代码全部内联），可直接重新上传到 WorkBuddy。

---

## 一、怎么运行

- **直接玩**：双击 `index.html`（Chrome / Edge / 手机浏览器均可）。
- **修改后重新构建**（改的是 `src/` 里的源码时）：
  ```powershell
  & "C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\python\python.exe" build\build.py
  ```
  构建会把 `src/astronomy.js → engine.js → render.js → ui.js` 和 `assets/` 里的贴图一起内联成单文件 `index.html`。
- **原版备份**：`index_original_backup.html`（未改动的初始版本，可对照）。

## 二、本次按需求改了什么

| 用户要求 | 实现 |
|---|---|
| ① 跳跃到各个星球，第一站月球，月球用网上下载的真实月球照片做贴图 | 太阳系每一站都用真实星球影像生成的球体贴图：月球（LRO/Selene 月面反照率图）、水星、金星、火星、木星、土星、天王星、海王星、冥王星（NASA New Horizons PIA19952）；来源 Solar System Scope / NASA，授权见 `assets/manifest-textures.json` 与游戏内「玩法说明」署名 |
| ② 抵达月球弹出成就「我的一小步，大肥鱼们的一大步」 | `a_one_small_step` 成就，金框弹窗动画，+150 星辰币；存档永久记录 |
| ② 月球成为新跳跃点，可再次起跳 | 抵达界面「从月球再次起跳 → 水星」；每站都按「当前天体 → 下一站」重新进入发射台 |
| ② 起跳基础速度按当地重力/地球重力比例 | HUD 显示 `11.186 km/s × 重力比`；地球 11.19、月球 1.85、火星 4.24、木星 28.3 …；飞行手感也随重力调整 |
| ② 下一目标点严格按真实天文距离测算 | `src/astronomy.js`：地月 384,400 km；行星间按轨道半长轴之差（NASA/IAU 数据）；恒星按视差距离、星系按真实距离，总航程 465 亿光年；界面显示每段距离，测算依据见 `docs/astronomy-notes.md` |
| ② 右下角跳跃高度/距离不要一成不变：航程尺长度不变、满量程增长、人物标记按比例往下移 | 右下角「航程尺」：固定像素长度；满量程随已飞距离按 1/2/5 档增长（5万→10万→38.4万 km…），标记 = 已飞/满量程，**满量程跳档时标记明显下移**；到终点前再爬回顶部 |
| ③ 飞行途中随机出现外星飞船攻击 | 飞碟随机从两侧进入、悬停并发射红色弹幕；有攻击预警圈；被击中扣 1 血，铁锅可挡 |
| ④ 人物形象：大肥鱼，护盾时头顶铁锅；护盾最多 1 个不叠加 | 默认角色（用户提供的 DeepSeek 金鱼娘 PNG）；拾取护盾后头顶出现程序绘制的铁锅，受击时铁锅旋转飞出并短暂无敌；已有铁锅时再吃护盾转化为燃料+星辰币，**不叠加** |
| ⑤ 发射界面长按人物：背景缩小到整个太阳系 → 白色虚线预测航线 → 瞬间切回 → 可操作躲避/收集 | 发射台长按（或按住空格）2.6s：发射场景缩小淡出、太阳系全景浮现、白色虚线动画航迹（霍曼转移示意）；锁定 0.75s 后白闪并**瞬间切回**发射界面，随即进入飞行。飞出太阳系后同一套机制换成银河系螺旋地图；最后换成可观测宇宙「宇宙网 + 微波背景视界」地图 |
| ⑤ 太阳系最后落点冥王星；之后银河系、可观测宇宙 | 28 站：太阳系 9 → 银河系 12 → 可观测宇宙 7；抵达半人马座α、银河系边缘、可观测宇宙视界均有层级突破提示与成就 |
| ⑤ 星系/宇宙尺度也要「真实图像」 | 仙女座星系、三角座星系、大麦哲伦云、小麦哲伦云使用 NASA/ESA 真实观测照片（抵达页面圆形取景 + 宇宙地图缩略图）；室女座/后发座星系团与宇宙视界用程序化星系团/微波背景视觉 |
| ⑥ 商城 + 伙伴：星辰币购买角色、可以两个角色同时跳跃、等级解锁功能 | 「星际商城」3 个角色：深海小鲸娘（默认）/ 聊天酱（ChatGPT 幼态拟人）/ 小星芒（Claude 幼态拟人）；星辰币购买（Lv.2 解锁购买）、Lv.3 解锁双人同行；伙伴在飞行中跟随，并按角色给被动加成；等级/成就界面常驻 |
| ⑥ ChatGPT / Claude 幼态拟人立绘，与默认角色画风复核 | 以默认金鱼娘为基底做 HSV 主题色重映射 + 4x 手绘赛璐璐配饰（耳机麦克风/对话气泡；星芒/蝴蝶结），线稿、比例、上色层次同源；见 `assets/chars/preview_compare.png` |

## 三、玩法速览

- **操作**：WASD / 方向键 / 手机拖动摇杆；P 暂停；发射台长按角色（或按住空格）做航线预演。
- **飞行**：自动沿航线前进；躲避陨石和飞碟弹幕；吃星辰币（本局收集）、燃料罐、铁锅护盾。
- **航程尺**：右下角，满量程增长、标记下移是刻意设计（对应需求「总高度增长、人物位置向下调整」）。
- **推进**：抵达后点「再次起跳」继续下一站；28 站全部抵达后进入终章「飞出可观测宇宙」。
- **商城**：收集星辰币 → 提升飞行员等级 → 解锁购买/双人同行。

## 四、文件结构

```
FatFish-Playable/
├─ index.html                 ← 最终交付：自包含单文件游戏（构建产物，勿手改）
├─ index_original_backup.html ← 改版前原版备份
├─ hero.png                   ← 用户提供的默认角色立绘（原样保留）
├─ src/                       ← 源码（改动请改这里再构建）
│  ├─ astronomy.js            ← 28 站真实天文数据与航段计算（astro-data 交付）
│  ├─ engine.js               ← 状态机/存档/飞行玩法/商城/成就/调试接口
│  ├─ render.js               ← 贴图/星球/角色/铁锅/飞碟/发射场景/航线地图
│  ├─ ui.js                   ← 全部界面与输入
│  └─ index.template.html
├─ build/                     ← build.py（内联构建）、astro 自检、E2E 脚本
├─ assets/
│  ├─ tex/                    ← 真实星球球体贴图（globe_*.png）+ manifest
│  └─ chars/                  ← 聊天酱 / 小星芒 立绘 + preview_compare.png
├─ docs/                      ← SPEC、天文测算说明、本文件
├─ reports/                   ← 资产/测试报告、QA 截图
└─ tools/                     ← cdp_check.mjs（无依赖 Chrome headless 测试工具）
```

## 五、数据与授权

- **星球贴图**：Solar System Scope（CC BY 4.0）等距柱状真实星球贴图 → 正交球体渲染；冥王星用 NASA/JHUAPL/SwRI New Horizons PIA19952（公共领域）。游戏内「玩法说明」已署名。
- **天文数据**：NASA Planetary Fact Sheet、IAU 2009 行星定义/轨道半长轴、Gaia/视差距离、NED 星系距离、Planck 可观测宇宙半径；测算细节见 `docs/astronomy-notes.md`。
- **角色**：默认角色来自用户提供的 `hero.png`；ChatGPT / Claude 幼态拟人为基于该立绘的同源重绘（调色+配饰），不含第三方素材。
- **字体**：系统字体（system-ui / 微软雅黑 / 苹方），无外部字体依赖。

## 六、自动化测试 / 调试

- 测试工具（零依赖 Chrome headless CDP）：
  ```powershell
  $node = 'C:\Users\admin\.dsh\dsh-runtimes\dsh-plugin-desktop-primary-runtime\dependencies\node\bin\node.exe'
  & $node tools/cdp_check.mjs --url "file:///C:/Users/admin/Desktop/FatFish-Playable/index.html" --scenario smoke --shot reports/shots/x.png --out reports/qa-x.json
  ```
- 游戏内调试接口（浏览器控制台）：`window.__FATFISH__.state()` / `jumpTo('moon')` / `setProgress(0.5)` / `unlockAll()` / `arriveNow()` 等。
- URL 调试参数：`?screen=shop|hangar|launch|flight|arrive|ending`、`?stop=moon`、`?progress=0.6`、`?zoom=0.9`（航线预演定格）、`?unlock=1&rich=1`。

## 七、已知局限 / 可继续的方向

1. 室女座/后发座星系团与可观测宇宙视界暂无合适的单张真实照片（体积/版权原因），用程序化「星系团 / 宇宙网 + 微波背景视界」视觉；恒星（半人马座α、天狼星等）用程序化恒星发光效果。后续拿到图源放进 `assets/tex/` 重新构建即可自动生效。
2. 航段距离采用「轨道半长轴之差 / 径向距离差」的工程近似（真实飞行还受发射窗口、相位角、转移轨道影响），已在天文说明里标注；不是真实飞船航线。
3. 双人同行目前为视觉同行 + 被动加成，尚未做双角色独立操作。
4. 商城目前是 3 个角色、2 个功能解锁点（购买 Lv.2 / 双人 Lv.3）；「更多功能」按需求本期只留了等级框架。
5. 声音为简单合成音效，未做音乐；可在设置里静音。

---

*改版：2026-11-18 · 构建版本 v3.0.0*
