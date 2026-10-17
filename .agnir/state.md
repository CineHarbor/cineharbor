# CineHarbor Current State

CineHarbor/cineharbor is the organization facade for the seven-repository release unit. Product code lives in the six specialized repositories.

## Objective

Autonomously implement the Principal's Release-Ready 100% plan for **1.0.0**, including commits and verified pushes, without final public publication. Scope and gate rules: docs/releases/1.0.0/scope.md. Observed status: docs/releases/1.0.0/status.json.

**RELEASE_READY = false. PUBLIC_RELEASE_EXECUTED = false.** Historical migration milestones and source inventories do not certify release acceptance.

## Architecture

ADR-0006 supersedes the native-RPC/dual-content-surface target: in-process pure core compiled native/WASM, with Stremio-compatible remote addons providing content and media services. Web must not require a native daemon for its primary content path. Retained application/control/release APIs require explicit ownership, consumers and authentication boundaries. Existing duplicate implementations and remaining Douban/image/media helper routes still require consumer audit; do not delete them or declare retirement complete without evidence.

## Verified execution checkpoint — 2026-09-20

Source inventory run 35424839669 attempt 4, artifact 10596207415, was downloaded and its ZIP/internal archive hashes verified. The inventory is recovery input, not test acceptance. The existing pinned release-toolbox artifact enabled real locked offline Rust verification. Older recovery evidence remains in `.agnir/evidence/2026-09-19-execution-recovery.md`.

Desktop main **1fd69e23d3d493b57ac280ff72623ab0eadb7d4d** passed complete CI twice: **35447427945** and **35448987352**. Every required job/step was inspected, including Windows x64, macOS Intel and Apple Silicon sidecar/check/tests/strict Clippy and actual unsigned installer builds, plus portable safety and pinned WASM/static export. The earlier 8f5c74dc run 35441377610 failed and is historical, not the current main result. These unsigned builds do not certify signed RCs, installed playback or updater/data retention.

SDK media repair PR **#3** was implemented, pushed, passed PR run **35483622714**, and merged to **ca2ffa7c34c7c5e212f24c36b8defe2ea11256d0**. It fixes HLS credential placement/scope, final-response/document-relative resource resolution and signed-URL error disclosure. Eight new tests were added. Local locked verification passed all **47** workspace tests, owned formatting, check, doc-test execution and strict Clippy; four negative-control regressions failed on the previous implementation. Complete main runs **35483666706** and **35483692103** both passed every required Rust gate. Evidence is tied to the merged tree and exact code blobs; prior Core/SDK version alignment was retained.

Web 9fd1fc0b94ca72578dec2f0afbf3cea97e70cccc retains the previously observed successful workflow conclusions for 35438906907 and 35439140734, not blanket product certification. Web/Desktop still pin older Core/SDK inputs and still advertise 0.1.0; downstream release-version/pin alignment and fresh CI remain pending. No production deploy or public release was executed in this checkpoint.

See `.agnir/evidence/2026-09-20-media-and-native-verification.md` and `docs/releases/1.0.0/status.json`.

## Remaining acceptance

Media egress/SSRF/DNS-rebinding/no-open-proxy policy, Live authorization, Range/HEAD/bounded byte handling, final cross-repository source/version alignment, complete browser/user-path acceptance, ADR retirement, signed three-platform RCs, real old-to-new updater/data retention, production deployments, diagnostics/security/license/brand review and release assets remain required. The updater deferral applied only to an earlier Web migration phase and does not waive 1.0.0 acceptance.

The previously supplied 939-byte implementation ZIP contains only README.md and readiness.json, no code or logs. Its implementation/test claims must not be used as evidence. Resume from verified destination refs, source snapshots and actual CI results; neither a chat response failure nor a historical status file defines the current repository outcome.

Project urn:cineharbor:project:cineharbor; lineage urn:cineharbor:lineage:cineharbor. Agnir Core/Profile 1.0 / repository-filesystem/1.0 and operations 1.0.2 at b5626394ec40a5cb7a28c01892acde07cc0adc8e remain unchanged. License baseline CC-BY-NC-SA-4.0; final inventory remains to be verified.

## Current remote reconciliation — 2026-10-17 (supersedes older current-status claims above)

The seven remote main SHAs, source/version pins and 2026-09-20 two-run CI were re-read and recorded in `.agnir/evidence/2026-10-17-release-matrix-install-first.md`. Core 246411ba, SDK 3ab4ff8, Web 97cf1bf5, Desktop 39d88553 and Worker bb26dffa passed twice at their exact heads. Download Site 531a3e73 passed the 2026-10-17 scheduled build/deploy workflow. SDK media security and Web/Desktop 1.0.0 integration are now **implemented and passing their source gates**; the earlier observations of 0.1.0 Web/Desktop pins and missing SDK SSRF/Live/Range handlers are historical, not current source state. Real runtime/player/production verification remains outstanding.

Principal 2026-10-17 directive prioritizes **real unsigned application installation and startup** now; production signing/notarization and cryptographically verified updater are deferred to the **separate public release phase**, not waived, fabricated or considered passed. Actual native install/restart/data checks are **not yet verified**. Desktop signing prerequisite run 35510892575 reports the updater key present but Apple/Windows signing prerequisites incomplete. Facade dependency-audit PR #1 run 35511058147 found Rust/Web dependency issues; old Web PR #1 remains conflicted. Canonical status.json is reconciled. **RELEASE_READY=false; PUBLIC_RELEASE_EXECUTED=false.**

### 2026-10-17 dependency-review artifact classification

Downloaded and inspected audit artifacts from facade PR #1 run 35511058147. These are real lock findings, not mere CI transport errors: Web 32 advisories (3 critical, 13 high, 13 moderate, 3 low), and SDK/Core/Desktop each contains vulnerable rustls 0.23.43 (first patched 0.23.45). Desktop also has 6 unmaintained plus 1 unsoundness advisory warnings. See `.agnir/evidence/2026-10-17-dependency-findings.md`. This is based on 2026-09-20 advisory evidence, not a newly run 2026-10-17 scan. Installation-first priority and release_ready=false remain unchanged.

## 2026-10-18 verified installed smoke + SDK dependency repair

Three native Desktop unsigned installers were **actually installed and launched twice** in GitHub hosted PR CI 39041060877 (Windows x64, macOS Intel, macOS Apple Silicon). PR #3 merged to Desktop main 40e073df8c338b0530facbe403d8a8929afa0a6d. Main post-merge CI and deeper PR #4 /health/SQLite checks were still running when this checkpoint was recorded. SDK rustls security lock fix 0.23.45 merged to 10ce024c9f5b1ea739fca9e239488ee4411f403c; two full SDK main CI runs 39060396338 and 39060462972 passed. Core security alignment PR #3 and Web/desktop residual audit require work. See `.agnir/evidence/2026-10-18-three-platform-install-and-security.md`. Signing/updater deferred until public release, release_ready=false.

## 2026-10-18 additional verification

Core patched SDK/rustls alignment at dc94a185 passed two full main CI rounds 39060680237/39060804061. Desktop real-install main 40e073df passed two complete matrices including three native installs (39059537440/39061854359). Deeper sidecar/SQLite PR #4 passed 39060011521 and merged to Desktop f961c92a; new main CI 39061967719 was still running, so real persisted-data acceptance on final main is pending. `.agnir/evidence/2026-10-18-install-and-core-ci-followup.md`. Public signing deferred; release_ready=false.

## 2026-10-18 patched Web + Desktop integration progress

Verified Desktop f961c92a's first full main run 39061967719 passed all Windows/macOS installed sidecar/SQLite checks; second main run 39064018486 ongoing. Web c9f76d1c merges PR #4 patched Core/SDK pins after green PR run 39063901064; fresh Web main run 39064309813 in progress. Desktop PR #5 de7a099c5 repins all three source dependencies, PR run 39064374670 underway, not merged. These are separate candidate/source results; no claim of final twice-green updated unit. See `.agnir/evidence/2026-10-18-patched-integration-progress.md`. Security Node and manual GUI acceptance remain open; release_ready=false.
