# China Travel Guide — 英文版中国旅游攻略站

面向欧美游客的免签热门城市深度攻略站。**Astro 5 静态站点**，SEO 优先，可部署到 Cloudflare Pages。

## 技术栈

- **Astro 5**（静态站点生成，Markdown 内容集合）
- **@astrojs/sitemap**（自动 sitemap）
- **@astrojs/rss**（RSS 支持）
- 前端实时搜索（fetch search-index.json 过滤，零后端）
- Cloudflare Pages 部署（wrangler.toml + GitHub Actions）

## 快速开始

```bash
# 开发
npm run dev

# 构建（生成 dist/ + sitemap + search-index.json）
npm run build

# 预览
npm run preview
```

## 目录结构

```
china_travel_guide/
├── src/
│   ├── content/
│   │   ├── articles/       # 文章（6 篇：签证/支付/高铁/eSIM/北京/上海）
│   │   └── cities/         # 10 城元数据
│   ├── components/         # AdSlot / AffiliateLink / Breadcrumb / RelatedArticles / TOC
│   ├── layouts/            # BaseLayout（含搜索框 + JSON-LD）
│   └── pages/              # index / cities / guides / about / 404
├── scripts/
│   └── generate-search-index.mjs  # 构建后生成搜索索引
├── public/                 # 静态资源
├── astro.config.mjs        # Astro 配置（sitemap 集成）
├── wrangler.toml           # Cloudflare Pages 配置
├── .github/workflows/deploy.yml  # CI/CD 部署
└── flask_version/          # Flask 原型备份（已弃用，勿用）
```

## 内容管理（大富灌内容流程）

1. **城市文章**：`src/content/articles/<slug>.md`，frontmatter 含 `city` 字段关联城市
2. **城市元数据**：`src/content/cities/<slug>.md`（名称、描述、坐标、标签）
3. **FAQ**：frontmatter 的 `faq` 数组（question/answer），自动生成 FAQPage JSON-LD
4. **构建**：`npm run build`（自动更新 sitemap + search-index.json）

## 需求覆盖

| 需求 | 状态 |
|---|---|
| 首页（10 城入口 + 热门攻略置顶） | ✅ |
| 城市总览页（每城 1 个，聚合文章） | ✅ 10 城 |
| 文章页（模板板块 + TOC + 相关文章） | ✅ |
| 实用指南页（签证/支付/高铁/eSIM/安全） | ✅ 4 篇（安全待补） |
| 关于页（信任建立） | ✅ |
| 搜索框（站内实时过滤） | ✅ 前端搜索 |
| 面包屑导航 | ✅ |
| 移动端响应式 | ✅ |
| 广告位预留（文章 3 位 + 侧边栏） | ✅ 占位未启用 |
| 联盟链接组件（Booking/Agoda/Klook） | ✅ 占位未启用 |
| JSON-LD（Article + FAQPage + BreadcrumbList） | ✅ |
| sitemap.xml + robots.txt | ✅ |
| Cloudflare Pages 部署 | ✅ 配置就绪 |

## 待办

- [ ] 安全指南（safety）文章
- [ ] 8 城核心攻略（第 2 批）
- [ ] 长尾内容（美食/交通/景点，第 3 批）
- [ ] 域名确定后替换 `astro.config.mjs` 的 `site`
- [ ] 真实图片（WebP）替换占位
- [ ] 上线：挂 Search Console + Bing Webmaster

## 端口

- 开发/预览：**4321**
