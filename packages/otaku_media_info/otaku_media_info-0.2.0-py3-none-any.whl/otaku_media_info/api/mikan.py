import requests
from bs4 import BeautifulSoup


def search(keyword: str):
    session = requests.Session()

    res = session.get(
        f"https://mikanani.me/Home/Search?searchstr={keyword}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        },
    )

    bs = BeautifulSoup(res.text, "html.parser")

    bs = bs.select_one(".central-container .an-ul a[href]")

    href = bs.attrs["href"]

    res = session.get(f"https://mikanani.me{href}")

    bs = BeautifulSoup(res.text, "html.parser")

    bs = bs.select_one(".pull-left.leftbar-container")

    title = bs.select_one(".bangumi-title")
    title = title.text.strip() if title else None

    infos = bs.select(".bangumi-info")

    infos = [info.text.strip() for info in infos]

    return {
        "title": title,
        "infos": infos,
    }


result = search("Aru Majo ga Shinu Made")

print(result)
