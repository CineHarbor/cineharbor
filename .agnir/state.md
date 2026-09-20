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
