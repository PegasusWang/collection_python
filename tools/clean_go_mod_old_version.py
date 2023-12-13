#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
清理 go mod 缓存的旧版本。
使用命令 go clean --modcache  可以清理所有的 go mod 拉下来的包，但是这里指向清理旧版本。

实现：列举所有的 dir，然后 sort 一下，保留最新的版本，旧版本删除。
需要使用 sudo 权限执行。切到一个特定的 go mod 目录下执行即可
"""

import os
import sys
import shutil
import functools
from pkg_resources import parse_version as version


def remove(path, real_remove=False):  # 删除文件夹或者文件
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        if real_remove:
            os.remove(path)  # remove the file
            print("remove", path)
        else:
            print("to remove", path)
    elif os.path.isdir(path):
        if real_remove:
            shutil.rmtree(path)  # remove dir and all contains
            print("rmtree", path)
        else:
            print("to rmtree", path)
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def get_all_sub_dir():
    dirs = [f for f in os.listdir("./") if os.path.isdir(f)]
    dirs.sort(key=functools.cmp_to_key(cpm_version))  # 排序后每个包只保留最后一个版本
    packages = set()
    for d in dirs:
        packagename = d.split("@")[0]
        packages.add(packagename)  # commonbiz@v1.1.10 获取包名  -> commonbiz

    package_maxversion = {}
    for d in dirs:  # 已经排序，这里每个包遍历赋值一遍就是最大的版本
        packagename = d.split("@")[0]
        package_maxversion[packagename] = d
    for k, v in package_maxversion.items():
        print(k, v)
    return package_maxversion


def remove_packagename_old_version(to_remove_package_name):
    dirs = [f for f in os.listdir("./") if os.path.isdir(f)]
    dirs.sort(key=functools.cmp_to_key(cpm_version))  # 排序后每个包只保留最后一个版本
    packages = set()
    for d in dirs:
        packagename = d.split("@")[0]
        packages.add(packagename)  # commonbiz@v1.1.10 获取包名  -> commonbiz

    package_dirs = []
    for d in dirs:  # 已经排序，这里每个包遍历赋值一遍就是最大的版本
        packagename = d.split("@")[0]
        if packagename == to_remove_package_name:
            package_dirs.append(d)
    to_remove_dirs = package_dirs[0:len(package_dirs)-1]  # 最后一个包是最新的，之前的都清理掉
    for remove_dir in to_remove_dirs:
        remove(remove_dir, True)


def cpm_version(dir1, dir2):
    s1 = dir1.split("@")[1]
    s2 = dir2.split("@")[1]
    try:  # 处理合法版本 v1.0.0
        v1 = version(s1)
        v2 = version(s2)
        if v1 < v2:
            return -1
        elif v1 == v2:
            return 0
        else:
            return 1
    except Exception:  # 处理类似这种版本 "v0.0.0-20231011075303-d9230068a794" < "v0.0.0-20231012052358-9836c2e23432"
        if s1 < s2:
            return -1
        elif s1 == s2:
            return 0
        else:
            return 1


def cpm_version_test():
    """
    pip install pytest
    """
    assert version("v1.0.0") < version("v1.0.1")
    assert version("v1.0.0") < version("v1.0.1-rc2")
    assert version("v1.0.87") < version("v1.0.443")
    assert "v0.0.0-20231011075303-d9230068a794" < "v0.0.0-20231012052358-9836c2e23432"


def main():
    try:
        packagename = sys.argv[1]
    except IndexError:
        print("please input package name")
        exit()
    remove_packagename_old_version(packagename)


if __name__ == "__main__":
    main()
