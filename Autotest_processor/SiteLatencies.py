import re


class SiteLatencies():

    def get_site_specific_latencies(self, data_dict, match_pattern, buf, site_specific):
        raw_data = match_pattern.findall(buf)

        if (len(raw_data)) <= 0:
            print("There is no website latency related info in cpu_results_file")
            return None
        else :
            for i in range(len(raw_data)):
                interim_list = raw_data[i].split('\t')
                site_name = interim_list[0].split('_')[3]
                
                if site_specific:

                    iterator = interim_list[0].split('_')[0]

                    if (int(iterator[-2]) > 0):
                        loop_count = int(iterator[-2]+iterator[-1])
                    else:
                        loop_count = int(iterator[-1])

                    data_dict[site_name][loop_count] = float(interim_list[3])
            return 1
