import os, sys
from platform import python_version

from clicknium.common.constants import _Constants

class Utils:

    PythonVersion = python_version()    

    @staticmethod
    def is_need_telemetry(func: str):
        for blankList in _Constants.TelemetryBlanklist:
            if(func.__contains__(blankList)):
                return False
        return True

    @staticmethod
    def get_automation_libfolder():
        src_path = os.path.realpath(__file__).split('common')[0]
        lib_path = os.path.join(src_path, ".lib", "automation")
        return lib_path

    @staticmethod
    def create_file(file_path):
        dir = os.path.dirname(file_path)
        if dir and not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(file_path):
            open(file_path, mode='w')
        if not os.path.isfile(file_path):
            return False
        return True

    @staticmethod
    def get_import_dlls(dir_path):
        files = os.listdir(dir_path)
        import_files = []
        for file in files:
            if file and file.endswith(".dll") and file.startswith("Clicknium"):
                import_files.append(file)
        return import_files

    @staticmethod
    def get_project_folder(identifier):
        folder = os.path.abspath(sys.path[0])
        while folder:
            target = os.path.join(folder, identifier)
            if os.path.exists(target):
                return folder
            elif len(list(filter(None, folder.split('\\')))) == 1:
                return ""
            folder = os.path.abspath(os.path.dirname(folder))
        return ""

    @staticmethod
    def run_cmd_as_admin(exePath:str, args: str):  
        try:    
            cmd = "powershell -Command \"Start-Process %s -Verb RunAs -ArgumentList '%s' -wait -WindowStyle Hidden\"" %(exePath, args)
            result = os.system(cmd)
            return result == 0
        except:
            return False

    @staticmethod
    def resolveWebExtensionExitCode(exitcode: int, type: str, operation: str):
        if exitcode == 4:
            return _Constants.BrowserNotInstalled % (type, operation, type)
        elif exitcode == 5:
            return _Constants.BrowserVersionNotSupported % (type, operation, type)
        elif exitcode == 8:
            return _Constants.ExtensionInstallerIsRunning % (type, operation)
        elif exitcode == 11:
            return _Constants.ExtensionOperationCancelled % (type, operation)
        else:
            return _Constants.ExtensionOpearationFailed % (type, operation)