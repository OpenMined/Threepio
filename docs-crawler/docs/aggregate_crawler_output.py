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
        alpha = re.compile('[a-zA-Z]')
        return alpha.sub('', name).lower()

    def generate_attrs(self, code):
        split_def = re.compile(r'^([\w\.]+)\((.*)\)')
        return split_def.match(code)[1].split('.')

    def populate_command(self, lib):
        for f in getattr(self, lib):
            nfunc = self.normalize_func_name(f['function_name'])
            f['attrs'] = self.generate_attrs(f['code'])
            f['args'] = self.hydrate_args(f['args'], f['kwargs'])
            del f['kwargs']
            self.main_map[lib][nfunc] = f
            self.base_defs.add(nfunc)

    def load_base_defs(self):
        self.populate_command('tf')
        self.populate_command('tfjs')
        self.populate_command('torch')

    def hydrate_args(self, base_args, base_kwargs):
        ba = [
            {
                'name': self.normalize_func_name(a),
                'is_kwarg': False,
                'optional': a.endswith('?'),
                'index': i
            } for i, a in enumerate(base_args)
        ]
        bk = [
            {
                'name': self.normalize_func_name(a[0]),
                'is_kwarg': True,
                'optional': True
            } for a in base_kwargs
        ]
        return ba + bk

    def match_arg_names(self, base, match, to_lang):
        for base_arg in base:
            try:
                match_arg = next(
                    m for m in match if m.get('name') == base_arg.get('name')
                )
                base_arg[to_lang] = match_arg.get('name', None)
            except Exception:
                # TODO: check for alternate word level translations
                base_arg[to_lang] = None
        return base

    def load_translations(self, from_lang):
        langs = ['torch', 'tfjs', 'tf']
        langs.pop(langs.index(from_lang))

        for d in self.base_defs:
            # Check if translation exists in our from language
            if d not in self.main_map[from_lang]:
                continue

            base_args = self.main_map[from_lang][d]['args']
            # Check if translatable to other langs
            for to_lang in langs:
                if d not in self.main_map[to_lang]:
                    for a in self.main_map[from_lang][d]['args']:
                        a.update({to_lang: None})
                    continue

                # Format & match args
                match_args = self.main_map[to_lang][d]['args']
                self.main_map[from_lang][d]['args'] = self.match_arg_names(
                    base_args, match_args, to_lang
                )

    def output_data(self):
        with open('../../static/mapped_commands.json', 'w',
                  encoding='utf8') as f:
            json.dump(self.main_map, f, indent=4, ensure_ascii=False)


def main():
    c = Compiler()
    c.load_base_defs()
    c.load_translations('tfjs')
    c.load_translations('torch')
    c.load_translations('tf')
    c.output_data()


if __name__ == '__main__':
    main()
