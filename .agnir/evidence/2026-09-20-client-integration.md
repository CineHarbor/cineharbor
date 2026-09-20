# Verified client integration and release review — 2026-09-20

## Authority and immutable continuity

Continue the canonical release-ready scope without public 1.0.0 publication. Facade base d91fbf77f690f8625dbd13537a41518acf1a205a, tree 3bb08599c0680d3795b0c992cc0413b61798ad0c; activation, selected lineage, current state/next and decisions were read directly. The older audit-workflow facade checkout is not authoritative current facade content. Source/code and material state are checkpointed together; no provenance/identity migration.

Source inventory run 35424839669 attempt 6, artifact 10604060897, ZIP SHA256 e10fe235fb775147f8d98c42ebb867c6b6872541fc2f3d566bdfdf5398bb2dc8 was downloaded and verified. Its source and dependency artifacts were reconciled with live refs before writes. Source inventory is not acceptance.

## Implemented and merged

Core PR #2 merged to 246411ba6c72b5b79b6e14598228c62a16857309; tree 8f9f6be0ad8f5e20f2dbf3525d4f4fb4d1dde3fd. SDK pin and exactly two owned sibling lock versions aligned. Actual WASM transport uses no-store, omit credentials and no-referrer. Local 161 native tests, doc execution, owned fmt, locked check, strict Clippy and native/WASM builds passed. The real compiled-WASM test fails on the old transport and passes after repair. PR 35507272478 and both main runs 35507419988 / 35507456971 passed all five lanes and mandatory steps. Fresh anchor read; post-merge evidence comment 5749486479.

Web PR #2 merged to 97cf1bf55033ed16a2f0f77a97c28848aa323956; tree 2a2faec19adc1948196694649cefec78d9d4d8b3. Signed VOD/Live/download URLs remain opaque, expiry/401/403 renewal is bounded and race-safe, browser signing-secret reads are removed, signed metadata bypasses PWA HTTP cache, and owned version/release metadata is 1.0.0/canonical. Intentional offline data is preserved. 134 suites/714 Jest tests, 31 tooling tests, strict lint/typecheck and two consecutive production builds passed. An initial repeated-build failure caused by a shared dependency symlink was resolved by independently restoring the hash-verified dependency directory, without changing the lock or tests. Old URL/cache/transport implementations fail targeted negative controls.

Web PR 35508332862 passed. Both exact-main runs 35508691724 / 35508936072 passed every quality/runtime step. Each downloaded runtime summary has exactly seven cases, no errors/signals, exitCode=0, and every individual .exit file equals 0: compiled-WASM request policy, WASM CDP, addon/VOD/Douban cross-origin, media HTTP, PWA production. Media checks exercise 14 real Rust router fixtures plus the real VOD binary's issued capabilities, 401/403/HEAD/CORS behavior and zero private egress. These are not full production-player or installed acceptance.

Main runtime artifact 10603739944 SHA256 a31e494e9cde07bbadb61be93da48b2e95b01a0f53ac0331b146941b8d2f53c6; independent artifact 10604763684 SHA256 e802bd195fe7379cc83489eeca3a7f3463685cebd4c22143e72bdd41fbb478d7. Both were downloaded, hashed and inspected. Both actual WASM builds report 1.0.0 and digest 9099c56afee38713a9fbc5e9694e469b9d16ab2e2d0ef957dd0fc70d35d61812. Fresh anchor read; post-merge comment 5749647948.

Download Site PR #2 merged to 531a3e731f9c1027ea81676491a068d35bfd04f6; tree efa22f1d329a7506132ba2e105f102606dc6db67. Replaced stale 200.0.1 preparation metadata, preserved empty preview and excluded draft 1.0.0 while real public 0.1.0 remains available. Local 10 Jest and 10 Node tests/typecheck/build/syntax passed; the old version fails the negative control. PR 35509088800 passed. Main 35509622677 and 35509653604 passed all required checks, real public export/build and gh-pages publication. Required jobs: 106075142286/106075190969 and 106075224461/106075276367. Fresh main and anchor read; post-merge comment 5749737812.

## Desktop candidate and observed repair

PR #2 candidate f159db179b181256dc6dc142c855326c2f0ec309, tree efebd46a1108dc539f3979467b2ec53481490e8f; branch release/1.0.0-desktop-integration. All owned manifests/lock entries/display versions are 1.0.0 and pins match the above verified Core/SDK/Web. Integration validation rejects mixed versions or pins. Draft creation now fails before any release asset write if approved updater/macOS/Windows signing prerequisites are absent; ad-hoc signing is not a formal RC. Credentials are scoped to the signing step, and a separate trusted-main report emits statuses only. Approved updater key/endpoints and production CSP are unchanged.

The temporary exact-tree branch materializer (35509601190) applied and verified the candidate but its normal GITHUB_TOKEN correctly refused a workflow-file push. The already-authorized repository connector published the exact tree, without escalating runner permissions. All temporary transport files were removed before PR CI.

Initial PR run 35509724548 at fd304b5f passed portable and actual pinned WASM/static export, but Windows job 106075738202 failed a literal-LF lock matcher under CRLF checkout before native compilation. Follow-up f159 normalizes only in-memory TOML/lock text and adds valid-CRLF-byte-preservation, stale-CRLF-version and duplicate-entry regressions. All three fail against the former parser. All 44 Jest tests, 40 tooling tests, typecheck/CSP/fmt/integration checks pass after repair. Repaired native run 35510061151 passed every required step: portable 106076826845, actual WASM/export 106076826730, Apple Silicon 106077198571, Intel 106077198578 and Windows 106077198656. PR #2 was normally merged to main 39d885531144636487bad37af497373ca4ca6a78, with the identical efebd46a tree. Two exact-main matrices and the signing-prerequisite report remain to be inspected; no signed/installed acceptance is inferred.

## Recovered current sources, not reimplemented work

SDK 3ab4ff8fcc38a6f0849389a7c6b66291f3ca341d: main runs 35501487450 / 35501530721 had every required fmt/check/test/Clippy step inspected and passed. Scoped capabilities, egress and bounded forwarding already exist; complete independent security and deployment review remains open.

Worker bb26dffab86813d42d072eca3ac6af1f1e25cc66: main 35455531459 / 35455550411, jobs 105930006627 / 105930063149, passed install/check/tests/real-workerd/build/dry-run/audit/clean-tree steps. Its durable cross-repository consumer audit found the gateway optional and unused; current Core/Web/Desktop pins do not introduce it. This does not remove deployment obligations for actual used addon/media services.

## New dependency review implementation

Pinned-input collector and hosted workflow audit four Node locks and three Rust locks, including development/optional/platform dependencies. Frozen installation disables dependency scripts; no dependency fixing, advisory ignores, registry-error suppression or platform filtering is used. cargo-audit 0.22.2 is pinned, its binary/toolchain and current advisory database revision are recorded, and warnings are denied. Each report records exact source/tree, lock SHA256, commands/exit codes and stdout/stderr hashes. Missing tools, timeouts, malformed JSON, advisories and inconsistent source all fail. Twelve local regression tests and Python/YAML syntax passed; real hosted outcomes remain unobserved at this checkpoint. Collected pnpm licenses are inventory, not legal approval.

## Remaining acceptance and external boundaries

Repository metadata for the Download Site explicitly reports has_pages=false. Existing gh-pages pushes therefore do not prove a served site. The connected repository surface has no Pages-administration mutation. Official actions/configure-pages v5/action.yml requires a non-default token for enablement; no extra privilege was invented. Record SITE-PAGES-ENABLEMENT as EXTERNAL_BLOCKER until approved administration and served smoke are observed.

Public Desktop release 378518356 / desktop-v0.1.0 has existed since 2026-08-28 and includes signature assets. None of this proves cryptographic signature verification, installed launch or actual old-to-new upgrade. Hosted signing-secret availability must be learned from the trusted-main report rather than local environment absence.

Still required: complete repaired Desktop native and final-source repeats; real dependency/advisory triage and license review; OS-signed/notarized RCs; installed playback/download and native long-running capability expiry; real 0.1.0 to 1.0.0 signed upgrade with retained accounts/config/database/download data; used production addon/media and served download site; complete product/browser paths; ADR-0006 consumer retirement; security/brand/release notes/assets and final seven-repository evidence closure. RELEASE_READY=false; PUBLIC_RELEASE_EXECUTED=false.
