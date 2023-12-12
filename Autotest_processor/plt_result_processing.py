import time
import sys
from datetime import datetime
import SummaryData as sd
import WebsiteDataProcessor as wdp
import VersionGenerator as vg
import FileProcessing as fp


def write_header(data_dict, ws):

    for key in data_dict.keys():
        col = 1
        for state in data_dict[key].keys():
            if state == 'cpufreq':
                ws.write(0, col, 'CPuFreq(mHz)')
            elif state == 'memtotal':
                ws.write(0, col, 'Total Memory KB')
            elif state == 'memavailable':
                ws.write(0, col, 'Available Memory KB')
            elif state == 'memfree':
                ws.write(0, col, 'Free Memory KB')
            else:
                ws.write(0, col, state)
            col += 1
        break
    
def main():
    base_path = sys.argv[1]
    summary_path = base_path+'/*.xlsx'
    
    vi = vg.VersionInfo(base_path)
    wi = wdp.WebsiteDataProcessor(base_path)
    sum_data = sd.SummaryData(base_path)
    FileOper = fp.FileProcessing()

    site_count = 0;
    summary_files = FileOper.convert_expr_to_path(summary_path)

    if summary_files:
        FileOper.check_for_summary(summary_files)
    
    summary_wb = FileOper.create_workbook(base_path)

    versioninfo_ws = FileOper.create_worksheet('Platform_info', summary_wb)
    plt_summary_ws = FileOper.create_worksheet('Summary_data', summary_wb)
    website_info_ws = FileOper.create_worksheet('Website_cpu_stats', summary_wb)
    website_lat_ws = FileOper.create_worksheet('Website_latency_stats', summary_wb)
    
    ver_info = vi.get_version_info()
    
    if len(ver_info) != 0:
        site_data = wi.site_specific_cpu_stats(ver_info['TotalMem'])
    else:
        site_data = wi.site_specific_cpu_stats(' ')

    site_latency_data = wi.site_specific_latency_stats()
    summary_data = sum_data.create_plt_summary_data()
    
    FileOper.write_platform_data(ver_info, versioninfo_ws)

    website_info_ws.write(0, 0, 'site_url')
    
    write_header(site_data, website_info_ws)

    try:
        FileOper.write_results_info(site_data, website_info_ws)
    except AttributeError:
        print("execption case in writing the website_results_info")
        summary_wb.close()
        
    website_lat_ws.write(0, 0, 'site_url')

    write_header(site_latency_data, website_lat_ws)

    try:
        FileOper.write_matrix(site_latency_data, website_lat_ws)
    except AttributeError:
        print("execption case")
        summary_wb.close()

    plt_summary_ws.write(0, 0, 'loop_number')

    write_header(summary_data, plt_summary_ws)

    try:
        FileOper.write_matrix(summary_data, plt_summary_ws)
    except AttributeError:
        print("execption case")
        summary_wb.close()
    summary_wb.close()

if __name__ == "__main__":
    main()
