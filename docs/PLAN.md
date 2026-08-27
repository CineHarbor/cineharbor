# CineHarbor 开发计划

## 已批准的决策（2026-08-27，决策人 Matt）

| 决策 | 结论 |
| --- | --- |
| 迁移方式 | 冷启动新仓：在新目录全新 `git init`，代码按模块搬运；旧仓保留作上游参考 |
| 上游关系 | 硬分叉独立：不再跟踪上游仓库，上游新功能手动移植 |
| addon 协议 | 兼容 Stremio 协议（实现其 manifest/catalog/meta/streams 契约，可用现成公开源） |
| 老用户数据 | 不迁移（不承诺读旧客户端的 sqlite 数据） |

## 仓库拓扑（ADR-0003，2026-08-27 拆多仓）

| 仓库 | 内容 | 状态 |
| --- | --- | --- |
| `cineharbor`（本仓） | 门面：README、PLAN、ADR、品牌史 | ✅ |
| `cineharbor-core` | 6 crate：core/storage/sync/profile/download/local-service | ✅ P1 完成 |
| `cineharbor-addon-sdk` | 2 crate：addon-protocol/addon-sdk + protocol.md | ✅ 骨架 |
| `cineharbor-web` | Next.js 客户端（P4） | ✅ 占位 |
| `cineharbor-desktop` | Tauri 客户端（P5） | ✅ 占位 |
| `cineharbor-worker` | 边缘代理（P6） | ✅ 占位 |
| `cineharbor-download-site` | 下载站（P6） | ✅ 占位 |

## 阶段计划

| 阶段 | 内容 | 产出 | 状态 |
| --- | --- | --- | --- |
| **P0 骨架** | git init + 双 workspace + 8 crate 占位 + CI + 文档 | 空仓可 `cargo check`、CI 就绪 | ✅ 完成 |
| **P1 core 落地** | 5 个 crate 迁入（storage/sync/profile/download/local-service），新建 core 门面；清旧品牌字符串 | Rust core 编译通过 | ✅ 完成 |
| **P2 addon 协议/SDK** | Stremio 兼容契约 + SDK；bangumi/douban/live 抽成参考 addon（douban 随 P4） | 首个 addon 跑通 streams 聚合 | ✅ 协议/SDK/bangumi+live 参考 addon |
| **P3 local-service 重构** | 变 addon host + 统一数据出口；桌面端不再 Tauri command 直连 | 本地 daemon 可托管 addon | ⏳ |
| **P4 Web 客户端** | `src/` 迁入 apps/cineharbor-web，清旧品牌类名与旧 manifest；数据访问切 core/RPC | cineharbor-web 起服务 | ⏳ |
| **P5 桌面客户端** | Tauri 壳改名 cineharbor-desktop，productName/identifier/updater 换新 | 打包成功 | ⏳ |
| **P6 周边** | worker、proxy、下载站迁入改名；logo 冻结后换 favicon/icons/PWA | 品牌一致 | ⏳ |

## 旧名对照

迁移期新旧对照已归档至 `docs/brand/cineharbor-process-log.md`（品牌史），本文件不再保留旧名。

## 开放问题

1. **许可证**：上游 `LICENSE` 为 CC BY-NC-SA 4.0，但 `Cargo.toml` 误写 GPL-3.0-only、README 徽章误写 MIT。本仓暂按 LICENSE 文件（CC BY-NC-SA 4.0）发布。若想换成 GPL/MIT，需先厘清继承代码的作者权，或重写无关本体的部分。
2. ~~**Stremio 兼容范围**~~ → **已解决（2026-08-27）**：完全跟随 Stremio 协议，双向互操（本地 host 可加载 Stremio addon；我们的参考 addon 可被 Stremio 官方客户端加载）。契约冻结于 `cineharbor-addon-sdk` 仓的 `protocol.md`（ADR-0002）。
3. ~~**sqlite schema 版本**~~ → **已解决（2026-08-27）**：全新从 `1` 起步（老数据不迁移，无兼容包袱）。
4. **桌面 updater 渠道**：旧客户端用户不再平滑过渡（决策 4 已定），新渠道直接发布 cineharbor-desktop。
