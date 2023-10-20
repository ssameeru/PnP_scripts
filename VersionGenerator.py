import re
import os

class VersionInfo():

    def __init__(self, base_path):
        """ Version Details Generator class"""
        self._path = base_path
        self._cb_file = base_path +'/sysinfo/reboot_current/log'
        self._cros_file = base_path+'/sysinfo/reboot_current/crossystem'
        self._mem_file = base_path+'/sysinfo/reboot_current/meminfo'
        self._os_log_path = base_path +'/keyval'
        self.version_dict = {}

    
    def _create_version_info_dict(self):
        """ Create a dictionary for the DUT software version """

        self._extract_firmware_details()
        self._extract_os_details()
                
        return self.version_dict
        
    def _extract_firmware_details(self):
        
        cb_buf = self._read_from_file(self._cb_file)

        if cb_buf == None:
            print("'can't read Coreboot  version details")
            return
        else:
            self.version_dict['cpuid'] = self._extract_version("CPU: ID.*", cb_buf)
            self.version_dict['ucode'] = self._extract_version("ucode:.*", cb_buf)
            self.version_dict['EC_RO'] = self._extract_version("ro:.*", cb_buf)
            self.version_dict['EC_RW'] = self._extract_version("rw:.*", cb_buf)
            self.version_dict['CSE_RO'] = self._extract_version("cse_lite:.RO.version.*", cb_buf) 
            self.version_dict['CSE_RW'] = self._extract_version("cse_lite:.RW.version.*", cb_buf)
            self.version_dict['MRC'] = self._extract_version("Reference.Code.\-.MRC.*", cb_buf)
            
        cros_buf = self._read_from_file(self._cros_file)

        if cros_buf == ' ':
            print("'can't read Coreboot Fwid version details")
            return
        else:            
            self.version_dict['FWID'] = self._extract_version("fwid.*", cros_buf)
            
    def _extract_os_details(self):

        os_buf = self._read_from_file(self._os_log_path)
        

        if os_buf == ' ':
            print("'can't read Chromeos version details")
            return
        else:
              self.version_dict['Board'] = self._extract_version("CHROMEOS.RELEASE.BOARD.*", os_buf)
              self.version_dict['Release'] = self._extract_version("MILESTONE.*", os_buf)
              self.version_dict['CPFE_OS'] = self._extract_version("CHROMEOS.RELEASE.VERSION.*", os_buf)
              self.version_dict['chrome'] = self._extract_version("CHROME.VERSION.*", os_buf)
              self.version_dict['kernel'] = self._extract_version("sysinfo.uname.*", os_buf)
              self.version_dict['cmdline'] = self._extract_version("sysinfo.cmdline.*", os_buf)
              self.version_dict['TotalMem'] = self._extract_version("sysinfo.memtotal.in.kb.*", os_buf)

    def _extract_version(self, match_str, buf):

        expr = re.findall(match_str, buf) if ('uname' in match_str or 'cmdline' in match_str or 'memtotal' in match_str) else re.search(match_str, buf)

        if expr:

            if 'cse' in match_str:
                return expr.group(0).split('=')[1].split('(')[0]

            if 'fwid' in match_str:
                return expr.group(0).split('=')[1].split('#')[0]

            if 'MILESTONE' in match_str or  'MRC' in match_str or 'CHROME' in match_str :
                return expr.group(0).split('=')[1]

            if 'uname' in match_str or 'memtotal' in match_str:
                if 'memtotal' in match_str:
                    return expr[0].split('=')[1].split(' ')[0]
                else:
                    return expr[1].split('=')[1].split(' ')[0]
                
            if'cmdline' in match_str:
                return expr[1].split('=',1)[1]
            
            return expr.group(0).split(':')[1]
        
        else:
            print("can't find %s match string in log:%s", match_str, check_file)
            return
   
    def _read_from_file(self, check_file):

        if os.path.exists(check_file):
            fp = open(check_file, 'r')
        else:
            print("file:"+check_file+" Doesn't exist", check_file)
            return None

        buf = fp.read()
        return buf

    def get_version_info(self):
        return self._create_version_info_dict()

            
            
        
