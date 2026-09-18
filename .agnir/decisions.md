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

## 2026-09-01 — Agnir 兼容线迁移到 1.0（Principal 授权）

- 按已发布契约 `CORE_0_1_TO_0_2_MIGRATION` + `CORE_0_2_TO_1_0_PROMOTION` 组合执行：0.1 → 0.2（隐式连续线显式化为初始 lineage）→ 0.2 → 1.0（语义保持晋升）。
- 授权与目标：Principal 明确选择迁移到最新稳定版 `v1.0.0`（iorLab/agnir tag `v1.0.0`，revision `6d16dcfd17b8e9f22fd25804e22b9f8a516d06c3`）。
- 兼容线声明改为 Core `1.0` / `repository-filesystem/1.0`；新增 `continuity.lineage: "urn:cineharbor:lineage:cineharbor"`（0.1 唯一隐式连续线的显式初始 lineage）。
- 保留：`project.identity`、memory locators 与 durable memory 内容、policy、`agnir/repository` 扩展、README/`AGENTS.md` 无关内容。

## 2026-09-12 — P4 退役剩余切面拍板（Principal）

收口 `docs/plans/web-api-retirement-plan.md` 决策点 2/3/5 与 bangumi/updater 待定。不接受能力降级；能补进 addon 的先补再删原生面。

1. **点播搜索富消费方**（web `/api/search*`；桌面共用同一 UI）：先把播放选源预取排序、成人过滤、下载页搜索、输入联想迁进 `cineharbor-addon-vod`，parity 齐再删 `/api/search*`。主搜索页已走 addon，保持。不现在删、不接受选源/过滤/下载搜索降级。
2. **下载媒体代理**：`cineharbor-media` / vod addon `/media/vod/*` 先补广告过滤（`filterM3U8` 对等）+ 鉴权，再转正 `USE_ADDON_MEDIA_PROXY` 并删 `/api/proxy/vod/*`。不接受无鉴权开放代理。`logo` / `image-proxy` / `m3u8-filter` / `m3u8-asset` 暂留 web 原生。
3. **豆瓣页**：搜索现在 cutover 到 `cineharbor-addon-douban`（catalog + `MetaPreview.rating` 已有跨源 E2E）。`recommends` / `categories` 暂留 `/api/douban/*`。
4. **首页番剧日历**：接到已有 `cineharbor-addon-bangumi`（catalog 或小扩展），保留首页日历。不删 `/api/bangumi/calendar` 直到 addon 接线完成。
5. **桌面 updater**：主线继续阶段 4。首次在线升级闭环后置，等要发桌面版时再验。不挡 web 退役。

## 2026-09-19 — Agnir 兼容操作升级到 v1.0.2

- 目标：已发布稳定版 `v1.0.2`（source `iorLab/agnir`，immutable revision `b5626394ec40a5cb7a28c01892acde07cc0adc8e`）。
- 分类：compatible operational upgrade；Core/Profile 仍为 `1.0` / `repository-filesystem/1.0`，保留 `project.identity`、`continuity.lineage`、memory locators/content、policy 与无关 Project 内容。
- 激活 packaging：新增 canonical 根 `AGNIR.md`；`AGENTS.md` 改为直达 `AGNIR.md` 的 locator；README `## Agnir Project Instructions` 收敛为兼容 locator。
- provenance：`AGNIR.yaml > extensions > agnir/operations` 更新为 release `1.0.2` / applied revision `b5626394ec40a5cb7a28c01892acde07cc0adc8e`。
