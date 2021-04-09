import sys
import scrapy
from scrapy.crawler import CrawlerProcess


class HtmlDownloadSpider(scrapy.Spider):
    name = "html_download_spider"
    start_urls = [sys.argv[1]]

    def parse(self, response):
        path = 'html_pages/'
        filename = path + sys.argv[1].split('/')[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)


c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
})
c.crawl(HtmlDownloadSpider)
c.start()
