#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


def remove_files_with_rollback(target_dir, file_names):
    # 创建回滚目录
    rollback_dir = os.path.join(target_dir, "rollback")
    os.makedirs(rollback_dir, exist_ok=True)

    # 查找要删除的文件
    file_paths = []
    for file_name in file_names:
        file_path = os.path.join(target_dir, file_name)
        if os.path.exists(file_path):
            file_paths.append(file_path)

    # 将文件移动到回滚目录
    for file_path in file_paths:
        backup_path = os.path.join(rollback_dir, os.path.basename(file_path))
        shutil.move(file_path, backup_path)

    # 删除文件
    for file_path in file_paths:
        os.remove(file_path)

    return True


def rollback_removed_files(target_dir):
    # 获取回滚目录下的文件列表
    rollback_dir = os.path.join(target_dir, "rollback")
    if not os.path.exists(rollback_dir):
        print("回滚目录不存在，无法回滚")
        return False

    file_names = os.listdir(rollback_dir)

    # 将文件从回滚目录复制回原位置
    for file_name in file_names:
        backup_path = os.path.join(rollback_dir, file_name)
        target_path = os.path.join(target_dir, file_name)
        shutil.copy(backup_path, target_path)

    # 删除回滚目录
    shutil.rmtree(rollback_dir)

    return True


if __name__ == '__main__':
    # 示例：删除/tmp目录中的test1.txt和test2.txt文件，并支持回滚操作
    target_dir = "/tmp"
    file_names = ["test1.txt", "test2.txt"]
    remove_files_with_rollback(target_dir, file_names)

    # 回滚删除的文件
    rollback_removed_files(target_dir)
