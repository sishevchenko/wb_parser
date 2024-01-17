import requests
import asyncio
import aiohttp
import urllib.parse
import json


ASYNC_MODE = True # Параметр для активации асинхронного режима
TARGET_ARTICLE: int = 180997293 # Искомый артикул
SEARCH_STRING: str = "футболка мужская" # Строка поиска


def get_article_position(target_articul: int, surch_string: str) -> int:
    encode_surch_string = urllib.parse.quote(surch_string) # В целом работает и без кодировки, но решил сделать идентичный оригинальному url
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&query={encode_surch_string}&resultset=catalog&sort=popular&spp=29&suppressSpellcheck=false"
    response = requests.get(url)
    for i, product in enumerate(response.json()["data"]["products"]):
        if product.get("id") == target_articul:
            return i + 1

async def async_get_article_position(target_articul: int, surch_string: str) -> int:
    encode_surch_string = urllib.parse.quote(surch_string) # В целом работает и без кодировки, но решил сделать идентичный оригинальному url
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&query={encode_surch_string}&resultset=catalog&sort=popular&spp=29&suppressSpellcheck=false"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = json.loads(await response.text())
            for i, product in enumerate(response_json["data"]["products"]):
                if product.get("id") == target_articul:
                    return i + 1

async def main():
    res = await async_get_article_position(TARGET_ARTICLE, SEARCH_STRING)
    print(res)


if __name__ == "__main__":
    if ASYNC_MODE:
        asyncio.run(main())
    else:
        print(get_article_position(TARGET_ARTICLE, SEARCH_STRING))
