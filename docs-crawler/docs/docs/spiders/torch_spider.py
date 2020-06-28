# -*- coding: utf-8 -*-

# Crawl modules in the Pytorch documentation to extract, format and return existing functions
#
# To understand how CrawlSpider works, See documentation in:
# https://docs.scrapy.org/en/latest/topics/spiders.html
import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TorchSpider(CrawlSpider):
    name = "torch" # Name of web crawler
    version = "1.4.0" # Version of Pytorch documentation to crawl
    allowed_domains = ['pytorch.org'] # Crawl only links from pytorch
    start_urls = [f'https://pytorch.org/docs/{version}/index.html'] # Crawler starts crawling from this url
    split_def = re.compile(r'^([\w\.]+)\(([\w,\s=\*\'\.\-]*)\)')  # Regex rules for compiling a string to a Regex object.

    # Rule(), guides the crawler starting at https://pytorch.org/docs/1.4.0/index.html to look for
    # the selector '.toctree-l1' to extract links.
    # The response of the links direct to different Pytorch modules and are passed to parse_api() for crawling.
    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+\.html')), # Allows only links ending with .html.
            restrict_css='.toctree-l1'), # Starts crawling from .toctree-l1.
            callback='parse_api',), # Passes the responses to the parse_api() method.
    )

    # The parse_api() method is the callback method that parses the response from each link extracted with the Rule above.
    # The response is a webpage containing documentations of the functions for that particular PyTorch module.
    # The goal is to process each function call format and cache in ApiItem to yield.
    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('dl.function') # Crawls the selector to create a list of each function documentation in the Module
        defs = {} # Caches the processed function call format of all functions in the module

        # Each item in the list fdef contains documentation of a function in the module currently being crawled.
        # The loop goes through each function documentation to extract Information about the function call and cache.
        for selector in fdef:
            cmd_info = {} # Caches the processed function call format of the current function in the module
            func_header = selector.css('dt') # Stores the function call format, The dt tag contains the Function call format for the currently crawled function.
            text = (remove_tags(func_header.get()) # Preprocesses func_header and stores the simplified representation.
                    .replace('\n', '')             # For example, in the format - torch.this_is_a_function(obj)¶
                    .replace('\\', '')
                    .replace('&gt', '')
                    .replace('&lt', '')
                    .replace(' ', '')
                    .replace('[source]', ''))
            if 'torchvision' in text:
                continue

            split_cmd = self.split_def.match(text) # Uses the Regex rules created earlers to convert to a Regex object for the simplified extraction of different parts of the function call.
            if split_cmd is None:
                continue

            function_name = split_cmd.groups()[0].split('.')[-1] # Extracts only the function name from the Regex encoded text

            cmd_info['code'] = text # Caches the formatted function call
            params = split_cmd.groups()[1].split(',') # Extracts every function input parameter and stores in a list

            cmd_info['args'] = [p for p in params if '=' not in p] # Caches only Default parameters
            cmd_info['kwargs'] = [p.split('=') for p in params if '=' in p] # Caches other parameters

            defs[function_name] = cmd_info # Stores the function cache in the global function cache

        # Loops through the global function cache to yield each function.
        for function_name, cmd_info in defs.items():
            item = ApiItem() # Initializes a Scrapy Item object, docs at https://docs.scrapy.org/en/latest/topics/items.html
            item['code'] = cmd_info['code'] # Stores the preprocessed function call
            item['function_name'] = function_name # Stores the function name
            item['args'] = cmd_info['args'] # Stores the function default parameters
            item['kwargs'] = cmd_info['kwargs'] # Stores the function parameters
            yield item  # Yields a structured representation of the function call format.
