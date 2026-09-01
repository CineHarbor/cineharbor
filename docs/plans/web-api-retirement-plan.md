# Web 原生 /api 与 TS 后端退役方案（P4，逐切面 strangler）

> 本文是 ADR-0006 终态在 web 侧的收尾执行蓝图。落地前置：抓取/媒体代理 standalone addon 与
> WASM 薄客户端底座均已就绪并经浏览器实测（worker + 四桥 + 存储 + CORS）。本方案逐「切面」
> 把页面从原生 `/api` 切到 addon 直连，再删对应 TS 后端。

## 现状（已核实的 seam）

- 数据面**两条**（ADR-0004）：既有页面走原生 `/api`（rich model `SearchResult`：聚合多视频源 +
  剧集流）；新客户端走 worker 直连 `CoreAddonClient`（`addon-types.ts` 承载协议 DTO）。local-service
  `/addons` 聚合客户端（`addon-client.ts`）**已于 2026-08-31 退役**（零页面消费，删除 + 协议类型迁 `addon-types.ts`）。
- content 服务 seam：`src/lib/core/content/service.ts` → `@/lib/downstream`
  `searchFromApi/getDetailFromApi`（**服务端直抓**视频源，正是要外置的部分）。
- 原生路由组（`src/app/api/*`）：`search|search/ws|search/one|search/suggestions|search/resources`、
  `detail`、`live/sources|channels|epg|precheck`、`douban/search|ratings|recommends|categories`、
  `proxy/m3u8|segment|key|vod/*|logo`、`image-proxy`、`favorites/follows/playrecords/searchhistory`、
  `admin/*`、`profile-sync/*`、`server-config`、`desktop/*`、`cron`、`login/logout/change-password`。

## 终态映射与 parity 缺口

| 原生 `/api` 组 | 终态载体 | parity 现状 | 主要缺口 |
| --- | --- | --- | --- |
| `proxy/*`、`image-proxy` | vod/live addon 的 `/media/*` | ◐ live 代理已删（进度 30）；**vod 代理 E2E 已证**（进度 31，`vod-media-proxy-smoke`） | **`proxy/vod/{m3u8,segment,key}` 三路由带原生专属 ad-filter（`filterM3U8`）+ auth（`requireAuthContextFromRequest`）+ desktop-dev-proxy，addon `/media/vod/*` 均无（裸代理 + CORS 开放）**；`logo`/`image-proxy`/`m3u8-filter`/`m3u8-asset` 亦无 addon 对等 |
| `live/*` | `cineharbor-addon-live` | ✅ **已退役**（`/api/live/{sources,channels,epg,precheck}` 已删，`USE_ADDON_LIVE` 默认转正） | 降级：无 precheck/EPG、logo 暂走原生 `/api/proxy/logo` |
| `search\|detail` | `cineharbor-addon-vod` | ◐ **详情已退役**（`/api/detail` 已删，`fetchContentDetail` 恒 addon）；**搜索保留** | 搜索富消费方（`playback-source-prefetch` / `DownloadsClient`）未 addon 化——删 `/api/search` 会断多源选源/下载搜索 |
| `douban/*` | `cineharbor-addon-douban` | ✅ 搜索 catalog + **rating 槽位（A）**（协议 `MetaPreview.rating` + douban addon 透出评分，`douban-cross-origin-smoke` E2E 验证 `rating=9.4`） | 搜索页 cutover + recommends/categories 外沿 |
| `favorites/follows/playrecords/searchhistory` | WASM core（pure）+ worker IndexedDB | ✅ Storage seam 已通 | core 侧补 domain 模型 + 桥 |
| `profile-sync/*` | core `sync`（已入纯模型） | ✅ 模型已入 core | local-service 消费 + 退役 TS 版 |
| `admin/*`、`cron`、`desktop/*`、鉴权 | desktop/local-service 对齐 | 未开始 | 纳入 desktop 对齐，最后退役 |

## 切面顺序（strangler，先重后轻、先代理后内容）

1. **媒体代理**（零 UI 语义变化，最安全先切）：`MEDIA_PROXY_BASE_URL` 指向 vod/live addon；观察对齐后删 `/api/proxy/*` + `image-proxy`。
2. **直播**：live addon 补 M3U parity → `live/page` 走 `CoreAddonClient.catalog('tv','channels')` + `streams('tv','live:{i}')` → 删 `/api/live/*`。
3. **点播搜索/详情**：vod addon 补多源 parity → `content/service.ts` 改走 `CoreAddonClient` + `catalog-bridge`（meta→`SearchResult` 骨架 + streams 另填剧集）→ 删 `/api/search|detail`。
4. **豆瓣**：douban addon 补 parity → 删 `/api/douban/*`。
5. **账户/收藏/历史**：core 补 domain → worker IndexedDB → 删对应 `/api`。
6. **鉴权/admin/cron/desktop updater**：desktop/local-service 对齐后退役。

## shape-bridge（已落地，两步映射完整）

- `src/lib/core/content/catalog-bridge.ts`：Stremio `meta` → rich `SearchResult` **骨架**（`episodes` 恒空）。
- `src/lib/core/content/streams-bridge.ts`：`Stream[]` → `episodes/episodes_titles` + `buildDetail`（合成
  完整 `SearchResult`）——Stremio 分离 meta/streams 的两步映射已完整（jest 3 绿）。

## 决策点（截至 2026-08-31 收敛）

1. **live 交互验证**：✅ 已执行（Matt「直接删」授权）——`USE_ADDON_LIVE` 默认转正 + `/api/live/*` 已删。
2. **点播富模型映射**：◐ 详情已退役（`/api/detail` 删）；**搜索留待 Matt 定富消费方取舍**（`playback-source-prefetch`
   多源选源排序 + 成人过滤、`DownloadsClient` 下载搜索、`fetchContentSuggestions` 建议均无 addon 对等）。
3. **豆瓣 ratings**：✅ 已定 A——协议加 `MetaPreview.rating` 通用评分槽（与 `imdb_rating` 并列），douban addon 已透出
   （`9.4`）。剩搜索页 cutover + recommends/categories 外沿。
4. **账户/收藏/历史 + 鉴权/admin/cron**：属「非抓取/媒体代理」范围，不在本目标退役（账户持久化已
   worker IndexedDB 直存对齐，鉴权/admin/cron/desktop 留 desktop 对齐）。
5. **下载媒体代理**（进度 49 核实）：`/api/proxy/vod/{m3u8,segment,key}` 三路由除转链外还带原生专属
   `filterM3U8`（广告过滤）、`requireAuthContextFromRequest`（会话鉴权）、`proxyDesktopDevVodRequest`
   （desktop dev）。addon `/media/vod/*` 是裸代理（无 ad-filter/auth，CORS 开放）。切换 = 下载侧丢广告过滤 +
   鉴权；需 Matt 定：addon `/media/vod/*` 补 ad-filter+auth，还是接受下载侧降级。`logo`/`image-proxy`/
   `m3u8-filter`/`m3u8-asset` 同理无 addon 对等，需「新端点 vs 接受损失」定夺。

## 切换/退役执行手册（可逆，Matt 确认后逐条执行）

前置：live/vod 两切面已 flag-wired（默认 off）+ 双真实 cross-origin E2E 通过（进度 26）。

### 第一步：切换（flip flag，默认 off → on，可独立回滚）

1. live：`NEXT_PUBLIC_USE_ADDON_LIVE=true` + `NEXT_PUBLIC_LIVE_ADDON_URL` 指 live addon；`pnpm dev`
   验证源/频道/播放/换台。
2. vod：`NEXT_PUBLIC_USE_ADDON_VOD=true` + `NEXT_PUBLIC_VOD_ADDON_URL` 指 vod addon；验证搜索→详情→播放。
3. 媒体代理：`MEDIA_PROXY_BASE_URL` 指向 vod/live addon（下载/logo 外沿）。

### 第二步：退役（switch 验证稳定后逐条删 + 回归）

1. `/api/live/sources|channels|epg|precheck`（接受无 EPG/precheck 降级后）。
2. `/api/search*`（非 ws）+ `/api/detail` + `content/service.ts` 抓取分支 + `downstream.ts`
   `searchFromApi/getDetailFromApi`（点播切走后）。
3. `/api/proxy/m3u8|segment|key` + `/api/image-proxy`（媒体代理全量 addon 化后）。

### 回滚

任一 flag 回 false 即回原生（strangler 默认 off，零数据迁移、零破坏）；路由删除在独立分支，可 revert。

### 未纳入本目标

- `/api/douban/*`：待 #3 定稿后单列。
- `favorites/follows/playrecords/searchhistory` + `profile-sync/*` + `admin/cron/desktop/鉴权`：
  不属「抓取/媒体代理外置」，留 desktop 对齐（账户持久化已 worker IndexedDB 直存）。

## 每条切面的验收门

- Rust：`cargo test`（addon parity 契约）+ `cargo check --workspace`；真实 addon smoke（curl header/json）。
- TS：`pnpm jest`（bridge/seam 单测）+ `pnpm typecheck` 全仓。
- 集成：`scripts/wasm-cdp-smoke.mjs`（headless Chrome，worker 直连真实 addon，需 addon 就绪）；
  `next dev` 实测对应页面仍可用，再删旧 `/api`。
- 删除路由逐条进行，每删一条跑一次相关页面回归；无空 catch、密钥走 env。