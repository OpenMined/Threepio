import re
import scrapy
from docs.items import ApiItem
from w3lib.html import remove_tags


class TorchSpider(scrapy.Spider):
    name = "torch"
    version = "1.4.0"
    split_def = re.compile('^([\w\.]+)\(([\w\,\s=\*\.]*)\)')

    def start_requests(self):
        urls = [
            f'https://pytorch.org/docs/{self.version}/torch.html',
            f'https://pytorch.org/docs/{self.version}/nn.html',
            f'https://pytorch.org/docs/{self.version}/nn.functional.html',
            f'https://pytorch.org/docs/{self.version}/tensors.html',
            f'https://pytorch.org/docs/{self.version}/tensor_attributes.html',
            f'https://pytorch.org/docs/{self.version}/autograd.html',
            f'https://pytorch.org/docs/{self.version}/cuda.html',
            f'https://pytorch.org/docs/{self.version}/distributed.html',
            f'https://pytorch.org/docs/{self.version}/distributions.html',
            f'https://pytorch.org/docs/{self.version}/hub.html',
            f'https://pytorch.org/docs/{self.version}/jit.html',
            f'https://pytorch.org/docs/{self.version}/nn.init.html',
            f'https://pytorch.org/docs/{self.version}/onnx.html',
            f'https://pytorch.org/docs/{self.version}/optim.html',
            f'https://pytorch.org/docs/{self.version}/quantization.html',
            f'https://pytorch.org/docs/{self.version}/rpc.html',
            f'https://pytorch.org/docs/{self.version}/random.html',
            f'https://pytorch.org/docs/{self.version}/sparse.html',
            f'https://pytorch.org/docs/{self.version}/storage.html',
            f'https://pytorch.org/docs/{self.version}/bottleneck.html',
            f'https://pytorch.org/docs/{self.version}/checkpoint.html',
            f'https://pytorch.org/docs/{self.version}/cpp_extension.html',
            f'https://pytorch.org/docs/{self.version}/data.html',
            f'https://pytorch.org/docs/{self.version}/dlpack.html',
            f'https://pytorch.org/docs/{self.version}/model_zoo.html',
            f'https://pytorch.org/docs/{self.version}/tensorboard.html',
            f'https://pytorch.org/docs/{self.version}/type_info.html',
            f'https://pytorch.org/docs/{self.version}/named_tensor.html',
            f'https://pytorch.org/docs/{self.version}/name_inference.html',
            f'https://pytorch.org/docs/{self.version}/__config__.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fdef = response.css('dl.function > dt')
        defs = []
        for selector in fdef:
            text = remove_tags(selector.get()).replace('\n', '')
            defs.append(text)

        for text in defs:
            split = self.split_def.match(text)
            if split is None:
                return
            
            function_name = split.groups()[0].split('.')[-1]
            params = split.groups()[1].split(',')
            args = [p for p in params if '=' not in p]
            kwargs = [p.split('=') for p in params if '=' in p]

            item = ApiItem()
            item['code'] = text
            item['function_name'] = function_name
            item['args'] = args
            item['kwargs'] = kwargs
            yield item