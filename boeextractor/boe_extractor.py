import scrapy
import re
from scrapy.crawler import CrawlerProcess

ADITTIONAL_DOCS = [
    'https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444', # CODIGO PENAL
    'https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229', # CONSTITUCIÓN
    'https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763' # CÓDIGO CIVIL
]

class BoeSpider(scrapy.Spider):

    def __init__(self, pages):
        super().__init__()
        self.pages = pages


    def start_requests(self):
        start_url = 'https://www.boe.es/buscar/legislacion.php?accion=Mas&id_busqueda=_cGhXenk1dEdldTRsT0JSRFkzVjBNNGpJWlg3aFBkZ0V5cTRMWTRJMjZDdjI1aEZVOWV5dENxWWRpUzNlQ0phVXdlR0xwV0RVNCtyb1hWZnNBaithamVzZWp1cjBSN0xqbkhzOGZnVGs3enhBTDJ4SDBKTENoSXU2ckRZUkpGdGtEdHErN0RCWTRKcWNFMSt3cEJIbnp3ekVIMVhLZjliTnk1RzAvTHowNFdjPQ%2C%2C-0-2000&page_hits=2000&sort_field%5B0%5D=FPU&sort_order%5B0%5D=desc'
        yield scrapy.Request(url=start_url, callback=self.parseSearch)

        for url in ADITTIONAL_DOCS:
            yield scrapy.Request(url, callback=self.parseArticle)
        

    def parseSearch(self, response):
        self.pages -= 1
        
        for result in response.css("a.resultado-busqueda-link-defecto::attr(href)").getall():
            if '=BOE-' in result or '=DOUE-' in result:
                yield response.follow(result, callback=self.parseArticle)
        
        if self.pages > 0:
            next = response.xpath('//a[span/@class="pagSig"]/@href').get()
            yield response.follow(next, callback=self.parseSearch)

        
    def parseArticle(self, response):
        filename = re.search(r'.*id=(.*)', response.url).group(1)
        with open('corpus/' + filename, 'wb') as f:
            for parrafo in response.xpath('//p[@class="parrafo"]/text()').getall():
                parrafo = re.sub(r'\.', '\n', parrafo)
                f.write(bytes(parrafo + '\n', 'utf-8'))
        print(f'Saved file {filename}')


crawler = CrawlerProcess(settings={
    'LOG_LEVEL': 'ERROR'
})
crawler.crawl(BoeSpider, pages=2)
crawler.start()
