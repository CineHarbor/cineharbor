# 2026-08-31 P1.c 同步纯模型抽取 checkpoint

- 把 profile-sync 的纯领域模型与无 I/O 函数从 `cineharbor-sync` 抽到 `cineharbor-core::sync`（新 `crates/cineharbor-core/src/sync.rs`）：
  - 常量 + `default_profile_sync_selected_domains`
  - `ProfileSyncErrorKind` / `ProfileSyncError`（用 `http::StatusCode` 替代 reqwest 再导出类型）
  - `ProfileSyncSession` / `ProfileSyncStatusResponse` / `RemoteServerConfigResponse` / `RemoteLoginResponse` / `ProfileSyncSessionMutation`
  - `build_profile_sync_target_url` / `session_from_login_response` / `normalize_optional_string`
- `cineharbor-sync` 改为 `pub use cineharbor_core::sync::{...}` 重导出；reqwest client（`ProfileSyncClient` + cookie 转发 + forward 类型）留在原地 → 消费方（local-service 等）零改动。
- `cineharbor-core` 新增依赖 `http` / `thiserror` / `url`（均 wasm 友好）。
- 验证：`cargo test --workspace` exit 0（sync 10 测试仍绿）；`cargo check -p cineharbor-core --target wasm32-unknown-unknown` exit 0。
- 遗留（P1.c 续）：引入 `HttpClient` / `Storage` trait 并让 `ProfileSyncClient` / sqlite 实现，native（reqwest/sqlite）与后续 wasm（fetch/IndexedDB）双实现。