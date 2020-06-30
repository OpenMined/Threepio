# _*_ coding: utf-8 -*-


# Crawl modules in the TensorFlow docs to extract functions
#
# To understand how CrawlSpider works, See documentation in
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TfSpider(CrawlSpider):
    name = "tf" # Name of the web crawler
    version = "2.1" # Version of TesnorFlow documentation to crawl
    allowed_domains = ['tensorflow.org'] # Crawls only links from TensorFlow


    # Base URL for crawling
    start_urls = [
        f'https://www.tensorflow.org/versions/r{version}/api_docs/python/tf']

    
    # Regex rules for compiling a string to a Regex object.
    split_def = re.compile(r'^([\w\.]+)\((.*)\)$')


    # Rule(), guides the crawler starting at
    # The reponse of the links direct to different TensorFlow modules
    # and are passed to parse_api() for crawling.
    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+api_docs\/python\/tf')), # allow the links under api_docs
            restrict_css='.devsite-nav-title'), # Starts crawling from .devsite-nav-title.
            callback='parse_api',), # calls parse_api() with response.
    )


    # The parse_api() method is the callback method that parses the response 
    # from each link extracted with the rule above.
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
