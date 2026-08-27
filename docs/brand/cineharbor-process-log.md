# CineHarbor 品牌过程记录

## 记录元数据

| 字段 | 值 |
| --- | --- |
| 品牌/产品 | CineHarbor（原 MoonTV / LunaTV / moontv；曾选 Fluma、Rillow，均因注册占用弃用） |
| 记录负责人 | Matt |
| 开始 | 2026-08-27 |
| 最后更新 | 2026-08-27 |
| 审批权 | 会话用户（直接决策人，Matt） |

## 简报

### 受众与定位

- 跨平台影视聚合播放器生态：core + 各端客户端 + 内容源（addon）协议，三层架构（对标 Stremio）。
- 定位语：多源汇流、自由播放（Freedom to Stream 精神，但全新意象，不复用 Stremio 措辞）。

### 目标载体

- 桌面客户端（Tauri）、Web（Next.js/PWA）、Rust core、内容源 addon SDK。
- 后续：favicon/PWA/social、应用图标、下载站。

### 语言

- 英文优先、全球可用；文档跟随会话语言（当前中文）。

### 约束与排除

- 彻底跳出天文/月亮/星空意象（明确排除 Moon、Luna 及其衍生）。
- 名字必须能自然派生包名（`<name>-core` / `<name>-web` / `<name>-desktop` / `<name>-addon-sdk`）。
- 短、易拼写发音、无拼写歧义。
- 审美校准（第三轮问答追加）：大平台产品感（Netflix/Hulu 式 2–3 音节、大众响亮），词根必须零学习成本——拒绝陌生造词，也拒绝小清新复合词。

### 成功标准

- 一个名字统领整个生态，三层架构共享同一品牌前缀。
- 商标/域名/npm 包名一次性可注册性优先。

## 证据登记

| 日期 | 证据 | 位置 | 确立了什么 | 状态 |
| --- | --- | --- | --- | --- |
| 2026-08-27 | 现有品牌名 MoonTV、包名 `moontv`、目录名 `LunaTV` | `README.md` / `package.json` / 工作目录 | 旧品牌命名与天文意象 | 已记录 |
| 2026-08-27 | `public/manifest.json` name=MoonTV、`background_color`=#000000 | `public/manifest.json` | 旧品牌资产与深色底 | 已记录 |
| 2026-08-27 | 现有 logo：`public/logo.png`、`public/favicon.ico`、`public/icons/icon-*.png` | `public/` | 旧品牌图形资产位置 | 待替换 |
| 2026-08-27 | CSS 类名 `luna-*`（如 `luna-section-title`）散落于 `src/app/page.tsx` | `src/app/page.tsx` | 旧品牌前缀在实现中的残留 | 待清理 |
| 2026-08-27 | 用户三项命名决策：① 覆盖整个生态平台 ② 彻底跳出天文意象 ③ 英文优先全球可用 | 会话问答（ask_user_question） | 命名战略边界 | 已批准 |
| 2026-08-27 | Fluma 撞名：fluma.in（印度 AI 网红营销平台，预发布）+ 同名 iOS T 恤购物 App（RAPID ACCELERATION INDIA），行业类别不相交但检索混淆成立 | web_search + apps.apple.com | Fluma 不可沿用 | 已确认 |
| 2026-08-27 | 候选拉网初检：Talweg/Rillow 近零撞名且 npm、crates.io 均未注册；Rilo（rilo.tv 同类自托管影视平台）、Confluo（Berkeley OSS + Confluent 音近）、Runnel/Lotic/Aflux 均有占用，排除 | web_search + npm registry + crates.io API | 替代候选收敛空间 | 已确认 |
| 2026-08-27 | Rillow GitHub 组织已被注册（用户确认；`api.github.com/users/rillow` 探测 200 佐证） | 会话 + GitHub API | Rillow 不可用 | 已确认 |
| 2026-08-27 | GitHub 组织名囤积现实：talweg/eyot/sluice/freshet/swale/rivulet 等冷僻真词与 ryvo/onda/kino/reelo 等响亮短词全部被既有账号占用（多批探测） | GitHub API 探测 | 可用名只能来自独特造词或熟词新组 | 已确认 |
| 2026-08-27 | 终选注册表初检：CineHarbor 在 GitHub 组织、npm、crates.io 三处均未注册；备选池 Rivanta/Fluvanta/Cineonda/Rivoda/Volanta/CinePlay 同样三处空闲 | GitHub API + npm registry + crates.io API | 注册表层面可用 | 已确认 |
| 2026-08-27 | 网页级撞名检索不可用：web_search 连续返回非实时内容、DuckDuckGo 人机验证拦截、DNS 探测被沙箱通配劫持返回假数据 | 会话工具记录 | 本轮未能联网核实品牌撞名 | 阻塞（转待办） |

## 探索与决策

| 日期 | 方向或决策 | 证据/预览 | 结果 | 理由 | 审批人 |
| --- | --- | --- | --- | --- | --- |
| 2026-08-27 | 方向 A「汇流/河流」：Fluma（主推）、Tributary | 会话文本 | Fluma 被选中 | 造词可注册性最好；2 音节；「河流/汇流」契合三层架构（河床/渡口/支流） | Matt |
| 2026-08-27 | 方向 B「万花筒」：Kaleido、Prism | 会话文本 | 拒绝 | 撞 Jupyter Kaleido / Kaleido 区块链等，检索成本高 | Matt |
| 2026-08-27 | 方向 C「拼图/经纬」：Tessera、Loom/Weft | 会话文本 | 拒绝 | Tessera 撞忠诚度/保险科技；Loom/Warp 撞 Apache/Cloudflare | Matt |
| 2026-08-27 | 方向 D「自由/漂移」：Drift、Unbound | 会话文本 | 拒绝 | Drift 撞营销 SaaS/赛车；Unbound 撞 DNS 软件，注册风险高 | Matt |
| 2026-08-27 | Fluma 弃用：撞名 fluma.in 及同名购物 App | web_search 证据（见证据登记） | 撤销第一次品牌名决策 | 组织占用成立，用户要求换名 | Matt |
| 2026-08-27 | 方向 A 延续「汇流/河流」替代候选：Talweg、Rillow；排除 Rilo/Confluo/Runnel/Lotic/Aflux | 清权初检（见证据登记） | Rillow 被选中 | 造词近零撞名；rill（小溪）+ willow 音感；沿用河流意象与三层前缀派生能力 | Matt |
| 2026-08-27 | Rillow 弃用：GitHub 组织被占 | 用户确认 + GitHub API 探测 | 撤销第二次品牌名决策 | 组织 handle 不可注册 | Matt |
| 2026-08-27 | 造词批提案：Rivolet/Rivoka/Velowa（+ Fluvent 因 ANSYS Fluent 音近自行排除） | 三表（GitHub/npm/crates）全绿 | 拒绝 | 词根随机、缺乏含义锚点 | Matt |
| 2026-08-27 | 乡村复合词批提案：Rilloway/Larkbrook/Wendbeck/Rivengate | 三表全绿 | 拒绝 | 气质不对味 | Matt |
| 2026-08-27 | 审美校准问答：大平台产品感 + 熟词根可读 | ask_user_question | 确立命名气质边界 | 前几轮被否源于气质错位，先校准再产名 | Matt |
| 2026-08-27 | 平台感造词批提案：Rivanta/Fluvanta/Cineonda/Rivoda/Volanta | 三表全绿 | 拒绝 | 整词太陌生 | Matt |
| 2026-08-27 | 熟词新组批：CineHarbor（cine 电影 + harbor 港湾）选中；CinePlay 为备选（历史同名影视产品，风险未核实）；路线 B（品牌与组织名解耦，如 `warpdotdev` 惯例）提出但未被采纳 | 三表全绿 + 会话问答 | CineHarbor 被选中 | 词根零学习成本、聚合隐喻（众流泊入同一港）与三层架构契合、注册表全绿 | Matt |

## 已批准的不变量

- **品牌名**：`CineHarbor`（品牌标记默认 CamelCase；包名、组织 handle、域名等机器标识统一全小写 `cineharbor`）。
- **GitHub 组织 handle**：`CineHarbor`（handle 大小写不敏感，当前空闲）。
- **三层命名规范**（待冻结，见开放问题）：
  - 核心：`cineharbor-core`
  - Web 客户端：`cineharbor-web`
  - 桌面客户端：`cineharbor-desktop`
  - 内容源 SDK：`cineharbor-addon-sdk`
  - 同步/存储（如沿用 Rust crate 拆分）：`cineharbor-storage` / `cineharbor-sync` / `cineharbor-profile`

### 图形与比例

待定（logo 概念方向探索中；词标两段式 CamelCase 提供「Cine + Harbor」双词素构图切入点）。

### 配色

待定（方向见开放问题；候选为深色底 + 青蓝「水光」主色，脱离旧 #000000 纯黑）。

### 字体与大小写

待定。

### 负空间与背景

待定。

### 锁定关系与间距

待定。

## 审批检查点

| 日期 | 检查点 | 决策 | 证据 | 审批人 |
| --- | --- | --- | --- | --- |
| 2026-08-27 | 品牌名选定（第一次） | 采纳 Fluma | 用户回复「就 Fluma」 | Matt |
| 2026-08-27 | 品牌名选定（第二次，替代 Fluma） | 采纳 Rillow；Talweg 为记录在案的备选 | 清权初检 + 会话问答（ask_user_question） | Matt |
| 2026-08-27 | 品牌名选定（第三次，替代 Rillow） | 采纳 CineHarbor；备选池与路线 B 记录在案 | 三表全绿 + 会话问答（ask_user_question） | Matt |

## 推断与未知

| 条目 | 分类 | 支撑证据 | 跟进 |
| --- | --- | --- | --- |
| CineHarbor 商标/域名可注册性 | 未知 | GitHub/npm/crates.io 三处已核实空闲；网页级撞名与商标库、whois 未查 | 正式清权检索（联网工具恢复后） |
| CineHarbor 是否有既有含义/语源冲突 | 推断 | cine-（电影，国际通用词根）+ harbor（港湾）均为高频英语词；本轮联网检索不可用，未能核实既有同名品牌 | 恢复联网后补查 |
| 备选池启用顺序 | 已决策 | CinePlay（需先撞名核实）→ Rivanta/Fluvanta/Cineonda/Rivoda/Volanta（熟度递减）；Talweg/Rillow 记录在案但分别有发音门槛/GitHub 占用问题 | 若 CineHarbor 清权受阻则依序启用 |
| 路线 B（品牌与组织名解耦） | 未采纳 | 用户未选择；惯例先例 `warpdotdev` / `obsidianmd` 记录在案 | 若未来 handle 纠纷再议 |
| 旧 MoonTV 品牌资产替换范围 | 推断 | `public/` 资产 + `luna-*` 类名 + `package.json` name | 待 logo 冻结后统一替换 |

## 开放问题

1. logo 图形概念方向（探索中，待用户选择；词标双词素为现成切入点）。
2. 配色基调确认（深色底 + 青蓝主色，还是其他）。
3. 商标/域名正式清权检索（联网检索恢复后执行；GitHub handle `CineHarbor`、npm `cineharbor`、crates.io `cineharbor` 当前均空闲，宜尽快占位）。
4. 三层架构仓库拆分的命名落地（`cineharbor-core` 等）与现有 `moontv` 包名迁移顺序。
