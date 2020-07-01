# _*_ coding: utf-8 -*-

# Crawl modules in the TensorFlow docs to extract functions

# To understand how CrawlSpider works, See documentation in
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
import scrapy
from docs.items import ApiItem
from w3lib.html import remove_tags


class TfjsSpider(scrapy.Spider):
    name = "tfjs"  # Name of the web crawler
    version = "1.5.1"  # Version of TesnorFlow documentation to crawl
    # Regex rules for compiling a string to a Regex object.
    # Here the rules match on to two groups and expect a
    # fucntion call similar to foo.bar(arg1, arg2)
    # the first group refers to foo.bar
    # the second group refers to arg1, arg2
    split_def = re.compile(r'^([\w\.]+)\((.*)\)$')

    def start_requests(self):
        # Base URL crawling
        urls = [
            f'https://js.tensorflow.org/api/{self.version}/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # The parse() fucntion is the callback method that parses the response
    # from each link extracted with the Rule above.
    # The response is a webpage containing documentations of the functions for
    # that particular TensorFlow.js module.
    # The goal is to process the function call format inorder to yield.
    def parse(self, response):

        # Crawls the selector to create a list.
        fdef = response.css('div.function > div.symbol-header')

        defs = []  # Caches the processed call format of all functions.

        # Each item in the list fdef contains documentation of a function
        # in the module currently being crawled.
        # The loop goes through each function documentation to extract
        # Information about the function call and cache.
        for selector in fdef:
            # Preprocesses func_header and stores the processed representation.
            text = remove_tags(selector.get())\
                .replace('\n', '')\
                .replace(' ', '')\
                .replace('Source', '')\
                .replace('function', '')\
                .replace('method', '')
            defs.append(text)

        for text in defs:
            # Uses the Regex rules to compile the function call
            split = self.split_def.match(text)
            if split is None:
                return
            # Extracts only the function name from the Regex encoded text
            function_name = split.groups()[0].split('.')[-1]

            # Extracts every function input parameter and stores in a lis
            params = split.groups()[1].split(',')

            # Caches only Default parameters
            args = [p for p in params if '=' not in p]

            # Caches other parameters
            kwargs = [p.split('=') for p in params if '=' in p]

            # Initializes a Scrapy Item object
            # Check docs at https://docs.scrapy.org/en/latest/topics/items.html
            item = ApiItem()

            item['code'] = text  # Caches the function call
            item['function_name'] = function_name  # Caches the function name
            item['args'] = args  # Caches the default paramaters
            item['kwargs'] = kwargs  # Caches other parameters

            # Yields a structured representation of the function call format.
            yield item
