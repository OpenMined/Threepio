import torch
import tensorflow as tf


def process_tests(command, threepio, check_answer):
    for i, input in enumerate(command["inputs"]):
        translations = threepio.translate(input, lookup_command=True)
        for j, translation in enumerate(translations):
            result = translation.execute_routine()
            answer = command["answers"][i][j]
            check_answer(result, answer)


def round(val, decimals=0):
    multiplier = tf.constant(10 ** decimals, dtype=val.dtype)
    return tf.round(val * multiplier) / multiplier


def torch_check_answer(result, answer):
    return bool(torch.all(torch.eq(result, answer)))


def tf_check_answer(result, answer):
    assert tf.reduce_all(tf.equal(round(result, 3), round(answer, 3)))
