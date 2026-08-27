# ADR-0001：单仓布局与工作区边界

日期：2026-08-27
状态：已接受

## 背景

从旧项目硬分叉重建为 CineHarbor。目标形态对标 Stremio：Rust 核心 + 各端客户端 + Stremio 兼容 addon 协议。原仓库单仓平铺（5 个 crate + Next.js + Tauri + worker + 下载站混合在根目录），难以表达「核心 / 客户端 / addon」的边界。

## 决策

采用**单一 pnpm + 单一 Cargo workspace 的分区单仓**：

```
apps/       客户端（web、desktop）
crates/     Rust crate（core、storage/sync/profile/download、local-service、addon-protocol、addon-sdk）
addons/     参考 addon 实现
services/   边缘/后台（Cloudflare worker、proxy）
sites/      静态站（下载站）
docs/       ADR、plan、品牌记录
```

- Cargo workspace 成员 = `crates/*`；桌面 Tauri 包入列时加入其路径。
- pnpm workspace 包 = `apps/*`、`addons/*`、`services/*`、`sites/*`。
- 所有机器标识（crate、package、目录、org handle）统一全小写 `cineharbor-*`，与品牌不变量一致。

## 理由

- 分区表达架构边界，P0 即可见「三层架构」骨架。
- 不引入 Turborepo/Nx：现状是「一个 web app + 少量 rust crate」，pnpm + cargo 双轨足够，工具链成本最低。

## 影响

- CI 需同时覆盖 rust 与 pnpm 两侧（见 `.github/workflows/ci.yml`）。
- migrate 阶段（P1、P4）需保留「上游模块 ↔ 新路径」的对照，避免漏迁。
