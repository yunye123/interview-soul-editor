# 访谈灵魂剪辑 / Interview Soul Editor

[English](README_EN.md) · 中文

一个以“原句优先、逐字核验、人工选题”为核心的访谈剪辑 Agent Skill。

它把长访谈的原始视频、音频或逐字稿，整理成可回到原素材直接剪辑的短视频方案：主题地图、灵魂四问、冗余候选稿、结构复审、钩子与结尾、逐字核验和时间码剪辑单。

> **红线：不改一句话、不补录、不转述、不意译。只做取舍、重排、拼接、切段和节奏编排。**

## 为什么做这个 Skill

访谈剪辑最危险的 AI 失误，不是“写得不好”，而是它把受访者的话润色得更顺，最后却无法在原素材里找到同一句话。

本 Skill 不相信模型自报“我没有改写”。它要求每个连续原句进入带唯一 ID 的 `VERBATIM` 块，再由确定性脚本逐块检查原文。改一个词、少一句话或偷偷润色，都会核验失败。

## 核心流程

```text
素材盘点
  ↓
本地转写（TXT + SRT + JSON）
  ↓
主题地图 + 灵魂四问
  ↓ 用户只选择一个主题
冗余候选剪辑稿
  ↓
删减 → 流量压力测试 → 环环相扣终审
  ↓
钩子与结尾
  ↓
逐字原文核验 + 字数/时长核验
  ↓
带时间码剪辑单
  ↓ 用户批准策略后才执行真实切割
```

### 灵魂四问

1. 我对谁说？
2. 我想说什么？
3. 希望对什么人产生什么影响？
4. 我的对立面是谁？

“对立面”优先指观念、误区、惯性或制度张力，不用于凭空树敌。

## 主要能力

- 处理视频、音频、TXT、SRT、JSON 逐字稿。
- 长访谈拆成 3–7 个真正不同的候选主题。
- 设置选题门：用户确认前，不批量生成所有主题的完整稿。
- 最终 3 分钟时先准备约 5 分钟冗余原句，方便继续删减。
- 三轮复审：删减、流量压力测试、“环环相扣，从一而终”终审。
- 从原文筛选开头钩子、结尾、悬念和评论互动候选。
- 机器核验每个成片口播片段是否逐字存在于源稿。
- 由脚本统计内容单位，禁止模型心算字数。
- 输出源文件、入点、出点、原句、结构角色和情绪备注齐全的剪辑单。
- ASR 疑似错字标记 `[待复听]`，不在剪辑稿中静默改字。

## 安装

### Codex

```bash
git clone https://github.com/yunye123/interview-soul-editor.git \
  ~/.codex/skills/interview-soul-editor
```

重新打开一个 Codex 任务，让技能列表刷新。

### Claude Code

```bash
git clone https://github.com/yunye123/interview-soul-editor.git \
  ~/.claude/skills/interview-soul-editor
```

其他支持 Agent Skills 的宿主，可把仓库放入该宿主的 Skills 目录。

## 转写前置能力

本仓库不重复实现 ASR。视频或音频输入时，优先调用宿主已有的本地转写工具，输出：

- TXT：逐字核验；
- SRT / JSON：时间码定位与回剪。

当前作者环境使用本地 `v2t`：

```bash
v2t "/absolute/path/interview.mp4" "/absolute/path/edit/transcripts" --spk
```

如果只有无时间码 TXT，也能做主题与文稿规划，但不能伪造精确剪辑时间码。

## 使用方法

```text
用 $interview-soul-editor 处理这段访谈。
目标是 2–3 分钟的精品短视频。
先提取逐字稿并规划主题，停在选题门等我确认。
```

用户选题后：

```text
我选择主题 2。先给我约 5 分钟的冗余候选剪辑稿。
严格遵守：不改一句话、不补录、不转述、不意译。
```

## 原文核验

剪辑稿中的口播原句使用以下格式：

```markdown
<!-- VERBATIM:C001 -->
我第一次见到他的时候，我就觉得这个人跟别人不一样。
<!-- /VERBATIM -->
```

运行核验：

```bash
python3 scripts/audit_cut.py \
  --source edit/transcripts/interview.txt \
  --cut edit/04-final-cut.md \
  --target-units 900 \
  --pure-out edit/04-final-cut-pure.txt
```

只有 `missing_verbatim_blocks: 0` 才能称为“已通过原文核验”。脚本的内容单位口径是“中文汉字 + 英文/数字词”；最终字数和节奏仍以 WPS/Word 与实际试听为准。

## 标准产物

```text
edit/
├── project.md
├── transcripts/
├── 01-theme-map.md
├── 02-candidate-cut.md
├── 03-source-audit.md
├── 04-final-cut.md
├── 04-final-cut-pure.txt
├── 05-hooks-endings.md
└── 06-edit-sheet.md
```

## 验证状态

- 官方 Skill 结构校验通过。
- 原句正例通过；润色反例被准确拦截。
- 独立前向测试只生成项目状态和主题地图，按要求停在用户选题门。
- 当前交付边界是“已核验剪辑稿 + 钩子结尾候选 + 时间码剪辑单”，不是承诺一次生成爆款。

## 开源项目复用边界

- 本地转写：复用宿主已有 ASR，不重复封装 Whisper。
- 自动 EDL/渲染：可按需接入 [browser-use/video-use](https://github.com/browser-use/video-use)。
- DaVinci Resolve 与大素材库：可评估 [StoryToolkitAI](https://github.com/octimot/StoryToolkitAI)。
- Node.js 字幕解析：优先使用 npm [`subtitle`](https://www.npmjs.com/package/subtitle)，不手写 SRT 解析器。

详细判断见 [references/open-source-reuse.md](references/open-source-reuse.md)。

## 授权

本项目采用 [MIT License](LICENSE)。你可以免费使用、复制、修改、合并、发布、分发、再许可和销售本项目，包括用于商业或闭源产品；条件是保留原版权声明和 MIT 许可证文本。本项目按“原样”提供，不附带任何担保。
