# ADR-0004 addon 前端切换边界：/addons 先服务互操作，不强行改写既有 UI

- 状态：已采纳
- 日期：2025-08-28（项目内相对）
- 决策者：CineHarbor（单维护者）

## 背景

P3 起 local-service 变为 Stremio 兼容 addon host，`/addons` 聚合端点已提供
`manifest/catalog/meta/stream`；P4 迁入的旧 Next.js 客户端自带一套**以「来源 + 剧集」为核心的**
富数据模型（`/api/search` 返回 `source/source_name/episodes/episodes_titles`，按站点分组、
可选源、逐集点播）。两者数据模型不对齐：

- addon `MetaPreview` 只有 `id/name/poster/year/description`，没有「来源分组」与「逐集」；
- 播放流要按条目再调 `/addons/stream/…`，而旧 UI 在搜索结果里已内联每集的播放地址。

## 决策

1. P4（Web 客户端**迁入**）的完成判据是「迁入 + 清品牌 + 可构建起服务」，已达成；
   迁入同步交付了 addon **传输层**（`src/lib/transport/addon-client.ts`）与
   local-service 的三个内置 addon（live/douban/vod）。
2. **既有 Web 的前端数据流保持走原生 `/api`**（来源/剧集富模型），不强行降级到
   addon 的扁平模型，避免回归产品能力；`/addons` 面用于 **Stremio 双向互操作**与
   **新客户端**（桌面壳等）按需消费。
3. 「把既有页面逐页改写为经 `/addons`」列为**长尾跟进**（非阶段门禁），随产品需要推进。

## 后果

- 优：迁入/互操作并行推进，不牺牲既有搜索-点播体验；addon 协议回归 Stremio 纯契约语义。
- 劣：`/addons` 与旧 `/api` 并存，短期存在两条数据通路；需在 README/PLAN 明确边界，
  避免后续把两者混为一谈。