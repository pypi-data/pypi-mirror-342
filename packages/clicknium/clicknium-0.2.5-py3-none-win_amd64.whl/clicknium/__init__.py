__version__ = "0.2.5"

import sys
from typing import List, Union
from clicknium.core.models.web.webdriver import WebDriver
from ._clicknium import _Clicknium as clicknium
from .locator import _Locator
from clicknium.common.enums import WindowMode, MouseActionBy
from clicknium.core.models.uielement import UiElement
from .common.models.trace.uploader import upload_trace_log
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

locator = _Locator()
config = clicknium.config
chrome = clicknium.chrome
ie = clicknium.ie
firefox = clicknium.firefox
edge = clicknium.edge
window = clicknium.window
sap = clicknium.sap
java = clicknium.java
ui = clicknium.ui
mouse = clicknium.mouse

upload_trace_log({"actionPosition": "pythonSDK.module.initization","message":"clicknium module init"})

def chromium(browser_name: str
    ) -> WebDriver :
    """
        Get web driver for chromium based browser.

        Parameters:
            browser_name[Required]: chromium based browser name, such as 'brave', 'vivaldi' and so on.

        Returns:
            WebDriver object.
    """
    return clicknium.chromium(browser_name)

def find_element(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        window_mode: Literal["auto", "topmost", "noaction"] = WindowMode.Auto
    ) -> UiElement:
    """
        Return UI element defined by the given locator.

        Remarks:

            1.Use "Ctrl + F10" to record locator.

            2.Import window_mode type definition with " from clicknium.common.enums import * ".

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q.

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator.

            window_mode: define whether to set the UI element's parent window to topmost before an action is invoked.
                auto: default value, means setting the window to topmost if it is not, and doing nothing if it is already topmost;
                topmost: always set the window to topmost;
                noaction: doing nothing to topmost mode.

        Returns:
            UiElement object.
    """
    return clicknium.find_element(locator, locator_variables, window_mode)

def find_elements(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> List[UiElement]:

    """
        Return list of all matched UI elements by the given locator.

        Remarks:

            1.Use "Ctrl + F10" to record locator.

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator

            timeout: timeout for the operation, unit is second, default value is 30 seconds.

        Returns:
            List of matched UiElement object.
        """
    return clicknium.find_elements(locator, locator_variables, timeout)

def send_hotkey(hotkey: str) -> None:
    """
        Send hotkey to the cursor's current position.

        Parameters:
            hotkey[Requried]: hotkey string represents one key or combined keys. For example, to represent the letter A, input string "A". To represent the letters A, B, and C, input paremeter "ABC". For special keys, please refer to [hotkeys](https://docs.microsoft.com/en-au/dotnet/api/system.windows.forms.sendkeys?view=windowsdesktop-6.0#remarks).

        Returns:
            None
    """
    clicknium.send_hotkey(hotkey)

def send_text(text: str) -> None:
    """
        Send text to the cursor's current position.

        Parameters:

            text[Requried]: text string to be sent.

        Returns:
            None
    """
    clicknium.send_text(text)

def wait_disappear(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> bool:
    """
        Wait for the UI element to disappear within specified timeout.

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator

            wait_timeout: timeout for the operation, the unit is second, and default value is 30 seconds.

        Returns:
            bool, return True if the element disappears within timeout otherwise return False.
        """
    return clicknium.wait_disappear(locator, locator_variables, wait_timeout)

def wait_appear(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        wait_timeout: int = 30
    ) -> UiElement:
    """
        Wait for the UI element to appear and return it within specified timeout.

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator

            wait_timeout: timeout for the operation, the unit is second, and default value is 30 seconds.

        Returns:
            UiElement object, or None if the element does not appear.
    """
    return clicknium.wait_appear(locator, locator_variables, wait_timeout)

def is_existing(
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ) -> bool:
    """
        Check whether the UI element exists or not.

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator

            timeout: timeout for the operation, the unit is second, and default value is 30 seconds.

        Returns:
            Return True if the UI element exists, otherwise return False.
    """
    return clicknium.is_existing(locator, locator_variables, timeout)

def get_screenshot(image_file: str) -> None:
    """
        Saves a screenshot of the current window to an image file

        Parameters:

            image_file[Required]: file path to save image

        Returns:
            None
    """
    clicknium.get_screenshot(image_file)

def scrape_data(
    locator: Union[_Locator, str],
    locator_variables: dict = {},
    next_page_button_locator: Union[_Locator, str] = None,
    next_page_button_locator_variables: dict = {},
    next_page_button_by: Union[Literal["default", "mouse-emulation", "control-invocation", "dom-event-invocation"], MouseActionBy] = MouseActionBy.Default,
    wait_page_load_time: int = 5,
    max_count: int = -1,
    timeout: int = 30
) -> object:
    """
        Scrape data from applications.

        Parameters:
            locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.table'.

            locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator

            next_page_button_locator: the visit path of locator for goto next page UI element. If it's None, means just extract the current page data.

            next_page_button_locator_variables: set to initialize parameters in next_page_button_locator

            next_page_button_by: Defines the method to click the UI element.
                    mouse-emulation: click the target UI element by simulating mouse.
                    control-invocation: click the target UI element by invoking its UI method. It may not be supported if it is a Windows desktop element.
                    dom-event-invocation: call event methods bound to the dom elements.
                    default: automatically choose method per element type. For Web element, use `control-invocation`; for Window element, use `mouse-emulation`.

            wait_page_load_time: time to wait for the next page to load, the unit is second. If the value less than 0, use 0.

            max_count: maximum number of extracte data items. default value is -1. If the value less than 0, means extract all data until the last page.

            timeout: timeout for the operation to find the 'locator' UI element, the unit is second, and default value is 30 seconds.

        Returns:
            The json object of extracted data.
    """
    return clicknium.scrape_data(locator, locator_variables, next_page_button_locator, next_page_button_locator_variables, next_page_button_by, wait_page_load_time, max_count, timeout)
