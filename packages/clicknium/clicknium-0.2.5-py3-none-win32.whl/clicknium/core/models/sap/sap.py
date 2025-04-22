from typing import Union
from clicknium.core.service.invokerservice import _ExceptionHandle, _InvokerService, LocatorService
from clicknium.locator import _Locator
from clicknium.core.models.sap.sapelement import SapElement

class Sap(object):

    def __init__(self):
        self._sap_driver = _InvokerService.get_sapdriver()

    @_ExceptionHandle.try_except
    def find_element(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {}
    ) -> SapElement:
        """
            Initialize sap element by the given locator.

            Remarks: 
                1.Use "Ctrl + F10" to record locator.
 
            Parameters:
                locator[Required]: the visit path of locator for target UI element, eg: 'locator.saplogon.edit_1001', locator store is saplogon, and locator name is edit_1001  

                locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator  

            Returns:
                SapElement object
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        ele = self._sap_driver.GetElement(locator_item.Locator, locator_item.Locator_Variables)
        return SapElement(ele)

    @_ExceptionHandle.try_except
    def login(
        self,
        login_path: str,
        connection: str,
        client: str,
        user: str,
        password: str,
        timeout: int = 30
    ) -> None:
        """
            Login in sap application.

            Parameters:

                login_path[Required]: login path string, sap application login path

                connection[Required]: connection string, sap application connection

                client[Required]: client string, sap application client

                user[Required]: user string, sap application user

                password[Required]: password string, sap application password

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._sap_driver.Login(login_path, connection, str(client), str(user), str(password), timeout * 1000)

        