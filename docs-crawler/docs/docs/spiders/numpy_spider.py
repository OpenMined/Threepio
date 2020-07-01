# _*_ coding: utf-8 -*-
# Crawl modules in the scipy docs to extract functions
# To understand how CrawlSpider works, See documentation in
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class NumpySpider(CrawlSpider):
    name = "numpy"  # Name of The Web crawler
    version = "1.17.0"  # Version Used
    allowed_domains = ['scipy.org']  # Crawls only links from scipy

    # Base URL which is needed for crawling
    start_urls = ['https://docs.scipy.org/doc/numpy/reference/generated/']

    # Following part is Regex expression, used to define the search pattern
    # which follows the Regex rules.

    split_def = re.compile(r'^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

    # The following part guides the crawler starting at
    # https://docs.scipy.org/doc/numpy/reference/generated/
    # The reponse of the links direct to different modules
    # and are passed to parse_api() for crawling
    rules = (
      Rule(LinkExtractor(
        allow=(re.compile(r'.+\.html')),
      ),
        callback='parse_api', ),
    )

    # The parse_api() method is the callback method that parses the response
    # from each link extracted with the Rule above.
    # The response is a webpage containing documentations of the functions
    # for that particular scipy module.
    # The objective is to format the function call method to yield
    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('dl.function > dt')
        defs = []
        for selector in fdef:

            text = (remove_tags(selector.get())
                    .replace('\n', '')  # Used to replace the newline character
                    .replace(' ', '')  # Used to replace the space character
                    .replace('[source]', ''))  # Used to replace '[source]'
            defs.append(text)  # Adding the appended text in defs

        for text in defs:

            split = self.split_def.match(text)
            if split is None:
                continue

            # Extracts only the function name from the Regex encoded text
            function_name = split.groups()[0].split('.')[-1]

            # Extracts every function input arguments and stores in a list
            params = split.groups()[1].split(',')

            # Caches the Default arguments
            args = [p for p in params if '=' not in p]

            # Caches other arguments
            kwargs = [p.split('=') for p in params if '=' in p]

            item = ApiItem()
            item['code'] = text  # Caches the function call
            item['function_name'] = function_name  # Caches the function name
            item['args'] = args  # Caches the default arguments
            item['kwargs'] = kwargs  # Caches other arguments
            # Yields a structured representation of the function call format.
            yield item
