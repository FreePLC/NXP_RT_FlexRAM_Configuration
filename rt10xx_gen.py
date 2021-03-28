#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

import main


# 修改startup_MIMXRTxxxx.s for IAR
# 注意小写s对应IAR，大写S对应MDK
def set_startup_10xx_iar(path_startup_list, gpr17):
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(path_startup_list, "r", encoding="utf-8") as f:  # 打开startup文件
                for line in f:
                    if 'CPSID' in line:
                        line = line + "\t\tLDR		R0, =  0x400AC038\n"
                        line = line + "\t\tLDR		R1, =  0x00AA0000\n"
                        line = line + "\t\tSTR     R1, [R0]\n"

                        line = line + "\t\tLDR		R0, =  0x400AC044\n"
                        line = line + "\t\tLDR		R1, =  0x%08x\n" % gpr17
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
            with open(path_startup_list, "w", encoding="utf-8") as f:
                f.write(file_data)
            f.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_startup_10xx_mdk(path_startup_list, gpr17):
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(path_startup_list, "r", encoding="utf-8") as f:  # 打开startup文件
                for line in f:
                    if 'cpsid' in line:
                        line = line + "\tldr		r0, =  0x400AC038\n"
                        line = line + "\tldr		r1, =  0x00AA0000\n"
                        line = line + "\tstr     r1, [r0]\n"

                        line = line + "\tldr		r0, =  0x400AC044\n"
                        line = line + "\tldr		r1, =  0x%08x\n" % gpr17
                        line = line + "\tstr     r1, [r0]\n"

                        line = line + "\tldr		r0, =  0x400AC040\n"
                        line = line + "\tldr		r1, =  0x00200007\n"
                        line = line + "\tstr     r1, [r0]\n"
                        file_data += line
                        get_Flag = 1
                    if get_Flag == 1 and '0xE000ED08' not in line:
                        continue
                    elif '0xE000ED08' in line:
                        get_Flag = 0
                    file_data += line
            f.close()
            with open(path_startup_list, "w", encoding="utf-8") as f:
                f.write(file_data)
            f.close()
            break
        except:
            print("打开文件发现异常\n\r")


# 修改board.c
def set_boards_10xx_mpu(path_board_list):
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
                            line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, " \
                                          "ARM_MPU_REGION_SIZE_512KB);\n "
                            jump_flag = 1
                        # DTCM
                        if '0x20000000' in line:
                            line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, " \
                                          "ARM_MPU_REGION_SIZE_512KB);\n "
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
def set_linkfile_rt10xx_ram_iar(file_dir, flexram_itcm_size, flexram_dtcm_size, flexram_ocram_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    ocram_size = int(flexram_ocram_size * 1024)
    if '1062' in file_dir:
        ocram_size = ocram_size + 0x80000
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(file_dir, "r", encoding="utf-8") as f:  # 打开link文件
                for line in f:
                    if 'm_text_start' in line and 'symbol' in line:
                        line = line + "\t\tdefine symbol m_text_end               = 0x%08x;\n" % (itcm_size - 1)
                        line = line + "\t\tdefine symbol m_data_start             = 0x20000000;\n"
                        line = line + "\t\tdefine symbol m_data_end               = 0x%08x;\n" % (
                                (dtcm_size | 0x20000000) - 1)
                        line = line + "\t\tdefine symbol m_data2_start            = 0x20200000;\n"
                        line = line + "\t\tdefine symbol m_data2_end              = 0x%08x;\n" % (
                                (ocram_size | 0x20200000) - 1)
                        file_data += line
                        get_Flag = 1
                    if get_Flag == 1 and 'Sizes' not in line:
                        continue
                    elif 'Sizes' in line:
                        get_Flag = 0
                    file_data += line
                f.close()
            with open(file_dir, "w", encoding="utf-8") as fw:
                fw.write(file_data)
            fw.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_linkfile_rt10xx_xip_iar(file_dir, flexram_itcm_size, flexram_dtcm_size, flexram_ocram_size):
    # itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    ocram_size = int(flexram_ocram_size * 1024)
    if '1062' in file_dir:
        ocram_size = ocram_size + 0x80000
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(file_dir, "r", encoding="utf-8") as f:  # 打开link文件
                for line in f:
                    if 'm_data_start' in line and 'symbol' in line:
                        line = line + "\t\tdefine symbol m_data_end               = 0x%08x;\n" % (
                                (dtcm_size | 0x20000000) - 1)
                        line = line + "\t\tdefine symbol m_data2_start            = 0x20200000;\n"
                        line = line + "\t\tdefine symbol m_data2_end              = 0x%08x;\n" % (
                                (ocram_size | 0x20200000) - 1)
                        line = line + "\t\tdefine exported symbol m_boot_hdr_conf_start = 0x60000000;\n"
                        line = line + "\t\tdefine symbol m_boot_hdr_ivt_start           = 0x60001000;\n"
                        line = line + "\t\tdefine symbol m_boot_hdr_boot_data_start     = 0x60001020;\n"
                        line = line + "\t\tdefine symbol m_boot_hdr_dcd_data_start      = 0x60001030;\n"
                        file_data += line
                        get_Flag = 1
                    if get_Flag == 1 and 'Sizes' not in line:
                        continue
                    elif 'Sizes' in line:
                        get_Flag = 0
                    file_data += line
                f.close()
            with open(file_dir, "w", encoding="utf-8") as fw:
                fw.write(file_data)
            fw.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_linkfile_rt10xx_ram_mdk(file_dir, flexram_itcm_size, flexram_dtcm_size, flexram_ocram_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    ocram_size = int(flexram_ocram_size * 1024)
    if '1062' in file_dir:
        ocram_size = ocram_size + 0x80000
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(file_dir, "r", encoding="utf-8") as f:  # 打开link文件
                for line in f:
                    if 'm_text_start' in line and 'define' in line:
                        line = line + "\t#define m_text_size                0x%08x\n" % (itcm_size - 0x400)
                        line = line + "\t#define m_data_start              0x20000000\n"
                        line = line + "\t#define m_data_size                0x%08x\n" % dtcm_size
                        line = line + "\t#define m_data2_start                  0x20200000\n"
                        line = line + "\t#define m_data2_size                   0x%08x\n" % ocram_size
                        file_data += line
                        get_Flag = 1
                    if get_Flag == 1 and 'Sizes' not in line:
                        continue
                    elif 'Sizes' in line:
                        get_Flag = 0
                    file_data += line
                f.close()
            with open(file_dir, "w", encoding="utf-8") as fw:
                fw.write(file_data)
            fw.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_linkfile_rt10xx_xip_mdk(file_dir, flexram_itcm_size, flexram_dtcm_size, flexram_ocram_size):
    #itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    ocram_size = int(flexram_ocram_size * 1024)
    if '1062' in file_dir:
        ocram_size = ocram_size + 0x80000
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(file_dir, "r", encoding="utf-8") as f:  # 打开link文件
                for line in f:
                    if 'm_data_start' in line and 'define' in line:
                        line = line + "\t#define m_data_size                \
                        (0x%08x - m_interrupts_ram_size)\n" % dtcm_size
                        line = line + "\t#define m_data2_start                  0x20200000\n"
                        line = line + "\t#define m_data2_size                   0x%08x\n" % ocram_size
                        file_data += line
                        get_Flag = 1
                    if get_Flag == 1 and 'Sizes' not in line:
                        continue
                    elif 'Sizes' in line:
                        get_Flag = 0
                    file_data += line
                f.close()
            with open(file_dir, "w", encoding="utf-8") as fw:
                fw.write(file_data)
            fw.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_linkfile_rt10xx(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size, flexram_ocram_size):
    for num in range(0, len(path_linkfile_list)):
        if '_ram.icf' in path_linkfile_list[num]:
            set_linkfile_rt10xx_ram_iar(path_linkfile_list[num], flexram_itcm_size,
                                        flexram_dtcm_size, flexram_ocram_size)
        if 'flexspi_nor.icf' in \
                path_linkfile_list[num]:
            set_linkfile_rt10xx_xip_iar(path_linkfile_list[num], flexram_itcm_size,
                                        flexram_dtcm_size, flexram_ocram_size)
        if '_ram.scf' in path_linkfile_list[num]:
            set_linkfile_rt10xx_ram_mdk(path_linkfile_list[num], flexram_itcm_size,
                                        flexram_dtcm_size, flexram_ocram_size)
        if 'flexspi_nor.scf' in \
                path_linkfile_list[num]:
            set_linkfile_rt10xx_xip_mdk(path_linkfile_list[num], flexram_itcm_size,
                                        flexram_dtcm_size, flexram_ocram_size)


def set_startup_10xx_s(path_startup_list, rt10xx_gpr17):
    for num in range(0, len(path_startup_list)):
        if '.s' in path_startup_list[num]:
            set_startup_10xx_iar(path_startup_list[num], rt10xx_gpr17)
        elif '.S' in path_startup_list[num]:
            set_startup_10xx_mdk(path_startup_list[num], rt10xx_gpr17)
        else:
            print("Unsupport now \r\n")
