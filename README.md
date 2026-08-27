# CineHarbor

> 🎬 多源汇流、自由播放的跨平台影视聚合播放器生态。

CineHarbor 是一个对标 Stremio 的三层架构开源影视聚合项目：**Rust 核心 + 各端客户端 + Stremio 兼容的内容源 addon 协议**。所有支流最终泊入同一个港湾——所有内容源经由统一协议汇入同一个播放器。

## 目录

```
apps/                        客户端
  cineharbor-web/            Web 客户端（Next.js + PWA）
  cineharbor-desktop/        桌面客户端（Tauri）
crates/                      Rust 工作区（core + addon 协议）
  cineharbor-core/           核心门面：聚合 storage/sync/profile/download
  cineharbor-storage/        本地持久化（sqlite）
  cineharbor-sync/           云端/跨端同步
  cineharbor-profile/        用户配置与鉴权
  cineharbor-download/       下载执行器
  cineharbor-local-service/  本地守护服务 + addon host
  cineharbor-addon-protocol/ Stremio 兼容契约
  cineharbor-addon-sdk/      addon 开发 SDK
addons/                      参考 addon（bangumi / douban / live …）
services/cineharbor-worker/  Cloudflare 边缘代理
sites/cineharbor-download-site/  下载站
docs/                        架构 ADR、迁移来的开发计划、品牌过程记录
```

## 快速开始

```bash
cargo check --workspace   # Rust 核心
```

Web / 桌面客户端将在各自阶段加入 workspace（见 `docs/PLAN.md`）。

## 许可证

CC BY-NC-SA 4.0（沿用上游公开授权；上游元数据存在 GPL/MIT 与其 LICENSE 不一致的问题，见 `docs/PLAN.md` 开放问题）。

## 文档

- 开发计划与决策记录：`docs/PLAN.md`
- 架构决策：`docs/adr/`
- 品牌过程记录：`docs/brand/cineharbor-process-log.md`
