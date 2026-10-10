# China Travel Guide — 英文版中国旅游攻略站

面向欧美游客的免签热门城市深度攻略站。**Markdown 存内容 → 预渲染静态 HTML → Flask 托管**，SEO 友好、移动端优先。

## 快速开始

```bash
# 1. 构建静态站点（读取 content/*.md → 输出 build/）
python3 build_site.py

# 2. 启动服务（端口 8095）
python3 app.py

# 3. 访问
# http://127.0.0.1:8095/
```

## 目录结构

```
china_travel_guide/
├── site_config.py        # 站点配置：10 城元数据、5 指南、广告位、联盟链接
├── build_site.py         # 构建器：预渲染 + JSON-LD + TOC + sitemap + robots + 搜索索引
├── app.py                # Flask 托管 + 搜索 API + 健康检查
├── gen_drafts.py         # 批量生成占位文章（8 城）
├── verify_site.py        # 端到端验证脚本（39 项检查）
├── verify_jsonld.py      # JSON-LD 有效性验证（15 页）
├── verify_final.py       # 城市页 + 搜索 API 验证
├── content/
│   ├── guides/           # 实用指南（5 篇，独立于城市）
│   │   ├── visa-free-china.md
│   │   ├── payments-in-china.md
│   │   ├── high-speed-rail-china.md
│   │   ├── esim-china.md
│   │   └── safety-in-china.md
│   └── cities/           # 城市文章
│       ├── beijing/beijing-overview.md      # ✅ 完整
│       ├── shanghai/shanghai-overview.md    # ✅ 完整
│       └── xian/... (8 城 draft 占位)
├── templates/            # Jinja2 模板
├── static/               # CSS / JS / 图片
└── build/                # 构建产物（自动生成，勿手改）
```

## 如何添加内容（大富灌内容流程）

1. **新建文章**：在 `content/cities/<城市slug>/` 或 `content/guides/` 下新建 `.md` 文件
2. **Frontmatter 格式**（每篇必填）：

```markdown
---
title: "文章标题"
description: "SEO 描述（150 字内）"
keywords: "关键词, 逗号分隔"
date: 2026-10-10
updated: 2026-10-10
type: city-overview   # 或 guide
city: beijing         # 城市文章必填（对应 site_config.py 的 slug）
draft: true           # 占位文章标记（可选，发布时删除）
---
```

3. **正文用 Markdown**，支持表格、列表、引用块
4. **FAQ 板块**：`## FAQ` 标题下用 `**Q: ...?**` / `**A:** ...` 格式，自动生成 FAQPage JSON-LD
5. **重新构建**：`python3 build_site.py`（自动更新 sitemap、搜索索引、JSON-LD）

## 已实现功能

| 需求 | 状态 |
|---|---|
| 首页（10 城入口 + 热门攻略置顶） | ✅ |
| 城市总览页（每城 1 个，聚合文章） | ✅ |
| 文章页（模板板块 + TOC + 相关文章） | ✅ |
| 实用指南页（签证/支付/高铁/eSIM/安全） | ✅ 5 篇 |
| 关于页（信任建立） | ✅ |
| 搜索框（站内过滤） | ✅ 页面 + API |
| 面包屑导航 | ✅ |
| 移动端响应式（70% 手机访问） | ✅ 2 个断点 |
| 广告位预留（文章 3 位 + 侧边栏） | ✅ 占位未启用 |
| 联盟链接组件（Booking/Agoda/Klook） | ✅ 占位未启用 |
| JSON-LD（Article + FAQPage + BreadcrumbList） | ✅ 15/15 页 |
| sitemap.xml + robots.txt | ✅ 29 URL |
| 图片 WebP + 懒加载 | ⏳ 占位 SVG，上线换 WebP |
| Core Web Vitals | ⏳ 预渲染已达标，上线后实测 |
| Google Search Console + Bing Webmaster | ⏳ 上线当天挂 |

## 待办（等大富素材库）

- [ ] 8 城 draft 文章替换为完整内容（西安/成都/重庆/广州/深圳/杭州/桂林/张家界）
- [ ] 第 2 批：10 城各 2 篇核心攻略
- [ ] 第 3 批：长尾（美食/交通/景点）
- [ ] 域名确定后替换 `site_config.py` 的 `SITE.url`
- [ ] 真实图片替换占位 SVG（WebP 格式）
- [ ] 上线：挂 Search Console + Bing Webmaster

## 端口

- 服务端口：**8095**
- 健康检查：`GET /api/health`
- API 文档：`GET /api/docs`
