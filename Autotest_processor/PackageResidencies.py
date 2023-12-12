import re

class PackageResidencies():


    def get_pkg_residencies(self, data_dict, match_pattern, file_buf, site_specific):
        raw_data = match_pattern.findall(file_buf)

        if (len(raw_data)) <= 0:
            print("There is no website Pkgc related info in cpu_results_file")
            return None
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

                if 'C0_C1' in interim_list[0]:
                    data_dict[iterator]['PC0'] += float(interim_list[1])
                    if site_specific:
                        data_dict[iterator]['Browsed'] += 1
                if 'C2' in interim_list[0]:
                    data_dict[iterator]['PC2'] += float(interim_list[1])
                if 'C3' in interim_list[0]:
                    data_dict[iterator]['PC3'] += float(interim_list[1])
                if 'C6' in interim_list[0]:
                    data_dict[iterator]['PC6'] += float(interim_list[1])
                if 'C8' in interim_list[0]:
                    data_dict[iterator]['PC8'] += float(interim_list[1])
                if 'C10' in interim_list[0]:
                    data_dict[iterator]['PC10'] += float(interim_list[1])
            return 0

    def get_cpuidle_residencies(self, data_dict, match_pattern, file_buf, site_specific):
        raw_data = match_pattern.findall(file_buf)
        acpi = 0

        if 'ACPI' in file_buf:
            acpi = 1
            
        if (len(raw_data)) <= 0:
            print("There is no website cpuidle related info in cpu_results_file")
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

                if 'C0' in interim_list[0]:
                    data_dict[iterator]['C0'] += float(interim_list[1])
                if 'C1E' in interim_list[0] or 'C1_ACPI' in interim_list[0]:
                    data_dict[iterator]['C1'] += float(interim_list[1])
                if 'C6' in interim_list[0] or 'C2_ACPI' in interim_list[0]:
                    data_dict[iterator]['C6'] += float(interim_list[1])

                if acpi:   
                    if 'C3_ACPI' in interim_list[0]:
                        data_dict[iterator]['C10'] += float(interim_list[1])
                else:
                    if 'C8' in interim_list[0]:
                        data_dict[iterator]['C8'] += float(interim_list[1])
                    if 'C10' in interim_list[0]:
                        data_dict[iterator]['C10'] += float(interim_list[1])
            return 0

    def get_gpu_idle_residencies(self, data_dict, match_pattern, file_buf, site_specific):
            raw_data = match_pattern.findall(file_buf)

            if (len(raw_data)) <= 0:
                print("There is no website gpuidle related info in cpu_results_file")
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
                        
                    if 'RC0' in interim_list[0]:
                        data_dict[iterator]['RC0'] += float(interim_list[1])
                    if 'RC6' in interim_list[0]:
                        data_dict[iterator]['RC6'] += float(interim_list[1])
                return 0
