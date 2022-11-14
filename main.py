import cloudscraper
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('test.db')

conn.execute('''CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);''')

cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
for row in cursor:
   print("ID = ", row[0])
   print("NAME = ", row[1])
   print("ADDRESS = ", row[2])
   print("SALARY = ", row[3], "\n")

print("Opened database successfully")

conn.close()

exit(1)

# confetti-aj1691-900   ->  confetti
# halloween-943806-012  ->  halloween
# mamba-mentality       ->  mamba-mentality
def remove_suffix(str):
    for x in range(2):
        i = len(str) - 1
        while i >= 0 and str[i] != '-':
            i -= 1
        if any(j.isdigit() for j in str[i : len(str)]):
            str = str[0 : i]
    return str

INPUT_FILE = "resources/input_shoes.csv"

url = "https://www.goat.com/search?query=nike+kyrie+4&size_converted=us_sneakers_men_8.5&product_condition=new_no_defects"

scraper = cloudscraper.create_scraper(delay=10,   browser={'custom': 'ScraperBot/1.0',})
req = scraper.get(url)
soup = BeautifulSoup(req.content, 'html.parser')


for url in soup.find_all('a'):
    try:
        sneaker_name = url.get('href')
        if not sneaker_name.startswith("/sneakers/kyrie-4-"):
            continue
        sneaker_name = sneaker_name.removeprefix("/sneakers/kyrie-4-")
        sneaker_name = remove_suffix(sneaker_name)
        thing = url.find(attrs={'data-qa': 'grid_cell_product_price'})
        print(sneaker_name + " " + thing.text)
    except:
        continue
