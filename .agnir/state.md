# CineHarbor Current State

`CineHarbor/cineharbor` 是组织门面仓：存放整体计划、架构决策（ADR）、品牌史；代码分散在各专业化仓库。

- 架构：三层对标 Stremio —— Rust 核心 + 各端客户端 + Stremio 兼容 addon 协议。
- 仓库拓扑：`cineharbor-core`、`cineharbor-addon-sdk`、`cineharbor-web`、`cineharbor-desktop`、`cineharbor-worker`、`cineharbor-download-site`（六仓，见 README 表格）。
- 依赖图：`cineharbor-addon-sdk` → `cineharbor-core`（local-service 作 addon host）；`cineharbor-desktop` 嵌入 local-service 并链 core；`cineharbor-web` 经 local-service HTTP/RPC；worker、download-site 独立。
- 开发约定：`cineharbor-core` 与 `cineharbor-addon-sdk` 推送走 `github.com-matt` SSH 别名；其余走 HTTPS + gh 凭据助手。
- 文档：`docs/PLAN.md`（P0–P6 批准决策与分阶段计划）、`docs/adr/`、`docs/brand/`、`docs/plans/README.md`。
- 协议：内容源 addon 跟随 Stremio addon 协议，契约在 `cineharbor-addon-sdk` 仓 `protocol.md`。
- 许可证：CC BY-NC-SA 4.0（继承上游公开授权）。
- Agnir：7 仓各自运行 `repository-filesystem/1.0` durable continuity（identity `urn:cineharbor:project:*`，lineage `urn:cineharbor:lineage:*`）。
- Agnir 操作基线：`iorLab/agnir` 稳定发布 `v1.0.0`（revision `6d16dcfd17b8e9f22fd25804e22b9f8a516d06c3`，distribution `agnir-agent-skill`）；2026-09-01 经 Principal 授权完成兼容线迁移 Core `0.1` → `1.0`（经 0.2 lineage 迁移 + 稳定晋升）。
- 数据面终态（ADR-0006，2026-08-31，取代 ADR-0005 数据面机制）：core = 纯状态机，native + WASM 双编译（web 跑 Web Worker）；抓取/媒体代理外置为 remote addon（Stremio 协议）；web 薄客户端 = WASM core + Service Worker + addon HTTP。分阶段方案见 `docs/plans/stremio-faithful-cutover-plan.md`。
- P4 退役剩余切面已于 2026-09-12 拍板并落地：豆瓣搜索、bangumi 日历、点播搜索富消费方、vod 媒体代理（广告过滤+token 鉴权）均切 addon；对应原生 `/api/douban/search`、`/api/bangumi/calendar`、`/api/search*`、`/api/proxy/vod/*` 已删。logo/image-proxy 与 douban recommends/categories 仍留 web。桌面 updater 首次验证后置。详见 `.agnir/decisions.md`。
