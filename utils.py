import json
import random

with open('id2char', 'r', encoding='utf-8') as f_id2char:
    id2char = json.load(f_id2char)
char_length = len(id2char)

with open('words', 'r', encoding='utf-8') as f_words:
    words = f_words.read().splitlines()
words_length = len(words)


def sentence_generation(length):
    """
    :param length: 要生成句子的长度
    :return: 生成的句子
    """
    sentence = ''
    for i in range(length):
        index = random.randint(0, char_length - 1)
        sentence += id2char[str(index)]
    return sentence


def random_word():
    temp = random.randint(0, 19)
    index = random.randint(0, words_length-1)
    right = 6 if len(words[index]) > 6 else len(words[index])
    return words[index][:right] if temp else ''
