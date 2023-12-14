import os
import FileProcessor as fr
import Renamer as rn
import csv
import time

fp = fr.FileProcessor()
rc = rn.Renamer()

class CsvMod():

    def check_and_remove_temp_file(self, path):

        if os.path.exists(path+"\\temp.csv"):
            os.remove(path+"\\temp.csv")
        else:
            print("No temp file found creating it")

    def _modify_csv_file(self, path, pfm):

        if rc.check_for_summary_file(path, pfm):
            if pfm == 'Windows':
                file_p = path+'\Sum*.csv'
                act_file = fp.convert_expr_to_path(file_p)
            else:
                file_p = path+'/Sum*.csv'
                act_file = fp.convert_expr_to_path(file_p)
            try:
                self.check_and_remove_temp_file(path)
                with open(path+'\\temp.csv', 'x', newline='') as out_file:
                    with open(act_file, 'r') as in_file :
                        reader = csv.reader(in_file, delimiter = ',')
                        writer = csv.writer(out_file, delimiter = ',')
                        header = next(reader)
                        header[0] = 'Index'
                        print(header)
                        writer.writerow(header)
                        for row in reader:
                            writer.writerow(row)
                os.remove(act_file)
                time.sleep(1)
                os.rename(path+'\\temp.csv', act_file)

            except OSError as e:
                print(e)
        else:
            print("No summary File Found in Directory")


    def adapt_cpd_mes_to_bi(self, kpi_path, pfm):

        for kpi,path in kpi_path.items():
            items = os.listdir(path)
            if not items:
                print(path,"Directory is empty")
            else:
                for i in items:
                    file_path = os.path.join(path, i)
                    self._modify_csv_file(file_path, pfm)
