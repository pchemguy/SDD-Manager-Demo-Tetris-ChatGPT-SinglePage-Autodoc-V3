# Repository layout

## Application and contract ownership

[ARCHITECTURE](ARCHITECTURE.md) and [DECOMPOSITION](DECOMPOSITION.md) define logical boundaries; [PLAN](PLAN.md) defines their delivery route. Paths below are intended owners, not claims that application/test/tool files already exist.

| Path | Owner and purpose |
| --- | --- |
| tetris.html | Sole application entry and deployable source. Embedded style, markup and one classic script contain every application component. |
| tetris.html: settings-policy and domain sections | Canonical runtime settings definition, piece geometry and Engine. Pure named closures support extraction from this exact HTML for checks. |
| tetris.html: session, validation and codecs sections | SessionStore, complete semantic validation, duplicate-aware JSON decoder and lazy SQLiteCodec. No separate runtime source/schema fetch. |
| tetris.html: adapters, controller and presentation sections | ProtocolAdapter, FileController, DependencyLoader, Controller, Input, Renderer and bootstrap. Browser I/O stays here. |
| docs/dev/contracts/session.schema.json | Canonical saved-session JSON Schema, owned by SPEC; copied unchanged into generated release assets. Semantic requirements stay in SPEC. |
| VERSION | Application release version consumed/checked by packaging; independent of saved-session format version. |

Use explicit comment markers and closure boundaries for embedded sections; extraction must not create a second maintained implementation. Runtime closures expose the component surfaces to their actual collaborators, without a production global test API. CDN source is an external dependency; pin its URL/version/integrity/license evidence in the SQLite loader and dependency documentation when verified.

## Tests and developer tooling

| Path | Owner and purpose |
| --- | --- |
| tests/unit/ | pytest domain/settings/validation/codec scenarios; deterministic fixture-driven calls into extracted application sections. |
| tests/support/ | Node extraction/adapter harness and Python browser/HTTP fixtures; helpers, not application implementations. |
| tests/browser/ | pytest with Playwright for Chromium/Firefox, direct-file/localhost HTTP, focus/keyboard/layout/persistence/file workflows. |
| tests/fixtures/ | Small deterministic gameplay and valid/invalid JSON/SQLite fixtures, with explicit provenance; no credentials or user's real session data. |
| requirements-dev.txt | Pinned pytest, Playwright and schema-validation tooling, established during provisioning. Python/Node/browser tooling is development-only. |
| scripts/package.py | Build a release directory by copying the sole HTML and required documentation/schema, check embedded version, and generate SHA256SUMS. It does not assemble application source. |
| scripts/check_artifact_names.py | Reject versioned or unexpected actual asset basenames; shared by direct packaging and CI. |
| .github/workflows/checks.yml | Run the established tests and package/name checks in the supported CI environment. |
| dist/ | Generated version-free release files only; ignored, reproducible from the pinned release source. |
| test-results/ | Temporary browser traces/screenshots/reports; ignored. |

pytest is the test entry. Unit scenarios can invoke Node harnesses; browser scenarios use the Python Playwright binding so all checks remain under pytest. Exact setup/check commands are introduced and validated by Phase 1 provisioning before AGENTS or README calls them verified. No development dependency is needed to play the delivered HTML. Dedicated environments follow the repository browser policy; no unverified system-wide installation is prescribed.

## Documentation and continuity

| Path | Purpose |
| --- | --- |
| README.md | Playing/installing, current delivered capabilities, controls, direct-file/HTTP distinctions and validated developer commands. |
| docs/FILE-FORMATS.md | JSON/SQLite format/version examples, strict rejection and manual restore behavior, linked to canonical SPEC/schema. |
| docs/DEPENDENCIES.md | Verified CDN pin, license/integrity details, loading behavior and test-tool/browser version evidence. |
| RELEASE-NOTES.md | Final current release message for default-branch release commit, tag and GitHub body. |
| docs/dev/PROJECT.md, ARCHITECTURE.md, DECOMPOSITION.md, SPEC.md, PLAN.md, layout.md | Current governing project inputs and canonical design/contract/delivery ownership. |
| docs/dev/TASKS.md | Complete implementation task hierarchy; created by task derivation. |
| docs/dev/DOCS_TASKS.md, DOCS_PREPARATION.md | Separate preparation checkoffs and control/decision evidence. |
| docs/dev/HANDOFF.md | Periodic checkpoint; reconstruct later work through current owning records and Git. |
| docs/dev/*-REVIEW-REPORT.md | Adjacent SPEC/PLAN/TASKS conformance evidence. |
| docs/dev/reports/phases/<phase>/<milestone>.md | Delivery milestone review/testing/report evidence. |
| docs/dev/reports/phases/<phase>/PHASE-REPORT.md | Cross-milestone phase exit evidence. |
| docs/dev/reports/IMPLEMENTATION-REPORT.md | Final full-list results and unresolved eligible TODO aggregation. |

Root AGENTS.md retains controlling workflow/browser/discovery instructions and current navigation. Existing .agents plugin/skill source is preserved; application work does not modify the pinned plugin. Provenance scaffolding and manual logs under docs/ai-logs retain their independent instructions and are excluded from routine product review. No new generated instruction files, source trees or companion deployable assets are required.

## Packaging allocation

The release directory contains tetris.html, README.md and SHA256SUMS; Phase 6 onward also includes session.schema.json copied from its canonical contract path. Stable names are checked on actual generated files and hosted downloads. Version labels live in content, tags and release metadata rather than filenames. Generated copies are not second canonical sources. Test fixtures and development documentation are repository support, not runtime prerequisites.
