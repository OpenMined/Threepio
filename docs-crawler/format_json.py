import json
import re

ret = []
parsed_example = re.compile('^\s*(\w*\.)*(\w+)\((.*)\)')

with open('./docs/tf.json') as f:
    docs = json.load(f)
    for f in docs:
        code = f['code']
        if code.startswith('tf.'):
            new = {
                'code': code,
                'function_name': parsed_example.match(code).groups()[-2]
            }
            ret.append(new)


with open('./docs/tf2.json', 'w') as f:
    json.dump(ret, f)
