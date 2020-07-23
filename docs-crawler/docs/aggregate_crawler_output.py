import json
import re
import warnings
from translations import WORD_TRANSLATIONS, COMMAND_TRANSLATIONS


class Compiler(object):
    tf = []
    tfjs = []
    torch = []
    main_map = {'tf': {}, 'tfjs': {}, 'torch': {}}
    base_defs = set()

    def __init__(self):
        with open('docs-crawler/docs/output/tf/2.1.json') as tf_file, \
                open(
                'docs-crawler/docs/output/torch/1.4.0.json') as torch_file, \
                open('docs-crawler/docs/output/tfjs/1.5.1.json') as tfjs_file:
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

            if nfunc in self.main_map[lib]:
                existing_f = self.main_map[lib][nfunc][0]
                if len(f['attrs']) > len(existing_f['attrs']):
                    warnings.warn(
                        f'Ignoring op: {f}: {nfunc} is already defined in '
                        f'{lib} with shallower or '
                        f'same attrs path: {existing_f}'
                    )
                    continue
                else:
                    warnings.warn(
                        f'Overwriting op: {existing_f} with {f} '
                        'that has shallower attrs path'
                    )

            del f['kwargs']
            del f['code']
            del f['function_name']
            self.main_map[lib][nfunc] = [f]
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

    def match_arg_names(self, from_args, to_args, to_lang):
        for from_arg in from_args:
            try:
                to_arg = next(
                    m for m in to_args if m.get('name') == from_arg.get('name')
                )
                to_name = to_arg.get('name', None)
                if to_name is not None:
                    from_arg[to_lang] = to_name
            except Exception:
                to_name = WORD_TRANSLATIONS[to_lang].get(
                    from_arg['name'], None)
                if to_name is not None:
                    from_arg[to_lang] = to_name
        return from_args

    def load_translations(self, from_lang):
        langs = ['torch', 'tfjs', 'tf']
        langs.pop(langs.index(from_lang))

        for d in self.base_defs:
            # First perform any word level translations
            from_name = WORD_TRANSLATIONS[from_lang].get(d, False) or d

            # Check if translation exists in our from language
            if from_name not in self.main_map[from_lang]:
                continue

            # TODO: Treat as list
            from_def = self.main_map[from_lang][from_name][0]
            from_args = from_def['args']
            # Check if translatable to other langs
            for to_lang in langs:
                # Perform word level translation for target language
                to_name = WORD_TRANSLATIONS[to_lang].get(d, False) or d
                if to_name not in self.main_map[to_lang]:
                    continue
                # TODO: Treat as list
                to_def = self.main_map[to_lang][to_name][0]
                from_def[to_lang] = to_name

                # Format & match args
                to_args = to_def['args']
                from_def['args'] = self.match_arg_names(
                    from_args,
                    to_args,
                    to_lang
                )

    def slim_output(self, from_lang, to_lang):
        input_dict = {
            from_lang: self.main_map[from_lang],
            to_lang: self.main_map[to_lang]
        }
        output = {from_lang: {}, to_lang: {}}

        def hydrate_keys(input_dict, output, from_lang, to_lang):
            for k, v in input_dict[from_lang].items():
                # TODO: Treat as list
                v = v[0]
                if v.get(to_lang, '') in input_dict[to_lang]:
                    output[from_lang][k] = [v]
            return output

        output = hydrate_keys(input_dict, output, from_lang, to_lang)
        output = hydrate_keys(input_dict, output, to_lang, from_lang)

        return output

    def load_manual_translations(self):
        for lang, commands in COMMAND_TRANSLATIONS.items():
            self.main_map[lang].update(commands)

    def output_data(self):
        with open('pythreepio/static/mapped_commands_full.json', 'w',
                  encoding='utf8') as f:
            json.dump(self.main_map, f, indent=4, ensure_ascii=False)
        # Compressed map with only torch & tfjs
        torch_tfjs_map = self.slim_output('torch', 'tfjs')
        with open('static/mapped_commands_torch_tfjs.json', 'w',
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
    c.load_manual_translations()
    c.load_translations('tfjs')
    c.load_translations('torch')
    c.load_translations('tf')
    c.output_data()


if __name__ == '__main__':
    main()
