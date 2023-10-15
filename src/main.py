import database

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from csv import reader
from datetime import date

conn = database.init_db()

# confetti-aj1691-900   ->  confetti
# halloween-943806-012  ->  halloween
# mamba-mentality       ->  mamba-mentality
def remove_suffix(str):
    for x in range(2):
        i = len(str) - 1
        while i >= 0 and str[i] != '-':
            i -= 1
        if any(j.isdigit() for j in str[i: len(str)]):
            str = str[0: i]
    return str

def scrape(url):
    scraper = create_scraper(delay=10, browser={"custom": "ScraperBot/1.0"})
    req = scraper.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    print_list = []

    for url in soup.find_all("a"):
        try:
            sneaker_name = url.get("href")
            if not sneaker_name.startswith("/sneakers/kyrie-4-"):
                continue
            sneaker_name = sneaker_name.removeprefix("/sneakers/")
            sneaker_name = remove_suffix(sneaker_name)
            price = url.find(attrs={"data-qa": "grid_cell_product_price"})
            print_list.append((sneaker_name, price.text))
            database.insert(conn, sneaker_name, str(date.today()),
                            price.text.replace(",", "").replace("$", ""))
        except:
            continue

    print_list.sort(key = lambda x: x[0])
    for tup in print_list:
        print(tup[0] + " " + tup[1])

    conn.commit()

# https://www.goat.com/search?query=air+jordan+1+high&size_converted=us_sneakers_men_8.5&product_condition=new_no_defects&gender=men

INPUT_FILE = "../resources/input_shoes.csv"
with open(INPUT_FILE, "r") as file:
    csv_reader = reader(file)
    for row in csv_reader:
        for url in row:
            scrape(url)

conn.close()
