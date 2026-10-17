# Release status reconciliation and installation-first directive — 2026-10-17

Project: urn:cineharbor:project:cineharbor; lineage: urn:cineharbor:lineage:cineharbor.
Principal directive (2026-10-17): record remote progress, continue execution, prioritize **actual installation acceptance**; defer official signing/notarization to the separate public-publication stage. This is an ordering decision, not a test pass or authorization to publish.

## Immutable observed main source revisions

| Repository | main SHA | Observed successful workflow runs |
| --- | --- | --- |
| CineHarbor/cineharbor | `d91fbf77f690f8625dbd13537a41518acf1a205a` | facade source audit 35483816784 |
| CineHarbor/cineharbor-core | `246411ba6c72b5b79b6e14598228c62a16857309` | 35507419988, 35507456971 |
| CineHarbor/cineharbor-addon-sdk | `3ab4ff8fcc38a6f0849389a7c6b66291f3ca341d` | 35501487450, 35501530721 |
| CineHarbor/cineharbor-web | `97cf1bf55033ed16a2f0f77a97c28848aa323956` | 35508691724, 35508936072 |
| CineHarbor/cineharbor-desktop | `39d885531144636487bad37af497373ca4ca6a78` | 35510892612, 35511311874 |
| CineHarbor/cineharbor-worker | `bb26dffab86813d42d072eca3ac6af1f1e25cc66` | 35455531459, 35455550411 |
| CineHarbor/cineharbor-download-site | `531a3e731f9c1027ea81676491a068d35bfd04f6` | 39015356028 |

GitHub readback of each `refs/heads/main` and SHA-scoped Actions runs was checked on 2026-10-17. Core, SDK, Web, Desktop, Worker each have two successful full main CI runs at the listed exact SHAs. The latest Desktop run 35511311874 includes passing Windows x64, macOS Intel/arm64 native jobs, actual **unsigned installer builds**, sidecar, unit tests, strict Clippy and pinned frontend export. Web's 35508936072 confirms source WASM/frontend build and browser/addon integration suite, but not installed desktop behavior.

Download Site's scheduled 39015356028 passed on 2026-10-17 at the unchanged listed SHA, including static build and gh-pages publish job; this is not a served-site/installer authenticity inspection. Facade's main 35483816784 passed source audit, but does not reflect the newer product-repo commits until this reconciliation.

## Verified cross-repository pins

Web 97cf1bf5 pins Core 246411ba6c72b5b79b6e14598228c62a16857309 and SDK 3ab4ff8fcc38a6f0849389a7c6b66291f3ca341d. Desktop 39d88553 pins both and Web 97cf1bf55033ed16a2f0f77a97c28848aa323956. Web, Desktop, Download Site package versions are 1.0.0; prior 0.1.0 mismatch is no longer a current blocker.

SDK 3ab4ff8 adds signed scoped VOD/Live media capabilities, public-only outbound/redirect validation, Range/HEAD and stream bounds. Web/Core integration preserves/renews resource capabilities. CI and fixtures do not replace deployed/player/long-download security acceptance.

## Current external and safety findings

- Desktop release-signing prerequisite workflow **35510892575 failed** on the current Desktop SHA. Its report indicates configured updater signing key; missing Apple certificate/password/Developer ID/notarization and Windows approved signing provider. These are **DEFERRED_TO_PUBLIC_RELEASE** by the Principal for current work, **not passing**. No public release or signing bypass is permitted.
- Facade open PR #1 (head d1d0e584f56bb8004cccfcafd63caf980277a4a2), audit run **35511058147**: contract test succeeded; Rust lock audit found findings/error in Core, SDK and Desktop; Web Node lock audit found findings/error; Desktop/Worker/Download Site Node audits passed. Exact vulnerability severities require reading the audit artifacts; do not infer a clean security audit.
- Web open PR #1 head 0b3cba81bf2516c3aba97c59df60b1afb4b769ed has conflicts and failed its older CI 35455928652. It is not merged; inspect for unported behavior before closure or rebase.
- Public Desktop release enumeration shows only `desktop-v0.1.0`, published 2026-08-28, release id 378518356. There is no verified published 1.0.0 release and no installation/upgrade acceptance for it.

## Next execution slice: actual installation before signing

1. On the current unsigned Desktop 1.0.0 CI output, run native **installer install → verify installed bundle/executable/sidecar → launch/startup → cleanup** on genuine Windows x64 and both macOS hosted runners, recording OS, exact SHA, installer checksums, executable paths, startup outcome and process logs. Installation tests are separate from unsigned bundle construction.
2. Attempt real basic profile/settings/DB persistence across restart in installed apps and source a data-preserving upgrade rehearsal from the genuine existing 0.1.0 release if compatible; label any mocked/unverified or native-GUI-inaccessible path explicitly rather than a pass.
3. Keep full signed/notarized RC and cryptographically verified auto-upgrade **deferred to public release**; do not publicly tag or publish.
4. Triage dependency audit PR, add native acceptance regressions and complete production/browser/architecture/license acceptance independently.

As of this checkpoint **installed-app acceptance = NOT_YET_VERIFIED**, **signed RC/updater = DEFERRED_TO_PUBLIC_RELEASE**, **release_ready = false**, **public_release_executed = false**. This document is source/CI evidence, not proof that an installation was executed.
