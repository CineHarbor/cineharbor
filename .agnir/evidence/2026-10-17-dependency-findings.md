# Immutable dependency-audit findings triage — inspected 2026-10-17

Source: **CineHarbor/cineharbor PR #1**, failed workflow run [35511058147](https://github.com/CineHarbor/cineharbor/actions/runs/35511058147) (executed 2026-09-20). Reviewed original uploaded report archives; do not mistake the wrapper `FINDINGS_OR_ERROR` status for absence of actionable advisories. This review is a historical snapshot of its recorded advisory DB and source locks, not a fresh 2026-10-17 audit.

## Web Node lock

Revision `97cf1bf55033ed16a2f0f77a97c28848aa323956`, lock SHA256 `4800ac568de6208f6e88085a79699840b21e20805e43a6ed4fae6c49eff55d4e`. `pnpm install --frozen-lockfile --ignore-scripts` and license inventory succeeded; `pnpm audit --json` returned 1 with exactly **32 advisories: 3 critical, 13 high, 13 moderate, 3 low**.

Highest-priority affected dependency paths include `next` 14.x (two CRITICAL 2026 advisories, including Windows-hosted-server RCE and AVIF image-optimizer RCE) and `swiper` 11.x (one CRITICAL prototype pollution advisory). Additional listed high/severe entries include `postcss`, `glob`, `serialize-javascript` and `semver`. The recorded patched Next threshold for CVE-2026-75604 is `15.5.24`; Swiper advisory CVE-2026-27212 lists `>=12.1.2`. Upgrades may be major-version and require migration tests, not blind lock rewrites. A Windows-hosted-server advisory is not automatically exploitable in every deployment; risk must be evaluated for actual entry points, alongside other advisories.

The reports are exact audit lock findings; no severity suppression or unsafe automatic patching was applied. License inventory was collected, **not legally approved**.

## Rust locks

All three repos with independent locks contain **rustls 0.23.43**, affected by **RUSTSEC-2026-0285** (TLS 1.3 encryption-level boundary). The RustSec advisory states first patched version `0.23.45`: https://rustsec.org/advisories/RUSTSEC-2026-0285.html. The 2026-09-20 captured database SHA was `d5c17953a895cf19e8d3ce66eaa42b6fcfe1fb16`.

- SDK `3ab4ff8fcc38a6f0849389a7c6b66291f3ca341d`, lock SHA256 `85b86decc5fa80929dbdf374e24116b0c6a55c7231a8877a4a8702329115685e`: 1 rustls vulnerability.
- Core `246411ba6c72b5b79b6e14598228c62a16857309`, lock SHA256 `50da38274490afdc2a0278e19865143af77b55b280e293c1decbe3345883d1ab`: 1 rustls vulnerability.
- Desktop `39d885531144636487bad37af497373ca4ca6a78`, lock SHA256 `0ef778cdd8cad05eb4504a31ab13a4c778c7b1d44ff9`: 1 rustls vulnerability, plus **6 unmaintained advisories** from proc-macro-error/unic packages and **1 unsoundness warning** in glib 0.18.5 (`RUSTSEC-2024-0429`). Its warning count is not the same as additional six confirmed exploitable vulnerabilities.

## Remediation order after installed-gate smoke

1. Do not weaken real native install/startup acceptance just to get audit green; first capture the CI-installed result. In parallel prepare dependency compatibility evaluation.
2. Update rustls resolution to patched version in each independently maintained Rust lock, run all locked all-target gates, then repin downstream immutable SHAs in dependency order. Do not manually edit a lock checksum or suppress advisories.
3. Upgrade Next and Swiper with a real Web functionality/API migration and repeat full Jest + browser + WASM/build gates; review other high advisories and reach audited lock closure. The exact original findings remain as forensic evidence.
4. Re-run fresh dependency audits to include advisories published since the 2026-09-20 snapshot and classify unmaintained/unsound dependencies; finish license review. Keep the failed audit PR open or revise it; never misreport it as green.

**Status: actionable findings; remediation not yet merged.** No published 1.0.0 release and no full installed acceptance as of this audit triage.
