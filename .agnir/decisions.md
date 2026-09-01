# Agnir Decisions

## 2026-08-31 — Agnir initialization

- 本仓库以 `CineHarbor/cineharbor` 作为 Project 身份，identity `urn:cineharbor:project:cineharbor`。
- 采用 `repository-filesystem/0.1`，durable memory 落于 `.agnir/`；`AGNIR.yaml` 为 discovery anchor；根 `AGENTS.md` 仅作 locator；README `## Agnir Project Instructions` 为 canonical activation instruction。

## 2026-08-31 — 既有 Project 决策（源自 README）

- 三层架构对标 Stremio，代码分散专业化仓库。
- `cineharbor-core` / `cineharbor-addon-sdk` 推送走 `github.com-matt` SSH 别名（因 gh OAuth token 缺 `workflow` scope）。

## 2026-08-31 — Web 终态收敛（Principal 决策，ADR-0005）

- Web 终态 = 薄客户端；唯一数据面 = Rust local-service；web 原生 `/api` 与纯 TS 后端模块按切面退役（取代 ADR-0004 第 2、3 条）。
- `/addons` 是 local-service 的 Stremio 兼容子集，服务双向互操作与通用薄客户端。
- 富模型暴露方式（2026-08-31 续定）：采纳双表面——Stremio `/addons` 子集（互操作）+ 富模型 native RPC（web 完整能力），同一 Rust 核心，不接受能力降级。

## 2026-08-31 — 终态对齐 Stremio（Principal 决策，ADR-0006）

- 坚持对标 Stremio 到结尾：`cineharbor-core` 拆为纯状态机，native + WASM 双编译；web 在 Web Worker 里跑 WASM core，不再跨进程连 native RPC。
- 抓取（api_sites/douban/live 检索）与媒体代理（m3u8/vod/key/logo/image）从 core 外置为 remote addon（Stremio 协议）独立部署。
- 取代 ADR-0005 第 2、3、5 条（唯一数据面 = local-service 双表面/native RPC，即 2026-08-31 续定的「双表面」）；ADR-0005 第 1、4 条（web 薄客户端、逐切面退役）仍有效。
- 分阶段方案：`docs/plans/stremio-faithful-cutover-plan.md`。

## 2026-09-01 — Agnir 兼容操作升级到 v0.1.0

- 升级已应用的 Agnir 操作包到稳定发布 `v0.1.0`（source `iorLab/agnir`，immutable revision `2a0cb7bf2068b11f361e315670b2f2dc497b2588`）。
- 分类：compatible operational upgrade —— Core 兼容线仍为 `0.1`，profile 仍为 `repository-filesystem/0.1`；`project.identity`、memory locators、durable memory 内容与 `agnir/repository` 扩展均保留。
- 变更：`AGNIR.yaml` 增加 `extensions.agnir/operations` 操作出处；README `## Agnir Project Instructions` 追加 commit-boundary 规则；state.md 记录操作基线；新增升级证据文件。
