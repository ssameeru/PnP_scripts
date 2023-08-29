#SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2022-23 Intel Chrome PnP BA Team. All rights reserved.
# Author: Sameeruddin shaik <shaik.sameeruddin@intel.com>
#!/usr/bin/python

import re
import sys
import os
import glob
import statistics as st
from collections import defaultdict
import time
from datetime import datetime


cpu_results_summary = 'results/cpu_results_*_summary.txt'
key_val_path = 'results/keyval'
cb_log = 'sysinfo/reboot_current/log'
cros_system = 'sysinfo/reboot_current/crossystem'

def write_seperator(fp):
    fp.write("=======================================\n")

def get_sys_info(cb_log_fp, cros_log_fp, os_log_fp):
    ''' Get the OS, CB and Browser version and updates it in the summary file.'''

    cros_buf = cros_log_fp.read()
    os_log_buf = os_log_fp.read()
    cb_buf = cb_log_fp.read()

    cpuid_str = re.findall("CPU: ID.*", cb_buf)
    if cpuid_str:
        summary_fp.write("".join(cpuid_str)+'\n')

    cb_ver_str = re.findall("fwid.*", cros_buf)
    cb_ver = "".join(cb_ver_str).split('=')
    if cb_ver_str:
        summary_fp.write("Coreboot Version:"+cb_ver[1]+'\n')

    ec_ro_str = re.search("ro:.*", cb_buf)
    ec_rw_str = re.search("rw:.*", cb_buf)
    if ec_ro_str or ec_rw_str:
        summary_fp.write("EC RO version: {}".format(ec_ro_str.group(0))+'\n')
        summary_fp.write("EC RW version: {}".format(ec_rw_str.group(0))+'\n')

    cse_lite_ro_str = re.search("cse_lite:.RO.version.*", cb_buf)
    cse_lite_rw_str = re.search("cse_lite:.RW.version.*", cb_buf)
    if cse_lite_ro_str or cse_lite_rw_str:
        summary_fp.write("CSE Lite RO version: {}".format(cse_lite_ro_str.group(0))+'\n')
        summary_fp.write("CSE Lite RW version: {}".format(cse_lite_rw_str.group(0))+'\n')
    mrc_version = re.search("Reference.Code.\-.MRC.*", cb_buf)
    if mrc_version:
        summary_fp.write("MRC Version: {}".format(mrc_version.group(0))+'\n')

    board = re.search("CHROMEOS.RELEASE.BOARD.*", os_log_buf)
    if board:
        summary_fp.write("{}".format(board.group(0))+'\n')

    cpfe_version = re.search("CHROMEOS.RELEASE.VERSION.*", os_log_buf)
    if cpfe_version:
        summary_fp.write("{}".format(cpfe_version.group(0))+'\n')

    browser_version = re.search("CHROME.VERSION.*", os_log_buf)
    if browser_version:
        summary_fp.write("{}".format(browser_version.group(0))+'\n')

    kernel_version = re.findall("sysinfo.uname.*", os_log_buf)
    if kernel_version:
        interim_list = kernel_version[1].split('=')
        summary_fp.write("kernel Version:"+interim_list[1]+'\n')

def get_cst_updated_residencies(cpu_file, key):
    ''' Get the C-state residencies of each iteration for overall loop duration and
    also for individual workload and calculates the average of each-state residency
    and updates it in the summary file.'''

    cst_acpi_residencies = {k:[] for k in ['C0', 'C1_ACPI', 'C2_ACPI', 'C3_ACPI', 'C4_ACPI']}
    cst_residencies = {k:[] for k in ['C0', 'C1E', 'C6', 'C8', 'C10']}
    csn_str = r"loop[0-9][0-9]_{0}_*_C[0-9].*".format(key)
    match_csn = re.compile(csn_str)
    cpu_file.seek(0)
    buf = cpu_file.read()
    acpi = 0

    if buf == '':
        print("Results file is empty")
        exit(1)

    csn_list = match_csn.findall(buf)

    if 'ACPI' in buf:
        acpi = 1

    for i in range(len(csn_list)):
        interim_list = csn_list[i].split('\t')
        if acpi:
            if 'C0' in interim_list[0] and acpi:
                cst_acpi_residencies['C0'].append(float(interim_list[1]))
            if 'C1_ACPI' in interim_list[0]:
                cst_acpi_residencies['C1_ACPI'].append(float(interim_list[1]))
            if 'C2_ACPI' in interim_list[0]:
                cst_acpi_residencies['C2_ACPI'].append(float(interim_list[1]))
            if 'C3_ACPI' in interim_list[0]:
                cst_acpi_residencies['C3_ACPI'].append(float(interim_list[1]))
            if 'C4_ACPI' in interim_list[0]:
                cst_acpi_residencies['C4_ACPI'].append(float(interim_list[1]))
        else:
            if 'C0' in interim_list[0]:
                cst_residencies['C0'].append(float(interim_list[1]))
            if 'C1E' in interim_list[0]:
                cst_residencies['C1E'].append(float(interim_list[1]))
            if 'C6' in interim_list[0]:
                cst_residencies['C6'].append(float(interim_list[1]))
            if 'C8' in interim_list[0]:
                cst_residencies['C8'].append(float(interim_list[1]))
            if 'C10' in interim_list[0]:
                cst_residencies['C10'].append(float(interim_list[1]))

    summary_fp.write(key+','+ 'Average_Residency'+ ','+ 'Sum_Of_Residency'+ '\n')
    write_seperator(summary_fp)
    if acpi:
        for k,v in cst_acpi_residencies.items():
            if not  v:
                print("List is null, we don't have "+k+" c-state")
                break
            else:
                summary_fp.write(k+','+str(round(st.mean(v), 2))+','+str(round(sum(v),2))+'\n')
    else:
        for k,v in cst_residencies.items():
            summary_fp.write(k+','+str(round(st.mean(v), 2))+','+str(round(sum(v),2))+'\n')
    summary_fp.write('\n')

def get_pkgc_updated_residencies(cpu_file, key):
    ''' Get the PC-state residencies of each iteration for overall loop duration and
    also for individual workload and calculates the average of each-state residency
    and updates it in the summary file.'''

    pkg_residencies = {k:[] for k in ['PC0', 'PC2', 'PC3', 'PC6', 'PC8', 'PC10']}
    pcn_str = r"loop[0-9][0-9]_{0}_C[0-9].*".format(key)
    match_pcn = re.compile(pcn_str)

    cpu_file.seek(0)
    buf = cpu_file.read()

    if buf == '':
        print("Results file is empty")
        exit(1)

    pcn_list = match_pcn.findall(buf)
    for i in range(len(pcn_list)):
        interim_list = pcn_list[i].split('\t')
        if 'C0_C1' in interim_list[0]:
            pkg_residencies['PC0'].append(float(interim_list[1]))
        if 'C2' in interim_list[0]:
            pkg_residencies['PC2'].append(float(interim_list[1]))
        if 'C3' in interim_list[0]:
            pkg_residencies['PC3'].append(float(interim_list[1]))
        if 'C6' in interim_list[0]:
            pkg_residencies['PC6'].append(float(interim_list[1]))
        if 'C8' in interim_list[0]:
            pkg_residencies['PC8'].append(float(interim_list[1]))
        if 'C10' in interim_list[0]:
            pkg_residencies['PC10'].append(float(interim_list[1]))

    summary_fp.write(key+','+ 'Average_Residency'+'\n')
    write_seperator(summary_fp)
    for k,v in pkg_residencies.items():
        if not v:
            print("Pacakge C residencies support is not added in the PLT Autotest script")
            break
        else:
            summary_fp.write(k+','+str(round(st.mean(v), 2))+'\n')
    summary_fp.write('\n')

def get_power_avg(key_file):
    avg_pkg_pwr = 0
    total_dur_secs = 0
    match_pwr = "loop[0-9][0-9]_system_pwr_avg{perf}=[0-9].[0-9][0-9][0-9]"

    if platform == 'adln':
        match_dur = "loop[0-9][0-9]_system_duration{perf}=[0-9][0-9][0-9]*.[0-9]"
    else:
        match_dur = "loop[0-9][0-9]_psys_duration{perf}=[0-9][0-9][0-9]*.[0-9]"

    match_pkg = "loop[0-9][0-9]_package-0_pwr_avg{perf}=[0-9].[0-9][0-9][0-9]"
    match_disp = "loop[0-9][0-9]_level_backlight_percent{perf}=[0-9][0-9]*.[0-9]"

    key_file.seek(0)
    buf = key_file.read()
    pkg_pwr_avg = re.findall(match_pkg, buf)
    sys_pwr_avg = re.findall(match_pwr, buf)
    duration_loop = re.findall(match_dur, buf)
    disp_brightness = re.findall(match_disp, buf)

    no_of_loops = len(sys_pwr_avg)

    summary_fp.write(" Power \n")
    write_seperator(summary_fp)
    summary_fp.write('Loop'+','+'Package_Power'+','+'System_power'+','+'Duration'+','+'Display_brightness'+'\n')
    for i in range(len(sys_pwr_avg)):
        interim_sys_pwr = sys_pwr_avg[i].split("=")
        interim_sys_dur = duration_loop[i].split("=")
        interim_pkg_pwr = pkg_pwr_avg[i].split("=")
        interim_disp = disp_brightness[i].split("=")
        avg_pkg_pwr += (float(interim_pkg_pwr[1]))
        total_dur_secs += (float(interim_sys_dur[1]))
        summary_fp.write(str(i)+','+str(interim_pkg_pwr[1])+','+str(interim_sys_pwr[1])+','+str(interim_sys_dur[1])+','+str(interim_disp[1])+'\n')
    write_seperator(summary_fp)
    summary_fp.write('Average_power & Mins'+','+str(round(avg_pkg_pwr/no_of_loops, 2))+','+str(round(60.19/(total_dur_secs/3600), 2))+','+str(round(total_dur_secs/60, 2))+'\n')
    write_seperator(summary_fp)


def check_for_file(file_path):
    for file_obj in glob.glob(file_path):
        if os.path.isfile(file_obj):
            return file_obj
    return 0

def main():
    global summary_fp
    global platform

    if len(sys.argv) < 3:
        print()
        print("usage: python3 autotest_processing.py <path_to_autotest_results> <platform:adln/adl>")
        print("Eg : python3 autotest_processing.py /home/intel/autoPLT_jupiter_chrome_cpfe_results/default/power_LoadTest/ adl")
        print("Please provide the path to the Autotest Results Directory and platform")
        print()
        print("platform should be adln or adl, for rpl also please give adl as the platform")
        print()
        exit()
    #Base Directory path of results
    base_path = sys.argv[1]
    platform = sys.argv[2]

    print(platform)
    #create Summary file for writing the data
    if os.path.exists(base_path+'PLT-Autotest-Analysis-summary.csv'):
        os.remove(base_path+'PLT-Autotest-Analysis-summary.csv')

    summary_fp = open(base_path+'PLT-Autotest-Analysis-summary_' + str((time.localtime()).tm_mday) + '-' + str((time.localtime()).tm_mon) + '-' + str((time.localtime()).tm_hour) + '-' + str((time.localtime()).tm_min) + '.csv', 'a')
    cpu_summary_file = base_path+cpu_results_summary
    cpu_file_path = check_for_file(cpu_summary_file)

    if not os.path.exists(cpu_file_path):
        print("cpu results file doesn't exist in the directory")
        exit(1)

    if not os.path.exists(base_path+key_val_path):
        print("keyval file doesn't exist in the directory")
        exit(1)

    if os.path.exists(base_path+cb_log) and os.path.exists(base_path+cros_system) and os.path.exists(base_path+'keyval'):
        cb_log_fp = open(base_path+cb_log, 'r')
        cros_system_log = open(base_path+cros_system, 'r')
        os_log_fp = open(base_path+'keyval', 'r')
        summary_fp.write("System Info\n")
        write_seperator(summary_fp)
        get_sys_info(cb_log_fp, cros_system_log, os_log_fp)
        write_seperator(summary_fp)
        cb_log_fp.close()
        cros_system_log.close()
        os_log_fp.close()

    cpu_file = open(cpu_file_path, 'r')
    keyval_file = open(base_path+key_val_path, 'r')
    get_power_avg(keyval_file)
    summary_fp.write("Package C residencies\n")
    write_seperator(summary_fp)
    get_pkgc_updated_residencies(cpu_file, 'cpupkg')
    summary_fp.write(" C-state Residencies\n")
    write_seperator(summary_fp)
    get_cst_updated_residencies(cpu_file, 'cpuidle')
    write_seperator(summary_fp)
    summary_fp.write("Individual KPI CPU-PKG and CPU-Idle Residenices\n")
    write_seperator(summary_fp)
    get_pkgc_updated_residencies(cpu_file, 'browsing_cpupkg')
    get_pkgc_updated_residencies(cpu_file, 'email_cpupkg')
    get_pkgc_updated_residencies(cpu_file, 'document_cpupkg')
    get_pkgc_updated_residencies(cpu_file, 'video_cpupkg')
    get_cst_updated_residencies(cpu_file, 'browsing_cpuidle')
    get_cst_updated_residencies(cpu_file, 'email_cpuidle')
    get_cst_updated_residencies(cpu_file, 'document_cpuidle')
    get_cst_updated_residencies(cpu_file, 'video_cpuidle')
    print("Summary File is generated with results")

    cpu_file.close()
    keyval_file.close()

if __name__ == "__main__":
    main()
