# 2026-08-31 终态对齐 Stremio 切面（阶段 0 + 阶段 1 首切）checkpoint

- Principal 决策：坚持对标 Stremio 到结尾（ADR-0006）。core 纯状态机 native+WASM；抓取/代理外置 remote addon；web 薄客户端（WASM core + Service Worker + addon HTTP）。
- 阶段 0 基线：
  - 两仓 `cargo check --workspace` 绿（core ~11.3s、addon-sdk ~11.5s，exit 0）。
  - `wasm32-unknown-unknown` target 已安装（rustc 1.96.0）。
  - crate/依赖矩阵见 `docs/plans/stremio-faithful-cutover-plan.md` §0。
  - 关键事实：`cineharbor-core` 门面原为 13 行 re-export、**零消费方**（desktop 不链 core 库，local-service 直接依赖子 crate，web 走 HTTP）→ 可安全将其改造为纯核心。
- 阶段 1 首切（已完成、可复现）：
  - `cineharbor-core` 撤掉 storage/sync/profile/download 依赖，改为纯 `serde`/`serde_json`；
  - 新增 `crates/cineharbor-core/src/model.rs`：`SearchResult`/`SearchResponse`/`ContentSuggestion`/`SuggestionsResponse`/`LiveChannel`/`LiveProgram`/`LiveEpgData`（pub + serde）。
  - 验证 exit 0：`cargo check -p cineharbor-core -p cineharbor-download --target wasm32-unknown-unknown`；`cargo check -p cineharbor-addon-protocol --target wasm32-unknown-unknown`；两仓 `cargo check --workspace`。
- 下一步（阶段 1 续）：
  - local-service 改为 `use cineharbor_core::model::{...}` 复用并删除本地同名拷贝（先接线，再补 trait 化）。
  - Storage / SyncHttp / HttpClient trait 化，native 实现保持现状行为。
  - `ContentSuggestion.type` 的 `&'static str` 在 wasm-bindgen 暴露前需收窄为 owned 类型。