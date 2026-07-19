# Interview Soul Editor

English · [中文](README.md)

An Agent Skill for transcript-first interview editing with human topic approval and deterministic verbatim verification.

It turns long-form interview video, audio, or transcripts into a short-video editing package that can be traced back to the source footage: a topic map, the four editorial questions, an intentionally oversized rough cut, structural reviews, hook and ending options, source verification, and a timecoded edit sheet.

> **Non-negotiable rule: do not rewrite, paraphrase, translate, invent, or request re-recording. Only select, reorder, join, segment, and pace the speaker's original words.**

## Why this Skill exists

The most damaging AI failure in interview editing is not weak writing. It is polished writing that the editor cannot find anywhere in the original footage.

This Skill does not trust a model's claim that it preserved the transcript. Every continuous source excerpt must be placed in a uniquely identified `VERBATIM` block. A deterministic audit script then checks every block against the source transcript. A changed word, missing sentence, or hidden rewrite fails verification.

## Workflow

```text
Inventory footage
  ↓
Local transcription (TXT + SRT + JSON)
  ↓
Topic map + four editorial questions
  ↓ user selects one topic
Oversized verbatim candidate cut
  ↓
Trim → traffic stress test → structural final review
  ↓
Hooks and endings
  ↓
Verbatim audit + length/runtime check
  ↓
Timecoded edit sheet
  ↓ execute real cuts only after strategy approval
```

### The four editorial questions

1. Who am I speaking to?
2. What exactly am I trying to say?
3. Whose thinking, emotion, or action should this change—and how?
4. What idea, misconception, habit, or opposing force creates the tension?

The “opposing force” should normally be an idea, misconception, habit, or structural tension—not a fabricated enemy.

## Key capabilities

- Accept video, audio, TXT, SRT, or JSON transcripts.
- Split long interviews into 3–7 genuinely distinct topic candidates.
- Enforce a topic-selection gate before drafting full cuts.
- Build a 1.5–2× oversized verbatim candidate cut for deliberate trimming.
- Run three focused reviews: trimming, traffic stress testing, and end-to-end structural review.
- Select hooks, endings, cliffhangers, and interaction lines from the source transcript.
- Verify every spoken excerpt against the source text.
- Count content units with a script instead of letting the model guess.
- Produce an edit sheet with source file, in/out timecodes, verbatim text, structural role, emotion, and continuity notes.
- Mark suspected ASR errors as `[needs-listen]` rather than silently correcting the cut script.

## Installation

### Codex

```bash
git clone https://github.com/yunye123/interview-soul-editor.git \
  ~/.codex/skills/interview-soul-editor
```

Open a new Codex task so the skill list refreshes.

### Claude Code

```bash
git clone https://github.com/yunye123/interview-soul-editor.git \
  ~/.claude/skills/interview-soul-editor
```

For other Agent Skills-compatible hosts, clone the repository into that host's Skills directory.

## Transcription prerequisite

This repository intentionally does not implement another ASR wrapper. For video or audio input, use an existing local transcription tool that produces:

- TXT for verbatim verification;
- SRT or JSON for source timecodes.

The author's current environment uses a local `v2t` command:

```bash
v2t "/absolute/path/interview.mp4" "/absolute/path/edit/transcripts" --spk
```

A plain transcript without timecodes is sufficient for topic and script planning, but the Skill will not invent precise edit timecodes.

## Usage

```text
Use $interview-soul-editor to process this interview.
The target is a polished 2–3 minute short video.
Transcribe it, propose topic candidates, and stop at the topic-selection gate.
```

After selecting a topic:

```text
I choose topic 2. Build an approximately five-minute oversized candidate cut.
Do not rewrite, paraphrase, translate, invent, or request re-recording.
```

## Verbatim audit

Spoken source excerpts use the following format:

```markdown
<!-- VERBATIM:C001 -->
The first time I met him, I knew he was different from everyone else.
<!-- /VERBATIM -->
```

Run the audit:

```bash
python3 scripts/audit_cut.py \
  --source edit/transcripts/interview.txt \
  --cut edit/04-final-cut.md \
  --target-units 900 \
  --pure-out edit/04-final-cut-pure.txt
```

A cut is source-verified only when `missing_verbatim_blocks: 0`. The script counts Chinese Han characters plus English/number tokens. Final timing still depends on an editor's word processor statistics and listening to the actual performance.

## Standard output

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

## Validation status

- The official Skill structure validator passes.
- Genuine source excerpts pass; a rewritten negative example is correctly rejected.
- An independent forward test produced only the project status and topic map, then stopped at the human topic-selection gate.
- The current product boundary is a verified cut script, hook/ending candidates, and a timecoded edit sheet—not a promise of one-click virality.

## Reuse boundaries

- Local transcription: reuse the host's existing ASR instead of wrapping Whisper again.
- Automated EDL/rendering: optionally integrate [browser-use/video-use](https://github.com/browser-use/video-use).
- DaVinci Resolve and large footage libraries: evaluate [StoryToolkitAI](https://github.com/octimot/StoryToolkitAI).
- Node.js subtitle parsing: use npm [`subtitle`](https://www.npmjs.com/package/subtitle) instead of writing an SRT parser.

See [references/open-source-reuse.md](references/open-source-reuse.md) for the detailed decision record.

## License

This project is licensed under the [MIT License](LICENSE). You may use, copy, modify, merge, publish, distribute, sublicense, and sell the project, including as part of commercial or closed-source products, provided that the original copyright notice and MIT license text are preserved. The project is provided “as is,” without warranty.
