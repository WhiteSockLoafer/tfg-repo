import sys
import scrapy
import re
from scrapy.crawler import CrawlerProcess

ADITTIONAL_DOCS = [
    'https://www.boe.es/buscar/act.php?id=BOE-A-1889-4763',     # CÓDIGO CIVIL
    'https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229',    # CONSTITUCIÓN
    'https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444',    # CODIGO PENAL
    'https://www.boe.es/buscar/act.php?id=BOE-A-2000-323',      # LEY ENJUICIAMIENTO CIVIL
    'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430'     # ESTATUTO DE LOS TRABAJADORES
]

class BoeSpider(scrapy.Spider):

    name = "articulos"

    def __init__(self, pages, corpus_dir, start_url):
        super().__init__()
        self.pages = pages
        self.corpus_dir = corpus_dir
        self.start_url = start_url


    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parseSearch)

        for url in ADITTIONAL_DOCS:
            yield scrapy.Request(url, callback=self.parseArticle)
        

    def parseSearch(self, response):
        self.pages -= 1
        
        for result in response.css("a.resultado-busqueda-link-defecto::attr(href)").getall():
            if '=BOE-' in result:
                yield response.follow(result, callback=self.parseArticle)
        
        if self.pages > 0:
            next = response.xpath('//a[span/@class="pagSig"]/@href').get()
            yield response.follow(next, callback=self.parseSearch)

        
    def parseArticle(self, response):
        filename = re.search(r'.*id=(.*)', response.url).group(1)
        with open(self.corpus_dir + '/' + filename, 'wb') as f:
            for parrafo in response.xpath('//p[@class="parrafo"]/text()|//p[@class="parrafo_2"]/text()').getall():
                parrafo = re.sub(r'\.', '\n', parrafo)
                f.write(bytes(parrafo + '\n', 'utf-8'))
        print(f'Saved file {filename}')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        crawler = CrawlerProcess(settings={
            'LOG_LEVEL': 'ERROR'
        })
        crawler.crawl(BoeSpider, pages=int(sys.argv[1]), corpus_dir=sys.argv[2], start_url=sys.argv[3])
        crawler.start()
