import os
import glob
import xlsxwriter

class FileProcessing():

    def rewind_file(self, fd):
        return self.read_from_file(fd)

    def open_file(self, file_path):
        
        if os.path.exists(file_path):
            fp = open(file_path, 'r')
            return fp
        else:
            print("file %s doesn't exist", file_path)
            return -1
        
    def read_from_file(self, file_desc):

        file_desc.seek(0)

        buf = file_desc.read()

        return buf

    def convert_expr_to_path(self, file_path):
        paths = []
        for file_obj in glob.glob(file_path, recursive = False):
            if os.path.isfile(file_obj):
                paths.append(file_obj)
        if paths:
            return paths

    def check_for_summary(self, path):
        if len(path) > 1:
            for i in range(len(path)):
                if os.path.exists(path[i]):
                    os.remove(path[i])
        else:
            if (len(path) == 0):
                print("No Summary File found")
                return
            else :
                if os.path.exists(path[0]):
                    os.remove(path[0])
        
    def create_workbook(self, path):
        wb_path = path +'/summary.xlsx'

        try: 
            wb = xlsxwriter.Workbook(wb_path)
        except IOError:
            print("can't create summary workbook to write data")
        return wb

    def create_worksheet(self, sheet_name, wb):
        """ """    
        ws = wb.add_worksheet(sheet_name)
        return ws

    def write_platform_data(self, data_dict, ws):
        """ """
        row = 1
        col = 0
        for k,v in data_dict.items():
            ws.write(row, col, k)
            ws.write(row, col + 1, v)
            row += 1
            
    def write_results_info(self, data_dict, ws):
        row = 1
        col = 0
        site_count = 0
        for site,values in data_dict.items():
            col = 0
            browsed = data_dict[site]['Browsed']
            site_count += 1
            ws.write(row, col, site)
            for state,res in values.items():
                col += 1
                #ws.write(row, col, res)
                if state == 'Browsed':
                    ws.write(row, col, res)

                elif state == 'cpufreq':
                    ws.write(row, col , round(((res/browsed)/1000),2))
                    
                elif state == 'memtotal' and res != 0 :
                    print(res)
                    ws.write(row, col , (float(res.strip())/1024))
                    
                else:
                    ws.write(row, col , round((res/browsed),2))
            row += 1
        ws.write(row, 0, 'Total_sites')
        ws.write(row, 1, site_count)

    def write_matrix(self, data_dict, ws):
        row = 1

        for site, values in data_dict.items():
            col = 0
            ws.write(row, col, site)
            
            for loop, lat in values.items():
                if type(col) == str:
                    col = int(loop + 1) 
                    ws.write(row, col, lat)
                else:
                    col += 1
                    ws.write(row, col, lat)
            
            row += 1
