import sys
import platform
import ConfigReader as cr
import FileProcessor as fr
import Renamer as rn

#create instances for the classes

fp = fr.FileProcessor()
rp = rn.Renamer()
config = cr.ConfigReader()

def get_host_platform():
    return platform.system()

def get_config_file_path(config_glob):
    return fp.convert_expr_to_path(config_glob)

def check_for_access(path):
    fp.check_dir_perm(path)

def sanitizer(junk_str):
    temp = junk_str.strip(' $\n')
    return temp

def main():

    if len(sys.argv) < 2:
        print("Please provide the Work Week Root path of Power Measurements")
        exit(1)

    #Path for config file
    base_path = sys.argv[1]
    pfm = get_host_platform()
    if pfm == 'windows':
        config_glob = base_path+'\*.txt'
    else:
        config_glob = base_path+'/*.txt'

    # Check whether we have access to modify the file names or not
    # There is no point in Going forward if we don't have permissions
    check_for_access(base_path)

    #Convert the Glob expression txt_file path
    config_file_p = get_config_file_path(config_glob)

    #get prefix and destination folder ofrom config file
    prefix, dest = config.get_suffix(config_file_p)

    #saniztize the strings
    sanit_prefix = sanitizer(prefix)
    sanit_dest = sanitizer(dest)
    
    #Run get_path before renaming the file
    rp.get_path_for_each_kpi(base_path)
    rp.rename_each_file(sanit_prefix)

if __name__ == "__main__":
    main()
