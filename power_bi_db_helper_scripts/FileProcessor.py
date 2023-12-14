import os
import glob
import shutil

class FileProcessor():

    def rewind_file(self, fd):
        return self.read_from_file(fd)

    def check_dir_perm(self, path, key):
        if key == 'r':
            if os.access(path, os.R_OK):
                print("Have Read permissions for the directory:", path)
                return True
            else:
                print("Read Permission for the server path is denied:", path)
                exit(1)
        if key == 'w':
            if os.access(path, os.W_OK):
                print("Have Write permissions for the directory:", path)
                return True
            else:
                print("Write Permission for the server path is denied:", path)
                exit(1)

    def convert_expr_to_path(self, file_path):
        paths = []

        for file_obj in glob.glob(file_path, recursive = False):
            if os.path.isfile(file_obj):
                paths.append(file_obj)
        if len(paths) > 1:
            return paths
        else:
            return paths[0]

    def open_file(self, file_path):

        if os.path.exists(file_path):
            fp = open(file_path, 'r')
            return fp
        else:
            print("file %s doesn't exist", file_path)
            return -1

    def file_copier(self, kpi_path, pref, dest):
        items = os.listdir(kpi_path)

        if items:
            for i in items:
                if pref in i:
                    src_path = os.path.join(kpi_path, i)
                    dest_path = os.path.join(dest, i)
                    shutil.copy(src_path, dest_path)
                    print(src_path, ": File is copied to:", dest_path)
                else:
                    print("File containing:"+pref+" Not Found")
        else:
            print(kpi_path,":Directory is empty")

    def read_from_file(self, file_desc):

        file_desc.seek(0)

        buf = file_desc.readlines()

        return buf
