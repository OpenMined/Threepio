import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class KerasSpider(CrawlSpider):
    name = "keras"
    version = "2.3.0"
    allowed_domains = ['keras.io']
    start_urls = ['https://keras.io/api/']
    split_def = re.compile(r'^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

    rules = (
        Rule(LinkExtractor(
            restrict_css='.k-content li'),
            callback='parse_api',),
    )

    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('h3 + .codehilite')
        defs = []

        if len(fdef) == 0:
            return

        for selector in fdef:
            text = (remove_tags(selector.get())
                    .replace('\n', '')
                    .replace(' ', '')
                    .replace('[source]', ''))
            if '(' not in text and ')' not in text:
                continue

            defs.append(text)
        for text in defs:
            split = self.split_def.match(text)

            if split is None:
                continue

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
