# Media repair and native verification — 2026-09-20

## Authority and source continuity

Continue the Principal's 1.0.0 release-ready plan autonomously. This checkpoint changes SDK media code and facade release evidence; it does not publish a release, replace signing identities, weaken a check or claim all acceptance gates are complete. Facade base is `168844e467ea7528c64d9692d2b76182a4a0c3e8`, tree `d4e14993b0c6e08ed4e9d3f10a769ccfaf087b89`.

Refreshed source inventory: facade run `35424839669`, attempt 4, artifact `10596207415`; ZIP SHA256 `38dc8c1e81f551ca3d8067ed075202468330a06a43985eb7f4b9757b7d9ecab0`. ZIP and nested archive checksums passed. The audit workflow's own facade checkout is its older workflow revision, not the latest facade main, so current facade files and parent/tree were read directly before this checkpoint.

## SDK implementation, regression proof and publication

Repository: `CineHarbor/cineharbor-addon-sdk`.

Base: `55856760a0872e50bea4e9a4f0da77f8e30dfb2c`. Candidate `801b3213efb5df20f689c691edb2eea0d1a7bf19` was pushed to `release/1.0.0-media-resource-integrity`, passed PR #3 CI, and merged normally to main **`ca2ffa7c34c7c5e212f24c36b8defe2ea11256d0`**. Candidate and merged trees are **`350baa04311f5ba3b0934a069d9ec7c8a26cd511`**.

Repaired defects: VOD token placement on real HLS URI attributes rather than trailing names; credential scope restricted to the configured proxy origin/path and declared resource endpoints; redirect-aware and complete-document-relative VOD/Live URI resolution; signed upstream URL redaction in public errors. The existing 1.0.0 versions, locks and pinned Core `d51414bba4964dd7cee02780e41c73e35190ce76` were preserved.

Exact code blobs:

- `crates/cineharbor-media/src/lib.rs`: `1aaab747a05cf4a7eabd822664c83b7ef9ae6efe`
- `crates/cineharbor-media/src/serve.rs`: `1f5a7fc1e246eb256a14e0050486262d0736e125`
- `crates/cineharbor-media/src/serve/token.rs`: `ff108dc3706f78b61cb339674acb5511c9a0dcf0`

The project's release-toolbox artifact supplied the exact Rust 1.98.1 toolchain and offline locked registry. Owned formatting, locked all-target check, all-target/all-feature tests, doc-test execution, strict Clippy `-D warnings` and diff whitespace checks passed. **47 native workspace tests passed, 0 failed, 0 ignored** (media: 19, including eight added tests). Doc tests completed with no examples. Restoring the original implementation while retaining four new handler/URL tests made all four fail; restoring the repair returned the full suite to green. This is fixture/logic evidence, not real player or deployed-service acceptance.

Observed hosted runs:

| Run | Context | Required gate results |
| --- | --- | --- |
| 35483622714 | PR #3 at candidate 801b3213 | fmt, check, tests/doc tests, strict Clippy all passed |
| 35483666706 | main push at ca2ffa7c | all four gates and required steps passed |
| 35483692103 | independent main workflow dispatch at ca2ffa7c | all four gates and required steps passed |

Required job IDs for the main push: Clippy `106005920217`, tests `106005920267`, fmt `106005920271`, check `106005920285`. Independent main run: tests `106005997003`, check `106005997048`, Clippy `106005997058`, fmt `106005997093`. The repeat-dispatch helper is expected to skip outside push events; it is not a product gate. Post-merge results were also recorded on PR #3 rather than changing the tested SDK source just to record its own outcome.

## Desktop native CI reconciliation

Repository: `CineHarbor/cineharbor-desktop`; existing main **`1fd69e23d3d493b57ac280ff72623ab0eadb7d4d`**. Its Windows-only diagnostics repair predates this execution; this checkpoint independently inspected its results, not reimplemented it.

Runs **35447427945** (main push) and **35448987352** (independent main workflow dispatch) are complete successes at the same SHA. Every required step was inspected in portable safety/tooling/Rust formatting, actual pinned WASM/frontend export, Windows x64, macOS Intel and macOS Apple Silicon. Native steps include locked sidecar build, all-target check, native tests, strict Clippy, real unsigned installers and immutable source/lock checks. No required native gate was skipped.

First native job IDs: Intel `105909166870`, Apple Silicon `105909166872`, Windows `105909166920`. Second: Windows `105913205042`, Apple Silicon `105913205053`, Intel `105913205075`.

The older run 35441377610 at 8f5c74dc is a historical failure: macOS strict Clippy and Intel DMG packaging failed. It is no longer a blocker for the newer native-build revision. Unsigned installers remain categorically different from signed RC, installed playback/download and real old-to-new updater/data-preservation acceptance.

## Remaining work and handoff

Web/Desktop still use older Core/SDK dependency pins and 0.1.0 package versions. Their recorded successful CI must not be projected onto a future aligned release unit. Reconcile owned lock entries and exact source pins and require fresh downstream matrices.

The SDK code still requires a complete media egress/SSRF/DNS-rebinding/no-open-proxy boundary, Live authorization, and Range/HEAD/bounded or streaming byte forwarding. Production credentials/deployments, real media playback, signed RCs and updater/data preservation were not verified by this work. Architecture retirement, product/browser acceptance and security/license/brand/final-version review also remain open.

`RELEASE_READY=false`; `PUBLIC_RELEASE_EXECUTED=false`. Final evidence must continue to follow actual current source revisions and observed outcomes, not stale component prose or source-inventory success.
