# ADR-0007: vod 抓取外置为共享 crate + standalone addon

- Status: accepted
- Date: 2026-08-31
- Replaces/extends: ADR-0006（阶段 2 的「vod 抓取 addon」落法细则）

## Context

终态要求把抓取逻辑留在 core 之外、作为 remote addon 独立运行。douban / live 已各自独立成
standalone addon。vod（CustomAPI 视频站聚合搜索 + 详情 + 播单）最重、耦最深：抓取逻辑散在
`cineharbor-local-service` 的 `content_search.rs` / `content_detail.rs` 及 `lib.rs` 一堆 helper，
且依赖配置类型 `ApiSite` 和 `SearchResult`。

## Decision

1. **共享抓取核心 crate `cineharbor-api`**（放 `cineharbor-addon-sdk/crates/`）：收纳 vod 的
   「纯逻辑、无 IO」部分——`ApiSite` 配置 DTO + 解析/URL 构造/episodes 抽取/值规整。未来
   local-service 与 standalone vod addon 都依赖它，避免两份拷贝漂移。
2. **standalone vod addon `cineharbor-addon-vod`**：在 `cineharbor-api` 之上加网络请求
   （`search_site`/`fetch_content_detail`，reqwest）+ `Addon` trait + bin 服务。
3. **strangler 迁移**：先并行（local-service 内置版与新 addon 并存），后切依赖、删 local-service
   内部拷贝（含 `addon_vod.rs` / `content_search` / `content_detail` 抓取函数）。

## Extraction surface（已映射，local-service 内部拷贝清单）

- 类型：`ApiSite`（`lib.rs:1193`，`key/api/name/detail/ua/referer/disabled/disable_ad_filter`）。
- 值规整：`value_to_string` / `value_to_i64` / `parse_usize` / `normalize_year` / `collapse_whitespace`
  / `clean_html_tags`（`lib.rs:5670-5734`）。
- ID：`is_valid_content_id`（`lib.rs:5554`）。
- 剧集：`extract_episodes_from_play_url` + `looks_like_manifest_url`（`lib.rs:5559`、`7796`）。
- URL：`build_collection_api_url` + wrapped-target 判定 + query 编码（`lib.rs:5619-5668`）。
- 解析：`parse_search_payload`/`parse_search_item`（`content_search.rs`）、
  `parse_detail_payload`/`parse_custom_detail_html`/`extract_m3u8_matches`/`has_custom_detail_url`
  （`content_detail.rs` + regex）。
- 暂缓（随网络层迁移）：`build_downstream_headers`、`filter_adult_content_results`（内容策略）、
  `search_site`/`fetch_content_detail`/`fetch_json_detail`/`fetch_custom_detail`。
- 共享类型：`SearchResult` 直接用 `cineharbor-core::model`（跨仓依赖 `core → addon-protocol` 与
  `api → core`，无环）。

## Consequences

- `cineharbor-api` 是纯逻辑 crate（依赖 core/serde_json/regex/url/html-escape），可离线单测。
- local-service 未来改 `use cineharbor_api::...` 并删自身拷贝；`addon_vod.rs` 由新 addon 取代。
- `SearchResult` 单一来源在 core，三方（core / 新 addon / local-service）类型统一。