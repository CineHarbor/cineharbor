# CineHarbor

> 🎬 多源汇流、自由播放的跨平台影视聚合播放器生态 —— 对标 Stremio 的三层架构：Rust 核心 + 各端客户端 + Stremio 兼容 addon 协议。

本仓是组织的**门面仓**（`CineHarbor/cineharbor`）：存放整体计划、架构决策（ADR）、品牌史，代码分散在各专业化仓库。

## 仓库拓扑

| 仓库 | 职责 | 对应 Stremio |
| --- | --- | --- |
| [cineharbor-core](https://github.com/CineHarbor/cineharbor-core) | Rust 核心（终态：纯状态机，native + WASM）；storage/sync/profile/download + addon host + core 门面 | `stremio-core` |
| [cineharbor-addon-sdk](https://github.com/CineHarbor/cineharbor-addon-sdk) | addon 协议 + SDK + 参考 addon（bangumi/live），+ 协议契约 protocol.md | `stremio-addon-sdk` |
| [cineharbor-web](https://github.com/CineHarbor/cineharbor-web) | Web 客户端（Next.js + PWA） | `stremio-web` |
| [cineharbor-desktop](https://github.com/CineHarbor/cineharbor-desktop) | 桌面客户端（Tauri） | `stremio-shell` |
| [cineharbor-worker](https://github.com/CineHarbor/cineharbor-worker) | 边缘代理（Cloudflare） | — |
| [cineharbor-download-site](https://github.com/CineHarbor/cineharbor-download-site) | 下载/发布站 | — |

> GitHub 链接在 push 后生效，在此之前以本地目录 `/Users/jay/Code/cineharbor-*` 为准。

## 依赖图（终态，ADR-0006）

```
cineharbor-core（纯状态机，native + WASM）◀── 链接/嵌入：desktop、web(WASM)
        └── 经 addon 协议(HTTP) 消费 ──▶ remote addons（抓取/代理，独立部署）

cineharbor-addon-sdk：协议契约 + SDK（client 侧 wasm 友好 / router 服务端）
cineharbor-local-service：过渡期 addon 承载进程（随阶段 2 外置后退化）
cineharbor-worker、cineharbor-download-site：独立
```

> 历史（ADR-0003/0005）：web 曾经 local-service 的 native RPC / `/addons`；ADR-0006 起统一为「core 进程内（native/WASM）+ addon HTTP」，取消跨进程 native RPC。

## 实现进度（ADR-0006，2026-08-31）

- ✅ **core 纯状态机双编译**：`cineharbor-core`（native）+ `cineharbor-core-web`（wasm-bindgen 粘合，浏览器 worker 内运行）。
- ✅ **抓取/媒体代理外置 remote addon**：`douban` / `live`（多源 M3U8）/ `vod`（多源）+ `cineharbor-media` 转链（HLS 重写），CORS 跨源直连。
- ✅ **web 薄客户端底座**：core-worker RPC（四桥 + IndexedDB 存储）+ `CoreAddonClient` + 跨源浏览器端到端 + Service Worker（wasm 固化 + addon 元数据缓存）。
- 🔨 **P4 切面（退役执行中）**：`USE_ADDON_LIVE`/`USE_ADDON_VOD` 已默认转正；`/api/detail` + `/api/live/*` 原生路由**已删**；豆瓣 rating 槽位已加（协议 `MetaPreview.rating` + douban addon 透出）。剩余：`/api/search*`（非 ws）/`/api/proxy/*` 因富消费方（点播源预取排序/下载搜索/转流+logo）待定 + live 页死分支清理 + wasm 重建。
- 进度与退役清单 / 执行手册见 `docs/plans/stremio-faithful-cutover-plan.md`、`docs/plans/web-api-retirement-plan.md`。

## 开发约定

- `cineharbor-core` 与 `cineharbor-addon-sdk` 两仓的推送一律走 `github.com-matt` SSH 别名（`git remote set-url origin git@github.com-matt:CineHarbor/<repo>.git`）；其余仓走 HTTPS + gh 凭据助手。
- 原因：gh OAuth token 缺 `workflow` scope，无法推送含 `.github/workflows/` 的提交；`github.com-matt` SSH 身份为 mattamior（org admin），不受此限。

## 文档

- `docs/PLAN.md` —— 已批准决策与分阶段计划（P0–P6）
- `docs/adr/` —— 架构决策记录
- `docs/brand/cineharbor-process-log.md` —— 品牌过程记录（仅此处保留旧名历史）
- `docs/plans/README.md` —— 开发计划归属与状态索引（每条计划的归属仓 + 实现状态）

## 协议

内容源 addon 完全跟随 [Stremio addon 协议](https://github.com/Stremio/stremio-addon-sdk)，契约在 `cineharbor-addon-sdk` 仓的 `protocol.md`。

## 许可证

CC BY-NC-SA 4.0（继承自上游公开授权；全仓许可元数据已统一，见 `docs/PLAN.md` 开放问题 #1）。

## Agnir Project Instructions

Agnir 的 canonical Project 激活与操作说明位于 [`AGNIR.md`](AGNIR.md)。本节仅作为旧版 Agnir `1.0.0` 激活路径的向后兼容 locator，不复制第二份 procedure。
