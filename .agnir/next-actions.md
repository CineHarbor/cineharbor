# CineHarbor Next Actions

0. ~~提交并推送本次 Agnir 初始化~~ ✅ 已完成（2026-08-31，7 仓 commit + push 到 `github.com-matt`）。
1. ~~六仓尚未 push~~ ✅ 已完成（2026-08-31 全部推送；README 中 GitHub 链接已生效）。
2. P0–P6 均已落地；当前续作 douban-imdb-rt（见 3）。
3. ~~跟进 `docs/PLAN.md` 开放问题 #1（许可证）~~ ✅ 已解决（2026-08-28）。
4. 各子仓后续动作由其各自 Agnir `.agnir/next-actions.md` 维护。
5. douban-imdb-rt：P0 统一评分聚合层 + P1 IMDb 官方 datasets 零 key 已在 `cineharbor-web` 落地；剩余 P2（RT 真实数据源 + 播放详情页三源评分区）、P3 由 `cineharbor-web/.agnir/next-actions.md` 跟踪。
6. ~~待推送~~ ✅ 七仓 `main` 已与 `origin/main` 对齐（2026-09-07 Agnir 1.0 迁移之后无领先提交）。
7. ~~Web 数据面收敛（ADR-0005 双表面/native RPC）~~ → 已被 ADR-0006 取代：终态改为 Stremio 式（core WASM 化 + 抓取/代理外置 addon）。
8. **终态对齐 Stremio（ADR-0006）**：阶段 0–3 ✅。P4 退役剩余切面已于 2026-09-12 拍板（见 `.agnir/decisions.md`），执行序见 9。
9. **P4 拍板后执行序**（不接受能力降级）：
   1. ~~豆瓣搜索页 cutover~~ ✅ 2026-09-12：`getDoubanTitleSearch` 直连 douban addon，删 `/api/douban/search`。recommends/categories 仍原生。
   2. ~~首页番剧日历接 bangumi addon~~ ✅ 2026-09-12：`GetBangumiCalendarData` 直连 bangumi addon（`genres[0]`=weekday），独立 bin `:11474`，删 `/api/bangumi/calendar`。
   3. ~~搜索富消费方迁 vod addon~~ ✅ 2026-09-12：`fetchContentSearchResults` / suggestions / prefetch / 下载搜索走 vod addon + 客户端成人过滤；删 `/api/search*`（含 ws/one/resources/suggestions）。
   4. ~~vod 媒体代理补过滤+鉴权再切~~ ✅ 2026-09-12：`cineharbor-media` 广告过滤 + `token` 鉴权；下载 URL 恒走 `/media/vod/*`；删 `/api/proxy/vod/*`。logo/image-proxy 仍留 web。
   5. 桌面 updater 首次在线升级闭环后置，不挡本序。