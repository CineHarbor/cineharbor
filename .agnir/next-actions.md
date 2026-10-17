# CineHarbor Next Actions — 2026-10-18

1. Desktop real installation main 40e073df is twice verified (39059537440/39061854359). Finish inspecting deeper installed sidecar /health, config and SQLite persistence on Desktop f961c92a new main run 39061967719, then repeat complete final main CI twice; repair any native failure.
2. SDK rustls 0.23.45 (10ce024c9) and Core patched SDK lock (dc94a185) are each merged and twice CI-verified. Next update Web then Desktop immutable dependency pins to the verified source graph; execute fresh browser/native/installed matrices twice.
3. Remediate Web Next/Swiper/PostCSS and Desktop rustls vulnerabilities without suppressions; run fresh audit across entire current lock graph. Reconcile stale Web PR #1 only after checking parity, and facade audit PR #1 after all findings repaired.
4. Extend automated installed functional login/settings/profile/download/media/sidecar life-cycle, staged deployed addon/media/browser/PWA integration, download-site served link check, ADR consumer inventory, licensing/brand review. Treat external production/site access not granted as a specific manual blocker.
5. Formal signing/notarization and real signed old-to-new updater only at separately authorized public release; no public assets now. RELEASE_READY=false / PUBLIC_RELEASE_EXECUTED=false.
