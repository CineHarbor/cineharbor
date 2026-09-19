# CineHarbor Next Actions

Target: **1.0.0 release-ready; do not publicly release**. See `docs/releases/1.0.0/scope.md`. Continue autonomously within the Principal's authorization; do not treat this checklist as completion evidence.

1. Resolve and inventory all seven current main revisions; reconcile per-repository continuity and remaining API/content consumers.
2. Repair and execute all actual CI/build/test gates from clean checkouts. Core baseline formatting fails before check/test/clippy. Confirm every mandatory step executed and obtain two successful main runs.
3. Finish ADR-0006 content-data-plane retirement without capability loss; classify retained control/release APIs and remove only confirmed unused legacy implementations.
4. Execute Web browser acceptance, persistence, PWA/update/error cases, addon compatibility and media authentication tests.
5. Finish Desktop multi-platform RC packaging and a real signed old-to-new upgrade preserving user data. This is a 1.0.0 blocker, not a deferred migration item.
6. Verify production Worker/addon/media services and download-site deployment; record unavailable credentials/identity/platform access as explicit EXTERNAL_BLOCKER without stopping independent work.
7. Complete security/license/brand/dependency review, version alignment, release notes, signed assets and checksums. Record P2 limitations and post-1.0 backlog; no P0/P1 may remain.
8. Reconcile and publish final evidence-bound Agnir checkpoints for all repositories, verify destination refs, then fresh-resolve each selected lineage. Set release-ready only when every gate is observed passing at the final revisions.

Source-inventory success, historical milestone checkmarks, prepared configuration and mocked tests do not substitute for release acceptance. The only action left after genuine acceptance should be final public publication plus post-release monitoring/backlog.
