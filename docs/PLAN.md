# CineHarbor 开发计划

## 已批准的决策（2026-08-27，决策人 Matt）

| 决策 | 结论 |
| --- | --- |
| 迁移方式 | 冷启动新仓：在新目录全新 `git init`，代码按模块搬运；旧仓保留作上游参考 |
| 上游关系 | 硬分叉独立：不再跟踪 MoonTechLab/LunaTV，上游新功能手动移植 |
| addon 协议 | 兼容 Stremio 协议（实现其 manifest/catalog/meta/streams 契约，可用现成公开源） |
| 老用户数据 | 不迁移（不承诺读旧 LunaTV 的 sqlite 数据） |

## 阶段计划

| 阶段 | 内容 | 产出 | 状态 |
| --- | --- | --- | --- |
| **P0 骨架** | git init + 双 workspace + 8 crate 占位 + CI + 文档 | 空仓可 `cargo check`、CI 就绪 | ✅ 完成 |
| **P1 core 落地** | 5 个 crate 迁入（storage/sync/profile/download/local-service），新建 core 门面；清 moontv 字符串 | Rust core 编译通过 | ⏳ |
| **P2 addon 协议/SDK** | 定 Stremio 兼容契约 + SDK；把 bangumi/douban/live 抽成参考 addon | 首个 addon 跑通 streams 聚合 | ⏳ |
| **P3 local-service 重构** | 变 addon host + 统一数据出口；桌面端不再 Tauri command 直连 | 本地 daemon 可托管 addon | ⏳ |
| **P4 Web 客户端** | `src/` 迁入 apps/cineharbor-web，清 luna-\* 类名与旧 manifest；数据访问切 core/RPC | cineharbor-web 起服务 | ⏳ |
| **P5 桌面客户端** | Tauri 壳改名 cineharbor-desktop，productName/identifier/updater 换新 | 打包成功 | ⏳ |
| **P6 周边** | worker、proxy、下载站迁入改名；logo 冻结后换 favicon/icons/PWA | 品牌一致 | ⏳ |

## 命名映射（旧 → 新）

| 旧 | 新 |
| --- | --- |
| moontv-storage / -sync / -profile / -download / -local-service | cineharbor-storage / …（后缀不变） |
| lunatv-desktop-shell（lib 名 lunatv_desktop_shell） | cineharbor-desktop |
| package.json#name: moontv | cineharbor（monorepo 根） |
| worker/、proxy.worker.js、download-site/ | services/cineharbor-worker、sites/cineharbor-download-site |

## 开放问题

1. **许可证**：上游 `LICENSE` 为 CC BY-NC-SA 4.0，但 `Cargo.toml` 误写 GPL-3.0-only、README 徽章误写 MIT。本仓暂按 LICENSE 文件（CC BY-NC-SA 4.0）发布。若想换成 GPL/MIT，需先厘清继承代码的作者权，或重写无关本体的部分。
2. ~~**Stremio 兼容范围**~~ → **已解决（2026-08-27）**：完全跟随 Stremio 协议，双向互操（本地 host 可加载 Stremio addon；我们的参考 addon 可被 Stremio 官方客户端加载）。契约冻结于 `docs/addon-protocol.md`（ADR-0002）。
3. **sqlite schema 版本**：全新版本号从 1 起步，还是保留上游 200.x 语义再 +1？老数据不迁移的前提下建议从 1 起步。
4. **桌面 updater 渠道**：旧 LunaTV 用户不再平滑过渡（决策 4 已定），新渠道直接发布 cineharbor-desktop。
