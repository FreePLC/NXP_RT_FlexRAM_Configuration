#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

import main

"""
cpu_rt1010 = 'MIMXRT1011'
cpu_rt1015 = 'MIMXRT1015'
cpu_rt1020 = 'MIMXRT1021'
cpu_rt1050 = 'MIMXRT1052'
cpu_rt1060 = 'MIMXRT1062'
cpu_rt1170 = 'MIMXRT1176'

compiler_iar = 'iar'
compiler_mdk = 'mdk'
"""

flexram_itcm = 'ITCM'
flexram_dtcm = 'DTCM'
flexram_ocram = 'OCRAM'

"""
# 获取用户编译器类型
def get_usr_compiler():
    global compiler_selected
    print("请选择编译器类型：\n")
    print("1.IAR\n")
    print("2.MDK\n")
    n = input()
    while True:
        try:
            n = float(n)
            if n == 1:
                compiler_selected = compiler_iar
                print("您选择了IAR\n")
                break
            elif n == 2:
                compiler_selected = compiler_mdk
                print("您选择了MDK\n")
                break
            else:
                n = input("输入错误，必须为32的倍数，请重新输入：")
        except:
            n = input("输入错误，只能为数字，请重新输入：")
    return n
"""

# 获取用户配置：ITCM Size, DTCM Size, OCRAM Size
def get_usr_input(flexram_type):
    print('Hello userinput\n\r')
    if flexram_type == flexram_itcm:
        n = input("请输入ITCM Size Unit K (需要32的倍频)：")
    elif flexram_type == flexram_dtcm:
        n = input("请输入DTCM Size Unit K (需要32的倍频)：")
    else:
        n = input("请输入OCRAM Size Unit K (需要32的倍频)：")
    while True:
        try:
            n = float(n)
            if float(n) % 32 == 0:
                # print("成功")
                break
            else:
                n = input("输入错误，必须为32的倍数，请重新输入：")
        except:
            n = input("输入错误，只能为数字，请重新输入：")
    return n
