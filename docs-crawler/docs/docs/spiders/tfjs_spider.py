import scrapy
from w3lib.html import remove_tags


class TfjsSpider(scrapy.Spider):
    name = "tfjs"

    def start_requests(self):
        urls = [
            'https://js.tensorflow.org/api/latest/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fdef = response.css('div.function > div.symbol-header')
        defs = []
        for selector in fdef:
            text = remove_tags(selector.get())\
                .replace('\n', '')\
                .replace(' ', '')\
                .replace('Source', '')\
                .replace('function', '')\
                .replace('method', '')
            defs.append(text)
        
        with open('tfjs-functions.txt', 'w') as f:
            f.write('\n'.join(defs))

        print('\n'.join(defs))