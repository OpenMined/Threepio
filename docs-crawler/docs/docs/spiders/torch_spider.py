import scrapy
from w3lib.html import remove_tags


class TorchSpider(scrapy.Spider):
    name = "torch"

    def start_requests(self):
        urls = [
            'https://pytorch.org/docs/stable/torch.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fdef = response.css('dl.function > dt')
        defs = []
        for selector in fdef:
            text = remove_tags(selector.get()).replace('\n', '')
            defs.append(text)
        
        with open('torch-functions.txt', 'w') as f:
            f.write('\n'.join(defs))

        print('\n'.join(defs))