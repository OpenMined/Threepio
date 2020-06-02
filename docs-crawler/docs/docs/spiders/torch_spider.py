import re
from docs.items import ApiItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class TorchSpider(CrawlSpider):
    name = "torch"
    version = "1.4.0"
    allowed_domains = ['pytorch.org']
    start_urls = [f'https://pytorch.org/docs/{version}/index.html']
    split_def = re.compile(r'^([\w\.]+)\(([\w,\s=\*\'\.\-]*)\)')

    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(r'.+\.html')),
            restrict_css='.toctree-l1'),
            callback='parse_api',),
    )

    def parse_api(self, response):
        self.logger.info(f'Scraping {response.url}')
        fdef = response.css('dl.function')
        defs = {}
        for selector in fdef:
            cmd_info = {}
            func_header = selector.css('dt')
            text = (remove_tags(func_header.get())
                    .replace('\n', '')
                    .replace('\\', '')
                    .replace('&gt', '')
                    .replace('&lt', '')
                    .replace(' ', '')
                    .replace('[source]', ''))
            if 'torchvision' in text:
                continue

            split_cmd = self.split_def.match(text)
            if split_cmd is None:
                continue

            function_name = split_cmd.groups()[0].split('.')[-1]

            cmd_info['code'] = text
            params = split_cmd.groups()[1].split(',')

            cmd_info['args'] = [p for p in params if '=' not in p]
            cmd_info['kwargs'] = [p.split('=') for p in params if '=' in p]

            defs[function_name] = cmd_info

        for function_name, cmd_info in defs.items():
            item = ApiItem()
            item['code'] = cmd_info['code']
            item['function_name'] = function_name
            item['args'] = cmd_info['args']
            item['kwargs'] = cmd_info['kwargs']
            yield item
