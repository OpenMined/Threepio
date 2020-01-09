import re
import json


parsed_example = re.compile('^\s*(\w*\.)*(\w+)\((.*)\)')
tfjs_docs = {}
torch_docs = {}

with open('./docs/tf2.json') as f:
    tf_docs = json.load(f)
    tf_docs = sorted(tf_docs, key = lambda k: k['code'])

with open('./docs/tfjs-functions.txt', 'r') as f:
    for line in f.readlines():
        m = parsed_example.match(line)
        tfjs_docs[m.groups()[-2]] = m

with open('./docs/torch-functions.txt', 'r') as f:
    for line in f.readlines():
        m = parsed_example.match(line)
        torch_docs[m.groups()[-2]] = m


with open('torch-tfjs.md', 'w') as f:
    f.write('|torch method| tfjs method |\n')
    f.write('|---| --- |\n')
    for meth, matches in torch_docs.items():
        if meth in tfjs_docs:
            tfjs_meth = tfjs_docs[meth]
            f.write(f'| {matches.group()} | {tfjs_meth.group()} |\n')
        else:
            f.write(f'| {matches.group()} | tbd |\n')
            
with open('tf-tfjs.md', 'w') as f:
    f.write('|tf method| tfjs method |\n')
    f.write('|---| --- |\n')
    for doc in tf_docs:
        if doc['function_name'] in tfjs_docs:
            tfjs_meth = tfjs_docs[doc['function_name']]
            f.write(f'| {doc["code"]} | {tfjs_meth.group()} |\n')
        else:
            f.write(f'| {doc["code"]} | tbd |\n')


print('done')