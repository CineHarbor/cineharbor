# Agnir Decisions

## 2026-08-31 — Agnir initialization

- 本仓库以 `CineHarbor/cineharbor` 作为 Project 身份，identity `urn:cineharbor:project:cineharbor`。
- 采用 `repository-filesystem/0.1`，durable memory 落于 `.agnir/`；`AGNIR.yaml` 为 discovery anchor；根 `AGENTS.md` 仅作 locator；README `## Agnir Project Instructions` 为 canonical activation instruction。

## 2026-08-31 — 既有 Project 决策（源自 README）

- 三层架构对标 Stremio，代码分散专业化仓库。
- `cineharbor-core` / `cineharbor-addon-sdk` 推送走 `github.com-matt` SSH 别名（因 gh OAuth token 缺 `workflow` scope）。
