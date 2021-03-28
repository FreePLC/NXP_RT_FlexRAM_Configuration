#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

from userinput import *
from rt10xx_gen import *
from rt11xx_gen import *
from getpath import *

# import userinput
# import rt10xx_gen
# import rt11xx_gen
# import getpath

cpu_none = 'MIMXRTNONE'

cpu_rt1010 = 'MIMXRT1011'
cpu_rt1015 = 'MIMXRT1015'
cpu_rt1020 = 'MIMXRT1021'
cpu_rt1050 = 'MIMXRT1052'
cpu_rt1060 = 'MIMXRT1062'
cpu_rt1170 = 'MIMXRT1176'

cpu_selected = cpu_none

compiler_iar = 'iar'
compiler_mdk = 'mdk'

flexram_itcm = 'ITCM'
flexram_dtcm = 'DTCM'
flexram_ocram = 'OCRAM'

flexram_itcm_size = 0
flexram_dtcm_size = 0
flexram_ocram_size = 0

compiler_selected = compiler_iar

rt10xx_gpr17 = 0

rt11xx_gpr17 = 0
rt11xx_gpr18 = 0

path_board_list = []
path_startup_list = []
path_linkfile_list = []


# 检查用户配置：ITCM Size, DTCM Size, OCRAM Size
def check_usr_config(file_dir):
    global flexram_itcm_size
    global flexram_dtcm_size
    global flexram_ocram_size

    global flexram_itcm
    global flexram_dtcm
    global flexram_ocram

    while True:
        try:
            if cpu_selected == cpu_rt1050 or cpu_selected == cpu_rt1060:
                flexram_itcm_size = get_usr_input(flexram_itcm)
                flexram_dtcm_size = get_usr_input(flexram_dtcm)
                flexram_ocram_size = get_usr_input(flexram_ocram)
                if flexram_ocram_size == 0:
                    print("OCRAM至少要大于32K")
                    continue
                if flexram_itcm_size + flexram_dtcm_size + flexram_ocram_size < 513:
                    print("设置成功\n\r")
                    break
                else:
                    print("ITCM %dK" % flexram_itcm_size)
                    print("DTCM %dK" % flexram_dtcm_size)
                    print("OCRAM %dK" % flexram_ocram_size)
                    print("总和不能超过512K，请重新输入\n\r")
                    pass

            if cpu_selected == cpu_rt1020:
                flexram_itcm_size = get_usr_input(flexram_itcm)
                flexram_dtcm_size = get_usr_input(flexram_dtcm)
                flexram_ocram_size = get_usr_input(flexram_ocram)
                if flexram_ocram_size == 0:
                    print("OCRAM至少要大于32K")
                    continue
                if flexram_itcm_size + flexram_dtcm_size + flexram_ocram_size < 257:
                    print("设置成功\n\r")
                    break
                else:
                    print("ITCM %dK" % flexram_itcm_size)
                    print("DTCM %dK" % flexram_dtcm_size)
                    print("OCRAM %dK" % flexram_ocram_size)
                    print("总和不能超过256K，请重新输入\n\r")
                    pass

            if cpu_selected == cpu_rt1010 or cpu_selected == cpu_rt1015:
                flexram_itcm_size = get_usr_input(flexram_itcm)
                flexram_dtcm_size = get_usr_input(flexram_dtcm)
                flexram_ocram_size = get_usr_input(flexram_ocram)
                if flexram_ocram_size == 0:
                    print("OCRAM至少要大于32K")
                    continue
                if flexram_itcm_size + flexram_dtcm_size + flexram_ocram_size < 129:
                    print("设置成功\n\r")
                    break
                else:
                    print("ITCM %dK" % flexram_itcm_size)
                    print("DTCM %dK" % flexram_dtcm_size)
                    print("OCRAM %dK" % flexram_ocram_size)
                    print("总和不能超过128K，请重新输入\n\r")
                    pass

            if cpu_selected == cpu_rt1170:
                print("请输入CM7配置\n\r")
                flexram_itcm_size = get_usr_input(flexram_itcm)
                flexram_dtcm_size = get_usr_input(flexram_dtcm)
                flexram_ocram_size = get_usr_input(flexram_ocram)

                if flexram_itcm_size + flexram_dtcm_size + flexram_ocram_size < 513:
                    print("设置成功\n\r")
                    break
                else:
                    print("ITCM %dK" % flexram_itcm_size)
                    print("DTCM %dK" % flexram_dtcm_size)
                    print("OCRAM %dK" % flexram_ocram_size)
                    print("总和不能超过128K，请重新输入\n\r")
                    pass

        except:
            print("程序发生异常：")
    # get_usr_compiler()
    # 检查完配置，开始计算GPR17
    if cpu_selected == cpu_rt1010 or cpu_selected == cpu_rt1015 or cpu_selected == cpu_rt1020 \
            or cpu_selected == cpu_rt1050 or cpu_selected == cpu_rt1060:
        itcm_bank_num = flexram_itcm_size / 32
        dtcm_bank_num = flexram_dtcm_size / 32
        ocram_bank_num = flexram_ocram_size / 32
        global rt10xx_gpr17
        rt10xx_gpr17 = 0
        for num in range(0, int(itcm_bank_num)):
            rt10xx_gpr17 |= 0x3 << (num * 2)
        for num in range(int(itcm_bank_num), int(dtcm_bank_num + itcm_bank_num)):
            rt10xx_gpr17 |= 0x2 << (num * 2)
        for num in range(int(dtcm_bank_num + itcm_bank_num), int(dtcm_bank_num + itcm_bank_num + ocram_bank_num)):
            rt10xx_gpr17 |= 0x1 << (num * 2)

        print("The GPR17 is %d" % rt10xx_gpr17)
        seek_path_startup_s(file_dir, path_startup_list)
        seek_path_linkfile(file_dir, path_linkfile_list)
        seek_path_board_c(file_dir, path_board_list)
        set_startup_10xx_s(path_startup_list, rt10xx_gpr17)
        set_linkfile_rt10xx(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size,
                            flexram_ocram_size)
        set_boards_10xx_mpu(path_board_list)

    elif cpu_selected == cpu_rt1170:
        itcm_bank_num = flexram_itcm_size / 32
        dtcm_bank_num = flexram_dtcm_size / 32
        ocram_bank_num = flexram_ocram_size / 32
        global rt11xx_gpr17
        global rt11xx_gpr18
        rt11xx_gpr17 = 0
        rt11xx_gpr18 = 0

        for num in range(0, int(itcm_bank_num)):
            rt11xx_gpr17 |= 0x3 << (num * 2)
        for num in range(int(itcm_bank_num), int(dtcm_bank_num + itcm_bank_num)):
            rt11xx_gpr17 |= 0x2 << (num * 2)
        for num in range(int(dtcm_bank_num + itcm_bank_num), int(dtcm_bank_num + itcm_bank_num + ocram_bank_num)):
            rt11xx_gpr17 |= 0x1 << (num * 2)

        rt11xx_gpr18 = rt11xx_gpr17 >> 16
        rt11xx_gpr17 = rt11xx_gpr17 & 0xFFFF
        print("The GPR17 is %d" % rt11xx_gpr17)
        print("The GPR18 is %d" % rt11xx_gpr18)
        seek_path_startup_s(file_dir, path_startup_list)
        seek_path_linkfile(file_dir, path_linkfile_list)
        seek_path_board_c(file_dir, path_board_list)
        set_startup_rt11xx_s(path_startup_list, rt11xx_gpr17, rt11xx_gpr18)
        set_linkfile_rt11xx(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size)
        set_boards_rt11xx_mpu(path_board_list)
    else:
        print("无法找到RT系列MCU，请确认路径是否正确\r\n")


# 查找需要修改FlexRAM的CPU型号
def get_rt_device(file_dir):
    cpu_get = cpu_none
    global cpu_selected
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for dir in dirs:
            if dir == cpu_rt1170:
                cpu_get = cpu_rt1170
                break
            elif dir == cpu_rt1050:
                cpu_get = cpu_rt1050
                break
            elif dir == cpu_rt1060:
                cpu_get = cpu_rt1060
                break
            elif dir == cpu_rt1020:
                cpu_get = cpu_rt1020
                break
            elif dir == cpu_rt1010:
                cpu_get = cpu_rt1010
                break
            elif dir == cpu_rt1015:
                cpu_get = cpu_rt1015
                break
    cpu_selected = cpu_get


if __name__ == '__main__':
    get_rt_device("./hello_world_rt1060_iar")
    check_usr_config("./hello_world_rt1060_iar")
# seek_path_startup_s("./hello_world_demo_cm7_mdk")
# seek_path_linkfile("./hello_world_demo_cm7_iar")
# seek_path_board_c("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
# set_startup_s("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
# set_linkfile("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
# set_boards_mpu("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
