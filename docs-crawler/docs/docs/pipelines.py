import os
import json


class DocsPipeline(object):
    def process_item(self, item, spider):
        return item

class OutputPipeline(object):

    def open_spider(self, spider):
        output_dir = f"output/{spider.version}"
        os.makedirs(output_dir, exist_ok=True)
        self.file = open(f'{output_dir}/{spider.name}.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

