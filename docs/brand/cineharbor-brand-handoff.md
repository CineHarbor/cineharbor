# CineHarbor 品牌交接（Brand Handoff）

## 批准主母版

| 字段 | 值 |
| --- | --- |
| 可编辑源 | `assets/brand/cineharbor-icon.svg` / `cineharbor-wordmark.svg` / `cineharbor-wordmark-dark.svg` / `cineharbor-og.svg` |
| 审批版本/commit | 见本仓 git 历史（P6 品牌资产提交） |
| 审批日期 | 2026-08-28 |
| 负责人 | Matt |

## 主母版不变量

### 图形与比例
纯字标 double-morpheme（无独立 mark）。水平锁定 `Cine`+`Harbor`（无空格）；图标为两行堆叠
`Cine` 上 / `Harbor` 下，置于 1:1 深底，两行基线间距 ≈ 0.16H。

### 配色
- 基底 `#0B1220`（深海军蓝，脱离旧纯黑）
- 主色 `#34C7D1`（青蓝水光）
- 白 `#FFFFFF`（字标次段）

### 字体与许可
Inter（Web 应用 `next/font` 一致；本机光栅化回退 Helvetica Neue/Helvetica）。CamelCase `CineHarbor`。

### 负空间与背景
图标/头像用不透明 `#0B1220` 底（maskable 满幅安全区）；字标用透明底。

### 锁定、间距与最小尺寸
水平锁定两词素自然衔接；堆叠 lockup 上下居中行距 ≈ 0.16H。favicon 最小尺寸 16px（靠字形块识别，
不承载完整可读性）。

## 资产清单

| 资产 | 格式/尺寸 | 目标载体 | 派生自 | 校验 |
| --- | --- | --- | --- | --- |
| cineharbor-icon.svg | SVG 1024 | 母版 | — | 像素抽样：navy/cyan/white 齐备 |
| cineharbor-wordmark.svg | SVG 1200×300 | Web 头部/文档 | — | — |
| cineharbor-wordmark-dark.svg | SVG 1200×300 | logo.png 源 | — | BMP 抽样白/青齐备 |
| cineharbor-og.svg | SVG 1200×630 | og-image 源 | — | BMP 抽样 |
| favicon.ico / favicon-16x16.png / favicon-32x32.png | 3 图 ICO + PNG 16/32 | Web favicon | icon.svg | ICO 头解析 3 图；尺寸 16/32 |
| apple-touch-icon.png | 180 | iOS 主屏 | icon.svg | 180×180 |
| icons/icon-{192,256,384,512}.png + icon-512-maskable.png | PNG | PWA manifest | icon.svg | 尺寸逐一核对 |
| logo.png / og-image.png | 1200×300 / 1200×630 | 站点 logo / 分享图 | wordmark-dark/og | 尺寸 1200 |
| src-tauri/icons/* | PNG 各尺寸 + icon.icns + icon.ico(4 图) | 桌面客户端 | icon.svg | iconutil 生成；icns magic `icns`；ico 4 图 |

## 实现

| 载体 | 位置 | 变更 | 验证证据 |
| --- | --- | --- | --- |
| Web | `cineharbor-web/public/*` + `manifest.json` + `src/app/layout.tsx` | 换 favicon/PWA/logo/og，manifest 增 maskable+theme_color #0B1220，layout 增 favicon/apple-touch/theme-color/og:image | BMP 像素抽样 + sips 尺寸 + `pnpm tsc` |
| 桌面 | `cineharbor-desktop/src-tauri/icons/*` | 全量换新图标（含 icns/ico） | `tauri build --bundles app` 通过 |

## 视觉 QA

| 检查 | 环境/尺寸 | 证据 | 结果 |
| --- | --- | --- | --- |
| 图标配色 | 512 PNG → BMP 抽样 | navy=249999 / cyan=3365 / white=6871 / AA=1909 | ✅ 三段字标齐备、比例符合 Cine(fewer)/Harbor(bolder) |
| 字标 | 1200×300 BMP 抽样 | white=225561 / cyan=6333 | ✅ 双词素分色 |
| OG | 1200×630 BMP 抽样 | navy/cyan/white 齐备 | ✅ |
| .ico | 头解析 | favicon 3 图 / icon.ico 4 图 | ✅ |
| .icns | 头解析 | magic `icns`，116KB | ✅ |

## 已知限制

- 本机无 Inter 二进制字体，栅格产物含 Helvetica 回退字形；批准字型（Inter）已写入母版与 Web `next/font`，
  需字形完全一致时在装有 Inter 的环境重新执行 `scripts/generate-brand-assets.sh`。
- og:image 为相对 URL，正式域名确定后需改为绝对 URL（社媒抓取要求）。
- 商标/域名正式清权检索仍未完成（见 process log 开放问题）。

## 未解决工作

1. 商标/域名正式清权（联网检索恢复后）。
2. 正式部署域名确定后改 og:image 为绝对 URL。
3. 在带 Inter 的环境重导出栅格以消除 Helvetica 回退差异。