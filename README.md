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

## 📊 数据说明
- 数据来源：[FitGirl Repacks](https://fitgirl-repacks.site/)
- 当前数据更新时间：`2026-09-25`
- 当前收录数量：`6806` 款游戏
- 首页默认加载与本次抓取对应的 CSV 数据
- “热门推荐”来自 `data/popular-repacks.json`

README 下方的更新列表由抓取程序根据最近获取到的数据自动生成，展示最新收录的 10 条记录。

## 🔄 更新
最后更新时间 `2026-09-25`，共 `6806` 款游戏。
- Escape Simulator 2 – v22719r + 2 DLCs/Bonuses
- Brave New Wonders
- Shape of Dreams – v1.4.0.13 + DLC
- Tenebris: Terra Incognita
- Sunken Realms
- MindsEye – v1527350/8332038 + 10 DLCs
- DeathSprint 66 – Build 17155957
- Demonic Mahjong – v0.2.67 + 2 DLCs/Bonuses
- The Alighieri Circle: Dante’s Bloodline
- Granblue Fantasy Versus: Rising – Legendary Edition, v2.61 + 64 DLCs/Bonuses
- ……

## 🤖 自动更新
GitHub Actions 按计划运行抓取程序，获取完整数据后生成新的 CSV、热门推荐和首页文件，并自动提交到仓库。你也可以在 [Actions 页面](https://github.com/Cvandia/fitgirl_repacks/actions) 查看运行状态。

## 📜 声明
本项目仅为数据镜像与索引页面，旨在帮助访问不便的用户浏览公开信息，不提供游戏下载服务，也不主张或鼓励侵犯版权的行为。请支持正版游戏，并在条件允许时优先访问原站。

## 🙏 感谢
- [FitGirl Repacks](https://fitgirl-repacks.site/)
