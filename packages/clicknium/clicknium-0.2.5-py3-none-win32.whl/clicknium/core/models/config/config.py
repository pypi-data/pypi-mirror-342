import os
from clicknium.common.utils import Utils
from Clicknium.LocatorStore.Services import AuthenticationProvider
from clicknium.core.service.invokerservice import _ExceptionHandle

class Config(object):

    def __init__(self):
        _base_folder = Utils.get_automation_libfolder()
        self._telemetry_setting_file = os.path.join(_base_folder, "Clicknium.Telemetry.dll.config")

    def enable_telemetry(self) -> None:
        """
            Enable 'usage data and errors' to be sent to Clicknium online service.
        """
        if os.path.exists(self._telemetry_setting_file):
            flist = []
            is_update = False
            with open(self._telemetry_setting_file, 'r+', encoding="utf-8") as f:
                flist = f.readlines() 
                if flist:
                    for i in range(len(flist)):
                        if(flist[i] and "IsEnableTelemetry" in flist[i]):
                            if "true" not in flist[i]:
                                flist[i] = "		<add key=\"IsEnableTelemetry\" value=\"true\"/>\n"
                                is_update = True
                            break
            if is_update:  
                with open(self._telemetry_setting_file, 'w+', encoding="utf-8") as f:  
                    f.writelines(flist)

    def disable_telemetry(self) -> None:
        """
            Disable 'usage data and errors' to be sent to Clicknium online service.
        """
        if os.path.exists(self._telemetry_setting_file):
            flist = []
            is_update = False
            with open(self._telemetry_setting_file, 'r+', encoding="utf-8") as f:
                flist = f.readlines() 
                if flist:
                    for i in range(len(flist)):
                        if(flist[i] and "IsEnableTelemetry" in flist[i]):
                            if "false" not in flist[i]:
                                flist[i] ="		<add key=\"IsEnableTelemetry\" value=\"false\"/>\n"
                                is_update = True
                            break
            if is_update:  
                with open(self._telemetry_setting_file, 'w+', encoding="utf-8") as f:  
                    f.writelines(flist)
                
    @staticmethod
    @_ExceptionHandle.try_except
    def set_license(licence):
        AuthenticationProvider.SetLicence(licence)

