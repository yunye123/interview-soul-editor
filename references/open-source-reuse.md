# 已核对的开源与 npm 复用边界

核对日期：2026-07-19。这里记录选择依据，不在技能安装时自动下载任何项目。

## 直接采用

### 本机 `local-transcribe` / `v2t`

- 用途：本地把视频或音频转为 TXT、SRT、JSON，可选说话人区分。
- 决策：作为本技能默认转写前置，不再实现另一套 Whisper 包装。
- 理由：本机已安装、中文访谈友好、不联网、没有 API 费用。

## 按需接入

### browser-use/video-use

- 仓库：https://github.com/browser-use/video-use
- 许可证：MIT。
- 适合：用户明确要求从逐字稿生成 EDL、真实切段、渲染字幕并检查切点。
- 借鉴/复用：逐字稿是主阅读面；策略批准后再动剪辑；片段边缘对齐词边界；转写缓存；EDL 后渲染与自检。
- 不默认安装：其标准转写依赖 ElevenLabs Scribe 和 API key，完整渲染链比本技能的文字策划目标更重。

### octimot/StoryToolkitAI

- 仓库：https://github.com/octimot/StoryToolkitAI
- 许可证：GPL-3.0。
- 适合：海量素材索引、语义搜索、说话人识别、DaVinci Resolve Studio、EDL/XML 导出。
- 不内嵌：它是独立应用且 GPL 传染边界需要谨慎；需要该工作台时单独安装使用。

## npm 组件

### `subtitle`

- 页面：https://www.npmjs.com/package/subtitle
- 仓库：https://github.com/gsantiago/subtitle.js
- 核对版本：4.2.2，MIT。
- 用途：成熟的 SRT/WebVTT 解析、过滤、重同步和输出。
- 决策：以后实现 Node.js 字幕/时间轴转换时直接依赖它，不手写 SRT 解析器；当前 Python 审核脚本只处理 TXT 与明确的 `VERBATIM` 块，因此不新增 Node 依赖。

### `nodejs-whisper`、`@illyism/transcribe`、`@codearcade/subtitle-generator`

- 用途：分别提供本地 Whisper 或云端 Whisper 转写封装。
- 决策：不作为默认依赖，因为与现成 `v2t` 重复；`@illyism/transcribe` 还需要 OpenAI API key。只有迁移到没有 `v2t` 的 Node 环境时再评估。

## 本技能独有部分

开源项目普遍解决“转写、搜索、时间轴、渲染”，没有覆盖本技能的完整判断链：灵魂四问、单主题击穿、冗余候选稿、多轮删减/压力测试/终审、严格禁止润色、原文逐块核验、钩子与结尾的人工作品门槛。这部分保留为 Skill 指令和轻量审核脚本。
