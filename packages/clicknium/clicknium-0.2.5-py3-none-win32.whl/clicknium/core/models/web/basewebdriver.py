import sys
from typing import List, Union
from clicknium.common.enums import WebUserDataMode
from clicknium.core.models.web.browser import Browser
from clicknium.core.models.web.browsertab import BrowserTab
from clicknium.core.service.invokerservice import _ConvertEnumService, _ConvertOptionService, _ExceptionHandle, _InvokerService, LocatorService
from clicknium.common.models.exceptions import *
from clicknium.locator import _Locator

if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal

class BaseWebDriver(object):

    def __init__(self, browser_type, is_custom = False,using_cdp=False):
        if is_custom:            
            self._webdriver = _InvokerService.get_chromiumwebdriver(browser_type)
        else:
            if using_cdp:
                self._webdriver = _InvokerService.get_cdpwebdriver(_ConvertEnumService.convert_browser_type_enum(browser_type))
            else:
                self._webdriver = _InvokerService.get_webdriver(_ConvertEnumService.convert_browser_type_enum(browser_type))

    @property
    @_ExceptionHandle.try_except
    def browsers(self) -> List[Browser]:
        """
            Get all opened browsers object by browser type.
                                
            Returns:
                list of Browser object, a list with browsers if any was found or an empty list if not
        """
        browser_list = []
        if self._webdriver.Browsers:            
            for browser in self._webdriver.Browsers:
                browser_list.append(Browser(browser))
        return browser_list
        
    @_ExceptionHandle.try_except
    def open(
        self,
        url: str,
        is_maximize: bool = True,
        is_wait_complete: bool = True,
        userdata_folder_mode: Literal["automatic", "default", "custom"] = WebUserDataMode.Automatic,
        userdata_folder_path: str = "",
        args: List[str] = None,
        timeout: int = 30
    ) -> BrowserTab:
        """
            Open browser tab with specified website and get a browser tab object.

            Remarks:  

                1.Import parameter's type with " from clicknium.common.enums import * "  

                2.When you use the function and run the python script with VSCode's "Start Debugging (F5)" or "Run Without Debugging (Ctrl+F5)", the new opened browser will be closed after the run is finished
 
            Parameters:

                url[Required]: website string, ex: https://www.bing.com

                is_maximize: is_maximize is set to define whether to maximize the browser window. Default is True

                is_wait_complete: is_wait_complete is set to define whether to wait for a browser to load completely. Default is True

                userdata_folder_mode: userdata_folder_mode define whether to use custom user data folder when opening browser   
                    automatic: use user data folder automatically.  
                    default: use default folder of the user data.  
                    custom: use the folder specified by parameter 'userdata_folder_path'.

                userdata_folder_path: user data's folder path

                args: additional arguments to pass to the browser instance. The list of Chromium flags can be found at https://peter.sh/experiments/chromium-command-line-switches/, ex: args=["--profile-directory=Default"]

                timeout: timeout for the operation, unit is second, default value is 30 seconds

            Returns:
                BrowserTab object, you can use the browser tab to do the following operation: find_element, close_tab, refresh and so on
        """
        open_options = _ConvertOptionService.convert_open_browser_option(userdata_folder_mode, userdata_folder_path, args)
        tab_object = self._webdriver.New(url, is_maximize, is_wait_complete, timeout * 1000, open_options)
        return BrowserTab(tab_object)

    @_ExceptionHandle.try_except
    def attach(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        is_maximize: bool = True,
        timeout = 30
    ) -> BrowserTab:
        """
            Attach to current broswer tab with specified locator.
 
            Parameters:
                locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q  

                locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator  

                is_maximize: is_maximize is set to define whether to maximize the browser window. Default is True

                timeout: timeout for the operation, unit is second, default value is 30 seconds

            Returns:
                BrowserTab object, you can use the browser tab to do the following operation: find_element, close_tab, refresh and so on
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        tab_object = self._webdriver.Attach(locator_item.Locator, locator_item.Locator_Variables, is_maximize, timeout * 1000)
        return BrowserTab(tab_object)

    @_ExceptionHandle.try_except
    def attach_by_title_url(
        self,
        title: str = '',
        url: str = '',
        is_maximize: bool = True,
        timeout = 30
    ) -> BrowserTab:
        """
            Attach to an open browser tab with a specified title and/or url.
 
            Parameters:

                title: title string, current web page's title

                url: url string, current web page's url

                is_maximize: is_maximize is set to define whether to maximize the browser window. Default is True

                timeout: timeout for the operation, unit is second, default value is 30 seconds

            Returns:
                BrowserTab object, you can use the browser to do the following operation: find_element, close_tab, refresh and so on
        """
        tab_object = self._webdriver.Attach(title, url, is_maximize, timeout * 1000)
        return BrowserTab(tab_object)