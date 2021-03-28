#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

import main

cpu_rt1010 = 'MIMXRT1011'
cpu_rt1015 = 'MIMXRT1015'
cpu_rt1020 = 'MIMXRT1021'
cpu_rt1050 = 'MIMXRT1052'
cpu_rt1060 = 'MIMXRT1062'
cpu_rt1170 = 'MIMXRT1176'


# 查找startup_MIMXRTxxxx.s
def seek_path_startup_s(file_dir, path_startup_list):
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if os.path.splitext(file)[1] == '.s' or os.path.splitext(file)[1] == '.S':
                path_startup_list.append(root + '\\' + file)
    return path_startup_list


# 查找board.c
def seek_path_board_c(file_dir, path_board_list):
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if file == 'board.c':
                path_board_list.append(root + '\\' + file)
    return path_board_list


# 查找link文件
def seek_path_linkfile(file_dir, path_linkfile_list):
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if os.path.splitext(file)[1] == '.icf':
                path_linkfile_list.append(root + '\\' + file)

    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if os.path.splitext(file)[1] == '.scf':
                path_linkfile_list.append(root + '\\' + file)

    return path_linkfile_list
