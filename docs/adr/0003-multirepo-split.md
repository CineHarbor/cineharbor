# ADR-0003：拆分为多仓（镜像 Stremio 仓库拓扑）

日期：2026-08-27
状态：已接受（取代 ADR-0001）

## 背景

用户决定照 Stremio 模式拆为多仓。此前 P0 按分区单仓落地（ADR-0001）。拆分时点选在 P0 完成、尚无真实代码迁入之前，成本最低。

## 决策

仓库切分如下（org：`CineHarbor`）：

| 仓库 | 语言/构建 | 内容 | 对应 Stremio |
| --- | --- | --- | --- |
| `cineharbor` | docs-only | 组织门面：README、PLAN、ADR、品牌史、迁移中的旧开发计划 | (org 级入口) |
| `cineharbor-core` | Rust/cargo | crate：core、storage、sync、profile、download、local-service | `stremio-core` |
| `cineharbor-addon-sdk` | Rust/cargo | crate：addon-protocol、addon-sdk + protocol.md | `stremio-addon-sdk` |
| `cineharbor-web` | Node/Next.js | Web 客户端 + PWA | `stremio-web` |
| `cineharbor-desktop` | Rust/Tauri | 桌面壳 | `stremio-shell` |
| `cineharbor-worker` | Node/CF | 边缘代理 worker | — |
| `cineharbor-download-site` | 静态站 | 下载/发布站 | — |

## 依赖图

```
cineharbor-addon-sdk  ──(被依赖)──▶ cineharbor-core（local-service 作 addon host）
                                          ▲
                                          │ 嵌入 local-service + 链 core 库
                                     cineharbor-desktop
cineharbor-web ──(HTTP/RPC)──▶ cineharbor-core 的 local-service
cineharbor-worker：独立边缘代理；cineharbor-download-site：独立静态站
```

## 跨仓规则

- 每个仓库独立 `0.1.0` 起步、独立 CI、独立发版、独立权限。
- 跨仓依赖走**发布产物**（crates.io / 私有 registry）+ git tag 引用；本地协作用 path 或 yalc/link。
- 协议字段变更（addon-sdk）属跨仓 breaking change：先发 sdk 版本，再升 core/web/desktop 引用点。
- 参考 addon（bangumi/douban/live）P2 再建 `cineharbor-addons` 仓，暂不占位。

## 影响

- ADR-0001 作废；门面仓移除 Cargo/pnpm workspace 与 CI。
- 本地开发需多仓 clone 与链接；这是已接受的协调成本。
- 各仓许可证沿用 CC BY-NC-SA 4.0（与门面仓 LICENSE 一致）。
