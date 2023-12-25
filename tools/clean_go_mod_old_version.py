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
    dirs.sort(key=functools.cmp_to_key(cmp_version))  # 排序后每个包只保留最后一个版本
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
    dirs.sort(key=functools.cmp_to_key(cmp_version))  # 排序后每个包只保留最后一个版本
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


def cmp_version(dir1, dir2):
    """
    比较版本号，需要处理多种格式的版本。先获取版本号，然后拆分成两部分 a.b.c 和 后半部分。先比较前半部分，然后比较后半部分
    base@v0.0.5-rc1
    commonbiz@v1.1.26
    novel_fm_mealsdk@v0.0.0-20230322064632-ab19d8ea0f0e
    """
    s1 = dir1.split("@")[1]
    s2 = dir2.split("@")[1]

    sv1 = s1.split("-")[0]
    sv2 = s2.split("-")[0]

    # 先比较第一部分
    v1 = version(sv1)
    v2 = version(sv2)
    if v1 < v2:
        return -1
    if v1 > v2:
        return 1
    # 如果第一部分相等，比较第二部分
    ss1 = s1.split("-")
    ss2 = s2.split("-")
    s1second = ss1[1] if len(ss1) > 1 else ""
    s2second = ss2[1] if len(ss2) > 1 else ""
    if s1second < s2second:
        return -1
    elif s1second == s2second:
        return 0
    else:
        return 1


def version_test():
    """
    pip install pytest
    """
    assert version("v1.0.0") < version("v1.0.1")
    assert version("v1.0.0") < version("v1.0.1-rc2")
    assert version("v1.0.87") < version("v1.0.443")
    assert "v0.0.0-20231011075303-d9230068a794" < "v0.0.0-20231012052358-9836c2e23432"


def cpm_version_test():
    assert cmp_version("pkg@v1.0.0", "pkg@v1.0.1") == -1
    assert cmp_version("pkg@v1.0.0", "pkg@v1.0.1-rc2") == -1
    assert cmp_version("pkg@v1.0.87", "pkg@v1.0.443") == -1
    assert cmp_version("pkg@v0.0.0-20231011075303-d9230068a794",
                       "pkg@v0.0.0-20231012052358-9836c2e23432") == -1
    assert cmp_version(
        "pkg@v1.0.24", "pkg@v1.0.29-0.20230703093406-7d8703fcbc29") == -1
    assert cmp_version("pkg@v1.0.24", "pkg@v1.0.24") == 0


def main():
    try:
        packagename = sys.argv[1]
    except IndexError:
        print("please input package name")
        exit()
    remove_packagename_old_version(packagename)


if __name__ == "__main__":
    # cpm_version_test()
    main()
