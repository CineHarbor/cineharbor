# 开发计划归属与状态索引

> `docs/plans/` 存放从旧项目迁入的开发计划。本表记录每条计划的归属仓与实现状态；计划落地时的正文改动归对应仓库，门面仓只保留方案与索引。

## 索引

| 计划 | 归属仓 | 状态 |
| --- | --- | --- |
| `player-enhancements-audio-visual.md` | cineharbor-core + cineharbor-web | ✅ 已实现（core `local-service` 提供 `player_enhancements` 级别化配置；web `app/layout.tsx` / `app/live` 已消费） |
| `music-player-rustified-plan.md` | cineharbor-web + cineharbor-core | 🟡 部分落地：web 已有 music 导航/播放器安全区雏形（`PageLayout` / `globals.css`）；正文文件引用仍是旧机器路径，续作前需先修链接 |
| `douban-imdb-rt-integration-plan.md` | cineharbor-web | 🟡 P0 落地：统一评分聚合层 + `POST /api/ratings/batch` + 豆瓣真实接入 + IMDb/RT 配置门控优雅降级；搜索页已切统一接口、VideoCard 已加评分行；IMDb/RT 真实数据源与播放详情页待接入 |
| `desktop-follow-updates-plan.md` | cineharbor-desktop（Web 后续复用） | 📋 方案就绪，未实现 |
| `cache-and-download/`（5 篇） | cineharbor-worker + cineharbor-web | 📋 方案库（SW 缓存 / IndexedDB / Background Fetch 选型） |

## 备注

- 计划正文内的文件链接有新旧两种写法：douban 计划已指向本机新多仓路径；`music-player-rustified-plan.md` 仍指向 `/Users/jay-workstation/AI-CODE/CineHarbor/...`（另一机器旧路径），续作前先统一为新仓相对路径。
- 状态约定：✅ 已实现 / 🟡 部分落地 / 📋 方案就绪未实现。