import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class NumpySpider(CrawlSpider):
    name = "numpy"
    version = "1.17.0"
    allowed_domains = ['scipy.org']
    start_urls = [f'https://docs.scipy.org/doc/numpy/reference/generated/']
    split_def = re.compile(r'^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+\.html')),
        ),
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
