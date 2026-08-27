# ADR-0002：内容源 addon 协议采用 Stremio 兼容契约

日期：2026-08-27
状态：已接受（实现边界见开放问题）

## 背景

原 LunaTV 的内容源（bangumi / douban / live 等）硬编码在 Web 端 API 路由内，新增源要改 core，不可扩展。目标架构需要把「找源」从「改核心」解耦成 addon 插件生态。

## 决策

`cineharbor-addon-protocol` 实现 **Stremio addon 契约**：`/manifest.json`、`/catalog/<type>/<id>.json`、`/meta/<type>/<id>.json`、`/streams/<type>/<id>.json`。addon 以独立进程/服务暴露 HTTP，由 `cineharbor-local-service` 作 host 聚合。

## 理由

- 直接复用现成公开 addon 生态，内容源从第一天就丰富；自建封闭协议无此红利。
- 契约被大量客户端验证过，字段语义稳定。
- 与「对标 Stremio」的总体方向一致。

## 影响与开放问题

- 兼容范围待定：只求「协议互操」（能装 Stremio addon），还是 addon 反向兼容 Stremio 客户端。二者 SDK 与校验严格度不同，P2 开工前冻结。
- Web/worker 的既有源适配逻辑需重写为 addon 形态（P2 一并完成 bangumi/douban/live 三个参考 addon）。
