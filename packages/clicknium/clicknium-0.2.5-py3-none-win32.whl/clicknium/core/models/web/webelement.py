import sys
from typing import Union
from clicknium.common.enums import By
from clicknium.core.models.uielement import UiElement
from clicknium.core.service.invokerservice import _ConvertEnumService, _ConvertOptionService, _ExceptionHandle, LocatorService
from clicknium.locator import _Locator
from clicknium.common.models.exceptions import ArgumentError
from clicknium.common.utils import Utils
from clicknium.common.constants import _Constants

if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal


class WebElement(UiElement):

    def __init__(self, element):
        super(WebElement, self).__init__(element)

    @property
    @_ExceptionHandle.try_except
    def parent(self):
        """
            Get parent element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.Parent:
            return WebElement(self._element.Parent)
        return None

    @property
    @_ExceptionHandle.try_except
    def children(self):
        """
            Get element's children elements.
                                
            Returns:
                list of WebElement object, a list with elements if any was found or an empty list if not
        """
        child_list = []
        if self._element.Children:            
            for child in self._element.Children:
                child_list.append(WebElement(child))
        return child_list

    @property
    @_ExceptionHandle.try_except
    def next_sibling(self):
        """
            Get next sibling element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.NextSibling:
            return WebElement(self._element.NextSibling)
        return None

    @property
    @_ExceptionHandle.try_except
    def previous_sibling(self):
        """
            Get previous sibling element.
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        if self._element.PreviousSibling:
            return WebElement(self._element.PreviousSibling)
        return None
    
    @_ExceptionHandle.try_except
    def child(self, index: int):
        """
            Get child element with its index.

            Parameters:
                index[Required]: index specified, get the nth child
                                
            Returns:
                WebElement object if it was found, or None if not
        """
        child_element = self._element.Child(index)
        if child_element:
            return WebElement(self._element.Child(index))
        return None

    @_ExceptionHandle.try_except
    def set_property(
        self,
        name: str,
        value: str,
        timeout: int = 30
    ) -> None:
        """
            Set web element's property value.
 
            Parameters:

                name[Required]: property name, different ui elements may support different property list

                value[Required]: property value

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                None
        """
        self._element.SetProperty(str(name), str(value), timeout * 1000)

    @_ExceptionHandle.try_except
    def execute_js(
        self,
        javascript_code: str, 
        method: str = '', 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript code snippet for the target element.

            Remarks: 
                1.For javascript code, use "_context$.currentElement." as the target element. 

                2.For parameter "method", valid string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                javascript_code[Required]:  javascript code snippet to be executed upon target element.

                method: the method to be invoked should be defined in the javascript file. If any parameter need to passed to the method, it can be included in this parameter value, for eg.: SetText("test").

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        return self._element.ExecuteJavaScript(javascript_code, method, timeout * 1000)

    @_ExceptionHandle.try_except
    def execute_js_file(
        self,
        javascript_file: str, 
        method: str = '', 
        timeout: int = 30
    ) -> str:
        """
            Execute javascript file for the target element.

            Remarks: 
                1.For javascript script, use "_context$.currentElement." as the target element. 

                2.For method invoke, valid method string should like "run()", or when passing parameters should like "run("execute js", 20)".
 
            Parameters:

                javascript_file[Required]: javascript file path, eg.: "c:\\test\\test.js".

                method: the method to be invoked should be defined in the javascript file. If any parameter need to passed to the method, it can be included in this parameter value, for eg.: SetText("test").

                timeout: timeout for the operation, unit is second, default value is 30 seconds
                                            
            Returns:
                str
        """
        with open(javascript_file, "r", encoding="utf-8") as f:
            javascript_code = f.read()
        return self._element.ExecuteJavaScript(javascript_code, method, timeout * 1000)

    @_ExceptionHandle.try_except
    def scroll(
        self,
        delta_x: int = 0,
        delta_y: int = 0,
        timeout: int = 30
    ) -> None:
        """
            Scroll target element, if the element has scroll bar.

            Parameters:

                delta_x: pixels to scroll horizontally.  

                delta_y: pixels to scroll vertically.  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.

            Returns:
                None
        """
        option = _ConvertOptionService.convert_scrolloption(delta_x, delta_y)
        self._element.Scroll(option, timeout * 1000)

    @_ExceptionHandle.try_except
    def find_element(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ):
        """
            Find element by the given locator.
 
            Parameters:
                locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q  

                locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.
 
            Returns:
                WebElement object
        """
        locator_item = LocatorService.get_locator(locator, locator_variables)
        ele = self._element.FindElement(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)
        return WebElement(ele) if ele else None

    @_ExceptionHandle.try_except
    def find_elements(
        self,
        locator: Union[_Locator, str],
        locator_variables: dict = {},
        timeout: int = 30
    ):
        """
            Find elements by the given locator.

            Remarks: 

                1.Use "ctrl + f10" to record locator.
 
            Parameters:
                locator[Required]: the visit path of locator for target UI element, eg: 'locator.chrome.bing.search_sb_form_q', locator store is chrome, and locator name is search_sb_form_q  

                locator_variables: set to initialize parameters in locator, eg: { "row": 1,  "column": 1}, more about variable, please refer to https://www.clicknium.com/documents/concepts/locator#parametric-locator  

                timeout: timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                list of WebElement object
        """
        elements = []
        locator_item = LocatorService.get_locator(locator, locator_variables)
        results = self._element.FindElements(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)
        if results:
            for element in results:
                elements.append(WebElement(element))
        return elements
    
    @_ExceptionHandle.try_except    
    def find_element_by_css_selector(
        self,
        css_selector: str,
        timeout: int = 30
    ) :
        """
            Find element by the given css selector.

            Parameters:
                css_selector[Required]: the css selector of the element to find.

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.

            Returns:
                WebElement object
        """
        by = _ConvertEnumService.convert_by_method(By.CssSelector)
        ele = self._element.FindElement(by, css_selector, timeout * 1000)
        return WebElement(ele) if ele else None

    @_ExceptionHandle.try_except
    def find_elements_by_css_selector(
        self,
        css_selector: str,
        timeout: int = 30
    ) :
        """
            Find elements by the given css selector.

            Parameters:
                css_selector[Required]: the css selector of the element to find.

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.

            Returns:
                list of WebElement object
        """
        elements = []
        by = _ConvertEnumService.convert_by_method(By.CssSelector)
        results = self._element.FindElements(by, css_selector, timeout * 1000)
        if results:
            for element in results:
                elements.append(WebElement(element))
        return elements

    @_ExceptionHandle.try_except
    def find_element_by_xpath(
        self,
        xpath: str,
        timeout: int = 30
    ) :
        """
            Find element by the given xpath.

            Parameters:
                xpath[Required]: the xpath of the element to find.

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.

            Returns:
                WebElement object
        """
        by = _ConvertEnumService.convert_by_method(By.XPath)
        ele = self._element.FindElement(by, xpath, timeout * 1000)
        return WebElement(ele) if ele else None

    @_ExceptionHandle.try_except
    def find_elements_by_xpath(
        self,
        xpath: str,
        timeout: int = 30
    ) :
        """
            Find elements by the given xpath.

            Parameters:
                xpath[Required]: the xpath of the element to find.

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds.

            Returns:
                list of WebElement object
        """
        elements = []
        by = _ConvertEnumService.convert_by_method(By.XPath)
        results = self._element.FindElements(by, xpath, timeout * 1000)
        if results:
            for element in results:
                elements.append(WebElement(element))
        return elements

    @_ExceptionHandle.try_except
    def screenshot_to_image(
        self,
        image_file: str,
        timeout: int = 30
    ) -> None :
        """
            Save target element's screenshot to file using cdp tech. Only support for chromium webelements.
 
            Parameters:

                image_file[Required]: file path to save image

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        image = self._element.CaptureScreenShotCDP(timeout * 1000)
        if not Utils.create_file(image_file):
            raise ArgumentError(_Constants.FilePathInvalidError)
        image.Save(image_file)
