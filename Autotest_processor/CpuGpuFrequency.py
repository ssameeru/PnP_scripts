import re

class CpuGpuFrequency():

    def get_cpu_frequency(self, data_dict, match_pattern, file_buf, site_specific):
        raw_data = match_pattern.findall(file_buf)

        if (len(raw_data)) <= 0:
            print("There is no website CPU Frequency related info in cpu_results_file")
            return -1
        else :
            for i in range(len(raw_data)):
                interim_list = raw_data[i].split('\t')
                if site_specific:
                    iterator = interim_list[0].split('_')[3]
                else:
                    loop = interim_list[0].split('_')[0]
                    # check if the Loop Number is Double digit 
                    if (int(loop[-2]) > 0):
                        interim_iter = loop[-2]+loop[-1]
                        iterator = int(interim_iter)
                    else:
                        iterator = int(loop[-1])
                data_dict[iterator]['cpufreq'] += float(interim_list[1])
                
            return 0
