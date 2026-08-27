# ADR-0002：内容源 addon 协议完全跟随 Stremio 协议（双向互操）

日期：2026-08-27
状态：已接受

## 背景

原项目的内容源（bangumi / douban / live 等）硬编码在 Web 端 API 路由内，新增源要改 core，不可扩展。目标架构需要把「找源」从「改核心」解耦为 addon 插件生态。

## 决策

`cineharbor-addon-protocol` **完全跟随 Stremio addon 协议**，不做自有封闭协议：

- 端点、资源类型、JSON 字段与官方契约逐项对齐，权威来源：
  - SDK 仓库：https://github.com/Stremio/stremio-addon-sdk
  - 协议参考：https://stremio.github.io/stremio-addon-sdk/protocol.html
- **双向互操**：
  - 消费侧：`cineharbor-local-service` 作为 addon host，能加载并聚合任意 Stremio 兼容 addon；
  - 供给侧：我们的参考 addon（bangumi / douban / live）按同一契约实现，可被 Stremio 官方客户端直接加载。
- 契约冻结于 `cineharbor-addon-sdk` 仓库的 [protocol.md](../../cineharbor-addon-sdk/protocol.md)。

## 理由

- 直接复用现成公开 addon 生态，内容源从第一天就丰富；自建封闭协议无此红利。
- 契约已被大量客户端验证，字段语义稳定。
- 与「对标 Stremio」的总体方向一致；用户明确「Stremio 用什么协议我们就用什么」。

## 影响

- 官方 SDK 为 Node.js；我们用 Rust 重实现同契约（`cineharbor-addon-sdk`），字段/端点严格对齐。
- 不扩展私有字段：自有扩展一律进 `behaviorHints`，保证与 Stremio 客户端不冲突。
- Web/worker 的既有源适配逻辑改为 addon 形态（P2 完成 bangumi/douban/live 三个参考 addon）。
