import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class ScikitLearnSpider(CrawlSpider):
    name = "sk"
    version = "0.23.1"
    allowed_domains = ['scikit-learn.org']
    start_urls = ['https://scikit-learn.org/stable/modules/classes.html']
    split_def = re.compile(r'^([\w\.]+)\(([\w,\s=\*\'\.\-]*)\)')

    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+\.html')),
            restrict_css='.section tbody td:first-child p'),
            callback='parse_api',),
    )

    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('.function > dt')
        if not fdef:
            return

        fdef = fdef[0]
        text = (remove_tags(fdef.get())
                .replace('\n', '')
                .replace(' ', '')
                .replace('[source]', ''))

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
