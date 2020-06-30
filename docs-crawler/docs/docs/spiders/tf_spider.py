# _*_ coding: utf-8 -*-

# Crawl modules in the TensorFlow docs to extract functions

# To understand how CrawlSpider works, See documentation in
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TfSpider(CrawlSpider):
    name = "tf"  # Name of the web crawler
    version = "2.1"  # Version of TesnorFlow documentation to crawl
    allowed_domains = ['tensorflow.org']  # Crawls only links from TensorFlow

    # Base URL for crawling
    start_urls = [
        f'https://www.tensorflow.org/versions/r{version}/api_docs/python/tf']

    # Regex rules for compiling a string to a Regex object.
    # Here the rules match on to two groups and expect a
    # fucntion call similar to foo.bar(arg1, arg2)
    # the first group refers to foo.bar
    # the second group refers to arg1, arg2
    split_def = re.compile(r'^([\w\.]+)\((.*)\)$')

    # Rule(), guides the crawler starting at
    # https://www.tensorflow.org/api_docs/python/tf to look for
    # the selector '.devsite-nav-title' to extract links.
    # The reponse of the links direct to different TensorFlow modules
    # and are passed to parse_api() for crawling.
    rules = (
        Rule(LinkExtractor(
            # Allows the links under api_docs.
            allow=(re.compile(r'.+api_docs\/python\/tf')),
            # Starts crawling from .devsite-nav-title.
            restrict_css='.devsite-nav-title'),
            callback='parse_api',),  # Calls parse_api() with response.
    )

    # The parse_api() method is the callback method that parses the response
    # from each link extracted with the Rule above.
    # The response is a webpage containing documentations of the functions
    # for that particular TensorFlow module.
    # The goal is to process the function call format inorder to yield.
    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        item = ApiItem()

        # Crawls the selector to create a list of each python doc.
        function_header = response.css('.lang-python')
        if len(function_header) == 0:
            return

        text = remove_tags(function_header.get())\
            .replace('\n', '')\
            .replace(' ', '')
        # Uses the Regex rules to compile the function call
        split = self.split_def.match(text)
        if split is None:
            return

        # Extracts only the function name from the Regex encoded text
        function_name = split.groups()[0].split('.')[-1]

        # Extracts every function input parameter and stores in a list
        params = split.groups()[1].split(',')

        # Caches only Default parameters
        args = [p for p in params if '=' not in p]

        # Caches other parameters
        kwargs = [p.split('=') for p in params if '=' in p]

        if '__' in text or 'compat' in text:
            return

        item['code'] = text  # Caches the function call
        item['function_name'] = function_name  # Caches the function name
        item['args'] = args  # Caches the default paramaters
        item['kwargs'] = kwargs  # Caches other parameters
        # Yields a structured representation of the function call format.
        yield item
