import os
from clicknium.common.constants import _Constants
from clicknium.common.models.exceptions import ExtensionOperationError
from clicknium.common.utils import Utils


class JavaExtension:

    def __init__(self):
        lib_folder = Utils.get_automation_libfolder()
        self.exe_path = os.path.join(lib_folder, "Clicknium.Java.ExtensionInstaller.exe")        

    def install(self, java_install_path: str = '') -> None:
        """
            Install java extension.
 
            Parameters:

                java_install_path: java install path string, you can provide java install path like "C:\\Program Files\\Java\\jdk-17.0.2". If you don't give that path, it will scan java install path under "Program Files && Program Files (x86)"
                                            
            Returns:
                None
        """
        args = "-install"
        scan_folder = "Program Files && Program Files (x86)"
        if java_install_path:
            args = '{} -p ""{}"""'.format(args, java_install_path)
            scan_folder = java_install_path
        else:
            args = "%s -d" % args
        print(_Constants.ExtensionOperationStart % ("install", "java") )
        print(_Constants.JavaScanFolder % scan_folder)
        if Utils.run_cmd_as_admin(self.exe_path, args) == False:   
            raise ExtensionOperationError("install", "Java", _Constants.JavaExtensionFailed % "installation")
        print(_Constants.JavaExtensionEnd % "installation")
        

    def uninstall(self, java_install_path: str = '') -> None:
        """
            Install java extension.
 
            Parameters:

                java_install_path: java install path string, you can provide java install path like "C:\\Program Files\\Java\\jdk-17.0.2". If you don't give that path, it will scan java install path under "Program Files && Program Files (x86)"
                                            
            Returns:
                None
        """
        args = "-uninstall"
        scan_folder = "Program Files && Program Files (x86)"
        if java_install_path:
            args = "%s -p %s" % (args, java_install_path)
            scan_folder = java_install_path
        else:
            args = "%s -d" % args
        print(_Constants.ExtensionOperationStart % ("uninstall", "java") )
        print(_Constants.JavaScanFolder % scan_folder)
        if Utils.run_cmd_as_admin(self.exe_path, args) == False:            
            raise ExtensionOperationError("uninstall", "Java", _Constants.JavaExtensionFailed % "uninstallation")
        print(_Constants.JavaExtensionEnd % "uninstallation")