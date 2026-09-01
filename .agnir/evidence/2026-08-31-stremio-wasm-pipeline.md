# 2026-08-31 core→WASM→JS 管线验证（阶段 3 预研）

- 工具链：`wasm-bindgen` CLI / `wasm-bindgen-test-runner` 0.2.126 已装；`wasm-pack` 未装（可用 wasm-bindgen + cargo 替代）。
- 新增 `cineharbor-core/crates/cineharbor-core-web`（对标 Stremio `stremio-core-web`）：cdylib + wasm-bindgen 桥，暴露 `core_version` / `demo_search_result_json` / `default_sync_domains`；业务逻辑仍在 `cineharbor-core`。
- 验证（exit 0）：
  - `cargo build -p cineharbor-core-web --target wasm32-unknown-unknown` → `cineharbor_core_web.wasm`（9.5 MB debug）。
  - `wasm-bindgen --target web` → 生成 `cineharbor_core_web.js`（glue）+ `_bg.wasm` + `.d.ts`；导出符号 `core_version` / `default_sync_domains` / `demo_search_result_json` 均可见。
  - `cargo check --workspace`（native）exit 0。
- 结论：Rust core → WASM cdylib → wasm-bindgen glue 全链路可用，阶段 3 最硬风险已解除。
- 环境注意：构建 wasm 需下载 `bumpalo`/`wasm-bindgen*` 新 crate，而 `~/.cargo` 在沙箱工作区写权限之外 → 用 `CARGO_HOME=/Users/jay/Code/CineHarbor/.cargo-home`（workspace 本地）即可，无需提权。