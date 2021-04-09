import time
import re
import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import csv
import time

import sys


def extract_numbers(string):
    lst_numbers = re.findall(r'\d+', string)
    str_number = ''.join([str(elem) for elem in lst_numbers])
    int_number = int(str_number)

    return int_number


class FundaAllSpider(scrapy.Spider):
    name = "all_houses_spider"
    start_urls = [sys.argv[1]]

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    output = "data/funda_" + today_str + ".csv"

    def __init__(self):
        # empty outputfile
        open(self.output, "w").close()

    def parse(self, response):

        page_numbers = response.xpath('//a/@data-pagination-page').extract()

        page_numbers = [extract_numbers(i) for i in page_numbers]
        page_links = [self.start_urls[0] + 'p' + str(i) + '/' for i in
                      range(2, max(page_numbers) + 1)]
        # page_links = page_links + self.start_urls
        page_links.insert(0, self.start_urls[0])
        page_links = [sys.argv[1]]

        for link in page_links:
            yield response.follow(url=link, callback=self.parse_desc)
            time.sleep(2)

    def parse_desc(self, response):
        with open(self.output, "a", newline="") as f:
            writer = csv.writer(f)

            funda_streets = response.xpath(
                '//h2[@class="search-result__header-title fd-m-none"]/text()'
            ).extract()
            funda_zip = response.xpath(
                '//h4[@class="search-result__header-subtitle fd-m-none"]/text()'
            ).extract()
            funda_price = response.xpath(
                '//span[@class="search-result-price"]/text()'
            ).extract()
            living = response.xpath(
                '//span[@title="Gebruiksoppervlakte wonen"]/text()'
            ).extract()
            land = response.xpath(
                '//span[@title="Perceeloppervlakte"]/text()'
            ).extract()
            rooms = response.xpath(
                '//ul[@class="search-result-kenmerken "]/li[2]/text()'
            ).extract()

            links = response.xpath(
                '//div[@class="search-result__header-title-col"]/a[1]/@href'
            ).extract()

            funda_streets = [
                street.replace('\r\n              ', '').replace('\r\n        ',
                                                                 '')
                for street in funda_streets]

            funda_zip = [zipcode.replace('\r\n            ', '').replace(
                '\r\n\r\n        ', '')
                for zipcode in funda_zip]

            funda_price = [extract_numbers(i) for i in funda_price]

            living = [extract_numbers(i) for i in living]

            rooms = [extract_numbers(i) for i in rooms]

            update_date = [datetime.date.today()] * len(funda_streets)

            df = pd.DataFrame(list(
                zip(funda_streets, funda_zip, funda_price, living, rooms,
                    links, update_date)),
                columns=['street', 'zip', 'price', 'living_area',
                         'nr_rooms', 'link', 'update_date'])

            lst_values = df.values.tolist()
            for i in lst_values:
                writer.writerow(i)


c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
})
c.crawl(FundaAllSpider)
c.start()
