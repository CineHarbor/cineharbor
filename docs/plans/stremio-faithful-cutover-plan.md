# 终态对齐 Stremio：core 纯状态机 WASM 化 + 抓取/代理外置 addon（切面方案）

> 对应 ADR-0006。把「坚持对标 Stremio 到结尾」拆成可逐阶段验证的执行序列。

## 0. 现状基线（2026-08-31 实测）

### crate / 依赖矩阵

cin eharbor-core workspace：

| crate | 定位 | 关键依赖 | WASM 可行性 |
| --- | --- | --- | --- |
| `cineharbor-core` | 门面（13 行 re-export） | download/profile/storage/sync | 待长成纯核心 |
| `cineharbor-storage` | 本地持久化 | `rusqlite`（bundled sqlite） | ❌ sqlite 原生，wasm 需 IndexedDB/OPFS |
| `cineharbor-sync` | 云/跨端同步 | `reqwest` | ⚠️ 网络，wasm 需换 `fetch` |
| `cineharbor-profile` | 配置 + 鉴权 | storage（→rusqlite） | ❌ 传递原生 |
| `cineharbor-download` | 下载执行器 | `serde` | ✅ 纯 |
| `cineharbor-local-service` | 守护 + addon host + 抓取/代理（二进制 ~27k 行） | axum/hyper/reqwest/tokio | ❌ 服务端，非库 |
| `cineharbor-addon-host` | host 引擎 | addon-sdk + axum + reqwest | ⚠️ 客户端侧可拆 |

cineharbor-addon-sdk workspace：

| crate | 定位 | WASM 可行性 |
| --- | --- | --- |
| `cineharbor-addon-protocol` | 协议类型/校验 | ✅ 纯（serde 系） |
| `cineharbor-addon-sdk` | 消费侧 AddonClient + 供给侧 router | ⚠️ client 可 wasm；router（axum）服务端 |
| `cineharbor-addon-bangumi` / `-live` | 参考 addon（reqwest 抓取） | ⚠️ 属服务端 addon |

### 基线结论

- `wasm32-unknown-unknown` target 已安装（rustc 1.96.0）。
- 纯逻辑可 wasm 的当前只有 `cineharbor-download` + `cineharbor-addon-protocol`；「core 门面」经 storage→rusqlite、sync→reqwest 传递为原生。
- 抓取（api_sites/douban/live）与媒体代理（m3u8/vod/key/logo/image）全在 `local-service`，正是 Stremio 里属于 addon 的部分。

## 1. 目标组件映射（终态）

| Stremio | CineHarbor 终态 |
| --- | --- |
| `stremio-core`（纯状态机） | `cineharbor-core`：内容模型 + 库/同步 + profile + addon 聚合/派发 +（后续）getState/dispatch 状态机；native + WASM |
| `stremio-core-web` | `cineharbor-core-web`：wasm-bindgen 桥（cdylib → npm 产物），把纯 core 暴露给 web；✅ 骨架已建、wasm 管线验证通过 |
| 平台存储 | trait；native=`cineharbor-storage`(sqlite)、wasm=IndexedDB/OPFS |
| 平台网络/同步 | trait；native=`reqwest`/tokio、wasm=`fetch`(wasm-bindgen) |
| `stremio-addon-sdk` | `cineharbor-addon-protocol` + `cineharbor-addon-sdk`（client wasm 友好 / router 服务端） |
| 官方/社区 addon（catalog/meta/streams） | 抓取 addon（douban/live/vod-source）+ 媒体代理 addon，Stremio 协议 HTTP，独立部署 |
| `stremio-web` | 薄客户端：WASM core（Web Worker）+ Service Worker（CORS/缓存/流）+ addon HTTP |
| `stremio-shell` | `cineharbor-desktop`：shell + core(native) + addon 端点 |
| 浏览器下载面 | 交给 worker/Service Worker（衔接 cache-and-download 计划），与 core 解耦 |

## 2. 阶段与退出判据

### 阶段 0 —— 冻结基线 + WASM 可行性
- 产出：上方 crate/依赖矩阵；`cargo check --workspace` 基线；wasm target 可用性。
- 退出：阻塞 wasm 的依赖清单落本计划（见 §0）。

### 阶段 1 —— 抽 core 纯逻辑 + 平台 trait 化
- 内容：把 `local-service` 的纯模型/聚合/派发（`SearchResponse`/`SearchResult`/内容模型/addon 聚合等）抽进 `cineharbor-core`；引入 `Storage`/`SyncHttp`/`HttpClient` trait；native 实现保持现状行为。
- 退出：`cineharbor-core` + `cineharbor-download` + `cineharbor-addon-protocol` 过 `cargo check --target wasm32-unknown-unknown`；`local-service` 行为不变、测试绿。
- 进度：core 纯化 ✅；内容模型 `core::model` ✅；`core::sync`（profile-sync 纯模型）✅；`core::transport::HttpClient` trait + `native-http`(reqwest 实现) ✅；`core::storage` Storage trait + `native-storage`(sqlite 实现) ✅；addon 派发 `core::addons::RemoteAddon` + merge 聚合 ✅（依赖 `cineharbor-addon-protocol` 纯类型）。阶段 1 完成（wasm 侧 IndexedDB/fetch 于 P3 接入）。聚合 fan-out 已收口：addon-host 的 catalog/streams 改走 `core::addons::{merge_catalogs,merge_streams}`。

### 阶段 2 —— 抓取/代理外置 addon
- 内容：新建 `cineharbor-addons`（服务端 addon）：douban/live/vod-source 抓取 addon + 媒体代理 addon（m3u8/vod/key/logo/image）；自 local-service 移出；local-service 退化为 addon host。
- 退出：各 addon 可独立运行并通过 `/manifest.json` 自检；local-service 不再含抓取/代理逻辑。
- 进度：douban ✅ / live ✅ / vod ✅（三个 standalone 抓取 addon，bin + /manifest.json 自检 + 媒体转链）；媒体代理 ✅（`cineharbor-media` serve 转链 router，mock 上游端到端测试；vod/live addon 均已挂 `/media/{vod,live}/*`）。剩：local-service 移除内置版（P4，web 切走后）。

### 阶段 3 —— core WASM + web 桥
- 内容：`cineharbor-core`(纯) 编 wasm-bindgen；web 侧 Worker + bridge（getState/dispatch 式）；addon HTTP 走 fetch；Service Worker 承担 CORS/缓存/流。
- 退出：web 前端由 WASM core 拿到一条 catalog→meta→streams 数据；对应原生 `/api` 路由零流量。
- 预研 ✅：`cineharbor-core-web`（`stremio-core-web` 等价物）已建，core→WASM→wasm-bindgen glue 全链路跑通（evidence `2026-08-31-stremio-wasm-pipeline.md`）。
- 进度 1：addon HTTP 走 fetch ✅——`core-web::FetchHttpClient`（`HttpClient` 的 fetch 实现）+ `addon_{manifest,catalog,meta,streams}_json` 四桥；`tests/node_addon_flow.js` 端到端（mock addon + WASM）验证 catalog→meta→streams 全通。
- 进度 2：web 侧 WASM 集成骨架 ✅——`cineharbor-web/scripts/build-core-wasm.mjs`（core-web → `public/wasm/`）+ `public/core-worker.js`（模块 Worker + RPC）+ `src/lib/core/{bridge,worker-client}.ts`（`loadCoreBridge` 四桥；jest 6 绿 / tsc 0 错）。进度 3：直连传输适配器 ✅——`cineharbor-web/src/lib/transport/core-addon-client.ts`（`CoreAddonClient` + `getAddonProviderConfig`，jest 11 绿 / 全仓 typecheck 0 错）。进度 4：浏览器端到端 ✅——headless Chrome + CDP（`cineharbor-web/scripts/wasm-cdp-smoke.mjs`）验证 module Worker 加载 `--target web` glue → wasm 实例化 → fetch 直连 addon，四桥全通。进度 5：浏览器存储 seam ✅——worker IndexedDB（`public/core-worker.js` `storage_*` + `src/lib/core/storage-client.ts`），浏览器 E2E 验证 set/get/remove + 跨 worker 持久化（P3.b，host 侧实现，core 纯化无 IO）。
进度 6：standalone addon 跨源直连 CORS ✅——SDK `router()` 挂 permissive CORS（allow-origin `*` + 预检 204），e2e + 真实 live addon 验证（解挡浏览器 fetch 直连）。
进度 7：shape-bridge 首件 ✅——`cineharbor-web/src/lib/core/content/catalog-bridge.ts`（meta→SearchResult 骨架）；P4 退役执行蓝图见人间仓 `docs/plans/web-api-retirement-plan.md`。
进度 8：addon parity 复核 ✅——live M3U 摄入（实跑 3 频道验证）、vod 多源聚合、douban 搜索均已落地；剩外沿功能（douban ratings、live EPG/多源、vod 分页/建议）。
进度 9：媒体代理切面开工 ✅——`cineharbor-web/src/lib/core/media/addon-media-proxy.ts` 直连 `/media/{vod,live}/*` 构造器（对齐 Rust，jest 4 绿）。
进度 10：媒体代理首条接线 ✅——`download/proxy-url.ts` 加 `USE_ADDON_MEDIA_PROXY` 开关，vod 下载侧可分片外置到 addon `/media/vod/*`（strangler，缺省 off；jest + typecheck 绿）。
进度 11：跨源浏览器端到端 ✅——`addon-cross-origin-smoke.mjs` 证明「浏览器（A 源）wasm worker 直连真实 live addon（B 源）四桥全通 + 回转链 URL」，终局闭环。
进度 12：Service Worker（P3.d）✅——`runtime-caching.js`：core-wasm 固化 + addon 元数据 SWR + /api 排 auth/proxy（jest 3 绿 + 全仓 549 测绿）。
进度 13：live 页 addon 直连数据源 ✅——`addon-live-client.ts`（listChannels/getStreamUrl，jest 3 绿）；定位 seam `src/app/live/page.tsx`。
进度 14：live addon 多源 parity ✅——`LiveSource{key,name,ua,referer,channels}` 列表、每源 catalog、频道 id `live:{key}:{idx}`、per-source 转链；`addon-live-client.ts` 同步多源 aware（jest 4 绿）。
进度 15：live 页原生形状适配器 ✅——`addon-live-source.ts`（`AddonLiveDataSourceImpl`）把 addon 映射到原生 `LiveSource[]/LiveChannel[]`（jest 6 绿）；README 新增「实现进度」段。
进度 16：live 页切面（首个页面级）✅——`live/page.tsx` + `addon-live-source-factory.ts` 按 `NEXT_PUBLIC_USE_ADDON_LIVE`（默认 off）切源/频道/播放到 addon 直连，addon 模式降级（无预检/EPG、logo 暂原生代理）；typecheck 0 错 + jest 555 绿。
进度 17：点播 shape-bridge 补全 ✅——`streams-bridge.ts`（`streamsToEpisodes` + `buildDetail`）实现 vod 详情两步走（`/meta`+`/stream`）纯映射（jest 3 绿）。
进度 18：全链路绿扫 + 决策点清单 ✅——cargo check/test 全绿、jest 121 套件/560 测绿、typecheck 0 错；`web-api-retirement-plan.md` 收口 4 个需 Matt 拍板的决策点（live 交互验证 / 点播富模型映射 / 豆瓣 parity / 账户+鉴权边界）。
进度 19：退役 local-service `/addons` 聚合客户端 ✅——删 `transport/addon-client.ts`+测试，协议 DTO 迁 `addon-types.ts`（6 引用更新），jest 558 绿。
进度 20：点播两步数据源 ✅——`addon-content-data-source.ts`（search 预览 / detail=meta+stream，jest 2 绿）；点播映射口径定稿（Stremio 两步）。
进度 21：点播搜索页切面 ✅——`addon-content-data-source-factory.ts` + `LegacySearchPage`（传统搜索）按 `NEXT_PUBLIC_USE_ADDON_VOD`（默认 off）切换到 `AddonContentDataSource.search`（jest 回归绿、typecheck 0 错）。
进度 22：vod meta 类型自证 ✅——`meta()` 按抓取 `type_name` 推断类型（不信路径 ty），详情可统一 `detail('movie', vod:{site}:{vid})`（cargo 5 绿）。
进度 23：点播 id/source 还原 ✅——`parseVodId`+`reconcileVodResult` 把复合 `vod:{site}:{vid}` 还原原生 `{id=vid,source=站点key}`，搜索/详情与原生导航兼容（jest 2 绿）。
进度 24：点播详情/播放页切面 ✅——`fetchContentDetail` 按 `USE_ADDON_VOD`（默认 off、window 守卫）直连两步，四消费方单点收口（typecheck 0 错 + jest 562 绿）。点播切面（搜索+详情）全通。
进度 25：vod `skip` 分页 + 确定性排序 ✅（cargo 5 绿，关闭点播外沿「分页」）。
进度 26：点播跨源浏览器 E2E ✅——`vod-cross-origin-smoke.mjs` 通过（`VOD_CROSS_ORIGIN_RESULT`：catalog 2、meta 1 视频、streams 1 转链）；live+vod 两真实 cross-origin E2E 覆盖「addon HTTP 直连」双切面。剩：Matt 验证后退役 `/api/search*`（非 ws）+`/api/detail`+`/api/live/*`+`/api/proxy/*` → 豆瓣（rating 槽位决策）→ 退役 TS `/api`；外沿（suggest/EPG/logo）。

进度 27：退役执行（Matt 授权「直接删」+ 豆瓣「A」）✅——`USE_ADDON_VOD`/`USE_ADDON_LIVE` 默认转正（`!== "false"`）；删原生路由 `/api/detail` + `/api/live/{sources,channels,epg,precheck}`；`fetchContentDetail` 恒 addon 直连（删原生分支 + 测试迁移）。豆瓣 rating 槽位（A）✅——协议 `MetaPreview.rating`（与既存 `imdb_rating` 并列的通用评分槽）→ douban addon 反序列化/格式化评分（`9.4`，cargo 3 绿）→ web `AddonMeta.rating` DTO；核对 wasm `addon_catalog_json` 重序列化会带上该字段。验证：cargo check 双 workspace 绿 + jest 122·563 绿 + typecheck 0 错。剩：`/api/search*`（非 ws）/`/api/proxy/*` 因富消费方（点播源预取 `playback-source-prefetch`、下载搜索 `DownloadsClient`、建议 `fetchContentSuggestions`、转流+logo 代理）未退役，需 Matt 定「富消费方是否一并 addon 化（损排序/成人过滤/建议）」；live 页原生死分支清理 + wasm 重建（douban 评分透传）+ douban 搜索页直连（需 addon 基址可配以 hermetic E2E）。

进度 28：live 收官 ✅——live 页 4 处原生死分支/预检/二次代理移除（恒 addon 直连）；`live-client.ts` 删 4 个死函数（`buildLiveStreamProxyUrl`/`fetchLiveSources`/`fetchLiveChannels`/`precheckLiveStream`）+ `LiveStreamType`；wasm 重建同步 `MetaPreview.rating`，vod cross-origin E2E 复跑通过（`VOD_CROSS_ORIGIN_RESULT`）。EPG 退化为「tvgId 恒空→skip」（`fetchLiveEpg` 保留为 dormant）。验证：typecheck 0 + jest 122·563 绿。

进度 29：豆瓣 rating 槽位 E2E ✅——douban addon 搜索基址可配（`CINEHARBOR_DOUBAN_SEARCH_BASE_URL`，供 hermetic mock）+ `douban-cross-origin-smoke.mjs`：headless Chrome 跨源直连真实 douban addon，catalog(search) 返回 `douban:3541415`、`rating=9.4`（评分经 wasm 重序列化透传）。三 addon（live/vod/douban）跨源浏览器 E2E 全覆盖，抓取+评分外置闭环。

进度 30：live 媒体代理退役 ✅——删 `/api/proxy/{m3u8,segment,key}`（live 原生代理，已被 addon `/media/live/*` 取代、无消费者）；`media-proxy.ts` 删 `buildLiveProxy{M3u8,Segment,Key}Url`、`live-proxy.ts` 删 m3u8 重写段（保留 logo 代理）。验证 typecheck 0 + jest 122·561 绿。剩：`/api/proxy/vod/*`（下载，`USE_ADDON_MEDIA_PROXY` 待转正）+ `/api/proxy/logo`（无 addon 对等）+ `/api/proxy/m3u8-filter|m3u8-asset`（下载处理）。

进度 31：vod 媒体代理 E2E ✅——`vod-media-proxy-smoke.mjs`（node 直连真实 vod addon `/media/vod/*`）：mock 上游 m3u8→addon 重写（分片/密钥转链 + `source` 透传 + CORS `*`），重写后的分片/密钥 URL 真实转发字节（`segmentMatches`/`keyMatches` true）。补全「媒体代理外置」缺证：addon `/media/vod/*` 是原生 `/api/proxy/vod/*` 的 drop-in（退役前置证据齐，待 flip `USE_ADDON_MEDIA_PROXY` + 删）。

进度 32：剩余退役面精确核算 —— 枚举 web 原生 `/api` 全量，抓取/媒体代理外置仅剩 4 组（共 17 路由）：① `search/{route,one,resources,suggestions,ws}`+`searchhistory`（富消费方 prefetch/DownloadsClient/建议无 addon 对等）；② `douban/{route,search,categories,ratings,recommends}`（搜索页 cutover + 外沿无对等）；③ `proxy/vod/{m3u8,segment,key}`+`m3u8-filter`+`m3u8-asset`+`logo`+`image-proxy`（**核实三路由带原生专属 ad-filter+auth+desktop-dev-proxy，addon `/media/vod/*` 无**）；④ `bangumi/calendar`（无 Stremio 对等）。账户/admin/desktop/鉴权属非抓取面（决策点 4，不在本目标）。→ 全部 4 组均待 Matt 定取舍，无决策可再推进。

### 阶段 4 —— 退役原生面
- 内容：删 web 原生 `/api` 与 TS 后端（`server`/`download`/`profile-sync`/`live`/`douban`/`proxy`）；desktop/worker 对齐 addon 端点；core 门面长成 stremio-core 等价物。
- 退出：`cineharbor-web` 无原生 `/api` 路由；TS 后端模块移除；构建/测试全绿。

## 3. 回归门禁（每阶段共用）

- 阶段前：`cargo check --workspace` + `cargo test --workspace`（core、addon-sdk）记录基线。
- 阶段后：新表面 + 旧表面（未退役前）构建/测试全绿；行为差异写入阶段 evidence。

## 4. 风险与待定

- WASM 侧同步/存储边界（IndexedDB/OPFS vs sqlite）逐项定；首阶段先 stub。
- 抓取/代理 addon 的部署/鉴权/更新（自托管 vs 官方托管）。
- getState/dispatch 状态机为「更深对齐项」：阶段 1 以「纯逻辑 + 派发」铺路，不阻塞 0–4 主线。