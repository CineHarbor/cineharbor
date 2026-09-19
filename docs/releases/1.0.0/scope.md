# CineHarbor 1.0.0 release scope

Status: EXECUTING — not release-ready. Public release is not authorized by this preparation run.

## Authority and acceptance

The Principal authorized autonomous implementation of the Release-Ready 100% plan on 2026-09-19 and explicitly selected 1.0.0. Ordinary implementation, tests, CI repairs, cross-repository changes, commits and pushes do not require additional decisions. This does not authorize lowering release gates or declaring unexecuted checks successful.

The release unit contains seven repositories: CineHarbor/cineharbor, cineharbor-core, cineharbor-addon-sdk, cineharbor-web, cineharbor-desktop, cineharbor-worker and cineharbor-download-site. Every final evidence record must identify its repository and immutable source revision. A new revision invalidates affected previous evidence. All main-branch gates must execute successfully twice; missing, skipped, cancelled and unobserved checks are not passes.

## Required scope

- Pure Rust core and native/WASM bridges; Stremio-compatible protocol and SDK; Douban, Bangumi, Live, VOD and media services.
- Web search → detail → streams → playback, Live source/channel switching, Bangumi calendar, Douban, current downloads, favorites/history/settings and persistence, PWA updates and explicit failure UI.
- Desktop macOS arm64, macOS x64 and Windows x64: install, sidecar lifecycle, playback/downloads, diagnostics and real signed old-version → new-version upgrade with user-data preservation.
- Used Worker capabilities, production addon/media paths, release-data export, download-site build/deployment, release automation, signed assets, latest.json and checksums.
- Clean checkout reproducibility, security/dependency/license/brand review, version alignment, release notes and accurate Agnir continuity in every repository.

## Architecture boundary

ADR-0006 defines a single content data plane: in-process core (native/WASM) + remote addon HTTP. Content scraping and principal media proxy implementations belong in the addon/services repository, not Web or pure core. Each remaining Web API must be classified as content-data-plane, control-plane, release-plane or legacy, with owner, purpose, consumer, authentication boundary and deprecation status. The exit criterion is not mechanically zero `/api` routes. Control/application services (accounts, admin, profile orchestration, persistence, ratings aggregation) and release/updater endpoints may remain. Existing unclassified content/proxy endpoints remain migration work, not automatically approved control-plane exceptions.

## Explicit post-1.0 backlog

- Rotten Tomatoes real-data integration until a legally usable, stable source is available; never ship invented ratings or a misleading support claim.
- Expanded music features and follow updates. Existing visible UI must still be safe and coherent; deferral does not excuse a broken advertised path.
- Advanced Background Fetch/OPFS/cache experiments; current supported download paths remain required.
- New mobile/TV clients, unbounded addon expansion and nonblocking optimizations.

## Gate rules

P0 = 0 and P1 = 0. P2 must be documented; P3 belongs in the backlog. Mock protocol/UI tests are useful development evidence but do not replace real updater or production-deployment tests. External credentials, signing keys, OS/production access or provider authorization that cannot be obtained safely are recorded as EXTERNAL_BLOCKER; independent work continues. Never generate a replacement signing identity silently, disclose secrets, or publish a public release to make a gate appear complete.

The previous 2026-09-12 decision to defer the updater applied to the Web migration sequence only. It does not waive the 1.0.0 release requirement.

Final state may be set only after all required evidence is present:

```
CINEHARBOR_RELEASE_READY = true
PUBLIC_RELEASE_EXECUTED = false
```

Until then both values are false. Preparing this document or collecting sources does not satisfy any build, security, runtime or deployment gate.
