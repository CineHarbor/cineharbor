# Evidence: 2026-09-12 P4 退役剩余切面拍板

Principal 在会话中逐项拍板。结论写入 `.agnir/decisions.md`（2026-09-12），执行序写入 `.agnir/next-actions.md` §9。

| 项 | 结论 |
|---|---|
| 点播搜索富消费方 | 先迁进 vod addon 再删 `/api/search*` |
| 下载媒体代理 | addon 补广告过滤+鉴权再切；logo/image 留 web |
| 豆瓣页 | 搜索现在 cutover；recommends/categories 留原生 |
| 首页番剧日历 | 接已有 bangumi addon |
| 桌面 updater | 首次在线升级闭环后置 |

落地（同日）：

- web：删 `/api/douban/search`、`/api/bangumi/calendar`、`/api/search*`、`/api/proxy/vod/*`
- addon-sdk：bangumi 独立进程 + calendar 星期/评分；media 广告过滤 + token 鉴权
- 验证：`cineharbor-web` `pnpm test` 127 套件 / 577 测绿；`pnpm typecheck` 0 错；`cargo test -p cineharbor-addon-bangumi/media/vod/live` 绿

未验证：浏览器里连真实 addon 点完整搜索/首页/下载（需本地起 douban/bangumi/vod addon + `pnpm dev`）。桌面 updater 仍后置。
