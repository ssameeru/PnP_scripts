import re
import FileProcessing as fileoper
import PackageResidencies as pkgres
import CpuGpuFrequency as cpugpufreq
import MemoryProcessor as mp
import SiteLatencies as lt

class WebsiteDataProcessor():

    def __init__(self, base_path):
        """ Web site residencies, CPU, GPU frequencies"""
        self._path = base_path+'/results/cpu_results_*_summary.txt'
        self._mem_path = base_path+'/results/free_memory_results_*_summary.txt'
        self._keyval = base_path+'/results/keyval'
        self._websites = []
        self.fp = fileoper.FileProcessing()
        self.pkg = pkgres.PackageResidencies()
        self.freq = cpugpufreq.CpuGpuFrequency()
        self.mem = mp.MemoryProcessor()
        self.lat = lt.SiteLatencies()

    def _check_buf(self, buf):

        if buf == ' ':
            print("results buffer is empty")
            return None
        else :
            return buf


    def _get_site_specific_pkg_residecncies(self, data_dict, cpufp):
        site_pkg_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_cpupkg_C[0-9].*"
        pkg_pattern = re.compile(site_pkg_str)

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the Package C residencies as the results file is empty")

        ret = self.pkg.get_pkg_residencies(data_dict, pkg_pattern, buf, 1)

        if ret == None:
            print("There is not website related Package C residecncies info in Cpu results File")

    def _get_site_specific_cpuidle_residencies(self, data_dict, cpufp):

        site_cpuidle_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_cpuidle_C[0-9].*"
        cpuidle_pattern = re.compile(site_cpuidle_str)

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the CPUDILE C-state residencies as the results file is empty")

        ret = self.pkg.get_cpuidle_residencies(data_dict, cpuidle_pattern, buf, 1)
        
        if ret == None:
            print("There is not website related CPUIDLE C-state residecncies info in Cpu results File")

    def _get_site_specific_gpuidle_residencies(self, data_dict, cpufp):

        site_gpuidle_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_gpuidle_RC[0,6].*"
        gpuidle_pattern = re.compile(site_gpuidle_str)
        
        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the GPUDILE C-state residencies as the results file is empty")

        ret = self.pkg.get_gpu_idle_residencies(data_dict, gpuidle_pattern, buf, 1)
        
        if ret == None:
            print("There is not website related GPUIDLE C-state residecncies info in Cpu results File")

    def _get_site_specific_cpu_frequency(self, data_dict, cpufp):
        site_cpufreq_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_wavg_cpufreq.*"
        cpufreq_pattern = re.compile(site_cpufreq_str)

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the GPUDILE C-state residencies as the results file is empty")

        ret = self.freq.get_cpu_frequency(data_dict, cpufreq_pattern,  buf, 1)
        
        if ret == None:
            print("There is not website related GPUIDLE C-state residecncies info in Cpu results File")
            
    def _get_site_specific_memdata(self, data_dict, cpufp):
        site_memfree_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_MemFree.*"
        site_memavail_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_MemAvailable.*"
        memavail_pattern = re.compile(site_memavail_str)
        memfree_pattern = re.compile(site_memfree_str)
        

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the Memory data as the results file is empty")

        ret = self.mem.get_mem_results(data_dict, memavail_pattern, buf, 1)

        if ret == None:
            print("There is not website related Memory Available data in the Memory results File")

        ret = self.mem.get_mem_results(data_dict, memfree_pattern, buf, 1)

        if ret == None:
            print("There is not website related Memory Free data in the Memory results File")

    def _caluclate_site_memory_usage(self, data_dict, total_mem):

        if total_mem != ' ':
            for site, values in data_dict.items():
                data_dict[site]['memtotal'] = float(total_mem)
                data_dict[site]['memory_in_use'] = (data_dict[site]['memtotal'] - (data_dict[site]['memavailable'] + data_dict[site]['memfree']))
            return 1
        else:
            return None
                
                

    def _get_loop_count(self, match_pattern, buf):
        count  = 0
        raw_data = match_pattern.findall(buf)
        
        for i in range(len(raw_data)):
            interim_duration = raw_data[i].split("=")[1]
            if (float(interim_duration)) >= 3604.0:
                count += 1
        return count
        
    def _create_site_specific_latencies_dict(self, loop_count):
        latency_dict = {}
        for i in range(len(self._websites)):
            latency_dict.update({self._websites[i]:{}})
            latency_dict[self._websites[i]] = {k:0.0 for k in range(0, loop_count)}
        return latency_dict
        
    def _create_site_cpu_summary_dict(self, match_pattern, buf):
        site_data = {}
        site_list = match_pattern.findall(buf)

        for i in range(len(site_list)):
            interim_list = site_list[i].split('\t')
            site_name = interim_list[0].split('_')[3]
            if site_name not in site_data.keys():
                self._websites.append(site_name)
                site_data.update({site_name : ''})
                site_data[site_name] = {k: 0.0 for k in ['Browsed',
                                                         'PC0', 'PC2', 'PC3', 'PC6', 'PC8', 'PC10', 'C0', 'C1',
                                                         'C6', 'C8', 'C10','RC0', 'RC6', 'cpufreq',
                                                         'memtotal', 'memavailable', 'memfree', 'memory_in_use']}
        return site_data

    def _get_site_specific_latencies(self, data_dict, cpufp):
        site_lat_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_browse_cpupkg_C[0-9].*"
        latency_pattern = re.compile(site_lat_str)

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the site specific latency data as the results file is empty")
        
        ret = self.lat.get_site_specific_latencies(data_dict, latency_pattern, buf, 1)

        if ret == None:
            print("There is not website related latency data in the cpu results File")
        
    def _create_site_gpufreq_summary_dict(self):
        site_data = {}
        
        for i in range(len(self._websites)):
            site_data.update({i : ' '})
        return site_data
        
    def site_specific_cpu_stats(self, total_mem):
        site_pkg_str = r"loop[0-9][0-9]_web_page_www.*.[com,org]_cpupkg_C[0-9].*"
        pkg_pattern = re.compile(site_pkg_str)
        loop_count = 0

        self._cpu_results_summary = self.fp.convert_expr_to_path(self._path)
        self._mem_results_summary = self.fp.convert_expr_to_path(self._mem_path)
         
        try:
            if (type(self._cpu_results_summary) is list) :
                cpufp = self.fp.open_file(self._cpu_results_summary[0])
        except IOError:
            print("Cpu Results files not present in path")
            exit(1)

        buf = self.fp.read_from_file(cpufp)
        ret = self._check_buf(buf)

        if ret == None:
            print("Can't get the Package C residencies as the results file is empty")        

        site_cpu_summary_data = self._create_site_cpu_summary_dict(pkg_pattern, buf)
        self._get_site_specific_pkg_residecncies(site_cpu_summary_data, cpufp)
        self._get_site_specific_cpuidle_residencies(site_cpu_summary_data, cpufp)
        self._get_site_specific_gpuidle_residencies(site_cpu_summary_data, cpufp)
        self._get_site_specific_cpu_frequency(site_cpu_summary_data, cpufp)

        try:
            if (type(self._mem_results_summary) is list) :
                memfp = self.fp.open_file(self._mem_results_summary[0])
        except IOError:
            print("Memory Results files not present in path")
            exit(1)

        self._get_site_specific_memdata(site_cpu_summary_data, memfp)
        #ret = self._caluclate_site_memory_usage(site_cpu_summary_data, total_mem)

        if ret == None:
            print("can' caluclate the memory usage per site")
        
        return site_cpu_summary_data

    def site_specific_latency_stats(self):
        duration_loop = r"loop[0-9][0-9]_psys_duration{perf}=[0-9][0-9][0-9]*.[0-9]"
        dur_pattern = re.compile(duration_loop)

        try:
             keyfp = self.fp.open_file(self._keyval)
        except IOError:
            print("keyval file not present in path")
            exit(1)

        buf = self.fp.read_from_file(keyfp)
        ret = self._check_buf(buf)
        
        if ret is None:
            print("Keyval file is empty")
            exit(1)
            x
        loop_count = self._get_loop_count(dur_pattern, buf)
        site_latency_dict = self._create_site_specific_latencies_dict(loop_count)
        
        try:
            if (type(self._cpu_results_summary) is list) :
                cpufp = self.fp.open_file(self._cpu_results_summary[0])
        except IOError:
            print("Cpu Results files not present in path")
            exit(1)

        self._get_site_specific_latencies(site_latency_dict, cpufp)

        return site_latency_dict
