import re
import scrapy
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TfSpider(CrawlSpider):
    name = "tf"
    version = "2.1"
    allowed_domains = ['tensorflow.org']
    start_urls = [f'https://www.tensorflow.org/versions/r{version}/api_docs/python/tf']
    split_def = re.compile('^([\w\.]+)\((.*)\)$')

    rules = (
        Rule(LinkExtractor(
                allow=(re.compile('.+api_docs\/python\/tf')),
                restrict_css='.devsite-nav-title'), 
            callback='parse_api',),
    )

    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        item = ApiItem()
        function_header = response.css('.lang-python')
        if len(function_header) == 0:
            return
        text = remove_tags(function_header.get())\
            .replace('\n', '')\
            .replace(' ', '')

        split = self.split_def.match(text)
        if split is None:
            return
        
        function_name = split.groups()[0].split('.')[-1]
        params = split.groups()[1].split(',')
        args = [p for p in params if '=' not in p]
        kwargs = [p.split('=') for p in params if '=' in p]

        if '__' in text or 'compat' in text:
            return


        item['code'] = text
        item['function_name'] = function_name
        item['args'] = args
        item['kwargs'] = kwargs

        yield item
