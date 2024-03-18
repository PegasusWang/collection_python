#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import glob
import datetime

def backup_file(file_path):
    """备份文件"""
    backup_dir = os.path.dirname(file_path)
    backup_name = os.path.basename(file_path) + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(file_path, backup_path)
    print(f"备份文件 {file_path} 到 {backup_path}")

def rollback_file(backup_path, file_path):
    """回滚文件"""
    shutil.copy2(backup_path, file_path)
    print(f"回滚文件 {file_path} 到 {backup_path}")

def delete_files(path, pattern, backup=True):
    """删除指定路径下匹配某个模式的文件"""
    file_list = glob.glob(os.path.join(path, pattern))
    if not file_list:
        print(f"没有找到匹配 {pattern} 的文件")
        return

    for file_path in file_list:
        if backup:
            backup_file(file_path)
        os.remove(file_path)
        print(f"删除文件 {file_path} 成功")

def main():
    path = input("请输入文件路径：")
    pattern = input("请输入匹配模式：")
    backup = input("是否备份文件（y/n）：").lower() == 'y'

    delete_files(path, pattern, backup)

    if backup:
        rollback = input("是否回滚文件（y/n）：").lower() == 'y'
        if rollback:
            backup_list = glob.glob(os.path.join(path, pattern + '_*'))
            if not backup_list:
                print("没有找到备份文件")
                return

            print("备份文件列表：")
            for i, backup_path in enumerate(backup_list):
                print(f"{i + 1}. {backup_path}")

            index = int(input("请选择要回滚的备份文件编号："))
            if index < 1 or index > len(backup_list):
                print("无效的编号")
                return

            backup_path = backup_list[index - 1]
            file_path = backup_path[:-(len(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + 1)]
            rollback_file(backup_path, file_path)

if __name__ == '__main__':
    main()
