import re
import FileProcessing as fp
import PackageResidencies as pr
import CpuGpuFrequency as gp

class SummaryData():

    def __init__(self, base_path):
        self._path = base_path +'/results/keyval'
        self._cpu_sum_expr = base_path+'/results/cpu_results_*_summary.txt'
        self.summary_data = {}
        self.loop_count = 0
        self.file_oper = fp.FileProcessing()
        self.pkg = pr.PackageResidencies()
        self.freq = gp.CpuGpuFrequency()
        self._cpu_sum_path = self.file_oper.convert_expr_to_path(self._cpu_sum_expr)
            
    def check_for_valid_loop(self, data):
        loop_iter = data[0].split('_')[0]

        if (int(loop_iter[-2])) > 0:
            loop = int(loop_iter[-2]+loop_iter[-1])
        else:
            loop = int(loop_iter[-1])

        if loop > self.loop_count:
            return -1
        else:
            return loop
        
    def get_data(self, match_pattern, data_dict, key, key_file):

        buf = self.file_oper.rewind_file(key_file)
        raw_data = match_pattern.findall(buf)

        for i in range(self.loop_count):
            interim_list = raw_data[i].split("=")
            ret = self.check_for_valid_loop(interim_list)
            if ret >= 0:
                data_dict[ret][key] = float(interim_list[1])
            
    def get_loop_count(sel, buf, duration_pattern):
        count  = 0
        raw_data = duration_pattern.findall(buf)
        
        for i in range(len(raw_data)):
            interim_duration = raw_data[i].split("=")[1]
            if (float(interim_duration)) >= 3604.0:
                count += 1
        #return count + 1 to capture the overall loops data
        return count + 1

    def get_loop_count_create_dict(self, key_file):
        duration_str = "loop[0-9][0-9]_system_duration{perf}=[0-9][0-9][0-9]*.[0-9]"
        data_dict = {}
        duration_pattern = re.compile(duration_str)

        buf = self.file_oper.read_from_file(key_file)

        if buf ==' ':
            print("Keyval File is empty\n")
        else:
            self.loop_count = self.get_loop_count(buf, duration_pattern)

        for i in range(self.loop_count):
            data_dict.update({i:{}})
            data_dict[i] = {k:0.0 for k in ['soc_power', 'disp_brightness', 'sys_power', 'Duration',
                                            'PC0', 'PC2', 'PC3', 'PC6', 'PC8', 'PC10', 'C0', 'C1',
                                            'C6', 'C8', 'C10','RC0', 'RC6', 'cpufreq']}
            
        self.get_data(duration_pattern, data_dict, 'Duration', key_file)
    
        return data_dict

    
        
    def _get_dis_bright_percentage(self, data_dict, key_file):
        """ """ 
        disp_bright = "loop[0-9][0-9]_level_backlight_percent{perf}=[0-9][0-9]*.[0-9]"

        disp_pattern = re.compile(disp_bright)

        self.get_data(disp_pattern, data_dict, 'disp_brightness', key_file)
        
    def _get_sys_power_data(self, data_dict, key_file):
        """ """
        sys_power = "loop[0-9][0-9]_system_pwr_avg{perf}=[0-9].[0-9][0-9][0-9]"

        sys_pwr_pattern = re.compile(sys_power)

        self.get_data(sys_pwr_pattern, data_dict, 'sys_power', key_file)
        
    def _get_soc_power_data(self, data_dict, key_file):
        soc_power = "loop[0-9][0-9]_package-0_pwr_avg{perf}=[0-9].[0-9][0-9][0-9]"

        soc_pwr_pattern = re.compile(soc_power)

        self.get_data(soc_pwr_pattern, data_dict, 'soc_power', key_file)
    

    def _get_cpufreq_data(self, data_dict, key, key_file):
        """ """ 
        cpu_freq = "loop[0-9][0-9]_wavg_{0}*.*".format(key)
        cpu_freq_pattern = re.compile(cpu_freq)

        buf=self.file_oper.rewind_file(key_file)
        
        self.freq.get_cpu_frequency(data_dict, cpu_freq_pattern, buf, 0)  
        
    def _get_gpufreq_data(self, data_dict, key, key_file):
        """ """ 
      
    def _get_cpupkg_res(self, data_dict, key, key_file):
        """ """ 
        cpu_pkg = "loop[0-9][0-9]_{0}_*_C[0-9].*".format(key)
        cpu_pkg_pattern = re.compile(cpu_pkg)

        buf = self.file_oper.rewind_file(key_file)
        self.pkg.get_pkg_residencies(data_dict, cpu_pkg_pattern, buf, 0)
        
    def _get_cpuidle_res(self, data_dict, key, key_file):
        """ """
        cpu_idle = "loop[0-9][0-9]_{0}_*_C[0-9].*".format(key)
        cpu_idle_pattern = re.compile(cpu_idle)

        buf = self.file_oper.rewind_file(key_file)
        self.pkg.get_cpuidle_residencies(data_dict, cpu_idle_pattern, buf, 0)
        
    def _get_gpuidle_res(self, data_dict, key, key_file):
        """ """ 
        gpu_idle = "loop[0-9][0-9]_{0}_RC[0,6].*".format(key)
        gpu_idle_pattern = re.compile(gpu_idle)

        buf = self.file_oper.rewind_file(key_file)
        
        self.pkg.get_gpu_idle_residencies(data_dict, gpu_idle_pattern, buf, 0)
        
    def _get_mem_data(self, pattern, key_file):
        """ """ 


    def create_plt_summary_data(self):

        try:
            keyval_fd = self.file_oper.open_file(self._path)

        except IOError:
            print("There is no Keyval file in the results Directory")
            exit(1)

        try:
            if (type(self._cpu_sum_path) is list):
                cpu_fd = self.file_oper.open_file(self._cpu_sum_path[0])
        except IOError:
            print("There is no Keyval file in the results Directory")
            exit(1)

        self.summary_data = self.get_loop_count_create_dict(keyval_fd)
        self._get_soc_power_data(self.summary_data, keyval_fd)
        self._get_sys_power_data(self.summary_data, keyval_fd)
        self._get_dis_bright_percentage(self.summary_data, keyval_fd)
        self._get_cpupkg_res(self.summary_data, 'cpupkg', cpu_fd)
        self._get_cpuidle_res(self.summary_data, 'cpuidle', cpu_fd)
        self._get_gpuidle_res(self.summary_data, 'gpuidle', cpu_fd)
        self._get_cpufreq_data(self.summary_data, 'cpufreq', cpu_fd)
        return self.summary_data
            
                             
        
        
        


        
