# ADR-0006 终态对齐 Stremio：core 纯逻辑 WASM 化，抓取/代理外置为 remote addon

- 状态：已采纳
- 日期：2026-08-31
- 决策者：Matt（Principal）

## 背景

ADR-0005 定了「web 薄客户端、唯一数据面 = Rust local-service」，并采纳「双表面」（Stremio `/addons` 子集 + 富模型 native RPC）。进一步对照 Stremio 真实架构后确认：Stremio 的 `stremio-core` 是**纯状态机**，编译为 native（桌面/移动）与 **WASM（web，跑在 Web Worker）**；catalog/meta/streams 全是 **remote addon（HTTP）**；**core 不抓取、不代理媒体**。

CineHarbor 当前 `local-service` 把「抓取」（api_sites/douban/live 检索）与「媒体代理」（m3u8/vod/key/logo/image）都塞进了 core 侧，这偏离 Stremio 职责边界，也是 web 无法自足、必须连常驻 daemon 的根因。经 Principal 决策：**坚持对标 Stremio 到结尾**，采用 Stremio 式终态。

## 决策

1. **`cineharbor-core` 拆为纯状态机库**（对标 `stremio-core`）：内容模型、库/同步、profile、addon 聚合与派发；**不含抓取、不含媒体代理**。
2. **双编译目标**：native（桌面/移动/自托管）+ **WASM（web，Web Worker）**；web 通过 bridge（`getState`/`dispatch` 式）进程内消费，不再跨进程连 native RPC。
3. **抓取与媒体代理从 core 剥离**，作为 **remote addon**（Stremio 协议）独立部署；web 经 addon HTTP 直连消费 catalog/meta/streams，桌面亦然。
4. **web 改薄**：WASM core（Web Worker）+ Service Worker（CORS/缓存/流）+ addon HTTP；原生 `/api` 与 web 侧 TS 后端按切面退役（沿用 ADR-0005 第 1、4 条方向）。
5. 取代 ADR-0005 的第 2、3、5 条「唯一数据面 = local-service 双表面 / native RPC」表述 → 修订为「数据面 = core（进程内，native/WASM）+ remote addon（HTTP）」。

## 分阶段（详情入 `docs/plans/stremio-faithful-cutover-plan.md`）

- 阶段 0：冻结 crate 职责矩阵 + WASM 可行性 probe（编译 wasm 目标、识别 wasm 不友好依赖）。
- 阶段 1：把 local-service 中 core 纯逻辑（模型/聚合/派发/库/同步）抽进 `cineharbor-core`，local-service 退化为 addon 承载进程。
- 阶段 2：抓取/代理各拆为独立 remote addon（独立二进制/服务，Stremio 协议暴露）。
- 阶段 3：core 编译 WASM + web bridge（Web Worker）+ Service Worker，web 前端切 addon 直连。
- 阶段 4：退役 web 原生 `/api` 与 TS 后端；desktop/worker 对齐新 addon 端点；core 门面长成 stremio-core 等价物。

## 后果

- 优：职责边界与 Stremio 对齐；单核心、双目标、进程内数据面；web/desktop 真正同源。
- 劣：抓取/代理外置为服务带来部署与鉴权成本；WASM 承载同步/存储有 IndexedDB 边界；是跨仓大重构，须按阶段设回归门禁。

## 待定

- 抓取 addon 的部署形态（自托管 vs 官方托管）、更新/鉴权策略。
- WASM 侧的同步/本地存储边界（IndexedDB/OPFS），与 native 侧 sqlite 的对齐策略。