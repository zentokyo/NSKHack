import asyncio
import time

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from fz_scrapper.constants import LINKS, HEADERS


async def get_fz_page(session: ClientSession, link: str) -> str:
    response = await session.get(link, headers=HEADERS)
    return await response.text()


def get_info_from_page(page: str) -> tuple[str, list[str]]:
    soup = BeautifulSoup(page, "html.parser")

    time.sleep(0.4)

    container = soup.find("div",
                          class_="field field--name-body field--type-text-with-summary field--label-hidden field__item")
    header = soup.find("h1", class_="article-header__title")
    header_text_block = header.find("span")

    return header_text_block.text, [element.text for element in container if element.text is not None]


def create_markdown(header: str, text_list: list[str]) -> None:
    header = header.replace("/", "_")
    with open(f"md_files/{header}.md", "w", encoding="utf-8") as f:
        f.write(f"# {header}\n")
        for text in text_list:
            f.write(text + "\n")


async def main():
    async with ClientSession() as session:
        for link in LINKS:
            fz_page = await get_fz_page(session, link)
            header, text = get_info_from_page(fz_page)
            create_markdown(header, text)



if __name__ == "__main__":
    asyncio.run(main())
