# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the project request on 2026-11-01.
- Scope: the complete single-page Tetris target, including both execution modes, modern rules, penetrator, session-only settings, HTTP(S) configuration persistence, leaderboard and JSON/SQLite Save/Restore.
- Approval basis: PROJECT approval remains active; ARCHITECTURE through TASKS checkpoints are preapproved by autodoc. Material unresolved gameplay choices remain proposals until resolved.
- Stop: after published DOCS-008 and its verified issue closure, before DOCS-009 whole-package QC, integration or implementation.
- Tracking: enabled for documentation and implementation by root AGENTS.md. Publication is required after every owned commit.
- Reporting: Standard, using concise status reports; Minimal and Explicit profiles are available.

## Scope sequence

One documentation pass describes the entire requested product. Implementation must start with the simplest playable baseline and use bounded useful increments. A session-only configuration increment precedes persistence. Each completed, verified and integrated implementation phase receives a GitHub release. Detailed version/phase strategy remains proposed until the governing documents are accepted.

## Decisions and document evidence

| Task | Current evidence / decision basis |
| --- | --- |
| DOCS-001 | Initialization checks below; completion commit includes task checkbox and HANDOFF. Publication and issue closure require subsequent readback. |
| DOCS-002 | PROJECT proposal and material gameplay decisions pending; no human acceptance yet. |
| DOCS-003 through DOCS-008 | Not authored; scoped autodoc preapproval applies after PROJECT acceptance and prerequisite checks. |
| DOCS-009 | Not selected; remains pending beyond the autodoc stop. |

## Initialization

- Eligible clean Git worktree: main at bca50634127c43b9509133fbac663d5142cb5591; no prior development documents, application code or unfinished workflow branches.
- Actual execution host: Linux with Bash, Git 2.51.1, Node 24.22.1 and Python 3.12.14. Windows-only shell policy does not apply to this host.
- All four original root files retained: AGENTS.md, AI_DISCLOSURE.md, SDD-MANAGER.md and SKILL_DISCOVERY_PROTOCOL.md. None copied. Byte comparison against initial commit passed for all four. Full initial presence requires no extra continuation pause.
- Read-only repository skill/plugin discovery completed in chat: SDD Manager 0.16.1 with its 15 bundled skills and standalone technical-writing-assistant. The repository package is the pinned workflow source.
- Preparation tracking verified before repository writes: sdd-docs-main milestone 1; DOCS-001 through DOCS-009 issues 1 through 9, with exact package-generated bodies and milestone associations. No product phase objects activated.
- Manual provenance setup enabled by default. Base: bca50634127c43b9509133fbac663d5142cb5591. Seed: d38a6e619762679eb4207a24ad02b2977e4492fb on design-docs/ai-logs. Published two-parent main merge: 11ab200b481fa8d16a9d3656c968dc0bbdde05f1. Both scaffold files match package assets; exact three-path delta and whitespace checks passed. No conversation transcript was recorded.
- Protected credential exclusion was added to .gitignore and verified before storage. No credential value belongs in tracked content.
- Preparation branch design-docs/main starts from published merge 11ab200b481fa8d16a9d3656c968dc0bbdde05f1 and targets main.
- Required task definitions copied from the pinned DOCS_TASKS template; only DOCS-001 is checked. No reset or previous pass.

## Pending transitions

Publish/read back this initialization checkpoint, then close/read back issue 1 with evidence. Next prepare and publish PROJECT for human acceptance. Remaining documentation issues and preparation milestone stay open. No implementation range is selected yet.
