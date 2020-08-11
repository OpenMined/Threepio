# _*_ coding: utf-8 -*-
# Crawl modules in the scipy docs to extract functions
# To understand how CrawlSpider works, See documentation in
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class ScikitLearnSpider(CrawlSpider):
    name = "sklearn"  # Name of web crawler
    version = "0.23.1"  # Version of sklearn module to crawl
    allowed_domains = ['scikit-learn.org']  # Crawl only links from sklearn

    # Base URL
    start_urls = ['https://scikit-learn.org/stable/modules/classes.html']

    # Regex rules for compiling a string to a Regex object.
    # Here the rules match on to two groups and expect a
    # function call similar to foo.bar(arg1, arg2)
    # the first group refers to foo.bar
    # # the second group refers to arg1, arg2
    split_def = re.compile(r'^([\w\.]+)\(([\w,\s=\*\'\.\-]*)\)')

    # Rule(), guides the crawler starting at
    # https://scikit-learn.org/stable/modules/classes.html to look for
    # the selector '.section tbody td:first-child p' to extract links.
    # The response of the links direct to different Sklearn packages.
    # which are then passed to parse_api() for crawling.
    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+\.html')),
            restrict_css='.section tbody td:first-child p'),
            callback='parse_api',),
    )

    # The parse_api() method is the callback method that parses the response
    # from each link extracted with the Rule above.
    # The response is a webpage containing documentations of the functions for
    # that particular Sklearn package.
    # The goal is to process the function call format inorder to yield.
    def parse_api(self, response):

        self.logger.info(f'Scraping {response.url}')

        # Crawls the selector to obtain a function call format.
        fdef = response.css('.function > dt')

        # If no funciton for that module, return
        if not fdef:
            return

        # Extracts unprocessed function from list
        fdef = fdef[0]

        # Preprocesses the current function call(selector)
        # and stores the processed representation.
        # For example, in the format - foo(arg1, arg2=bar)¶
        text = (remove_tags(fdef.get())
                .replace('\n', '')
                .replace(' ', '')
                .replace('[source]', ''))

        # Uses the Regex rules to compile the function call
        split = self.split_def.match(text)

        if split is None:
            return

        # Extracts only the function name from the Regex encoded text
        function_name = split.groups()[0].split('.')[-1]

        # Extracts all the function input arguments and stores in a list
        params = split.groups()[1].split(',')

        # Caches non-keyword arguments
        args = [p for p in params if '=' not in p]

        # Caches keyword arguments
        kwargs = [p.split('=') for p in params if '=' in p]

        # Initializes a Scrapy Item object
        # Check docs at https://docs.scrapy.org/en/latest/topics/items.html
        item = ApiItem()

        item['code'] = text  # Caches the function call.
        item['function_name'] = function_name  # Caches the function name.
        item['args'] = args  # Caches the regular arguments.
        item['kwargs'] = kwargs  # Caches the keyword arguments.

        # Yields a structured representation of the function call format.
        yield item
