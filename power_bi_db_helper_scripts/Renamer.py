import os
import glob

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
                    
                else:
                    print(name," is Not a directory")

    def check_for_summary_file(self, path):
        if os.path.exists(path+'/summary.csv') or os.path.exists(path+'/Summary.csv'):
            return 1
        else:
            return 0
    
    def rename_summary_file(self, path, pref, kpi, run):

        new_name = pref+'_{}_R{}_Power.csv'.format(kpi, run)

        ret = self.check_for_summary_file(path)

        if ret:
            summary_path = path+'/summary.csv' if os.path.exists(path+'/summary.csv') else path+'/Summary.csv'
            os.rename(summary_path, path+'/'+new_name)
        else:
            print("Files are already renamed in:"+path+" Directory ")

        
                
    def rename_each_file(self, prefix):
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
                    self.rename_summary_file(summary_path, prefix, kpi, run_num)
                    run_num += 1
                
                    
