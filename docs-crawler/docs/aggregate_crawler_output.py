import json
import re


class Compiler(object):
    tf = []
    tfjs = []
    torch = []
    main_map = {'tf': {}, 'tfjs': {}, 'torch': {}}
    base_defs = set()

    def __init__(self):
        with open('./output/tf/2.1.json') as tf_file, \
            open('./output/torch/1.4.0.json') as torch_file, \
            open('./output/tfjs/1.5.1.json') as tfjs_file:
            self.tf = json.load(tf_file)
            self.tfjs = json.load(tfjs_file)
            self.torch = json.load(torch_file)

    def normalize_func_name(self, name):
        alpha = re.compile('[^a-zA-Z]')
        return alpha.sub('', name).lower()

    def load_base_defs(self):
        for f in self.tf:
            nfunc = self.normalize_func_name(f['function_name'])
            self.main_map['tf'][f['function_name']] = nfunc
            self.base_defs.add(nfunc)
        for f in self.tfjs:
            nfunc = self.normalize_func_name(f['function_name'])
            self.main_map['tfjs'][f['function_name']] = nfunc
            self.base_defs.add(nfunc)
        for f in self.torch:
            nfunc = self.normalize_func_name(f['function_name'])
            self.main_map['torch'][f['function_name']] = nfunc
            self.base_defs.add(nfunc)

def main():
    c = Compiler()
    c.load_base_defs()
    print(c.main_map)

if __name__ == '__main__':
    main()