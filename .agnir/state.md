# CineHarbor Current State

Canonical facade for the seven-repository release unit. Target: **1.0.0 release-ready**, under `docs/releases/1.0.0/scope.md`; no public 1.0.0 publication in this preparation run. **RELEASE_READY=false; PUBLIC_RELEASE_EXECUTED=false.**

## Observed integration — 2026-09-20

SDK main `3ab4ff8fcc38a6f0849389a7c6b66291f3ca341d` already contains server-only resource-scoped media capabilities, bounded public egress, Live authorization and Range/HEAD handling. Its two current main matrices (35501487450 / 35501530721) were independently inspected. This recovered work is newer than the previous ca2ffa7c checkpoint; do not overwrite it or describe the full media boundary as unimplemented. Production and complete independent security/player acceptance remain separate.

Core main `246411ba6c72b5b79b6e14598228c62a16857309` now pins that SDK with correct 1.0.0 lock entries and issues fresh, credential-free, referrer-free actual WASM addon requests. All five required PR lanes and two exact-main matrices (35507419988 / 35507456971) passed. Local native tests: 161 passed.

Web main `97cf1bf55033ed16a2f0f77a97c28848aa323956` aligns package/UI/release metadata to 1.0.0 and the verified Core/SDK unit. It preserves and renews signed playback/Live/download URLs, prevents stale-selection races, removes public signing-secret reads and excludes signed metadata from PWA HTTP caching without removing intentional offline data. 714 Jest tests, 31 tooling tests and two consecutive local production builds passed. Two exact-main matrices (35508691724 / 35508936072) passed, including all seven real runtime checks; downloaded artifacts and individual exit files were verified.

Download Site main `531a3e731f9c1027ea81676491a068d35bfd04f6` removed stale 200.0.1 preparation metadata without inventing 1.0.0 downloads. Two complete main runs (35509622677 / 35509653604) passed static verification, real public-release export and gh-pages publication. **Repository metadata reports has_pages=false: a served production download site is not verified.**

Desktop PR #2 merged to main `39d885531144636487bad37af497373ca4ca6a78` after candidate `f159db179b181256dc6dc142c855326c2f0ec309` passed every required PR gate, tree `efebd46a1108dc539f3979467b2ec53481490e8f`. It aligns all owned versions and dependency pins, enforces integration consistency, and prevents missing/ad-hoc signing configuration from being treated as a formal RC. Existing updater public key and production CSP are preserved. The initial fd304b5f PR failed Windows CRLF lock parsing before native compilation; the repaired candidate normalizes only in-memory parsing and adds three regressions. All 44 Jest and 40 tooling tests plus portable checks pass. Repaired native PR run 35510061151 passed every mandatory step on Windows x64, macOS Intel and Apple Silicon, plus portable checks and actual WASM/static export. Two exact-main matrices and the trusted-main signing report remain to be inspected.

Worker main `bb26dffab86813d42d072eca3ac6af1f1e25cc66` has two inspected complete current matrices (35455531459 / 35455550411). Its existing consumer audit classifies this Cloudflare gateway as optional and unused, not the browser PWA worker. Production credentials are not a release prerequisite unless an actual consumer is added; used addon/media services still require production acceptance.

## Dependency review and remaining gates

The new pinned-input audit collector has 12 passing local failure-mode tests and explicitly rejects network/tool errors, malformed reports, ignored findings and warnings. The hosted workflow audits all six product repositories using lockfiles, disabled dependency lifecycle scripts, cargo-audit 0.22.2 and pnpm 10.14.0/npm. It also captures pnpm license inventories as metadata, never as legal approval. The real audit results have not yet been observed at this checkpoint.

Finish Desktop exact-source native verification and inspect actual trusted-main signing prerequisites. Genuine OS-signed/notarized three-platform RCs, installed playback/download, long-running native media expiry, actual public 0.1.0 to signed 1.0.0 upgrade with retained data, production addon/media and served site, full user paths, ADR-0006 retirement, security/license/brand review and final assets remain open. Public desktop-v0.1.0 exists (release 378518356); signature-file existence is not signature or upgrade verification.

See `docs/releases/1.0.0/status.json` and `.agnir/evidence/2026-09-20-client-integration.md`. Historical recovery evidence remains preserved; obsolete prototype ZIP claims are not evidence. Final source snapshots or a successful workflow conclusion alone never certify the release.

Project urn:cineharbor:project:cineharbor; lineage urn:cineharbor:lineage:cineharbor. Agnir 1.0 / repository-filesystem/1.0, operations 1.0.2 at b5626394ec40a5cb7a28c01892acde07cc0adc8e and license baseline CC-BY-NC-SA-4.0 remain unchanged.
