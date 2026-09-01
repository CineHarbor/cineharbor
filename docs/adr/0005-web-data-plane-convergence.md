# ADR-0005 Web 数据面归一：终态收敛到 Rust local-service

- 状态：已采纳（第 2、3、5 条数据面机制被 [ADR-0006](./0006-stremio-faithful-core-wasm.md) 取代；第 1、4 条仍有效）
- 日期：2026-08-31
- 决策者：Matt（Principal）

## 背景

ADR-0004 在 P4 迁入期为「不回归产品能力」保留 Web 继续走原生 `/api`，把「逐页切 `/addons`」标为长尾跟进、非门禁。复盘现状（2026-08-31）：

- addon 传输层（`addon-client.ts` 的 catalog/meta/streams）仅被自身测试引用，「切面长尾」进度 ≈ 0；
- Web 仍是全栈 monolith（~50 原生 `/api` 路由 + web 侧 TS download/live/douban/proxy/profile-sync/server 模块）；
- 与 Rust local-service 形成并行实现（download/live/vod/douban/proxy/profile-sync 两套），`cineharbor-core` 门面仅 13 行、未长成 stremio-core 等价物；
- 近期新特性（评分聚合等）持续落在 web 原生面，深化分叉。

半迁移态每维持一轮，切面成本就上升一轮。

## 决策

1. **Web 终态 = 薄客户端**：只保留渲染/交互与本地缓存/传输层，不自建后端业务逻辑。
2. **唯一数据面 = Rust local-service**：搜索/详情/播放/直播/下载/档案同步/评分等数据访问统一走后端 local-service；`/addons` 是其中的 Stremio 兼容子集，服务双向互操作与通用薄客户端。
3. **web 原生 `/api` 与纯 TS 后端模块按切面退役**：`server`/`download`/`profile-sync`/`live`/`douban`/`proxy` 等逐批移除；admin 控制面的归属另行定（候选：保留 web 侧或迁 local-service）。
4. 取代 ADR-0004 的第 2、3 条（「保持走原生 `/api`」「逐页切列长尾」）；ADR-0004 的「迁入判据」与「addon 协议纯契约」结论仍有效。
5. `cineharbor-core` 门面在切面过程中收 `content_search` / `content_detail` 等公共模型，逐步长成 stremio-core 等价物。

## 已定：富模型双表面暴露（2026-08-31 续）

采纳候选 A：local-service 并存两表面——

- **Stremio `/addons` 子集**（manifest/catalog/meta/streams）：服务双向互操作与通用薄客户端，保持纯契约语义。
- **富模型 native RPC**（「来源 + 剧集 + 逐集 + 直播 + 评分」）：服务 web 薄客户端的完整产品能力，不接受降级。

两者共用同一 Rust 核心（`content_search`/`content_detail` 等），由切面逐步把 web 原生 `/api` 对应能力迁入。

## 后果

- 优：消灭双实现；单一数据面可测可运维；web/desktop 同源。
- 劣：切面是跨仓、跨语言迁移，须分页小步 + 回归门禁；admin 面可能长期保留 web 侧，成为「非薄客户端」特区，需单独标注边界。