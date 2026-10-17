# CineHarbor Next Actions — 2026-10-18 patched release unit

1. Confirm Desktop f961c92a installed sidecar/SQLite native CI twice (39061967719 success; 39064018486 running at checkpoint). Preserve installed checks for all Windows/macOS targets; real GUI user interactions remain unverified.
2. Verify twice-complete SDK 10ce024c and Core dc94a185 already done; finish Web c9f76d1c two main CI runs after passing PR #4; then finish Desktop patched-pin PR #5 de7a099c5 on all native installed lanes, merge and require two full final main runs. No downstream main pin assumptions before merge.
3. Once the source graph and installed CI are stable, hand off genuine installed GUI/manual playback and download tests on user's machine, recording exact artifact SHA, OS, sidecar/playback, settings/login/DB retention, source switching and failures. No false claim of manual GUI acceptance.
4. Independently fix Web Next/Swiper/PostCSS and remaining Desktop dependency audit findings and repeat fresh strict audits. Resolve Web old PR, production addon/media, release-site served proof, ADR legacy routes, license/brand and rollout diagnostics.
5. Official signing/notarization and real signed upgrade deferred by Principal to separate public-release phase; do not publish. RELEASE_READY=false / PUBLIC_RELEASE_EXECUTED=false.
