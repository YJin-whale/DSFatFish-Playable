# 幼态角色立绘生成提示词 · Grok / Kimi / GLM / Qwen / MiniMax

> 给 genderswapai.com（GenderSwapAI 的 AI 娘化生成器）用的**可直接粘贴**的提示词。
> 目的：把 5 位目前仍是「全身成熟版」的角色，生成成和前三位（ChatGPT / Claude / Gemini）同一画风的**幼态 Q 版立绘**；用户确认后**同名覆盖**，游戏里立刻生效。
> 交付目标：**竖版 3:4、纯白底、单人全身、PNG**。拿到图后交给 `assets/chars/process_chars.py` 自动抠图 → `assets/chars/<id>.webp`（300×400 透明底）。
> 维护：char-art · 2026-11-18 · 对应 `docs/SPEC-v4.md` 第 8 节

---

## 0. 统一画风基准（先看这一节，粘提示词时每段都自带画风句，不用额外补）

已经交付的三张幼态立绘是画风锚点（原图存档在 `assets/chars/raw/`，可直接当参考图上传）：

| 参考图 | 路径 | 可提供的画风信息 |
|---|---|---|
| ChatGPT 幼态 | `assets/chars/raw/chatgpt.png` | 三头身、白发 + 龙角 + 小翅膀、全身正面、白白净净的配色 |
| Claude 幼态 | `assets/chars/raw/claude.png` | 两头身~三头身、橙发大眼、抱书、圆脸幼态、暖色配色 |
| Gemini 幼态 | `assets/chars/raw/gemini.png` | 三头身、紫发猫耳、星星装饰、手脚短圆、Q 版比例 |

三张图的共同特征 = 我们要的画风：

- **比例**：两头身到三头身（头很大、身体小、手脚短圆），脸占画面存在感强；
- **线稿**：**粗描边**（深色、闭合、干净），不是细线也不是无描边厚涂；
- **上色**：**赛璐璐平涂** + 一层简单明暗（最多两层），少量高光，颜色饱和、干净；
- **脸**：大眼睛（占脸约 1/3）、小鼻子（一个点/一条短线）、小嘴；
- **构图**：单人、全身、正面站姿、脚底完整、人物占画面高度 ~80–85%；
- **背景**：纯白 `#FFFFFF`，**不要地面阴影、不要投影、不要渐变、不要边框**。

统一画风句（每节中文提示词里都已包含，若平台支持权重可在画风句后续加「重点」）：

> Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗描边线稿、平涂色块加简单明暗、大眼睛、小鼻子小嘴、短手短脚，纯白背景，无地面阴影、无边框、无文字、无水印。

---

## 1. 通用操作流程（genderswapai.com）

1. 打开 genderswapai.com 的 **AI 娘化 / 角色生成** 页面（站内若有「AI 娘化生成器」入口就用那个）。
2. **参考图**：按下面的「策略 A/B/C」上传；该角色的全身立绘一定要给，画风参考图给 2~3 张最稳。
3. **提示词**：把每节 §x.2 的中文提示词整段粘进描述框；如果站内有额外的「英文提示词 / Negative prompt」字段，再用 §x.3 的英文补充 + §2 的负面词。
4. **尺寸**：选**竖版 3:4**（如 768×1024、900×1200）。没有比例选项时选最接近的竖图；生成后不要自己拉伸。
5. **张数**：一次出 4 张，按 §9 挑选；不满意就换一次种子/重生成，不要手工 P 图改比例。
6. 存 PNG → 按 §8 命名回填 → 跑脚本 → 看 `preview_compare.png` 复核。

**参考图策略**

- **策略 A（平台支持多图，优先）**：3 张幼态图（chatgpt/claude/gemini）当**画风参考** + 该角色全身立绘当**要素参考**。若平台能调权重：画风图中等，角色全身图略高（让发型/服饰/道具更像）。
- **策略 B（只支持 1 张）**：传**该角色的全身立绘**，画风完全靠提示词里的画风句约束；或传 `gemini.png`（比例最接近目标）再靠文字描述角色要素。
- **策略 C（只支持 1 张又想要画风）**：自己拼一张 2×2 参考图（三张幼态图 + 目标角色全身图）当单图上传。
- **不要**传 `hero.png`（默认深海小鲸娘）或 `assets/chars/raw/legacy/` 里的 v3 换色图当参考 —— 会把它拉回「大肥鱼同一张脸」的老路，而那是用户明确否决过的方案。

> genderswapai.com 本质是性别转换/娘化生成器：如果它要求的是「原始角色图」，就上传该角色的**全身立绘**，提示词写描述框；如果它对长提示词支持有限，优先保住画风句 + 角色要素句（发色/瞳色/服饰/道具），其余删减。

---

## 2. 通用负面提示词（可选字段，能填就填）

中文：

> 半身像，坐姿，裁切脚部，地面阴影，投影，多个角色，真人写实，3D 渲染，厚涂写实光照，花哨背景，背景物体，文字，水印，签名，多余手指，肢体畸形，四头身以上，成熟大人比例，服装配色跑偏

英文：

> realistic, photo, 3d render, semi-realistic, half body, cropped feet, ground shadow, drop shadow, multiple characters, text, watermark, signature, complex background, scenery, extra limbs, bad anatomy, deformed hands, mature adult proportions, 5+ heads tall, oversaturated neon

---

## 3. Grok · 格萝克（金发双马尾 · 蝙蝠翼 · 黑红哥特裙 · 巨斧）

### 3.1 参考图怎么用

- 画风参考：`raw/gemini.png` + `raw/claude.png`（三头身、大眼、赛璐璐平涂、白底构图）；
- 要素参考：`raw/grok.png`（金发双马尾、蓝眼、黑色蕾丝尖顶发饰、黑红哥特裙、白蕾丝领口/袖口、小蝙蝠翼、巨斧）；
- **只取要素，不取比例**：全身图是七头身，要转成两头身~三头身。
- 想更“幼”一点：画风参考里多给 chatgpt（三头身白龙角那张）的 Q 感。

### 3.2 中文提示词（整段粘贴）

> 单个角色，Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗黑描边线稿、平涂色块加简单明暗、占脸三分之一的大眼睛、小鼻子小嘴、短手短脚，背景纯白无地面阴影。角色是金发双马尾的哥特小吸血鬼少女：奶油浅金色长发扎成双马尾，发尾长卷；蓝色大眼睛，微笑露出小尖牙；头戴黑色蕾丝尖顶小皇冠发饰，点缀金色星月；脚穿黑色小皮鞋和黑色吊带长袜。穿黑红配色哥特小礼服：黑色束腰裙身、暗红色内衬裙摆、白色蕾丝立领与袖口、黑色长袖、黑色领结、金色扣饰和小链条。背后一对小巧的黑色蝙蝠翼。一只手扶着一把巨大的黑色战斧：X 形双刃斧头、金色包边、长柄，斧头高度接近人物身高（允许往横向伸出画面外一点点）。整体配色：黑、暗红、金、浅金。人物占画面高度约 85%，全身完整、脚底不被裁切，脚边不画地面阴影，无文字、无边框、无水印。

### 3.3 英文补充提示词

> single character, chibi, 2.5 heads tall, cute chibi vampire girl, cream-blonde twin tails, blue eyes, small fangs, black lace mini crown, black and dark-red gothic dress, white lace collar and cuffs, black bow tie, black stockings, black shoes, small black bat wings, holding a giant black double-bladed axe with gold trim and long handle, cel shading, thick clean outlines, big eyes, anime illustration, full body, front view, standing, white background, no ground shadow, no text, no watermark, vertical 3:4

### 3.4 生成后交付要求

- PNG、**竖版 3:4**（≥768×1024）、**纯白底**、单人**全身**、脚底完整、无地面阴影/文字/水印；
- 要素核对：浅金双马尾 ✔ 蓝眼 ✔ 小尖牙 ✔ 黑色蕾丝尖顶发饰 ✔ 黑红哥特裙 + 白蕾丝领口/袖口 ✔ 蝙蝠翼 ✔ 巨斧（X 形双刃、金边）✔；
- 存为 `assets/chars/raw/grok.png`（覆盖旧图），然后见 §8。

---

## 4. Kimi · 月音酱（银白蓝发 · 长笛 · 音乐会礼服）

### 4.1 参考图怎么用

- 画风参考：`raw/chatgpt.png` + `raw/gemini.png`（三头身、白发/浅色系为例、大眼、粗描边）；
- 要素参考：`raw/kimi.png`（银白到浅蓝紫的长发、浅蓝紫眼睛、白色蕾丝小礼帽/发带、深蓝+白音乐会礼服、音符与 K 字吊饰、银色长笛、白色长袜 + 深蓝高跟）；
- 这个角色的「银白长发」是最容易糊成一团的地方：提示词里强调**发丝分层和粗描边**，别让 AI 画成白色糊块。

### 4.2 中文提示词（整段粘贴）

> 单个角色，Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗黑描边线稿、平涂色块加简单明暗、占脸三分之一的大眼睛、小鼻子小嘴、短手短脚，背景纯白无地面阴影。角色是银白发音乐少女：银白到浅蓝紫渐变的长发（大波浪、长到脚踝，发丝分层清楚，粗描边勾出每一缕）；浅蓝紫色眼睛；头戴白色蕾丝小礼帽发带，侧边点缀深蓝色花朵、白色缎带、彩虹小旗和音符造型吊饰。穿深蓝与白配色的音乐会礼服：白色荷叶边立领衬衫、黑色领结、深蓝色披肩外套、白色多层褶边长裙，裙摆和腰侧有银色音符与星星装饰；白色长袜、深蓝高跟小皮鞋。双手捧一支银色长笛（笛身细长、有一点反光），身边飘两三个小小的音符符号。整体配色：银白、浅蓝紫、深蓝。人物占画面高度约 85%，全身完整、脚底不被裁切，脚边不画地面阴影，无文字、无边框、无水印。

### 4.3 英文补充提示词

> single character, chibi, 2.5 heads tall, cute chibi music girl, long silver-white wavy hair with light blue-violet tint, pale blue-violet eyes, white lace mini hat headband with navy flowers, white ribbon and a tiny rainbow flag charm, navy and white concert gown, white frilled collar blouse, black bow tie, navy cape coat, layered white ruffled skirt with silver music-note and star ornaments, white stockings, navy high heels, holding a silver flute with both hands, a few floating music notes, cel shading, thick clean outlines, big eyes, anime illustration, full body, front view, standing, white background, no ground shadow, no text, no watermark, vertical 3:4

### 4.4 生成后交付要求

- PNG、**竖版 3:4**、**纯白底**、单人**全身**、脚底完整、无地面阴影/文字/水印；
- 要素核对：银白渐变长发 ✔ 浅蓝紫瞳 ✔ 白色蕾丝小礼帽 ✔ 深蓝+白礼服 + 白色褶边裙 ✔ 银色长笛 ✔ 音符装饰 ✔；
- 存为 `assets/chars/raw/kimi.png`（覆盖旧图），然后见 §8。

---

## 5. GLM · 墨卷酱（黑发狼耳 · GLM 书本 · 黑白长裙）

### 5.1 参考图怎么用

- 画风参考：`raw/chatgpt.png`（白发那张的「兽耳 + 大眼 + 白裙」组合最接近 GLM 的要素气质）；
- 要素参考：`raw/glm.png`（黑长直齐刘海、深紫蓝眼、黑色狼耳、黑色宽檐蕾丝帽 + 银色铃铛、白色荷叶边衬衫 + 黑领结 + 黑马甲 + 白围裙、黑边长裙、白长袜黑皮鞋、抱 GLM 书本）；
- 黑发 + 黑裙在 Q 版里容易糊成一坨：提示词里要求**黑发有明确高光和粗描边**、裙子黑白分层。

### 5.2 中文提示词（整段粘贴）

> 单个角色，Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗黑描边线稿、平涂色块加简单明暗、占脸三分之一的大眼睛、小鼻子小嘴、短手短脚，背景纯白无地面阴影。角色是黑发狼耳的书卷系少女：黑色长直发（齐刘海、长到脚踝，黑发上有清楚的高光和粗描边，不要糊成一团）；深紫蓝色眼睛；头顶一对黑色毛茸狼耳，戴一顶黑色宽檐蕾丝小帽，帽檐有白色蕾丝垂饰和银色小铃铛。穿黑白配色的女仆风长裙：白色荷叶边衬衫、黑色领结、黑色马甲、白色围裙、黑白长裙（裙摆有简单格纹和蕾丝装饰）；白色长袜、黑色小皮鞋。双手抱一本黑色厚书，书封面有简洁的「GLM」字样（文字画不清就换成抽象徽记）。整体配色：黑、白、银，气质安静。人物占画面高度约 85%，全身完整、脚底不被裁切，脚边不画地面阴影，无文字、无边框、无水印。

### 5.3 英文补充提示词

> single character, chibi, 2.5 heads tall, cute chibi bookish girl, long straight black hair with bangs, dark violet-blue eyes, black fluffy wolf ears, black wide-brim lace hat with white lace trim and silver bells, white frilled blouse, black bow tie, black vest, white apron, black and white long skirt with simple plaid and lace, white stockings, black shoes, holding a black hardcover book with a simple "GLM" cover mark, cel shading, thick clean outlines, big eyes, anime illustration, full body, front view, standing, white background, no ground shadow, no text except the book cover mark, no watermark, vertical 3:4

### 5.4 生成后交付要求

- PNG、**竖版 3:4**、**纯白底**、单人**全身**、脚底完整、无地面阴影/水印；
- 要素核对：黑长直齐刘海 ✔ 黑狼耳 ✔ 黑色宽檐蕾丝帽 + 铃铛 ✔ 黑白女仆风长裙 + 白围裙 ✔ GLM 书本 ✔；
- 存为 `assets/chars/raw/glm.png`（覆盖旧图），然后见 §8。

---

## 6. Qwen · 千问酱（蓝发汉服 · 折扇）

### 6.1 参考图怎么用

- 画风参考：`raw/gemini.png` + `raw/chatgpt.png`（三头身、长卷发、白底大眼）；
- 要素参考：`raw/qwen.png`（浅蓝长发 + 侧编发、蓝紫眼、蓝色小发冠带银星与流苏、蓝白汉服襦裙 + 大袖、白色百褶裙、白色折扇、蓝色小布袋、蓝色绣鞋）；
- 汉服大袖在 Q 版里容易把身体盖住：提示词要求**正面站姿、袖子不要遮手**，折扇要露出来。

### 6.2 中文提示词（整段粘贴）

> 单个角色，Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗黑描边线稿、平涂色块加简单明暗、占脸三分之一的大眼睛、小鼻子小嘴、短手短脚，背景纯白无地面阴影。角色是蓝发汉服少女：浅蓝色长发（侧边编一条小辫），蓝紫色眼睛；头戴浅蓝色小发冠小帽，点缀银色星星和流苏，戴一对小耳坠。穿蓝白配色的汉服襦裙：白色立领内衫、浅蓝色交领外袍和大袖、白色百褶长裙、蓝色腰封和飘带，裙摆有淡淡的云纹星纹暗花；蓝色绣花布鞋。一手拿着一把展开的白色折扇（扇面带淡蓝色花纹），另一手提一只蓝色小布袋。整体配色：白、浅蓝、银。人物占画面高度约 85%，全身完整、脚底不被裁切，袖子不要遮住手，脚边不画地面阴影，无文字、无边框、无水印。

### 6.3 英文补充提示词

> single character, chibi, 2.5 heads tall, cute chibi hanfu girl, light blue long hair with a side braid, violet-blue eyes, light blue hair crown with silver star ornaments and tassels, small earrings, blue and white hanfu, white inner collar, light blue crossed-collar outer robe with big sleeves, white pleated skirt, blue sash and ribbons, subtle cloud and star patterns on the skirt, blue embroidered shoes, holding an open white folding fan with pale blue pattern in one hand and a small blue cloth bag in the other, cel shading, thick clean outlines, big eyes, anime illustration, full body, front view, standing, white background, no ground shadow, no text, no watermark, vertical 3:4

### 6.4 生成后交付要求

- PNG、**竖版 3:4**、**纯白底**、单人**全身**、脚底完整、无地面阴影/文字/水印；
- 要素核对：浅蓝长发 + 编发 ✔ 蓝紫瞳 ✔ 蓝色小发冠 + 银星流苏 ✔ 蓝白汉服襦裙 + 大袖 ✔ 白色折扇 ✔ 蓝色小布袋 ✔；
- 存为 `assets/chars/raw/qwen.png`（覆盖旧图），然后见 §8。

---

## 7. MiniMax · 小麦克（橙发记者帽 · 麦克风 · MINIMAX 包）

### 7.1 参考图怎么用

- 画风参考：`raw/claude.png`（橙发 + 圆脸 + 抱书那张的暖色幼态感最接近）+ `raw/gemini.png`；
- 要素参考：`raw/minimax.png`（橙粉短发、红琥珀眼、白色记者帽、白色记者外套 + 白 T + 红领巾、米色格纹裙、MINIMAX 托特包、黑色采访麦克风、粉色运动鞋、悬浮照片）；
- 这个角色道具最多（帽子/包/麦克风/悬挂照片），Q 版里要**做减法**：保留帽子、麦克风、MINIMAX 包、格纹裙四个识别点，其余简化。

### 7.2 中文提示词（整段粘贴）

> 单个角色，Q 版幼态二到三头身，正面全身站姿，动漫赛璐璐插画风格：粗黑描边线稿、平涂色块加简单明暗、占脸三分之一的大眼睛、小鼻子小嘴、短手短脚，背景纯白无地面阴影。角色是元气记者少女：橙粉色蓬松短发（发尾偏粉），琥珀红色大眼睛，笑容活泼，露出一点点小虎牙；头戴白色报童帽（帽檐带红色细条纹）。穿白色短款记者外套（袖口和口袋有粉色线条装饰），内搭白 T 恤、红色小领巾、粉色 choker；米色格纹半身裙配棕色腰带；白色中筒袜、粉色运动鞋。斜挎一只白色托特包，包身印「MINIMAX」字样和彩色媒体小图标（文字画不清就用抽象图标代替）；一手握着黑色采访麦克风（话筒带海绵套），另一只手做出介绍和指向的手势；身边可加一张带蓝色边框的小小悬浮照片作为点缀。整体配色：白、橙粉、红、米格纹。人物占画面高度约 85%，全身完整、脚底不被裁切，脚边不画地面阴影，无文字、无边框、无水印。

### 7.3 英文补充提示词

> single character, chibi, 2.5 heads tall, cute energetic chibi reporter girl, fluffy orange-pink short hair, amber-red eyes, small fang, white newsboy cap with red stripe, white cropped reporter jacket with pink trim, white tee, red neckerchief, pink choker, beige plaid skirt with brown belt, white socks, pink sneakers, white tote bag with "MINIMAX" logo and colorful media icons, holding a black interview microphone, pointing with the other hand, a small floating photo with blue frame, cel shading, thick clean outlines, big eyes, anime illustration, full body, front view, standing, white background, no ground shadow, no watermark, vertical 3:4

### 7.4 生成后交付要求

- PNG、**竖版 3:4**、**纯白底**、单人**全身**、脚底完整、无地面阴影/水印；
- 要素核对：橙粉短发 ✔ 白记者帽 ✔ 白外套 + 红领巾 + 格纹裙 ✔ MINIMAX 托特包 ✔ 黑色采访麦克风 ✔ 粉色运动鞋 ✔；
- 存为 `assets/chars/raw/minimax.png`（覆盖旧图），然后见 §8。

---

## 8. 拿到图之后：入库流程（char-art 侧）

1. 把最终 PNG 按 id 覆盖存档：
   - `assets/chars/raw/grok.png`
   - `assets/chars/raw/kimi.png`
   - `assets/chars/raw/glm.png`
   - `assets/chars/raw/qwen.png`
   - `assets/chars/raw/minimax.png`
2. 跑处理流水线（自动去白底 / 去地面阴影 / 裁切 / 300×400 / webp / 重建预览和 manifest）：

```bash
# 5 张一起重跑
python assets/chars/process_chars.py --only grok,kimi,glm,qwen,minimax

# 或者一张一张来
python assets/chars/process_chars.py --only grok
```

3. 检查产物：
   - `assets/chars/<id>.webp` 单张必须 ≤ 90 KB（脚本会在 q88→82 间自动降档，仍超会报错）；
   - `assets/chars/preview_compare.png` 里这 5 张不再标「待替换幼态」；
   - `assets/chars/raw/processed/<id>.png` 可用于逐张对比（PNG 版，无压缩损失）。
4. 如果新图不是纯白底（浅蓝/浅粉/渐变背景），脚本的泛洪可能抠不干净：优先让 AI 重新生成纯白底；实在不行可以先把图手动抠成 RGBA 透明底再覆盖（脚本的 `mode=auto` 会自动走 alpha 分支）。
5. 如果新图脚底仍有地面阴影，脚本的「去地面阴影」步骤会自动处理；阴影特别大/特别深时可以把 `assets/chars/process_chars.py` 里 `clean_ground_shadow` 的 `bottom_frac` 从 0.12 调大一点再跑。

---

## 9. 挑选与验收清单（生成完逐条打勾）

**四选一挑图**

- [ ] 两头身~三头身，头大身小、手脚短圆（不是七头身、不是半身像）；
- [ ] 粗描边 + 赛璐璐平涂，和大眼睛的画风跟 ChatGPT/Claude/Gemini 三张能并排；
- [ ] 单人、全身、正面，**脚底完整**没被裁掉；
- [ ] 纯白底（不是灰白渐变、不是室内/天空背景）；
- [ ] **没有地面阴影/投影**；没有文字、水印、签名、边框；
- [ ] 发色、瞳色、服饰配色和原角色一致（见每节 §x.4 要素核对）；
- [ ] 标志物清楚：Grok 巨斧+蝙蝠翼 / Kimi 长笛+音符 / GLM 书本+狼耳 / Qwen 折扇+汉服 / MiniMax 麦克风+记者帽+MINIMAX 包；
- [ ] 画面横竖比是竖版 3:4（不是方图/横图）。

**入库验收**

- [ ] `assets/chars/raw/<id>.png` 已覆盖，纯白底、PNG、3:4；
- [ ] `python assets/chars/process_chars.py --only <id>` 跑通，`--check` 单张 ≤ 90 KB；
- [ ] `preview_compare.png` 并排看：头身比例与另外三张幼态接近，配色不撞；
- [ ] 深色底（游戏内）合成无白边、无残留白底；
- [ ] 通知 Lead 重新构建 `index.html`（`python build/build.py`）。
