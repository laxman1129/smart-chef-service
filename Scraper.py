import requests
from bs4 import BeautifulSoup
import string


def parse_page(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # table = soup.find_all('table', {"width": "600"})
    table_rows = soup.find_all('tr')
    i = 0
    for tr in table_rows:
        td1 = soup.find('td', {"valign": "top", 'width': '150'}).find('b')
        td2 = soup.find('td', {"valign": "top", 'width': '450'})
        print(td1, td2)
        i = i+1

url_a = 'https://theodora.com/food/index.html'
parse_page(url_a)

# for page in list(string.ascii_lowercase):
#     if 'a' == page:
#         url_a = 'https://theodora.com/food/index.html'
#         parse_page(url_a)
#     else:
#         url_page = f'https://theodora.com/food/culinary_dictionary_food_glossary_{page}.html'
#         parse_page(url_page)
