import os
from clicknium.common.constants import _Constants
from clicknium.common.enums import BrowserType, ExtensionStatus
from clicknium.common.models.exceptions import ExtensionOperationError
from clicknium.common.utils import Utils


class WebExtension(object):

    def __init__(self, browser_type, is_custom = False):  
        self.is_custom = is_custom   
        if is_custom:
            self.browser_identity = browser_type   
        elif browser_type == BrowserType.Chrome:
            self.browser_identity = "Chrome" 
        elif browser_type == BrowserType.FireFox:
            self.browser_identity = "FireFox" 
        elif browser_type == BrowserType.Edge:
            self.browser_identity = "Edge" 
        else:
            self.browser_identity = None
        lib_folder = Utils.get_automation_libfolder()
        self.exe_path = os.path.join(lib_folder, "Clicknium.Web.ExtensionInstaller.exe")

    def install(self) -> None: 
        """
            Install web extension.

            Remarks:  

                1.Before installing extension, you should make sure you have already closed edge, firefox and chrome browser.

                2.When extension is installed successfully, then you should turn on the extension manually.
                                            
            Returns:
                None
        """            
        if self.browser_identity:
            print(_Constants.ExtensionOperationStart % ("install", self.browser_identity))
            cmd = "cmd/c %s -install -t %s -l en-US" % (self.exe_path, self.browser_identity)
            if self.is_custom:
                cmd = cmd + " --customchrome"
            result = os.system(cmd)
            if result:
                error = Utils.resolveWebExtensionExitCode(result, self.browser_identity, "installation")
                print(error)
                raise ExtensionOperationError("Install", self.browser_identity, error)
            else:
                print(_Constants.BrowserOperationEnd % ("Install", self.browser_identity, self.browser_identity))            

    def update(self) -> None:
        """
            Update web extension.
                                        
            Returns:
                None
        """ 
        if self.browser_identity:
            print(_Constants.ExtensionOperationStart % ("update", self.browser_identity))
            cmd = "cmd/c %s -update -t %s -l en-US" % (self.exe_path, self.browser_identity)
            if self.is_custom:
                cmd = cmd + " --customchrome"
            result = os.system(cmd)
            if result:
                error = Utils.resolveWebExtensionExitCode(result, self.browser_identity, "update")
                print(error)
                raise ExtensionOperationError("Update", self.browser_identity, error)
            else:
                print(_Constants.BrowserOperationEnd % ("Update", self.browser_identity, self.browser_identity))   

    def detect(self) -> ExtensionStatus: 
        """
            Detect web extension installation status.
                                            
            Returns:
                ExtensionStatus object, `NotInstalled` means extension has not been installed, `NeedUpdate` means there is a new update for extension, `Installed` means the lastest extension has been installed.
        """
        if self.browser_identity:
            print(_Constants.ExtensionDetectOperationStart % (self.browser_identity))
            cmd = "cmd/c %s -detect -c -t %s -s" % (self.exe_path, self.browser_identity)
            if self.is_custom:
                cmd = cmd + " --customchrome"
            result = str(os.system(cmd))
            if result:
                if len(result) != 8 or str(result)[0:7] != "9999999":
                    print(_Constants.ExtensionDetectStatusUnknown % (self.browser_identity))
                    return ExtensionStatus.NotInstalled
                elif result[7] == '0':
                    print(_Constants.ExtensionDetectStatusUninstalled % (self.browser_identity))
                    return ExtensionStatus.NotInstalled
                elif result[7] == '1':
                    print(_Constants.ExtensionDetectStatusNeedUpdate % (self.browser_identity))
                    return ExtensionStatus.NeedUpdate
                elif result[7] == '2':
                    print(_Constants.ExtensionDetectStatusInstalled % (self.browser_identity))
                    return ExtensionStatus.Installed
            else:
                print(_Constants.ExtensionDetectStatusUnknown % (self.browser_identity))
                return ExtensionStatus.NotInstalled

    def install_or_update(self) -> bool:
        """
            Install or update web extension based on current detected extension status.
                                        
            Returns:
                bool, `True` means the extension has been installed or updated, `False` means the extension has already installed the lastest version.
        """ 
        current_status = self.detect()
        if current_status == ExtensionStatus.Installed:
            return False
        elif current_status == ExtensionStatus.NotInstalled:
            self.install()
        elif current_status == ExtensionStatus.NeedUpdate:
            self.update()
        return True

    def is_installed(self) -> bool:
        """
            Detect whether extension is installed.
                                        
            Returns:
                bool, `True` means the extension has been installed, `False` means the extension has not been installed.
        """ 
        current_status = self.detect()
        if current_status == ExtensionStatus.Installed or current_status == ExtensionStatus.NeedUpdate:
            return True
        else:
            return False
