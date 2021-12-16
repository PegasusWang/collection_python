# -*- coding: utf-8 -*-

"""
大数据处理，用来生成文件，分解文件等

分解文件有一个库：

https://github.com/ram-jayapalan/filesplit

https://www.bswen.com/2018/04/python-How-to-generate-random-large-file-using-python.html

"""
import os
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


def main():
    # 生成一个大文件
    filename = "nums.txt"
    generate_big_random_digits(filename, 1, 1000, 1024 * 1024)
    # 分割大文件，用于一些比较大数据处理的问题
    split(filename)


if __name__ == "__main__":
    main()
