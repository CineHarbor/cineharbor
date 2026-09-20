# CineHarbor Next Actions

Target: **1.0.0 release-ready; do not publicly release**. See `docs/releases/1.0.0/scope.md`. Continue autonomously within the Principal's authorization; do not treat this checklist as completion evidence.

1. Resume from `.agnir/evidence/2026-09-20-media-and-native-verification.md`, re-resolve current refs, and preserve newer work. SDK ca2ffa7c and Desktop 1fd69e23 have independently observed two-run CI evidence. Do not reclassify their historical predecessor failures as current blockers.
2. Complete media egress/SSRF/DNS-rebinding/no-open-proxy and Live authorization boundaries, then Range/HEAD and bounded/streaming byte forwarding. The HLS token/redirect/error-redaction repair is merged and tested, not a complete security certification.
3. Reconcile Core/SDK release inputs and owned lock entries; update Web to 1.0.0 and verified dependency pins, then Desktop to the verified Web/Core/SDK unit. Both currently retain 0.1.0 package versions and older pins. Execute all affected required gates twice on exact final main revisions.
4. Finish ADR-0006 content-data-plane retirement without capability loss; classify retained control/release APIs and remove only confirmed unused legacy implementations. Execute real Web search/detail/playback, live switching, Bangumi/Douban, downloads, persistence, PWA/update/offline/error and addon compatibility acceptance.
5. Finish Desktop signed multi-platform RC packaging, installed startup/sidecar/playback/download and a real signed old-to-new upgrade preserving user data. Two successful unsigned build matrices do not waive these gates.
6. Verify production Worker/addon/media services and download-site deployment; record unavailable credentials/identity/platform access as explicit EXTERNAL_BLOCKER without stopping independent work.
7. Complete security/license/brand/dependency review, version alignment, release notes, signed assets and checksums. Record P2 limitations and post-1.0 backlog; no P0/P1 may remain.
8. Reconcile final evidence-bound Agnir checkpoints for all seven repositories, verify destination refs and fresh-resolve each selected lineage. Set release-ready only when every required gate has observed evidence at the final revisions.

Source-inventory success, prepared configuration and mocked tests do not substitute for release acceptance. Final public publication remains outside this preparation run.
