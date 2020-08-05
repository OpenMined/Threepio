# _*_ coding: utf-8 -*-
# Aggregate the outputs gotten from crawling the documentation of
# different ML libraries

import json
import re
import warnings
from translations import WORD_TRANSLATIONS, COMMAND_TRANSLATIONS

# The Compiler class is responsible for handling every stage of the
# aggregation. The Class starts by reading the Individual outputs of
# each library, then If an Exisiting Aggregate exists, It loads the
# Aggregate from translations.py. The final step is to then merge
# the exisiting libraries, or update an exisitng Aggregate with new
# functions or Libraries.


class Compiler(object):
    tf = []  # Stores tensorflow translations
    tfjs = []  # Stores tensorflowjs translations
    torch = []  # Store Pytorch translation

    # Combines translations of the 3 libraries
    main_map = {'tf': {}, 'tfjs': {}, 'torch': {}}

    base_defs = set()  # Caches the standardized name of exisiting functions

    def __init__(self):
        # Opens the output of tensorflow, torch and tfjs
        # and then caches to their respective files
        with open('./output/tf/2.1.json') as tf_file, \
                open('./output/torch/1.4.0.json') as torch_file, \
                open('./output/tfjs/1.5.1.json') as tfjs_file:
            self.tf = json.load(tf_file)  # Caches tensorflow's docs
            self.tfjs = json.load(tfjs_file)  # Caches tfjs docs
            self.torch = json.load(torch_file)  # Caches Pytorch's docs

    # normalize_func_name(name), uses regex to standardize input string.
    # the regex instruction(alpha), converts all uppercase to lowercase.
    def normalize_func_name(self, name):

        # Regex Instruction to convert uppercase characters to lowercase.
        # Foo_Bar -> foo_bar.
        alpha = re.compile(r'[\W][a-zA-Z0-9]*')

        return alpha.sub('', name).lower()  # Returns the standardized name.

    # generate_attrs() used Regex to seperated package chains into
    # Lists containing individual packages as Items.
    def generate_attrs(self, code):

        # The regex Instruction split_def identifies the period sign.
        # packages are then broken up while the function parameters
        # are Ignored. Example, foo.bar.baz(a,b) -> [foo, bar, baz]
        split_def = re.compile(r'^([\w\.]+)\((.*)\)')

        # Returns the output after compiling with regex.
        return split_def.match(code)[1].split('.')

    # populate_command() is responsible for going through each
    # function from existing libraries.
    # function names are normalized and cached in base_defs.
    # Args and Kwargs are also preprocessed and combined
    # to be cached in f['args']
    # package name chains are broken down and stored
    # in f['attrs'] .e.g. foo.bar() -> [foo, bar].
    def populate_command(self, lib):
        # getattr receives a string and an object.
        # If the object has a varible with same name as the string value,
        # The content of the variable is looped through.
        for f in getattr(self, lib):

            # normalize_func_name() uses Regex to format the function name.
            # Exact operation is documented under the function
            nfunc = self.normalize_func_name(f['function_name'])

            # generate_attrs(), uses Regex to split a package
            # string into a list. Exact operation is documented
            # under the function.
            f['attrs'] = self.generate_attrs(f['code'])

            # hydrate_args(), combines args and kwargs into a list.
            # Where each Argument is represented as a dictionary in the list
            # with properties as key/value pairs.
            f['args'] = self.hydrate_args(f['args'], f['kwargs'])

            # caches the function_name
            f['name'] = f['function_name']

            # checks if for the particular library, the function
            # exists in main_map
            if nfunc in self.main_map[lib]:

                # main_map[lib][nfunc] should have a list of
                # size 1 as the value. The element in the list is a
                # dictionary containing attributes of the function.
                existing_f = self.main_map[lib][nfunc][0]

                # If the package chain of the processed function for
                # the library in focus is greater than its representation
                # in main_map continue else Overwrite.
                # The Idea is to give preference to the representation with
                #  a smaller package chain.
                # Example, foo.bar() and foo.baz.bar().
                # We would give preference to foor.bar().
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

            # delete f[kwargs], since we have cached a standard
            # form in f[args]
            del f['kwargs']

            del f['code']
            del f['function_name']

            # Overwrite the function for the processed library in main_map.
            self.main_map[lib][nfunc] = [f]

            # Caches the standardized function name.
            # base_defs would contain the function name for functions accross
            # every library.
            self.base_defs.add(nfunc)

    # load_base_defs() goes through the supported functions for each library,
    # It then Identifies each function and if exisiting, maps to the
    # respective libraries, which exists as keys in main_map.
    # base_defs caches all the standard function names accross each libraries.
    def load_base_defs(self):

        # Traverses through tf output to update main_map and base_defs
        self.populate_command('tf')

        # Traverses through tfjs output to update main_map and base_defs
        self.populate_command('tfjs')

        # Traverses through torch output to update main_map and base_defs
        self.populate_command('torch')

    # hydrate_args() splits args and kwargs
    # eg args -> [foo, bar] and kwargs -> [[oz, True]]
    # output would be -> args ->
    # [{'name': 'foo', 'kwarg': False, 'opt': False},
    # {'name': 'bar', 'kwarg': False, 'opt': False},
    # {'name': 'oz', 'kwarg': True, 'opt': True} ]
    def hydrate_args(self, base_args, base_kwargs):

        # filters out empty arguments or those with "?".
        base_args = list(filter(lambda a: a not in ['', '?'], base_args))

        # filters out empty kwargs or those with "?".
        base_kwargs = list(
            filter(lambda a: a[0] not in ['', '?'], base_kwargs)
        )

        # loops through the list of arguments to generate the
        # structured arguments as a list where each argument is represented as
        # a dictionary with property/value pair.
        ba = [
            {
                'name': self.normalize_func_name(a),  # normalize name
                'kwarg': False,  # False since it is an arg
                'opt': a.endswith('?'),  # signifies it is optional
            } for i, a in enumerate(base_args)  # Loops through args
        ]

        # Loops through the list of kwargs to generate the
        # structured arguments as a list where each argument is represented as
        # a dictionary with property/value pair.
        bk = [
            {
                'name': self.normalize_func_name(a[0]),  # normalize name
                'kwarg': True,  # True since it is a kwarg
                'opt': True  # signifies it is optional
            } for a in base_kwargs  # Loops through kwargs
        ]
        return ba + bk  # combines kwargs and args lists

    # match_arg_names() compares arguments in two libraries.
    # if an argument for a particular method exists in the target library.
    # The argument definition is updated in the source library, using the
    # target library name has key, and the function name had value
    def match_arg_names(self, from_args, to_args, to_lang):
        # loops through arg in arg list
        for from_arg in from_args:
            try:

                # If current arg exists in from_arg and to_arg,
                # append to list and get first occurance.
                to_arg = next(
                    m for m in to_args if m.get('name') == from_arg.get('name')
                )

                # Get name in to_arg
                to_name = to_arg.get('name', None)

                # If arg exists in target lang, assign to from_arg,
                # using to_lang as key.
                # {'name':'foo', 'kwarg':False, 'opt':False} to
                # {'name':'foo', 'kwarg':False, 'opt':False, 'pytorch':'foo'}
                if to_name is not None:
                    from_arg[to_lang] = to_name
            except Exception:
                # If error, for target library check translations.py for arg
                to_name = WORD_TRANSLATIONS[to_lang].get(
                    from_arg['name'], None)

                # If arg exists in target library, update the arg
                # dictionary in from_arg using the same format above.
                if to_name is not None:
                    from_arg[to_lang] = to_name

        # Returns updated from_args
        return from_args

    # load_translations() loops through every method in base_defs.
    # Each method is then compared between its representation in a
    # source library(from_lang) and across multiple target libraries in
    # order to identify different arguments that exists accross different
    # libraries.
    def load_translations(self, from_lang):

        # List of supported languages.
        langs = ['torch', 'tfjs', 'tf']

        # Removes current language, from_lang from langs
        langs.pop(langs.index(from_lang))

        # Loops through base_defs, base_defs contains the names
        # of existing methods accross every library.
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

                # Stores the method format from the target language
                # into the source language, using the language name as key
                # and the list containing the function dictionary as value.
                from_def[to_lang] = to_name

                # Format & match args
                to_args = to_def['args']
                from_def['args'] = self.match_arg_names(
                    from_args,
                    to_args,
                    to_lang
                )

    # slim_output() merges from_lang and to_lang into a single output
    def slim_output(self, from_lang, to_lang):

        # Extracts objects from_lang and to_lang in self.main_map.
        input_dict = {
            from_lang: self.main_map[from_lang],
            to_lang: self.main_map[to_lang]
        }

        # initializes output object
        output = {from_lang: {}, to_lang: {}}

        # hydrate_keys(), adds methods for each libarary in output only if the
        # method name exists as a property for the target library.
        def hydrate_keys(input_dict, output, from_lang, to_lang):

            # loops through key/value pair for source language in input_dict,
            # keys are method names, and the value is a list of size 1
            # whose value is a dictionary contianing method properties
            for k, v in input_dict[from_lang].items():
                # TODO: Treat as list
                # obtains dictionary containing method properties.
                v = v[0]

                # if target library exists in input_dict, add to output.
                # The idea behind this step is to support cross-platform
                # translations behind each method in the 2 libraries.
                if v.get(to_lang, '') in input_dict[to_lang]:
                    output[from_lang][k] = [v]

            return output

        # Runs hydrate_keys() in order to ensure only methods that exists
        # in both libraries are added.
        output = hydrate_keys(input_dict, output, from_lang, to_lang)
        output = hydrate_keys(input_dict, output, to_lang, from_lang)

        return output

    # load_manual_translations() manually updates existing languages
    # in main_map with the methods methods and arguments from
    # COMMAND_TRANSLATIONS in translations.py.
    def load_manual_translations(self):
        # for each existing language, loops through commands
        # in COMMAND_TRANSLATIONS
        for lang, commands in COMMAND_TRANSLATIONS.items():

            # Updates each language in main_map with new methods and arguments.
            self.main_map[lang].update(commands)

    # output_data() updates and save translations
    def output_data(self):
        with open('../../pythreepio/static/mapped_commands_full.json', 'w',
                  encoding='utf8') as f:

            # merges self.main_map and f in mapped_commands_full.json
            json.dump(self.main_map, f, indent=4, ensure_ascii=False)

        # compressed output containing only torch & tfjs
        torch_tfjs_map = self.slim_output('torch', 'tfjs')

        with open('../../static/mapped_commands_torch_tfjs.json', 'w',
                  encoding='ascii') as f:

            # merges only torch and tfjs in commands_torch.tfjs.json
            json.dump(
                torch_tfjs_map,
                f,
                separators=(',', ':'),
                ensure_ascii=False
            )


def main():
    c = Compiler()  # Initializes the compiler
    c.load_base_defs()  # Inserts values for self.main_map and self.base_def
    c.load_manual_translations()  # updates self.main_map from translations.py.

    # updates function arguments in tfjs compared with other languages
    c.load_translations('tfjs')

    # updates function arguments in torch compared with other languages
    c.load_translations('torch')

    # updates function arguments in tf compared with other languages
    c.load_translations('tf')

    c.output_data()  # saves updated translations.


if __name__ == '__main__':
    main()
