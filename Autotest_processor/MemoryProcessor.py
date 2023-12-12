import re

class MemoryProcessor():

    def get_mem_results(self, data_dict, match_pattern, file_buf, site_specific):
        raw_data = match_pattern.findall(file_buf)

        if (len(raw_data)) <= 0:
            print("There is no website Memory related info in Memory Results file")
            return None
        else:
            for i in range(len(raw_data)):
                interim_list = raw_data[i].split('\t')
                if site_specific:
                    iterator = interim_list[0].split('_')[3]
                else:
                    iterator = interim_list[0].split('_')[0]
                    # check if the Loop Number is Double digit
                    if (int(iterator[-2]) > 0):
                        interim_iter = iterator[-2]+iterator[-1]
                    iterator = int(interim_iter)
                if 'MemFree' in interim_list[0]:
                    data_dict[iterator]['memfree'] += float(interim_list[1])
                else:
                    data_dict[iterator]['memavailable'] += float(interim_list[1])
            return 0
                
                
                
        
