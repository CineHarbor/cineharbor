# CineHarbor Next Actions

Target: **1.0.0 release-ready; do not publicly release**. See `docs/releases/1.0.0/scope.md`. Continue autonomously within the Principal's authorization; do not treat this checklist as completion evidence.

1. Resume from the verified recovery checkpoint and re-resolve current refs. Never apply the old incomplete implementation ZIP over newer repository changes; reconcile the seven-repository source inventory and actual consumers.
2. Inspect Desktop native CI 35441377610 for repaired source 8f5c74dc7c6cbf9e3f115c6c9bd09f315cf12f39, then repair any remaining failures without weakening gates. Reconcile actual current Core/SDK/Web/Worker/site CI; the original Core fmt failure is historical. Confirm every mandatory step executes twice successfully at final revisions.
3. Finish ADR-0006 content-data-plane retirement without capability loss; classify retained control/release APIs and remove only confirmed unused legacy implementations.
4. Execute Web browser acceptance, persistence, PWA/update/error cases, addon compatibility and media authentication tests.
5. Finish Desktop multi-platform RC packaging and a real signed old-to-new upgrade preserving user data. This is a 1.0.0 blocker, not a deferred migration item.
6. Verify production Worker/addon/media services and download-site deployment; record unavailable credentials/identity/platform access as explicit EXTERNAL_BLOCKER without stopping independent work.
7. Complete security/license/brand/dependency review, version alignment, release notes, signed assets and checksums. Record P2 limitations and post-1.0 backlog; no P0/P1 may remain.
8. Reconcile and publish final evidence-bound Agnir checkpoints for all repositories, verify destination refs, then fresh-resolve each selected lineage. Set release-ready only when every gate is observed passing at the final revisions.

Source-inventory success, historical milestone checkmarks, prepared configuration and mocked tests do not substitute for release acceptance. The only action left after genuine acceptance should be final public publication plus post-release monitoring/backlog.
