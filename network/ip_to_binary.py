#!/usr/bin/env python
# -*- coding: utf-8 -*-
def ip_to_binary(ip):
    # 将IP地址拆分成四个数字
    nums = ip.split('.')
    # 将每个数字转换为8位的二进制数
    binary_nums = [bin(int(num))[2:].zfill(8) for num in nums]
    # 将四个二进制数拼接起来
    binary_str = ''.join(binary_nums)
    # 将32位二进制数转换为字符串格式并返回
    return binary_str


if __name__ == '__main__':
    ip = '192.168.1.1'
    binary_ip = ip_to_binary(ip)
    print(binary_ip)
