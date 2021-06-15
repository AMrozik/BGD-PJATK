from bs4 import BeautifulSoup
from requests import get
import csv

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


def parse_area(area):
    return float(area.replace('Powierzchnia:', '').replace('m²', '').replace(',', '.').strip())


def parse_rooms(rooms):
    return int(rooms.replace('Liczba pokoi:', '').replace('pokoje', '').replace('pokój', '').replace('i więcej', '').strip())


page = get(URL)

bs = BeautifulSoup(page.content, 'html.parser')

with open('test.csv', 'w', newline='') as csvfile:

    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(["title", "location", "price", "area", "rooms"])

    for offer in bs.find_all('div', class_='offer-wrapper'):
        footer = offer.find('td', class_='bottom-cell')
        location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')[0]
        title = offer.find('strong').get_text().strip()
        price = parse_price(offer.find('p', class_='price').get_text().strip())
        link = offer.find('a')
        area = None
        rooms = None
        print(link['href'].startswith('https://www.olx.pl'))
        if link['href'].startswith('https://www.olx.pl'):
            page2 = get(link['href'])
            bs2 = BeautifulSoup(page2.content, 'html.parser')
            tags = []
            for block in bs2.find_all('li', class_='css-ox1ptj'):
                tags.append(block.find('p', class_='css-xl6fe0-Text eu5v0x0'))
            rooms = parse_rooms(tags[-1].get_text().strip())
            area = parse_area(tags[-2].get_text().strip())

        else:
            page2 = get(link['href'])

            bs2 = BeautifulSoup(page2.content, 'html.parser')
            details = bs2.find_all('div', class_='css-1ytkscc ev4i3ak0')

            area = parse_area(details[0].get_text().strip())
            rooms = details[1].get_text().strip()
            print(area, rooms)

        print(location, title, price, area, rooms)
        csv_writer.writerow([title, location, price, area, rooms])