<div align="center">

# FitGirl Repacks 镜像库

[![GitHub Actions](https://github.com/Cvandia/fitgirl_repacks/actions/workflows/spider-workflow.yml/badge.svg)](https://github.com/Cvandia/fitgirl_repacks/actions/workflows/spider-workflow.yml)
[![License](https://img.shields.io/github/license/Cvandia/fitgirl_repacks.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Cvandia/fitgirl_repacks.svg)](https://github.com/Cvandia/fitgirl_repacks/commits/master)
[![Repository Size](https://img.shields.io/github/repo-size/Cvandia/fitgirl_repacks.svg)](https://github.com/Cvandia/fitgirl_repacks)
[![GitHub Stars](https://img.shields.io/github/stars/Cvandia/fitgirl_repacks.svg?style=social)](https://github.com/Cvandia/fitgirl_repacks/stargazers)

![](https://count.getloli.com/get/@fitgirl_repacks?theme=booru-lewd)

</div>

## 📖 项目简介
这是一个由 GitHub Actions 定时抓取并生成的 FitGirl Repacks 数据镜像，提供更方便的中文浏览入口。项目只整理公开页面中的游戏信息，不托管游戏文件。

## ✨ 功能
- 🔎 按关键词搜索游戏标题与相关信息
- 📚 分页浏览完整游戏索引
- 🔥 展示热门推荐游戏
- 🌓 支持浅色与深色主题切换
- 📦 保留 CSV 数据，便于下载和二次处理

## 🌐 在线使用
[打开 FitGirl Repacks 镜像库](https://cvandia.github.io/fitgirl_repacks/)

## 🛠️ 本地运行
项目是纯静态页面，无需安装 Node.js 或其他服务端依赖。

```bash
git clone https://github.com/Cvandia/fitgirl_repacks.git
cd fitgirl_repacks
```

随后使用浏览器打开 `index.htm` 即可。也可以使用 VS Code Live Server 等静态文件服务器访问。

运行 Python 爬虫需先安装 uv，在项目根目录执行：

```bash
uv sync --locked
uv run ruff check spider/spider.py
uv run --directory spider python spider.py
```

uv 会自动创建并使用 `.venv`，Python 版本由 `.python-version` 指定，依赖版本由 `uv.lock` 锁定。爬虫使用相对路径，需通过上述命令在 `spider` 目录运行。VS Code 中请选择 `.venv/Scripts/python.exe` 作为 Python 解释器。

## 📊 数据说明
- 数据来源：[FitGirl Repacks](https://fitgirl-repacks.site/)
- 当前数据更新时间：`2026-10-01`
- 当前收录数量：`6819` 款游戏
- 首页默认加载与本次抓取对应的 CSV 数据
- “热门推荐”来自 `data/popular-repacks.json`

README 下方的更新列表由抓取程序根据最近获取到的数据自动生成，展示最新收录的 10 条记录。

## 🔄 更新
最后更新时间 `2026-10-01`，共 `6819` 款游戏。
- The Handler of Dragons – v2.67
- FACEMINER – v2.4.1 + Bonus OST
- Woman Simulator – v1.0.20
- ENTITY: THE BLACK DAY – v1.01 + Operative DLC v0.2
- Kingdom Rush 6: Genesis TD – v1.00.44
- Garfield: Escape from Monday – v1.02.10
- Alaska Gold Fever – v2026.09.23.01 + 5 DLCs
- Nocturne – v1.0.0 + Supporter Pack DLC
- Le Mans Ultimate: WEC Full Access Bundle – v1.4.2 + 13 DLCs
- Pioneers of Pagonia: Gold Edition – v1.5.0-12845 + 6 DLCs/Bonuses
- ……

## 🤖 自动更新
GitHub Actions 按计划运行抓取程序，获取完整数据后生成新的 CSV、热门推荐和首页文件，并自动提交到仓库。你也可以在 [Actions 页面](https://github.com/Cvandia/fitgirl_repacks/actions) 查看运行状态。

## 数据保留策略
每周一北京时间 04:00 自动清理历史 CSV，仅保留最新的完整快照，保留热门榜单 JSON，并同步首页引用。清理前校验表头、列数、必填字段、时间、磁力链接、ID 唯一性，以及记录数不少于上次成功抓取数量；没有合格快照时停止，不删除文件。

历史快照没有逐页抓取记录，以上校验不能证明源站没有漏页；后续抓取遇到失败页或空页会终止，不发布新快照。

可手动运行 Weekly Data Cleanup 工作流，或在项目根目录执行 `python spider/archive.py --dry-run` 预览、`python spider/archive.py` 清理。此策略不重写 Git 历史，历史中的存储占用仍然保留。

## 📜 声明
本项目仅为数据镜像与索引页面，旨在帮助访问不便的用户浏览公开信息，不提供游戏下载服务，也不主张或鼓励侵犯版权的行为。请支持正版游戏，并在条件允许时优先访问原站。

## 🙏 感谢
- [FitGirl Repacks](https://fitgirl-repacks.site/)
