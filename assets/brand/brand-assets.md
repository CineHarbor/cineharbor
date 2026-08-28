# CineHarbor 品牌资产

冻结主母版（2026-08-28，审批见 `docs/brand/cineharbor-process-log.md`）。

## 不变量

- 图形：纯字标 double-morpheme（无独立 mark）。
- 配色：基底 `#0B1220`（深海军蓝）· 主色 `#34C7D1`（青蓝水光）· 白 `#FFFFFF`。
- 字体：Inter（Web 应用 `next/font` 一致）；本机光栅化回退 Helvetica Neue/Helvetica。
- 大小写：CamelCase `CineHarbor`，`Cine` 中重青蓝 + `Harbor` 粗重白，无空格。

## 母版文件

| 文件 | 用途 |
| --- | --- |
| `cineharbor-icon.svg` | 1024 方底堆叠 lockup，app 图标 / favicon 的栅格源 |
| `cineharbor-wordmark.svg` | 水平字标（透明底，深底反白），Web 头部 / 文档 |
| `cineharbor-wordmark-dark.svg` | 1200×300 深底字标，logo.png 源 |
| `cineharbor-og.svg` | 1200×630 深底字标，Open Graph 分享图源 |
| `fonts/Inter.ttf` | 官方 Inter 可变字库（OFL-1.1），栅格管线自包含所需的字库 |

## 栅格派生

`scripts/generate-brand-assets.sh` 把 Inter 以 `@font-face` 内嵌进每个渲染副本（不依赖系统字体），
经 QuickLook（WebKit）光栅化 → `sips` 缩放 → `iconutil`/stdlib 出 `.icns`/`.ico`，
下发到 `cineharbor-web/public`（favicon/PWA 图标）与 `cineharbor-desktop/src-tauri/icons`。
任何机器克隆后即可确定性复现同一字形。

## 已知限制

- Inter 可变字库 `fonts/Inter.ttf`（OFL-1.1）随仓分发，栅格已用真实 Inter 字形（经 `@font-face` 内嵌）。