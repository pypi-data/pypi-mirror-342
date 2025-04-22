from typing import List
from clicknium.core.models.web.browsertab import BrowserTab
from clicknium.core.service.invokerservice import _ExceptionHandle

class Browser(object):    

    def __init__(self, browser_object):
        self._browser = browser_object 

    @property
    @_ExceptionHandle.try_except
    def tabs(self) -> List[BrowserTab]:
        """
            Get current browser's all tabs.
                                
            Returns:
                list of BrowserTab object, a list with tabs if any was found or an empty list if not
        """
        tab_list = []
        if self._browser.BrowserTabs:            
            for tab in self._browser.BrowserTabs:
                tab_list.append(BrowserTab(tab))
        return tab_list

    @_ExceptionHandle.try_except
    def get_tab(self, title: str = '', url: str = '') -> BrowserTab:
        """
            Get browser's tab by title and url.

            Parameters:

                title: title string, browser tab's title

                url: url string, browser tab's url
                                            
            Returns:
                BrowserTab object, you can use the object to do the following operation: find_element, close_tab, refresh and so on
        """
        tab = self._browser.GetTab(title, url)
        if tab:
            return BrowserTab(tab)
        return None

    @_ExceptionHandle.try_except
    def get_active_tab(self) -> BrowserTab:
        """
            Get browser's active tab.
                                            
            Returns:
                BrowserTab object, you can use the object to do the following operation: find_element, close_tab, refresh and so on
        """
        tab = self._browser.GetActiveTab()
        if tab:
            return BrowserTab(tab)
        return None

    @_ExceptionHandle.try_except
    def close(self, is_force: bool = False) -> None:
        """
            Close the current browser.

            Parameters:

                is_force: bool, ex: whether to force close the browser
                                            
            Returns:
                None
        """
        self._browser.Close(is_force)

    @_ExceptionHandle.try_except
    def maximize(self) -> None:
        """
            Maximize the current browser.
        """
        self._browser.SetMaximize()

    @_ExceptionHandle.try_except
    def new_tab(self, url: str, is_wait_complete: bool = True, timeout: int = 30) -> BrowserTab:
        """
            Open a new tab in current browser.

            Parameters:

                url[Required]: url string, browser tab's url

                is_wait_complete: is_wait_complete is set to define whether to wait for a browser to load completely. Default is True

                timeout: timeout for the operation, the unit is second, and the default value is 30 seconds.  
                                            
            Returns:
                BrowserTab object, you can use the object to do the following operation: find_element, close_tab, refresh and so on
        """
        tab = self._browser.NewTab(url, is_wait_complete, timeout * 1000)
        if tab:
            return BrowserTab(tab)
        return None