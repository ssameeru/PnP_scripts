import os
import glob
import FileProcessor as fr

class ConfigReader():

    def __init__(self) :
        self.prefix = ' '
        self.dest = ' '
                    
    def get_suffix(self, path):

        fp = fr.FileProcessor()
        print(path)
        
        if (os.path.exists(path)):
            config_file_d = fp.open_file(path)

        buf = fp.read_from_file(config_file_d)


        for line in buf:
            if 'File_Name_prefix' in line:
                temp = line.split(':')
                self.prefix = temp[1]
            elif 'Destination_Folder' in line:
                temp = line.split(':')
                self.dest = temp[1]
            else:
                print("config file doesn't have prefix/ destination specified in present line")
    
        return self.prefix, self.dest
