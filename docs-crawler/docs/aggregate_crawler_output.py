import json
import re

TRANSLATIONS = {
    'tfjs': {
        'dim': 'axis',
        'input': 'a',
        'other': 'b',
        'eq': 'equal',
        't': 'transpose',
        'truediv': 'div'
    },
    'torch': {},
    'tf': {}
}


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
        alpha = re.compile(r'[\W][a-zA-Z0-9]*')
        return alpha.sub('', name).lower()

    def generate_attrs(self, code):
        split_def = re.compile(r'^([\w\.]+)\((.*)\)')
        return split_def.match(code)[1].split('.')

    def populate_command(self, lib):
        for f in getattr(self, lib):
            nfunc = self.normalize_func_name(f['function_name'])
            f['attrs'] = self.generate_attrs(f['code'])
            f['args'] = self.hydrate_args(f['args'], f['kwargs'])
            f['name'] = f['function_name']
            del f['kwargs']
            del f['code']
            del f['function_name']
            self.main_map[lib][nfunc] = f
            self.base_defs.add(nfunc)

    def load_base_defs(self):
        self.populate_command('tf')
        self.populate_command('tfjs')
        self.populate_command('torch')

    def hydrate_args(self, base_args, base_kwargs):
        base_args = list(filter(lambda a: a not in ['', '?'], base_args))
        base_kwargs = list(
            filter(lambda a: a[0] not in ['', '?'], base_kwargs)
        )
        ba = [
            {
                'name': self.normalize_func_name(a),
                'kwarg': False,
                'opt': a.endswith('?'),
            } for i, a in enumerate(base_args)
        ]
        bk = [
            {
                'name': self.normalize_func_name(a[0]),
                'kwarg': True,
                'opt': True
            } for a in base_kwargs
        ]
        return ba + bk

    def match_arg_names(self, base, match, to_lang):
        for base_arg in base:
            try:
                match_arg = next(
                    m for m in match if m.get('name') == base_arg.get('name')
                )
                match_name = match_arg.get('name', None)
                if match_name is not None:
                    base_arg[to_lang] = match_name
            except Exception:
                match_name = TRANSLATIONS[to_lang].get(
                    base_arg['name'], None)
                if match_name is not None:
                    base_arg[to_lang] = match_name
        return base

    def load_translations(self, from_lang):
        langs = ['torch', 'tfjs', 'tf']
        langs.pop(langs.index(from_lang))

        for d in self.base_defs:
            # First perform any word level translations
            from_d = TRANSLATIONS[from_lang].get(d, False) or d

            # Check if translation exists in our from language
            if from_d not in self.main_map[from_lang]:
                continue

            base_args = self.main_map[from_lang][from_d]['args']
            # Check if translatable to other langs
            for to_lang in langs:
                # Perform word level translation for target language
                to_d = TRANSLATIONS[to_lang].get(d, False) or d
                if to_d not in self.main_map[to_lang]:
                    continue

                self.main_map[from_lang][from_d][to_lang] = to_d

                # Format & match args
                match_args = self.main_map[to_lang][to_d]['args']
                self.main_map[from_lang][from_d]['args'] = \
                    self.match_arg_names(base_args, match_args, to_lang)

    def slim_output(self, from_lang, to_lang):
        input_dict = {
            from_lang: self.main_map[from_lang],
            to_lang: self.main_map[to_lang]
        }
        output = {
            from_lang: {},
            to_lang: {}
        }

        def hydrate_keys(input_dict, output, from_lang, to_lang):
            for k, v in input_dict[from_lang].items():
                translated_k = TRANSLATIONS[to_lang].get(k, False) or k
                if translated_k in input_dict[to_lang]:
                    output[from_lang][k] = v
            return output

        output = hydrate_keys(input_dict, output, from_lang, to_lang)
        output = hydrate_keys(input_dict, output, to_lang, from_lang)

        return output

    def output_data(self):
        with open('../../static/mapped_commands_full.json', 'w',
                  encoding='utf8') as f:
            json.dump(self.main_map, f, indent=4, ensure_ascii=False)
        # Compressed map with only torch & tfjs
        torch_tfjs_map = self.slim_output('torch', 'tfjs')
        with open('../../static/mapped_commands_torch_tfjs.json', 'w',
                  encoding='ascii') as f:
            json.dump(
                torch_tfjs_map,
                f,
                separators=(',', ':'),
                ensure_ascii=False
            )


def main():
    c = Compiler()
    c.load_base_defs()
    c.load_translations('tfjs')
    c.load_translations('torch')
    c.load_translations('tf')
    c.output_data()


if __name__ == '__main__':
    main()
