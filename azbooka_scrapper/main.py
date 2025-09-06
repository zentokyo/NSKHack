import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from constants import HEADERS, FIRST_URL, BASE_URL


async def get_azbooka_page(session: ClientSession) -> str:
    response = await session.get(FIRST_URL, headers=HEADERS)
    return await response.text()


def get_azbooka_links(page: str) -> list[str]:
    soup = BeautifulSoup(page, "html.parser")

    container = soup.find("div", class_="azbuka-zakupok__letters")
    elements = container.find_all("a", class_="azbuka-zakupok__letters_link")

    return [element["href"] for element in elements]


async def get_info_from_links(session: ClientSession, links: list[str]) -> None:
    for link in links:
        page = await get_page_from_link(session, link)

        soup = BeautifulSoup(page, "html.parser")

        await asyncio.sleep(0.4)
        container = soup.find("div", class_="azbuka-zakupok__content")
        header = container.find("h1")
        elements = container.find_all("p")

        element_text_list = [element.text for element in elements]
        create_markdown(header.text, element_text_list)


def create_markdown(header: str, text_list: list[str]) -> None:
    header = header.replace("/", "_")
    with open(f"md_files/{header}.md", "w", encoding="utf-8") as f:
        f.write(f"# {header}\n")
        for text in text_list:
            f.write(text + "\n")

async def get_page_from_link(session: ClientSession, link: str) -> str:
    page = await session.get(f"{BASE_URL}{link}", headers=HEADERS)
    return await page.text()


async def main():
    async with ClientSession() as session:
        azbooka_page = await get_azbooka_page(session)
        links = get_azbooka_links(azbooka_page)
        await get_info_from_links(session, links)


if __name__ == "__main__":
    asyncio.run(main())
