# -*- coding: utf-8 -*-

import json
import numpy as np
from pytablewriter import MarkdownTableWriter

# ======= DICTIONARY FOR FRAMEWORK ======

with open('./pythreepio/static/mapped_commands_full.json') as json_file:
    data = json.load(json_file)
    tf = data['tf']
    torch = data['torch']
    tfjs = data['tfjs']

# ======= TENSORFLOW TRANSLATIONS ======

tensorflow = []  # empty array

# Loop for ittirating through the mapped commands
for key, value in tf.items():
    command_dict = value[0]
    attrs = ".".join(command_dict['attrs'])
    translates_to_torch = "torch" in command_dict
    translates_to_tfjs = "tfjs" in command_dict
    tensorflow.append((attrs, translates_to_torch, translates_to_tfjs))
tensorflow = np.vstack(tensorflow)

# Add unicode for the respective strings
tensorflow = np.where(tensorflow == 'False', '✘', tensorflow)
tensorflow = np.where(tensorflow == 'True', '✔', tensorflow)

# Convert numpy array to list
tensorflow = tensorflow.tolist()

# Convert list to Markdown notation
writer = MarkdownTableWriter(
        table_name="Tensorflow",
        headers=["", "PyTorch", "TensorFlow.js"],
        value_matrix=tensorflow)
writer.write_table()

# ======= PYTORCH TRANSLATIONS ======

pytorch = []  # empty array

# Loop for ittirating through the mapped commands
for key, value in torch.items():
    command_dict = value[0]
    attrs = ".".join(command_dict['attrs'])
    translates_to_tf = "tf" in command_dict
    translates_to_tfjs = "tfjs" in command_dict
    pytorch.append((attrs, translates_to_tf, translates_to_tfjs))
pytorch = np.vstack(pytorch)

# Add unicode for the respective strings
pytorch = np.where(pytorch == 'False', '✘', pytorch)
pytorch = np.where(pytorch == 'True', '✔', pytorch)

# Convert numpy array to list
pytorch = pytorch.tolist()

# Convert list to Markdown notation
writer = MarkdownTableWriter(
        table_name="PyTorch",
        headers=["", "TensorFlow", "TensorFlow.js"],
        value_matrix=pytorch)
writer.write_table()

# ======= TENSORFLOW.js TRANSLATIONS ======

tensorflow.js = []  # empty array

# Loop for ittirating through the mapped commands
for key, value in tfjs.items():
    command_dict = value[0]
    attrs = ".".join(command_dict['attrs'])
    translates_to_torch = "torch" in command_dict
    translates_to_tf = "tf" in command_dict
    tensorflow.js.append((attrs, translates_to_torch, translates_to_tf))
tensorflow.js = np.vstack(tensorflow.js)

# Add unicode for the respective strings
tensorflow.js = np.where(tensorflow.js == 'False', '✘', tensorflow.js)
tensorflow.js = np.where(tensorflow.js == 'True', '✔', tensorflow.js)

# Convert numpy array to list
tensorflow.js = tensorflow.js.tolist()

# Convert list to Markdown notation
writer = MarkdownTableWriter(
        table_name="TensorFlow.js",
        headers=["", "TensorFlow", "PyTorch"],
        value_matrix=tensorflow.js)
writer.write_table()
