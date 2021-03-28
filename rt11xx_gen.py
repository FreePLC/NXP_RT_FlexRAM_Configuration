#!/usr/bin/python 
# coding=utf-8

import os
import io
import re

import main


def set_startup_rt11xx_cm7_iar(path_startup_list, rt11xx_gpr17, rt11xx_gpr18):
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(path_startup_list, "r", encoding="utf-8") as f:  # 打开startup文件
                for line in f:
                    if 'CPSID' in line:
                        line = line + "\t\tLDR		R0, =  0x400E4044\n"
                        line = line + "\t\tLDR		R1, =  0x%08x\n" % rt11xx_gpr17
                        line = line + "\t\tSTR     R1, [R0]\n"

                        line = line + "\t\tLDR		R0, =  0x400E4048\n"
                        line = line + "\t\tLDR		R1, =  0x%08x\n" % rt11xx_gpr18
                        line = line + "\t\tSTR     R1, [R0]\n"

                        line = line + "\t\tLDR		R0, =  0x400E4040\n"
                        line = line + "\t\tLDR		R1, =  0x0000AA07\n"
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


def set_startup_rt11xx_cm7_mdk(path_startup_list, rt11xx_gpr17, rt11xx_gpr18):
    while True:
        try:
            file_data = ""
            get_Flag = 0
            with open(path_startup_list, "r", encoding="utf-8") as f:  # 打开startup文件
                for line in f:
                    if 'cpsid' in line:
                        line = line + "\tldr		r0, =  0x400E4044\n"
                        line = line + "\tldr		r1, =  0x%08x\n" % rt11xx_gpr17
                        line = line + "\tstr     r1, [r0]\n"

                        line = line + "\tldr		r0, =  0x400E4048\n"
                        line = line + "\tldr		r1, =  0x%08x\n" % rt11xx_gpr18
                        line = line + "\tstr     r1, [r0]\n"

                        line = line + "\tldr		r0, =  0x400E4040\n"
                        line = line + "\tldr		r1, =  0x0000AA07\n"
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
def set_boards_rt11xx_cm7_mpu(path_board_list):
    while True:
        try:
            file_data = ""
            jump_flag = 0
            with open(path_board_list, "r", encoding="utf-8") as f:  # 打开link文件
                for line in f:
                    if jump_flag == 1:
                        jump_flag = 0
                        continue
                    # ITCM
                    if 'MPU->RBAR = ARM_MPU_RBAR(4, 0x00000000U)' in line:
                        line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, " \
                                      "ARM_MPU_REGION_SIZE_512KB);\n "
                        jump_flag = 1
                    # DTCM
                    if 'MPU->RBAR = ARM_MPU_RBAR(5, 0x20000000U)' in line:
                        line = line + "\tMPU->RASR = ARM_MPU_RASR(0, ARM_MPU_AP_FULL, 0, 0, 1, 1, 0, " \
                                      "ARM_MPU_REGION_SIZE_512KB);\n "
                        jump_flag = 1
                    file_data += line
            f.close()

            with open(path_board_list, "w", encoding="utf-8") as f:
                f.write(file_data)
            f.close()
            break
        except:
            print("打开文件发现异常\n\r")


def set_linkfile_rt11xx_ram_cm7_iar(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    get_Flag = 0
    file_data = ""
    with open(path_linkfile_list, "r", encoding="utf-8") as f:  # 打开link文件
        for line in f:
            if 'm_text_start' in line and 'symbol' in line:
                line = line + "\t\tdefine symbol m_text_end               = 0x%08x;\n" % itcm_size
                line = line + "\t\tdefine symbol m_data_start             = 0x20000000;\n"
                line = line + "\t\tdefine symbol m_data_end               = 0x%08x;\n" % (dtcm_size | 0x20000000)
                line = line + "\t\tdefine symbol m_data2_start            = 0x202C0000;\n"
                line = line + "\t\tdefine symbol m_data2_end              = 0x2033FFFF;\n"
                file_data += line
                get_Flag = 1
            if get_Flag == 1 and 'Sizes' not in line:
                continue
            elif 'Sizes' in line:
                get_Flag = 0
            file_data += line
        f.close()
        with open(path_linkfile_list, "w", encoding="utf-8") as fw:
            fw.write(file_data)
        fw.close()


def set_linkfile_rt11xx_xip_cm7_iar(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    get_Flag = 0
    file_data = ""
    with open(path_linkfile_list, "r", encoding="utf-8") as f:  # 打开link文件
        for line in f:
            if 'm_text2_start' in line and 'symbol' in line:
                line = line + "\t\tdefine symbol m_text2_end              = 0x%08x;\n" % (itcm_size - 1)
                line = line + "\t\tdefine symbol m_interrupts_ram_start   = 0x20000000;\n"
                line = line + "\t\tdefine symbol m_interrupts_ram_end     = 0x20000000 + __ram_vector_table_offset__;\n"
                line = line + "\t\tdefine symbol m_data_start             = m_interrupts_ram_start + " \
                              "__ram_vector_table_size__;\n "
                line = line + "\t\tdefine symbol m_data_end               = 0x%08x;\n" % ((dtcm_size | 0x20000000) - 1)
                file_data += line
                get_Flag = 1
            if get_Flag == 1 and '__use_shmem__' not in line:
                continue
            elif '__use_shmem__' in line:
                get_Flag = 0
            file_data += line
        f.close()
        with open(path_linkfile_list, "w", encoding="utf-8") as fw:
            fw.write(file_data)
        fw.close()


def set_linkfile_rt11xx_ram_cm7_mdk(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    get_Flag = 0
    file_data = ""
    with open(path_linkfile_list, "r", encoding="utf-8") as f:  # 打开link文件
        for line in f:
            if 'm_text_start' in line and 'define' in line:
                line = line + "\t#define m_text_size                0x%08x\n" % (itcm_size-0x400)
                line = line + "\t#define m_data_start              0x20000000\n"
                line = line + "\t#define m_data_size                0x%08x\n" % dtcm_size
                line = line + "\t#define m_data2_start                  0x202C0000\n"
                line = line + "\t#define m_data2_size                   0x00080000\n"
                file_data += line
                get_Flag = 1
            if get_Flag == 1 and 'Sizes' not in line:
                continue
            elif 'Sizes' in line:
                get_Flag = 0
            file_data += line
        f.close()
        with open(path_linkfile_list, "w", encoding="utf-8") as fw:
            fw.write(file_data)
        fw.close()


def set_linkfile_rt11xx_xip_cm7_mdk(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size):
    itcm_size = int(flexram_itcm_size * 1024)
    dtcm_size = int(flexram_dtcm_size * 1024)
    get_Flag = 0
    file_data = ""
    with open(path_linkfile_list, "r", encoding="utf-8") as f:  # 打开link文件
        for line in f:
            if 'm_text2_start' in line and 'define' in line:
                line = line + "\t#define m_text2_size                0x%08x\n" % itcm_size
                line = line + "\t#define m_interrupts_ram_start         0x20000000\n"
                line = line + "\t#define m_interrupts_ram_size          __ram_vector_table_size__\n"
                line = line + "\t#define m_data_start                   (m_interrupts_ram_start + " \
                              "m_interrupts_ram_size)\n "
                line = line + "\t#define m_data_size                    (0x%08x - m_interrupts_ram_size)\n" % (
                    dtcm_size)
                file_data += line
                get_Flag = 1
            if get_Flag == 1 and '__use_shmem__' not in line:
                continue
            elif '__use_shmem__' in line:
                get_Flag = 0
            file_data += line
        f.close()
        with open(path_linkfile_list, "w", encoding="utf-8") as fw:
            fw.write(file_data)
        fw.close()


def set_linkfile_rt11xx(path_linkfile_list, flexram_itcm_size, flexram_dtcm_size):
    for num in range(0, len(path_linkfile_list)):
        if 'cm7_ram.icf' in path_linkfile_list[num]:
            set_linkfile_rt11xx_ram_cm7_iar(path_linkfile_list[num], flexram_itcm_size,
                                            flexram_dtcm_size)
        if 'flexspi_nor.icf' in \
                path_linkfile_list[num]:
            set_linkfile_rt11xx_xip_cm7_iar(path_linkfile_list[num], flexram_itcm_size,
                                            flexram_dtcm_size)
        if 'cm7_ram.scf' in path_linkfile_list[num]:
            set_linkfile_rt11xx_ram_cm7_mdk(path_linkfile_list[num], flexram_itcm_size,
                                            flexram_dtcm_size)
        if 'flexspi_nor.scf' in \
                path_linkfile_list[num]:
            set_linkfile_rt11xx_xip_cm7_mdk(path_linkfile_list[num], flexram_itcm_size,
                                            flexram_dtcm_size)


def set_startup_rt11xx_s(path_startup_list, rt11xx_gpr17, rt11xx_gpr18):
    for num in range(0, len(path_startup_list)):
        if 'cm7.s' in path_startup_list[num]:
            set_startup_rt11xx_cm7_iar(path_startup_list[num], rt11xx_gpr17, rt11xx_gpr18)
        if 'cm7.S' in path_startup_list[num]:
            set_startup_rt11xx_cm7_mdk(path_startup_list[num], rt11xx_gpr17, rt11xx_gpr18)
        elif 'cm4' in path_startup_list[num]:
            print("Unsupport CM4 now \r\n")


def set_boards_rt11xx_mpu(path_board_list):
    for num in range(0, len(path_board_list)):
        if 'cm7' in path_board_list[num]:
            set_boards_rt11xx_cm7_mpu(path_board_list[num])
        elif 'cm4' in path_board_list[num]:
            print("Unsupport CM4 now \r\n")
