#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

cpu_none = 'MIMXRTNONE'
cpu_rt1170 = 'MIMXRT1176'
cpu_rt1020 = 'MIMXRT1021'
cpu_rt1050 = 'MIMXRT1052'
cpu_rt1060 = 'MIMXRT1062'
cpu_rt1010 = 'MIMXRT1011'
cpu_rt1015 = 'MIMXRT1015'

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

path_board_list = []
path_startup_list = []
path_linkfile_list = []


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


# 获取用户配置：ITCM Size, DTCM Size, OCRAM Size
def get_usr_input(flexram_type):
    if flexram_type == flexram_itcm:
        n = input("请输入ITCM Size Unit K (需要32的倍频)：")
    elif flexram_type == flexram_dtcm:
        n = input("请输入DTCM Size Unit K (需要32的倍频)：")
    else:
        n = input("请输入OCRAM Size Unit K (需要32的倍频且大于32)：")
    while True:
        try:
            n = float(n)
            if float(n) % 32 == 0:
                # print("成功");
                break
            else:
                n = input("输入错误，必须为32的倍数，请重新输入：")
        except:
            n = input("输入错误，只能为数字，请重新输入：")
    return n


# 检查用户配置：ITCM Size, DTCM Size, OCRAM Size
def check_usr_config():
    global flexram_itcm_size
    global flexram_dtcm_size
    global flexram_ocram_size

    global flexram_itcm
    global flexram_dtcm
    global flexram_ocram

    while True:
        try:
            flexram_itcm_size = get_usr_input(flexram_itcm)
            flexram_dtcm_size = get_usr_input(flexram_dtcm)
            flexram_ocram_size = get_usr_input(flexram_ocram)
            if flexram_ocram_size == 0 and cpu_selected == cpu_rt1050:
                print("OCRAM至少要大于32K")
                continue
            if flexram_itcm_size + flexram_dtcm_size + flexram_ocram_size < 512:
                print("设置成功\n\r");
                break
            else:
                print("ITCM %dK" % flexram_itcm_size)
                print("DTCM %dK" % flexram_dtcm_size)
                print("OCRAM %dK" % flexram_ocram_size)
                print("总和超过512K")
                pass
        except:
            prinf("程序发生异常：")
    get_usr_compiler()
    # 检查完配置，开始计算GPR17
    if cpu_selected == cpu_rt1060 or cpu_selected == cpu_rt1050:
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
    else:
        print("Default")


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


# 查找startup_MIMXRTxxxx.s
def seek_path_startup_s(file_dir):
    global path_startup_list
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if os.path.splitext(file)[1] == '.s' or os.path.splitext(file)[1] == '.S':
                path_startup_list.append(root + '\\' + file)
    return path_startup_list


# 查找board.c
def seek_path_board_c(file_dir):
    global path_board_list
    for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
        for file in files:
            if file == 'board.c':
                path_board_list.append(root + '\\' + file)
    return path_board_list


# 查找link文件
def seek_path_linkfile(file_dir):
    global path_linkfile_list
    global compiler_selected
    if compiler_selected == compiler_iar:
        for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
            for file in files:
                if os.path.splitext(file)[1] == '.icf':
                    path_linkfile_list.append(root + '\\' + file)
    else:
        for root, dirs, files in os.walk(file_dir):  # 在file_dir目录中遍历所有文件
            for file in files:
                if os.path.splitext(file)[1] == '.scf':
                    path_linkfile_list.append(root + '\\' + file)
    return path_linkfile_list


# 修改startup_MIMXRTxxxx.s for IAR
# 注意小写s对应IAR，大写S对应MDK
def set_startup_s(file_dir):
    while True:
        try:
            for num in range(0, len(path_startup_list)):
                file_data = ""
                get_Flag = 0
                with open(path_startup_list[num], "r", encoding="utf-8") as f:  # 打开startup文件
                    for line in f:
                        if 'CPSID' in line:
                            line = line + "\t\tLDR		R0, =  0x400AC038\n"
                            line = line + "\t\tLDR		R1, =  0x00AA0000\n"
                            line = line + "\t\tSTR     R1, [R0]\n"

                            line = line + "\t\tLDR		R0, =  0x400AC044\n"
                            line = line + "\t\tLDR		R1, =  0x%08x\n" % rt10xx_gpr17
                            line = line + "\t\tSTR     R1, [R0]\n"

                            line = line + "\t\tLDR		R0, =  0x400AC040\n"
                            line = line + "\t\tLDR		R1, =  0x00200007\n"
                            line = line + "\t\tSTR     R1, [R0]\n"
                            file_data += line
                            get_Flag = 1
                        if get_Flag == 1 and '0xE000ED08' not in line:
                            continue
                        elif '0xE000ED08' in line:
                            get_Flag = 0
                        file_data += line
                f.close()
                with open(path_startup_list[num], "r", encoding="utf-8") as f:  # 打开startup文件
                    for line in f:
                        if 'cpsid' in line:
                            line = line + "\t\tldr		r0, =  0x400AC038\n"
                            line = line + "\t\tldr		r1, =  0x00AA0000\n"
                            line = line + "\t\tstr     r1, [r0]\n"

                            line = line + "\t\tldr		r0, =  0x400AC044\n"
                            line = line + "\t\tldr		r1, =  0x%08x\n" % rt10xx_gpr17
                            line = line + "\t\tstr     r1, [r0]\n"

                            line = line + "\t\tldr		r0, =  0x400AC040\n"
                            line = line + "\t\tldr		r1, =  0x00200007\n"
                            line = line + "\t\tstr     r1, [r0]\n"
                            file_data += line
                            get_Flag = 1
                        if get_Flag == 1 and '0xE000ED08' not in line:
                            continue
                        elif '0xE000ED08' in line:
                            get_Flag = 0
                        file_data += line
                f.close()
                with open(path_startup_list[num], "w", encoding="utf-8") as f:
                    f.write(file_data)
                f.close()
            break
        except:
            print("打开文件发现异常\n\r")


# 修改board.c
def set_boards_mpu(file_dir):
    while True:
        try:
            for num in range(0, len(path_board_list)):
                file_data = ""
                jump_flag = 0
                with open(path_board_list[num], "r", encoding="utf-8") as f:  # 打开link文件
                    for line in f:
                        if jump_flag == 1:
                            jump_flag = 0
                            continue
                        # ITCM
                        if 'MPU->RBAR = ARM_MPU_RBAR(5, 0x00000000U)' in line:
                            line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, ARM_MPU_REGION_SIZE_512KB);\n"
                            jump_flag = 1
                        # DTCM
                        if '0x20000000' in line:
                            line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, ARM_MPU_REGION_SIZE_512KB);\n"
                            jump_flag = 1
                        file_data += line
                f.close()

                with open(path_board_list[num], "w", encoding="utf-8") as f:
                    f.write(file_data)
                f.close()
            break
        except:
            print("打开文件发现异常\n\r")


# 修改link file
def set_linkfile(file_dir):
    global path_linkfile_list
    global compiler_selected
    global flexram_itcm_size
    global flexram_dtcm_size
    global flexram_ocram_size
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    ocram_size = int(flexram_ocram_size * 1024)
    while True:
        try:
            for num in range(0, len(path_linkfile_list)):
                file_data = ""
                get_Flag = 0
                with open(path_linkfile_list[num], "r", encoding="utf-8") as f:  # 打开link文件
                    if compiler_selected == compiler_iar:
                        for line in f:
                            # ITCM
                            if 'm_text_end' in line and '0x0' in line:
                                line = "define symbol m_text_end               = 0x%08x\n;" % itcm_size
                            # DTCM
                            if 'm_data_end' in line and '0x2' in line:
                                line = "define symbol m_data_end               = 0x%08x\n;" % (dtcm_size | 0x20000000)
                            # OCRAM
                            if 'm_data2_end' in line and '0x202' in line:
                                line = "define symbol m_data2_end               = 0x%08x\n;" % (ocram_size | 0x20200000)
                            file_data += line
                    elif compiler_selected == compiler_mdk:
                        for line in f:
                            # ITCM
                            if 'm_text_size' in line:
                                line = "#define m_text_size                    0x%08x\n;" % itcm_size
                            # DTCM
                            if 'm_data_size' in line:
                                line = "#define m_data_size                    0x%08x\n;" % dtcm_size
                            # OCRAM
                            if 'm_data2_size' in line:
                                line = "#define m_data2_size                   0x%08x\n;" % ocram_size
                            file_data += line
                    else:
                        print("未找到编译环境")
                f.close()

                with open(path_linkfile_list[num], "w", encoding="utf-8") as f:
                    f.write(file_data)
                f.close()
            break
        except:
            print("打开文件发现异常\n\r")

get_rt_device("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
check_usr_config()
seek_path_startup_s("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
seek_path_linkfile("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
seek_path_board_c("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
set_startup_s("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
set_linkfile("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")
set_boards_mpu("./Python_HelloWorld_FlexRAM_RT1060_SDK290_IAR")