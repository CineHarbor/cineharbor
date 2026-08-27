# CineHarbor

> 🎬 多源汇流、自由播放的跨平台影视聚合播放器生态 —— 对标 Stremio 的三层架构：Rust 核心 + 各端客户端 + Stremio 兼容 addon 协议。

本仓是组织的**门面仓**（`CineHarbor/cineharbor`）：存放整体计划、架构决策（ADR）、品牌史，代码分散在各专业化仓库。

## 仓库拓扑

| 仓库 | 职责 | 对应 Stremio |
| --- | --- | --- |
| [cineharbor-core](https://github.com/CineHarbor/cineharbor-core) | Rust 核心：storage/sync/profile/download + local-service + core 门面 | `stremio-core` |
| [cineharbor-addon-sdk](https://github.com/CineHarbor/cineharbor-addon-sdk) | addon 协议 + SDK + 参考 addon（bangumi/live），+ 协议契约 protocol.md | `stremio-addon-sdk` |
| [cineharbor-web](https://github.com/CineHarbor/cineharbor-web) | Web 客户端（Next.js + PWA） | `stremio-web` |
| [cineharbor-desktop](https://github.com/CineHarbor/cineharbor-desktop) | 桌面客户端（Tauri） | `stremio-shell` |
| [cineharbor-worker](https://github.com/CineHarbor/cineharbor-worker) | 边缘代理（Cloudflare） | — |
| [cineharbor-download-site](https://github.com/CineHarbor/cineharbor-download-site) | 下载/发布站 | — |

> GitHub 链接在 push 后生效，在此之前以本地目录 `/Users/jay/Code/cineharbor-*` 为准。

## 依赖图

```
cineharbor-addon-sdk ──▶ cineharbor-core（local-service 作 addon host）
                              ▲
                              └── cineharbor-desktop（嵌入 local-service、链 core 库）
cineharbor-web ──HTTP/RPC──▶ cineharbor-core/local-service
cineharbor-worker、cineharbor-download-site：独立
```

## 开发约定

- `cineharbor-core` 与 `cineharbor-addon-sdk` 两仓的推送一律走 `github.com-matt` SSH 别名（`git remote set-url origin git@github.com-matt:CineHarbor/<repo>.git`）；其余仓走 HTTPS + gh 凭据助手。
- 原因：gh OAuth token 缺 `workflow` scope，无法推送含 `.github/workflows/` 的提交；`github.com-matt` SSH 身份为 mattamior（org admin），不受此限。

## 文档

- `docs/PLAN.md` —— 已批准决策与分阶段计划（P0–P6）
- `docs/adr/` —— 架构决策记录
- `docs/brand/cineharbor-process-log.md` —— 品牌过程记录（仅此处保留旧名历史）
- `docs/plans/` —— 从旧项目迁入的开发计划，随工作落地归属到对应仓库

## 协议

内容源 addon 完全跟随 [Stremio addon 协议](https://github.com/Stremio/stremio-addon-sdk)，契约在 `cineharbor-addon-sdk` 仓的 `protocol.md`。

## 许可证

CC BY-NC-SA 4.0（继承自上游公开授权；许可元数据问题见 `docs/PLAN.md` 开放问题）。
