import re
import aiohttp
import asyncio
import urllib.parse
from nonebot.log import logger
from bs4 import NavigableString, BeautifulSoup


class MCModScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def get_content(self, url: str):
        pattern = r"https?://[^/]+/([^/]+)/"
        match = re.search(pattern, url)
        if match:
            if match.group(1) == 'post':
                return await self.get_post(url)
            elif match.group(1) == 'item':
                return await self.get_item(url)
            elif match.group(1) in ('class', 'modpack'):
                return await self.get_profile(url)
        return None

    async def get_html(self, url: str):
        if not url:
            logger.error("错误：搜索查询不能为空。")
            return None

        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(url, timeout=15) as response:
                    response.raise_for_status()
                    return await response.text()
            except asyncio.TimeoutError:
                logger.error(f"错误：请求超时 ({url})")
            except aiohttp.ClientError as e:
                logger.error(f"错误：请求失败 ({url}) - {e}")
        return None

    async def search_mcmod(self, query: str, filter: int = 0, mold: int = 0):
        """
        在 MC百科 (search.mcmod.cn) 上搜索指定查询，并返回结果列表。

        Args:
            query (str): 要搜索的关键词。
            filter (int): 过滤器，0 表示无过滤，1 表示模组，2 表示整合包，3 表示资料，4 表示教程
        Returns:
            list: 包含搜索结果字典的列表，每个字典包含 'title', 'description', 'link'。
                  如果出错或找不到结果，则返回空列表或 None。
        """
        logger.info(f"正在搜索：{query}, 类别：{filter}")
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://search.mcmod.cn/s?key={encoded_query}&filter={filter}&mold={mold}"
        html = await self.get_html(search_url)
        if not html:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        result_items = soup.find_all('div', class_='result-item')

        extracted_results = []
        for item in result_items:
            title, link, description = None, None, None

            head_div = item.find('div', class_='head')
            if head_div:
                link_tag = head_div.find('a', recursive=False)
                title = link_tag.get_text(strip=True)
                link = link_tag.get('href')

            body_div = item.find('div', class_='body')
            texts = []
            for child in body_div.contents:
                if not getattr(child, 'name', None) or child.name != 'p':
                    text = child.strip() if isinstance(
                        child, NavigableString) else child.get_text(strip=True)
                    if text:
                        texts.append(text)
            description = "".join(texts)

            if title:
                extracted_results.append({
                    'title': title,
                    'description': description,
                    'link': link
                })
        # print(len(extracted_results))
        return extracted_results

    async def get_item(self, url: str):
        html = await self.get_html(url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        result_item = soup.find('div', class_='item-text')

        item_name_tag = result_item.find('div', class_='itemname').find('h5')
        item_name = item_name_tag.get_text(strip=True)

        content_html = result_item.find('div', class_='item-content')
        content_list = self.__parse_content(content_html)

        return item_name, content_list

    async def get_post(self, url: str):
        """教程"""
        html = await self.get_html(url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        result_item = soup.find('div', class_='post-row')

        item_name_tag = result_item.find('div', class_='postname').find('h5')
        item_name = item_name_tag.get_text(strip=True)

        content_html = result_item.find('div', class_='text')
        content_list = self.__parse_content(content_html)

        return item_name, content_list

    async def get_profile(self, url: str):
        html = await self.get_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        # 标题
        title_div = soup.find('div', class_='class-title')
        title = title_div.h3.get_text()
        if title_div.h4:
            title += '\n' + title_div.h4.get_text()
        # mc 版本
        mcver_li = soup.find('li', class_='mcver').ul
        mcver = ''
        for ul in mcver_li.children:
            mcver += ('\n' if mcver else '') + ul.get_text(separator=' ')
        # 正文
        content_html = soup.select_one('li.text-area.common-text')

        content_list = self.__parse_content(content_html)
        logger.info(f"mcver: {mcver}")
        return title, content_list, mcver

    def __parse_content(self, html: BeautifulSoup):
        """解析正文内容，返回一个列表，包含图片、标题和文本。"""
        parsed_data = []
        for tag in html.children:
            if tag.name in ('p', 'div', 'pre', 'table'):
                title_span = tag.find('span', class_='common-text-title')
                content_text = tag.get_text(strip=True)
                # 图片
                figures = tag.find_all('span', class_='figure')

                if figures:
                    for figure in figures:
                        img_tag = figure.find('img')
                        img_url = img_tag.get('data-src') or img_tag.get(
                            'src')  # Get src or data-src
                        # caption_tag = figure.find('span', class_='figcaption')

                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        if "mcmod.cn" not in img_url:
                            img_url = "https://www.mcmod.cn/images/loadfail.gif"
                        item = {"type": "image", "url": img_url}
                        if img_comment := figure.get_text(strip=True):
                            item["content"] = img_comment
                        parsed_data.append(item)

                # Case 2: Paragraph contains a title
                elif title_span or tag.get('style') == 'text-indent: 0em;':
                    # title_text = tag.get_text(strip=True)
                    item = {
                        "type": "title",
                        "content": content_text
                    }
                    parsed_data.append(item)

                elif content_text:
                    item = {"type": "text",
                            "content": content_text.replace('\xa0', ' ')}
                    parsed_data.append(item)

            elif tag.name in ('ul', 'ol'):
                list_items = tag.find_all('li')
                for li in list_items:
                    li_text = li.get_text(strip=True)
                    if li_text:
                        item = {"type": "text", "content": li_text}
                        parsed_data.append(item)
        return parsed_data


if __name__ == "__main__":
    async def main():
        scraper = MCModScraper()
        # 示例：获取模组包简介
        result = await scraper.get_content("https://www.mcmod.cn/class/6453.html")
        print(result)

    asyncio.run(main())
