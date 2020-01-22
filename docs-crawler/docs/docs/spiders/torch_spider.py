import re
import scrapy
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TorchSpider(CrawlSpider):
    name = "torch"
    version = "1.4.0"
    allowed_domains = ['pytorch.org']
    start_urls = [f'https://pytorch.org/docs/{version}/index.html']
    split_def = re.compile('^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

    rules = (
        Rule(LinkExtractor(
                allow=(re.compile('.+\.html')),
                restrict_css='.toctree-l1'), 
            callback='parse_api',),
    )
    
    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('dl.function > dt')
        defs = []
        for selector in fdef:
            text = (remove_tags(selector.get())
                    .replace('\n', '')
                    .replace(' ', '')
                    .replace('[source]', ''))
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