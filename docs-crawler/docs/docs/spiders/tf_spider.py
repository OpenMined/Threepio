# -*- coding: utf-8 -*-

# Crawl modules in the Tensorflow docs to extract functions
#
# To understand how CrawlSpider works, See documentation in:
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TfSpider(CrawlSpider):
    name = "tf"  # Name of web crawler
    version = "2.1"  # Version of tensorflow documentation to crawl
    allowed_domains = ['tensorflow.org']  # Crawl only links from tensorflow

    # Base URL for crawling
    start_urls = [
        f'https://www.tensorflow.org/versions/r{version}/api_docs/python/tf'
    ]

    # Regex rules for compiling a string to a Regex object.
    split_def = re.compile(r'^([\w\.]+)\((.*)\)$')

    # Rule(), guides the crawler starting at
    # https://www.tensorflow.org/versions/r2.1/api_docs/python/tf to look for
    # the selector '.devsite-nav-title' to extract links.
    # The response of the links which direct to different Tensorflow functions
    # are passed to parse_api() for crawling.
    rules = (
        Rule(LinkExtractor(
            # Allows only links containing 'api_docs/python/tf'.
            allow=(re.compile(r'.+api_docs\/python\/tf')),

            # Starts crawling from '.devsite-nav-title'.
            restrict_css='.devsite-nav-title'),

            # calls parse_api() with each response.
            callback='parse_api',),
    )

    # The parse_api() method is the callback method that parses the response
    # from each link extracted with the Rule above.
    # The response is a webpage containing documentations of a function
    # in Tensorflow
    # The goal is to process the function call format inorder to yield.
    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')

        # Initializes a Scrapy Item object
        # Check docs at https://docs.scrapy.org/en/latest/topics/items.html
        item = ApiItem()

        # Stores the function call example format, The lang-python tag contains
        # the Function call format for the currently crawled function.
        function_header = response.css('.lang-python')

        if len(function_header) == 0:  # Returns if no function call exists
            return

        # Preprocesses function_header and stores the processed representation.
        # For example, in the format - tf.eigvals(tensor,name=None)
        text = remove_tags(function_header.get())\
            .replace('\n', '')\
            .replace(' ', '')

        # Uses the declared Regex rules to compile the function call
        split = self.split_def.match(text)

        if split is None:
            return

        # Extracts only the function name from the Regex encoded text
        function_name = split.groups()[0].split('.')[-1]

        # Extracts the function input parameters and stores in a list
        params = split.groups()[1].split(',')

        # Extracts non-keyword arguments
        args = [p for p in params if '=' not in p]

        # Extracts only keyword arguments
        kwargs = [p.split('=') for p in params if '=' in p]

        if '__' in text or 'compat' in text:
            return

        item['code'] = text  # Caches the function call
        item['function_name'] = function_name  # Caches the function name
        item['args'] = args  # Caches other arguments
        item['kwargs'] = kwargs  # Caches keyword arguments

        # Yields a structured representation of the function call format.
        yield item
