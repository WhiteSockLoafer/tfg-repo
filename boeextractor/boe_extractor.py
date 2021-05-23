import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging


class BoeSpider(scrapy.Spider):
    name = "articulos"

    def start_requests(self):
        url = 'https://www.boe.es/buscar/legislacion.php?accion=Mas&id_busqueda=_cGhXenk1dEdldTRsT0JSRFkzVjBNNGpJWlg3aFBkZ0V5cTRMWTRJMjZDdjI1aEZVOWV5dENxWWRpUzNlQ0phVXdlR0xwV0RVNCtyb1hWZnNBaithamVzZWp1cjBSN0xqbkhzOGZnVGs3enhBTDJ4SDBKTENoSXU2ckRZUkpGdGtEdHErN0RCWTRKcWNFMSt3cEJIbnp3ekVIMVhLZjliTnk1RzAvTHowNFdjPQ%2C%2C-0-2000&page_hits=2000&sort_field%5B0%5D=FPU&sort_order%5B0%5D=desc'
        yield scrapy.Request(url=url, callback=self.parseSearch)

    def parseSearch(self, response):
        for result in response.css("a.resultado-busqueda-link-defecto::attr(href)").getall():
            yield response.follow(result, callback=self.parseArticle)

    def parseArticle(self, response):
        filename = re.search(r'.*id=(.*)', response.url).group(1)
        with open('corpus/' + filename, 'wb') as f:
            for parrafo in response.xpath('//p[@class="parrafo"]/text()').getall():
                parrafo = re.sub(r'\. |\.$', '\n', parrafo)
                f.write(bytes(parrafo, 'utf-8'))
        print(f'Saved file {filename}')


crawler = CrawlerProcess(settings={
    'LOG_LEVEL': 'ERROR'
})
crawler.crawl(BoeSpider)
crawler.start()
