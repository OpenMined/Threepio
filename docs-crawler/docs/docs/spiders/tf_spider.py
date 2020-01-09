import re
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags



class ApiItem(scrapy.Item):
    code = scrapy.Field()
    function_name = scrapy.Field()
    args = scrapy.Field()
    kwargs = scrapy.Field()

class TfSpider(CrawlSpider):
    name = "tf"
    allowed_domains = ['tensorflow.org']
    start_urls = ['https://www.tensorflow.org/api_docs/python/tf']
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
