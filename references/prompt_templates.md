# 提示词模板

英文提示词发给模型；中文提示词是对照翻译，只用于展示。两者内容要一致。

## 写法原则

每条公理怎么翻译成提示词，见 `skeleton_axioms.md` 各节的「提示词」部分。这里只放写法原则和完整模板。

- **描述可见的形状，不堆形容词。** 「两条等宽圆角条带绕中心 180° 对称咬合成 S」比「高级、现代、有张力的 S」有用得多。
- **布尔运算写结果，不写术语。** 写 `cut out as negative space`、`formed by the overlap of two circles`，不写 `boolean geometry`。
- **曲率写成模型能执行的样子。** 写 `continuous-curvature corners like a squircle, no visible joint`，不写 `G2`。
- **负向词两侧都封。** 只封一侧，模型会往另一侧跑（公理三）。
- **避免会触发插画风格的词**：botanical、delicate、organic lines、anatomical、realistic、detailed。
- **不要写 bold / thick / heavy，也不要写 thin / slender / hairline**，它们会把结果推向钟摆的一端。用 `balanced medium stroke weight`。
- **一次只描述一个结构**。互相冲突的要求（又要闭合又要开口）会让模型乱画。
- **骨架阶段不出现任何颜色名**，只用「近黑 + 纯白/米白」。

---

## 1. 骨架模板（阶段 2、3）

### 英文
```
Minimal modern brand mark: <对象与结构，用可见形状描述>.
Construction: built from circles, rounded rectangles and capsules that are merged, cut and overlapped, <布尔运算的结果，如 the counter cut out as negative space>; uniform stroke width throughout, balanced medium stroke weight; parallel strokes from concentric curves; smooth continuous-curvature corners like a squircle, no visible joint between straight and curved segments; taut arcs with tension; visually centered and balanced; <闭合方式或对称方式>.
Single flat color: near-black #1A1A1A on plain off-white #F7F7F5 background. Centered with generous margin. Highly legible at 16 pixels.
No text, no illustration, no realistic objects, no decorative add-ons, no floating detached elements, no calligraphic brush strokes, no hairline strokes, no chunky heavy blocks, no inflated plastic 3D, no bevel, no gradients, no shadows, no glow, no texture, no extra strokes. Flat vector logo, crisp edges.
```

### 中文
```
极简现代品牌标志：<对象与结构>。
构造：由圆、圆角矩形、胶囊相加、相减、相交得到，<布尔运算的结果，如字怀以负空间切出>；线宽统一，中量级粗细；平行笔画来自同心曲线；转角像超椭圆一样曲率连续，直线与曲线之间看不出接头；弧线紧绷有张力；视觉重心居中平衡；<闭合方式或对称方式>。
单一纯平色：近黑 #1A1A1A，米白纯色底 #F7F7F5。居中，留足边距。16 像素下依然清晰。
不出现文字，不画插画和写实物件，不外挂装饰，无脱离主体的漂浮部件，无毛笔笔触，无发丝细线，无笨重黑块，无充气塑料 3D，无倒角，无渐变、阴影、发光、纹理，无多余笔画。纯平矢量标志，边缘锐利。
```

### 示例（结构描述部分）

- 字母标闭合：`an upright vertical stem with a smooth arc that rises over the inner shape and loops back down to rejoin the stem near two-thirds height, forming a fully closed counter`
- 中心对称：`two identical rounded bands interlocking with 180-degree point symmetry around the center`
- 负空间：`a solid rounded-square tile with the letter cut out of it as negative space`
- 同心回路：`two concentric arcs nested inside the bowl of the letter, same stroke width, evenly spaced`

---

## 2. 骨架微调模板（阶段 3，带参考图）

```
Keep the reference mark exactly as it is: same overall silhouette, same proportions, same stroke width, same position. Only change: <只写一处改动>.
Single flat color: near-black #1A1A1A on plain off-white #F7F7F5. No gradients, no shadows, no 3D, no glow, no texture. Flat vector logo, crisp edges.
```
```
严格保持参考图中的标志不变：整体轮廓、比例、线宽、位置都不变。只改一处：<改动>。
单一纯平色：近黑 #1A1A1A，米白纯色底 #F7F7F5。无渐变、无阴影、无 3D、无发光、无纹理。纯平矢量标志，边缘锐利。
```

调用时加 `--ref output/<上一版>.png`。

---

## 3. 上色模板（阶段 4，带参考图）

### 纯色 / 双色
```
Recolor the reference mark only. Keep the shape exactly identical: same silhouette, proportions, stroke width, gaps and position. Do not add, remove or reshape anything.
Colors: <部件 A> in <颜色名> (<色值>); <部件 B> in <颜色名> (<色值>); background <颜色名> (<色值>).
Solid flat fills with hard edges between colors. No other colors, no gradients, no shadows, no 3D, no glow, no texture.
```
```
只给参考图中的标志重新上色。形状完全不变：轮廓、比例、线宽、间隙、位置都不变，不增加、不删除、不改形。
颜色：<部件 A> 用 <颜色名>（<色值>）；<部件 B> 用 <颜色名>（<色值>）；背景 <颜色名>（<色值>）。
纯色平涂，颜色之间硬边相接。不出现其他颜色，无渐变、无阴影、无 3D、无发光、无纹理。
```

### 渐变
```
Recolor the reference mark only. Keep the shape exactly identical. <部件> uses a smooth gradient from <颜色 1> (<色值>) to <颜色 2> (<色值>), running <方向，如 from bottom to top>, staying within the same hue family with no grey, brown or muddy midtones and no shift toward yellow. <其余部件> in solid <颜色> (<色值>). Background <颜色> (<色值>). No other colors, no shadows, no 3D, no glow, no texture.
```
```
只给参考图中的标志重新上色，形状完全不变。<部件> 用从 <颜色 1>（<色值>）到 <颜色 2>（<色值>）的平滑渐变，方向 <自下而上>，保持在同一色系内，中间不出现灰、褐、发脏的过渡，不偏黄。<其余部件> 用纯色 <颜色>（<色值>）。背景 <颜色>（<色值>）。不出现其他颜色，无阴影、无 3D、无发光、无纹理。
```

---

## 4. 展示图模板（可选）

只在用户需要宣传图时使用。logo 本体仍保持纯平，光感只属于背景。

```
Place the reference mark, unchanged and perfectly flat, at the center of <场景，如 a softly lit off-white studio surface with a subtle warm ambient glow behind it>. Keep the mark's shape and colors exactly identical. Generous empty space. No text.
```
```
把参考图中的标志原样、纯平地放在 <场景> 中央。标志的形状与颜色完全不变。四周大量留白。不出现文字。
```

---

## 5. 负向词

完整的两侧负向词表和用法见 `skeleton_axioms.md` 第 3 节（公理三）。要点：

- 第一轮两侧都封。
- 之后每轮针对上一轮掉进的那一侧加更具体的词，另一侧保留，防止矫枉过正。
- 字母标加上 `no letters other than <字母>`。
