import requests, asyncio, aiohttp
from bs4 import BeautifulSoup
import db


async def fetch(url, sem):
    async with sem:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            html = await response.text()

            # DEBUG
            print(f'\rRemained to download: {len(asyncio.all_tasks())}    ', end='')
    return html
    

def download_async(urls):
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(5)
    tasks = []

    for url in urls:
        tasks.append(fetch(url, sem))

    pages = loop.run_until_complete(asyncio.gather(*tasks))

    # DEBUG
    if len(urls) > 1:
        print()

    # loop.close()
    return pages


def download_sync(urls):
    amount = len(urls)
    pages = []

    for i in range(amount):
        # DEBUG 
        print(f"\rDownloading Page Number: {i+1}/{amount}", end='')
        
        r = requests.get(urls[i])

        # DEBUG
        print(f" || status code: {r.status_code}", end='')

        pages.append(r.content)
    
    if amount > 1:
        print()

    return pages


def scrap_data(cpu_name):
    
    scores = []
    pages = []


    # Define URL friendly search query
    cpu_name = str(cpu_name).replace(' ', '+')

    # Download the first page
    pages += download_async(["https://browser.geekbench.com/v5/cpu/search?utf8=%E2%9C%93&page=1&q=" + cpu_name])

    # Parse content
    soup = BeautifulSoup(pages[0], "lxml")

    # Get number of pages
    div = soup.select(".page-item:nth-last-child(2)")
    number_of_pages = 1 if len(div) == 0 else int(div[0].text.strip())

    # Create list of urls
    urls = [ ("https://browser.geekbench.com/v5/cpu/search?utf8=%E2%9C%93&page=" + str(i) + "&q=" + cpu_name) for i in range(2, number_of_pages+1) ]

    # Download these pages
    pages += download_async(urls)
    

    # Parse each page
    for i in range(number_of_pages):
        # DEBUG 
        print(f"\rProcessing Page Number: {i+1}/{number_of_pages}", end='')

        # Parse content
        soup = BeautifulSoup(pages[i], "html.parser")

        # Get single core scores
        singles = soup.select("div.list-col-inner > div.row > div.col-6:nth-child(4) > span.list-col-text-score")
        singles = [int(score.text.strip()) for score in singles]

        # Get multi core scores
        multies = soup.select("div.list-col-inner > div.row > div.col-6:nth-child(5) > span.list-col-text-score")
        multies = [int(score.text.strip()) for score in multies]

        # Add singles and multies to score table
        for i in range(len(singles)):
            scores.append([singles[i], multies[i]])
    
    print()
    return scores

