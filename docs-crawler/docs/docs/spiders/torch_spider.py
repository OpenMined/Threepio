import re
import scrapy
from docs.items import ApiItem
from w3lib.html import remove_tags


class TorchSpider(scrapy.Spider):
    name = "torch"
    split_def = re.compile('^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

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

        for text in defs:
            split = self.split_def.match(text)
            if split is None:
                return
            
            function_name = split.groups()[0].split('.')[-1]
            params = split.groups()[1].split(',')
            args = [p for p in params if '=' not in p]
            kwargs = [p.split('=') for p in params if '=' in p]

            item = ApiItem()
            item['code'] = text
            item['function_name'] = function_name
            item['args'] = args
            item['kwargs'] = kwargs
            yield item

        print('\n'.join(defs))