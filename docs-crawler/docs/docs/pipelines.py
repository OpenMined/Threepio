import os
import json


class DocsPipeline(object):
    def process_item(self, item, spider):
        return item

class OutputPipeline(object):

    def open_spider(self, spider):
        output_dir = f"output/{spider.name}"
        os.makedirs(output_dir, exist_ok=True)
        self.file = open(f'{output_dir}/{spider.version}.json', 'w')

    def close_spider(self, spider):
        self.file.close()
