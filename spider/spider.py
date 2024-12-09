import os
import csv
import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from datetime import datetime
from loguru import logger
from rich.progress import Progress

site_url = "https://fitgirl-repacks.site"
sem = asyncio.Semaphore(3)  # Limit to 3 concurrent tasks


async def fetch_page(session, url):
    async with sem:
        async with session.get(url) as response:
            return await response.text()


async def fetch_data(session, page):
    url = f"{site_url}/page/{page}"
    logger.info(f"正在爬取第 {page} 页")
    page_content = await fetch_page(session, url)
    soup = BeautifulSoup(page_content, "html.parser")
    articles = soup.find_all("article")
    return articles


async def process_articles(session, page, progress, task_id):
    articles = await fetch_data(session, page)
    data_list = []
    now_article = 0
    for article in articles:
        now_article += 1
        article_title_element = article.find("h1", class_="entry-title")
        article_time_element = article.find("time", class_="entry-date")
        article_link_element = article.find(
            "a", href=lambda href: href and href.startswith("magnet:")
        )
        article_cover_element = article.find("img", width="150")
        article_description_element = article.find("h3", string="Repack Features")
        article_content_element = article.select_one(
            "div.su-spoiler-title:-soup-contains('Game Description') + div.su-spoiler-content"
        )
        if article_link_element:
            article_id = article.get("id").split("-")[-1]
            logger.info(f"√ 已保存第 {now_article}/{len(articles)} 条数据")
            article_title = (
                article_title_element.text.strip() if article_title_element else None
            )
            article_time = (
                article_time_element.get("datetime") if article_time_element else None
            )
            article_link = article_link_element.get("href")
            article_cover = (
                article_cover_element.get("src") if article_cover_element else None
            )
            article_description = (
                article_description_element.find_next_sibling().text.strip()
                if article_description_element
                else None
            )
            article_content = (
                article_content_element.text.strip()
                if article_content_element
                else None
            )
            data_list.append(
                [
                    article_id,
                    article_title,
                    article_time,
                    article_link,
                    article_cover,
                    article_description,
                    article_content,
                ]
            )
        else:
            logger.warning(f"× 抛弃第 {now_article}/{len(articles)} 条数据")
        progress.update(task_id, advance=1)
    return data_list


async def main():
    async with aiohttp.ClientSession() as session:
        response = await fetch_page(session, site_url)
        soup = BeautifulSoup(response, "html.parser")
        page_links = soup.find_all("a", class_="page-numbers")
        start_page = 1
        end_page = max(
            int(link.get_text()) for link in page_links if link.get_text().isdigit()
        )

        if end_page < start_page:
            logger.error("未获取到有效页码，程序中止")
            os._exit(0)

        all_data = []
        with Progress(
            *Progress.get_default_columns(),
            "[yellow]{task.completed}/{task.total}",
        ) as progress:
            task_id = progress.add_task(
                "爬取中...", total=(end_page - start_page + 1) * 10
            )
            for i in range(start_page, end_page + 1, 3):
                tasks = [
                    process_articles(session, page, progress, task_id)
                    for page in range(i, min(i + 3, end_page + 1))
                ]
                for task in asyncio.as_completed(tasks):
                    data = await task
                    all_data.extend(data)
                    if len(all_data) % 6 == 0:
                        pause_time = random.randint(6, 12)
                        logger.info(f"暂停 {pause_time} 秒")
                        await asyncio.sleep(pause_time)

        config_file = "./config.txt"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                previous_count = int(f.read())
        else:
            previous_count = 0
        logger.info(f"共获取到 {len(all_data)} 条有效数据，上次 {previous_count} 条")

        if len(all_data) >= previous_count:
            save_path = "../data"
            os.makedirs(save_path, exist_ok=True)
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            csv_file = os.path.join(save_path, f"repacks-{current_time}.csv")
            with open(csv_file, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "标题", "时间", "链接", "封面", "说明", "简介"])
                writer.writerows(all_data)
            logger.info(f"数据文件 {csv_file} 已更新")

            with open(config_file, "w") as f:
                f.write(str(len(all_data)))
            logger.info(f"配置文件 {config_file} 已更新")

            template_file = "./readme.txt"
            md_file = "../README.md"
            with open(template_file, "r", encoding="utf-8") as f:
                template_content = f.read()
            template_content = template_content.replace(
                "{{lastupdated}}",
                f"{current_time[:4]}-{current_time[4:6]}-{current_time[6:8]}",
            )
            template_content = template_content.replace(
                "{{datalength}}", str(len(all_data))
            )
            for i in range(min(10, len(all_data))):
                template_content = template_content.replace(
                    "{{articletitle}}", all_data[i][1], 1
                )
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(template_content)
            logger.info(f"README 文件 {md_file} 已更新")

            template_file = "./template.txt"
            html_file = "../index.htm"
            with open(template_file, "r", encoding="utf-8") as f:
                template_content = f.read()
            template_content = template_content.replace("{{lastupdated}}", current_time)
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(template_content)
            logger.info(f"HTML 模板 {html_file} 已更新")
        else:
            logger.warning("爬取内容不完整，放弃数据更新")


if __name__ == "__main__":
    asyncio.run(main())
