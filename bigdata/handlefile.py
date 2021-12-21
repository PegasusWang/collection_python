# -*- coding: utf-8 -*-

"""
大数据处理，用来生成文件，分解文件等做测试。

1. 分解文件有一个库：

https://github.com/ram-jayapalan/filesplit

https://www.bswen.com/2018/04/python-How-to-generate-random-large-file-using-python.html


2. linux 文件命令 split 拆分文件

"""
import os
import itertools
import time
import random
import string


def gen_bin():
    # GB1 = 1024*1024*1024 # 1GB
    # size = 50 # desired size in GB
    GB1 = 1024
    size = 5  # desired size in GB
    with open('large_file.txt', 'wb') as fout:
        for _ in range(size + 1):
            fout.write(os.urandom(GB1))


def gen_random_ascii(filename="bla.txt"):
    t0 = time.time()
    open(filename, "wb").write(''.join(random.choice(
        string.ascii_lowercase) for i in range(10**7)))
    d = time.time() - t0
    print("duration: %.2f s." % d)


def generate_big_random_bin_file(filename, size):
    """
    generate big binary file with the specified size in bytes
    :param filename: the filename
    :param size: the size in bytes
    :return:void
    """
    import os
    with open('%s' % filename, 'wb') as fout:
        fout.write(os.urandom(size))  # 1

    print('big random binary file with size %f generated ok' % size)
    pass


def generate_big_random_letters(filename, size):
    """
    generate big random letters/alphabets to a file
    :param filename: the filename
    :param size: the size in bytes
    :return: void
    """
    chars = ''.join([random.choice(string.ascii_letters)
                    for i in range(size)])  # 1

    with open(filename, 'w') as f:
        f.write(chars)


def generate_big_sparse_file(filename, size):
    f = open(filename, "wb")
    f.seek(size - 1)
    f.write("\1")
    f.close()
    pass


def generate_big_random_sentences(filename, linecount):
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")

    all = [nouns, verbs, adj, adv]

    with open(filename, 'w') as f:
        for i in range(linecount):
            f.writelines([' '.join([random.choice(i) for i in all]), '\n'])


def generate_big_incr_digits(filename, start, step, size):
    i = itertools.count(start, step)
    nums = '\n'.join(
        (str(next(i)) for _ in range(size))
    )  # 1

    with open(filename, 'w') as f:
        f.write(nums)


def generate_big_random_digits(filename, start, end, size):
    nums = '\n'.join(
        (str(random.randint(start, end)) for _ in range(size))
    )  # 1

    with open(filename, 'w') as f:
        f.write(nums)


def split(filename):
    NUM_OF_LINES = 100000
    with open(filename) as fin:
        fout = open("output0.txt", "wb")
        for i, line in enumerate(fin):
            fout.write(line.encode())
            if (i+1) % NUM_OF_LINES == 0:
                fout.close()
                fout = open("output%d.txt" % (i/NUM_OF_LINES+1), "wb")

        fout.close()


"""
# TODO 如何合并大文件

1. cat 命令合并:
cat file1 file2 file3 > bigfile
cat file1 file2 file3 | sqlite database

2. 使用 python 块读取然后追加写入

https://stackoverflow.com/questions/5509872/python-append-multiple-files-in-given-order-to-one-big-file

def append_file_to_file(_from, _to):
    block_size = 1024*1024
    with open(_to, "ab") as outfile, open(_from, "rb") as infile:
        while True:
            input_block = infile.read(block_size)
            if not input_block:
                break
            outfile.write(input_block)
# Given this building block, you can use:

for filename in ['a.bin','b.bin','c.bin']:
    append_file_to_file(filename, 'outfile.bin')

3. use dask. https://rcpedia.stanford.edu/topicGuides/merging_data_sets_dask.html
"""


def main():
    # 生成一个大文件
    filename = "nums.txt"
    # generate_big_random_digits(filename, 1, 1000, 1024 * 1024)
    generate_big_incr_digits(filename, 1, 1, 1024 * 1024)
    # 分割大文件，用于一些比较大数据处理的问题
    split(filename)


if __name__ == "__main__":
    main()
