# CineHarbor Current State

`CineHarbor/cineharbor` is the organization facade: release scope, project plans, architecture decisions and brand history. Product code lives in six specialized repositories; the release unit contains seven repositories including this one.

## Current objective — 2026-09-19

Autonomously execute the Principal's Release-Ready 100% plan for version **1.0.0**, without performing final public release. Canonical current scope and gate rules: `docs/releases/1.0.0/scope.md`; machine-readable observed status: `docs/releases/1.0.0/status.json`.

**RELEASE_READY = false. PUBLIC_RELEASE_EXECUTED = false.** Historical P0–P6 migration milestones are not evidence of release acceptance.

## Architecture

ADR-0006 supersedes the ADR-0005 native-RPC/dual-surface content-data-plane target: pure core is compiled native/WASM and consumed in process; remote addons provide content discovery and media services over Stremio-compatible HTTP. Web must not require a native local-service daemon for its main content path. Control/application-plane and release-plane endpoints may remain with explicit ownership and authentication boundaries. Remaining duplicate content implementations require consumer audit before deletion; adoption of an ADR is not proof of its full implementation.

Prior durable records report completed Web cutovers for Douban search, Bangumi calendar, rich VOD search consumers and VOD media proxy. Their current implementations and runtime acceptance are being verified, not recertified by this checkpoint. Douban recommends/categories and image/logo/media helper routes must be classified explicitly.

## Observed baseline

- Core main `05989fb6f2fe388d8eaeb4128445ac4c61662f5a`, Actions run `35382333866`: formatting failed, including sibling SDK sources; check/test/clippy did not execute.
- Existing release documents contain stale native-RPC and developer-local-path descriptions; reconciliation is in progress.
- Real Desktop updater acceptance is mandatory for 1.0.0; the historical deferral only applied to Web migration.
- `Release source audit` collects tracked source snapshots and immutable revisions for diagnosis. Its success is not a release acceptance result.

## Durable continuity

Project identity `urn:cineharbor:project:cineharbor`; lineage `urn:cineharbor:lineage:cineharbor`. Core/Profile remain `1.0` / `repository-filesystem/1.0`. Agnir operations provenance remains `iorLab/agnir` v1.0.2, immutable revision `b5626394ec40a5cb7a28c01892acde07cc0adc8e`. Activation remains `AGENTS.md → AGNIR.md → AGNIR.yaml`. No Agnir migration or identity change is part of this release work.

License baseline: CC BY-NC-SA 4.0; final release inventory still requires verification. Historical architectural and operational decisions remain in `.agnir/decisions.md`.
