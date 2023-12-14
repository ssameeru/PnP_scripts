import os
import glob
import errno
import time
from shutil import move

kpi_path = {}

class Renamer():

    def get_path_for_each_kpi(self, path):
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                if name == 'GM':
                    kpi_path['GM'] = os.path.join(path, name)
                      
                elif name == 'IDO':
                    kpi_path['IDO'] = os.path.join(path, name)

                elif name == 'LVP':
                    kpi_path['LVP'] = os.path.join(path, name)
                    
                elif name == 'PLT':
                    kpi_path['PLT'] = os.path.join(path, name)
                    
                elif name == 'S0iX':
                    kpi_path['S0iX'] = os.path.join(path, name)

                elif name == 'PG3':
                    kpi_path['PG3'] = os.path.join(path, name)
                    
                else:
                    print(name," is Not a directory")
        return kpi_path

    def check_for_summary_file(self, path, pfm):
        if pfm == 'Windows':
            if os.path.exists(path+'\summary.csv') or os.path.exists(path+'\Summary.csv'):
                return 1
            else:
                return 0
        else:
            if os.path.exists(path+'/summary.csv') or os.path.exists(path+'/Summary.csv'):
                return 1
            else:
                return 0
            
    def rename_summary_file(self, path, pfm, pref, kpi, run):

        new_name = pref+'_{}_R{}_Power.csv'.format(kpi, run)

        ret = self.check_for_summary_file(path, pfm)

        if ret:
            if pfm == 'Windows':
                summary_path = path+'\\Summary.csv' if os.path.exists(path+'\\Summary.csv') else (path+'\\summary.csv')
                try:
                    move(summary_path, path+'\\'+new_name)
                    time.sleep(0.5)
                except OSError as e:
                    if e.errno == errno.EACCES and os.path.exists(path+'\\'+new_name):
                        print("Got access Error Don't have permission to delete the summary file, But Renmaing file is done")
            else:
                print(pfm)
                summary_path = path+'/summary.csv' if os.path.exists(path+'/summary.csv') else (path+'/Summary.csv')
                os.rename(summary_path, path+'/'+new_name)
                
        else:
            print("Files are already renamed in:"+path+" Directory ")

        
                
    def rename_each_file(self, prefix, pfm):
        temp_path = ' '
        run_num = 1
        def get_creation_time(item):
            item_path = os.path.join(temp_path, item)
            return os.path.getctime(item_path)
    
        for kpi,path in kpi_path.items():
            items = os.listdir(path)
            if not items:
                print(path,"Directory is empty")
            else:
                temp_path = path
                sorted_items = sorted(items, key=get_creation_time)
                for i in sorted_items:
                    summary_path = os.path.join(path, i)
                    self.rename_summary_file(summary_path, pfm, prefix, kpi, run_num)
                    run_num += 1
                
                    
