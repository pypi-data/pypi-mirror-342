from typing import List
import clr
import os
from clicknium.common.constants import _Constants, _ExceptionNames
from clicknium.common.enums import *
from clicknium.common.models.exceptions import *
from clicknium.common.models.rectangle import Rectangle
from clicknium.common.utils import Utils
from clicknium.common.models.locatoritem import LocatorItem

source_path = Utils.get_automation_libfolder()
black_dlls = ['Clicknium.Desktop.IA.Core.dll']
dlls = Utils.get_import_dlls(source_path)
for dll in dlls:
    if dll not in black_dlls:
        dll_path = os.path.join(source_path, dll)
        clr.AddReference(dll_path)

from Clicknium.Wrapper import UiElementRunner, BrowserTabExtension,Logger
from Clicknium.Wrapper.Options import *
from Clicknium.Common import BrowserType as dotnet_BrowserType, AutomationTech as dotnet_AutomationTech
from Clicknium.Common.Exception import ElementNotFoundException, DesktopException, WebException
from Clicknium.Common.Options import BringWindowType as dotnet_BringWindowType, InputMethod as dotnet_InputMethod, ClickType as dotnet_ClickType, \
                                    MouseButton as dotnet_MouseButton, ClickLocation as dotnet_ClickLocation, ClickMethod as dotnet_ClickMethod, \
                                    ModifierKeysEnum as dotnet_ModifierKeysEnum, PrefixAction as dotnet_PrefixAction, CheckType as dotnet_CheckType, \
                                    WebUserDataFolderMode as dotnet_WebUserDataFolderMode, OpenBrowserOption as dotnet_OpenBrowserOption, \
                                    ClearMethod as dotnet_ClearMethod, ClearHotKey as dotnet_ClearHotKey, ScrollOption as dotnet_ScrollOption, \
                                    WebInlineSelectorType as dotnet_WebInlineSelectorType, CaptureScreenShotOption as dotnet_CaptureScreenShotOption, \
                                    CaptureScreenShotMode as dotnet_CaptureScreenShotMode, ScreenShotRect as dotnet_ScreenShotRect
from Clicknium.LocatorStore import LocatorStoreManager
from Clicknium.LocatorStore.Common.Exceptions import UnAuthorizedException, LocatorStoreQueryException
from System.Collections.Generic import Dictionary, List as dotnet_List
from System import *
from System.Drawing import ColorTranslator, Point
#from Clicknium.Telemetry import TelemetryWrapper
# from Clicknium.Telemetry.Models import EventData, EventTypes as dotnet_EventTypes

#TelemetryInstance =  TelemetryWrapper("Python", Utils.PythonVersion, _Constants.SdkVersion)

class _ExceptionHandle:
    
    @staticmethod
    def try_except(func):
        def wrapper(*args, **kwargs):
            exception : Exception = None     
            properties = {_Constants.EventDataMethodKey: func.__name__}
            try:    
                # if func.__name__ and Utils.is_need_telemetry(func.__name__):             
                #     TelemetryService.report_event(EventTypes.ApiCall, properties)
                return func(*args, **kwargs)

            except ArgumentException as e:
                exception_name = e.__class__.__name__
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                if(exception_name.__eq__(_ExceptionNames.ArgumentNullException)):
                    exception = ArgumentNullError(exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.ArgumentNullException)):
                    exception = ArgumentOutOfRangeError(exception_message, exception_stacktrace)
                else:
                    exception = ArgumentError(exception_message, exception_stacktrace)

            except NotSupportedException as e:
                exception_name = e.__class__.__name__
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                if(exception_name.__eq__(_ExceptionNames.OperationNotSupportedException)):
                    automation_tech = _ConvertDotnetEnumService.convert_automatiom_tech_method(e.AutoTech)
                    control_type = e.ControlType
                    operation = e.Operation
                    exception = NotSupportedOperationError(automation_tech, control_type, operation, exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.OperationOptionNotSupportedException)):
                    automation_tech = _ConvertDotnetEnumService.convert_automatiom_tech_method(e.AutoTech)
                    control_type = e.ControlType
                    operation = e.Operation
                    option = e.Option
                    exception = NotSupportedOperationOptionError(automation_tech, control_type, operation, option, exception_message, exception_stacktrace)
                else:
                    exception = NotSupportedError(exception_message, exception_stacktrace)

            except InvalidOperationException as e:
                exception_name = e.__class__.__name__
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                if(exception_name.__eq__(_ExceptionNames.InvalidSelectedItemException)):
                    exception = InvalidSelectedItemError(e.Item, exception_message, exception_stacktrace)
                else: 
                    exception = InvalidOperationError(exception_message, exception_stacktrace)

            except TimeoutException as e:
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                exception = OperationTimeoutError(exception_message, exception_stacktrace)

            except ElementNotFoundException as e:
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                exception = ElementNotFoundError(exception_message, exception_stacktrace)

            except DesktopException as e:
                exception_name = e.__class__.__name__
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                if(exception_name.__eq__(_ExceptionNames.WindowsNativeException)):
                    name = e.Name
                    native_errorcode = e.NativeErrorCode
                    exception = WindowsNativeError(name, native_errorcode, exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.UiaPatternNotFoundException)):
                    exception = UiaPatternNotFoundError(exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.ScreenOperationException)):
                    name = e.Name
                    native_errorcode = e.NativeErrorCode
                    exception = ScreenOperationError(name, native_errorcode, exception_message, exception_stacktrace)
                else:
                    exception = WindowError(exception_message, exception_stacktrace)

            except WebException as e:
                exception_name = e.__class__.__name__
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                browser_type = e.BrowserName               
                if(exception_name.__eq__(_ExceptionNames.BrowserNotRunException)):
                    exception = BrowserNotRunError(browser_type, exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.BrowserNotInstallException)):
                    exception = BrowserNotInstallError(browser_type, exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.UnreachableBrowserExtensionException)):
                    exception = UnreachableBrowserExtensionError(browser_type, exception_message, exception_stacktrace)
                elif(exception_name.__eq__(_ExceptionNames.WebElementNotRespondingException)):
                    exception = WebElementNotRespondingError(browser_type, exception_message, exception_stacktrace)  
                elif(exception_name.__eq__(_ExceptionNames.ChromiumNotSupportException)):
                    exception = ChromiumNotSupportError(browser_type, exception_message, exception_stacktrace)
                else:
                    exception = WebError(browser_type, exception_message, exception_stacktrace)

            except LocatorStoreQueryException as e:
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                exception = LocatorRequestError(exception_message, exception_stacktrace)

            except UnAuthorizedException as e:
                exception_message = e.Message
                exception_stacktrace = e.StackTrace
                exception = UnAuthorizedError(exception_message, exception_stacktrace)

            except BaseError as e:
                exception = e

            except Exception as e:
                exception = BaseError(e.Message, e.StackTrace)             

            if exception:
                # TrackException
                properties[_Constants.EventDataMessageKey] = exception.message
                properties[_Constants.EventDataStacktraceKey] = exception.stacktrace
                # if func.__name__ and Utils.is_need_telemetry(func.__name__):
                #     TelemetryService.report_event(EventTypes.ExceptionReport, properties)
                raise exception;        

        return wrapper


class _InvokerService:    

    # region BrowserTabExtension

    @staticmethod
    @_ExceptionHandle.try_except
    def find_element_web(tab, locator, locator_variables = {}):  
        locator_item = LocatorService.get_locator(locator, locator_variables)
        return BrowserTabExtension.GetElement(tab, locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_element_by_xpath(tab, locator):
        return BrowserTabExtension.GetElement(tab, dotnet_WebInlineSelectorType.XPath, locator)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_element_by_css_selector(tab, locator):
        return BrowserTabExtension.GetElement(tab, dotnet_WebInlineSelectorType.CssSelector, locator)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_elements_web(tab, locator, locator_variables = {}, timeout = 30):  
        locator_item = LocatorService.get_locator(locator, locator_variables)
        return BrowserTabExtension.FindElements(tab, locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_elements_by_xpath(tab, locator, timeout = 30):
        return BrowserTabExtension.FindElements(tab, dotnet_WebInlineSelectorType.XPath, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_elements_by_css_selector(tab, locator, timeout = 30):
        return BrowserTabExtension.FindElements(tab, dotnet_WebInlineSelectorType.CssSelector, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_disappear_web(tab, locator, locator_variables = {}, timeout = 30):   
        locator_item = LocatorService.get_locator(locator, locator_variables)   
        return BrowserTabExtension.WaitElementDisappear(tab, locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_disappear_by_xpath(tab, locator, timeout = 30):
        return BrowserTabExtension.WaitElementDisappear(tab, dotnet_WebInlineSelectorType.XPath, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_disappear_by_css_selector(tab, locator, timeout = 30):
        return BrowserTabExtension.WaitElementDisappear(tab, dotnet_WebInlineSelectorType.CssSelector, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_appear_web(tab, locator, locator_variables = {}, timeout = 30):    
        locator_item = LocatorService.get_locator(locator, locator_variables)  
        return BrowserTabExtension.WaitElementAppear(tab, locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_appear_by_xpath(tab, locator, timeout = 30):
        return BrowserTabExtension.WaitElementAppear(tab, dotnet_WebInlineSelectorType.XPath, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_appear_by_css_selector(tab, locator, timeout = 30):
        return BrowserTabExtension.WaitElementAppear(tab, dotnet_WebInlineSelectorType.CssSelector, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def is_existing_web(tab, locator, locator_variables = {}, timeout = 30):
        locator_item = LocatorService.get_locator(locator, locator_variables)
        return BrowserTabExtension.ElementIsExist(tab, locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def is_existing_by_xpath(tab, locator, timeout = 30):
        return BrowserTabExtension.ElementIsExist(tab, dotnet_WebInlineSelectorType.XPath, locator, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def is_existing_by_css_selector(tab, locator, timeout = 30):
        return BrowserTabExtension.ElementIsExist(tab, dotnet_WebInlineSelectorType.CssSelector, locator, timeout * 1000)

    # endregion BrowserTabExtension

    # region UiElementRunner

    @staticmethod
    @_ExceptionHandle.try_except
    def find_element(locator, locator_variables = {}, window_mode = WindowMode.Auto):       
        mode = _ConvertEnumService.convert_window_mode_enum(WindowMode(window_mode))    
        locator_item = LocatorService.get_locator(locator, locator_variables)          
        return UiElementRunner.GetElement(locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, mode)

    @staticmethod
    @_ExceptionHandle.try_except
    def find_elements(locator, locator_variables = {}, timeout = 30):       
        locator_item = LocatorService.get_locator(locator, locator_variables)          
        return UiElementRunner.FindElements(locator_item.Locator, locator_item.Locator_Variables, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def get_webdriver(browser_type):
        return UiElementRunner.GetWebDriver(browser_type)

    @staticmethod
    @_ExceptionHandle.try_except
    def get_chromiumwebdriver(browser_name):
        return UiElementRunner.GetChromiumDriver(browser_name)

    @staticmethod
    @_ExceptionHandle.try_except
    def get_windowdriver():
        return UiElementRunner.GetDesktopDriver()

    @staticmethod
    @_ExceptionHandle.try_except
    def get_sapdriver():
        return UiElementRunner.GetSapDriver()

    @staticmethod
    @_ExceptionHandle.try_except
    def get_mousedriver():
        return UiElementRunner.GetMouseDriver()   

    @staticmethod
    @_ExceptionHandle.try_except
    def send_hotkey(hotkey):
        return UiElementRunner.SendHotKey(hotkey)

    @staticmethod
    @_ExceptionHandle.try_except
    def send_text(text):
        return UiElementRunner.InputText(text)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_disappear(locator, locator_variables = {}, timeout = 30):   
        locator_item = LocatorService.get_locator(locator, locator_variables)   
        return UiElementRunner.WaitElementDisappear(locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def wait_appear(locator, locator_variables = {}, timeout = 30):    
        locator_item = LocatorService.get_locator(locator, locator_variables)  
        return UiElementRunner.WaitElementAppear(locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def is_existing(locator, locator_variables = {}, timeout = 30):
        locator_item = LocatorService.get_locator(locator, locator_variables)
        return UiElementRunner.ElementIsExist(locator_item.Locator, locator_item.Locator_Variables, locator_item.Locator_Image, timeout * 1000)

    @staticmethod
    @_ExceptionHandle.try_except
    def get_screenshot():
        return UiElementRunner.GetScreenshot()

    @staticmethod
    @_ExceptionHandle.try_except
    def scrape_data(locator, locator_variables = {},next_page_button_locator=None, next_page_button_locator_variables={}, next_page_button_by=MouseActionBy.Default, wait_page_load_time=1, max_count=-2147483648, timeout = 30):
        locator_item = LocatorService.get_locator(locator, locator_variables)
        next_page_locator = None
        next_page_variables = None
        next_page_image = None
        if next_page_button_locator:
            next_page_button_locator_item = LocatorService.get_locator(next_page_button_locator, next_page_button_locator_variables)
            next_page_locator = next_page_button_locator_item.Locator
            next_page_variables = next_page_button_locator_item.Locator_Variables
            next_page_image = next_page_button_locator_item.Locator_Image
        click_option = _ConvertOptionService.convert_clickoption(click_method=next_page_button_by)
        return UiElementRunner.ScrapeData(locator_item.Locator, locator_item.MetaData, locator_item.Locator_Variables, 
            next_page_locator, next_page_image, next_page_variables, click_option, wait_page_load_time * 1000, max_count, timeout * 1000)
    
    @staticmethod
    @_ExceptionHandle.try_except
    def scrape_data_web(tab, locator, locator_variables = {},next_page_button_locator=None, next_page_button_locator_variables={}, next_page_button_by=MouseActionBy.Default, wait_page_load_time=1, max_count=-2147483648, timeout = 30):
        locator_item = LocatorService.get_locator(locator, locator_variables)
        next_page_locator = None
        next_page_variables = None
        next_page_image = None
        if next_page_button_locator:
            next_page_button_locator_item = LocatorService.get_locator(next_page_button_locator, next_page_button_locator_variables)
            next_page_locator = next_page_button_locator_item.Locator
            next_page_variables = next_page_button_locator_item.Locator_Variables
            next_page_image = next_page_button_locator_item.Locator_Image
        click_option = _ConvertOptionService.convert_clickoption(click_method=next_page_button_by)
        return BrowserTabExtension.ScrapeData(tab, locator_item.Locator, locator_item.MetaData, locator_item.Locator_Variables, 
            next_page_locator, next_page_image, next_page_variables, click_option, wait_page_load_time * 1000, max_count, timeout * 1000)
        
    @staticmethod
    @_ExceptionHandle.try_except
    def get_cdpwebdriver(browser_type):
        return UiElementRunner.GetCdpDriver(browser_type)
    # endregion UiElementRunner
    
    #region Logger
    def info(msg:str):
        Logger.Instance.Info(msg)
        
    def debug(msg:str):
        Logger.Instance.Debug(msg)
        
    def warn(msg:str):
        Logger.Instance.Warn(msg)
        
    def error(msg:str):
        Logger.Instance.Error(msg)
    #endregion 


class LocatorService:

    @staticmethod
    def get_locator(locator, locator_variables = {}):
        project_folder = Utils.get_project_folder(_Constants.ClickniumYaml)
        if not project_folder:
            project_folder = Utils.get_project_folder(_Constants.LocatorFolder)
        if not project_folder:
            raise LocatorUndefinedError(_Constants.LocatorNotExist % locator)
        variables = _ConvertBaseTypeService.convert_dict(locator_variables) 
        locator_item = LocatorStoreManager.GetLocator(project_folder, str(locator), variables)
        if not locator_item:
            raise LocatorUndefinedError(_Constants.LocatorNotExist % locator)
        
        return LocatorItem(locator_item.Content, locator_item.Image, variables, locator_item.MetaData)


# class TelemetryService:
    
#     @staticmethod
#     def report_event(type: str, properties: dict):
#         data = _ConvertOptionService.convert_event_data(type, properties)
#         TelemetryInstance.ReportEvent(data)


class _ConvertBaseTypeService:

    @staticmethod
    def convert_array(source_array):
        target_array = map(str, source_array)
        return Array[String](target_array)

    @staticmethod
    def convert_dict(source_dic):
        target_dict = Dictionary[String, Object]()
        for key in source_dic:
            target_dict[key] = str(source_dic[key])
        return target_dict

    @staticmethod
    def convert_dict_str(source_dic):
        target_dict = Dictionary[String, String]()
        for key in source_dic:
            target_dict[key] = source_dic[key]
        return target_dict

    @staticmethod
    def convert_list(source_list):
        target_list = dotnet_List[String]()
        for source in source_list:
            target_list.Add(source)
        return target_list

    @staticmethod
    def convert_color(color):
        return ColorTranslator.FromHtml(color)

    @staticmethod
    def convert_point(x, y):
        return Point(x,y)


class _ConvertOptionService:

    @staticmethod
    def convert_clickoption(click_type = ClickType.Click, mouse_button = MouseButton.Left, click_location = Location.Center, 
                    click_method = MouseActionBy.Default, modifier_key = ModifierKey.NoneKey, 
                    xoffset = 0, yoffset= 0, xrate=0, yrate = 0):
        click_option = ClickOption()        
        click_option.ClickType = _ConvertEnumService.convert_click_type_enum(click_type)
        click_option.MouseButton = _ConvertEnumService.convert_mouse_button_enum(MouseButton(mouse_button))
        click_option.ClickLocation = _ConvertEnumService.convert_click_location_enum(Location(click_location))
        click_option.ClickMethod = _ConvertEnumService.convert_click_method_enum(MouseActionBy(click_method))
        click_option.ModifierKey = _ConvertEnumService.convert_modifier_key_enum(ModifierKey(modifier_key))
        click_option.XOffset = xoffset
        click_option.YOffset = yoffset
        click_option.XRate = xrate
        click_option.YRate = yrate
        return click_option

    @staticmethod
    def convert_settext_option(input_method = InputTextBy.SetText, append = False):
        method = _ConvertEnumService.convert_input_method(InputTextBy(input_method))
        settext_option = SetTextOption()
        settext_option.InputMethod = method
        settext_option.IsAppend = append
        return settext_option

    @staticmethod
    def convert_cleartext_option(clear_method, clear_hotkey= ClearHotKey.CtrlA_Delete, preaction = PreAction.SetFocus):
        clear_hotkey_option = ClearHotKeyOption()
        clear_hotkey_option.HotKey = _ConvertEnumService.convert_clear_hotkey_method(ClearHotKey(clear_hotkey))
        clear_hotkey_option.PrefixAction = _ConvertEnumService.convert_preaction_method(PreAction(preaction))
        cleartext_option = ClearTextOption()
        cleartext_option.ClearMethod = _ConvertEnumService.convert_clear_method(ClearTextBy(clear_method))
        cleartext_option.ClearHotKeyOption = clear_hotkey_option
        return cleartext_option

    @staticmethod
    def convert_sendhotkey_option(preaction = PreAction.SetFocus):
        action = _ConvertEnumService.convert_preaction_method(PreAction(preaction))
        sendhotkey_option = SendHotKeyOption()
        sendhotkey_option.PrefixAction = action
        return sendhotkey_option

    @staticmethod
    def convert_dragdrop_option(xpoint = 0, ypoint = 0, speed = 50):
        dragdrop_option = DragdropOption()
        dragdrop_option.IntervalTime = speed
        dragdrop_option.XPoint = xpoint
        dragdrop_option.YPoint = ypoint
        return dragdrop_option

    @staticmethod
    def convert_check_option(check_type):
        check_option = CheckOption()
        check_option.CheckType = _ConvertEnumService.convert_checktype_method(CheckType(check_type))
        return check_option

    @staticmethod
    def convert_select_items_option(clear_selected):
        select_items_option = SelectMultipleItemOption()
        select_items_option.ClearSelected = clear_selected
        return select_items_option

    @staticmethod
    def convert_highlight_option(duration = 3, color = Color.Yellow):
        highlight_option = HighlightOption()
        highlight_option.HighlightTime = duration * 1000
        highlight_option.HighlightColor = _ConvertBaseTypeService.convert_color(color)
        return highlight_option
    
    @staticmethod
    def convert_save_image_option(img_width = 0, img_height = 0, xoffset = 0, yoffset  = 0):
        save_image_option = ScreenshotOption()
        save_image_option.ImgHeight = img_height
        save_image_option.ImgWidth = img_width
        save_image_option.XOffset = xoffset
        save_image_option.YOffset = yoffset
        return save_image_option

    @staticmethod
    def convert_capture_screenshot_option(mode: ScreenShotMode,  rect: Rectangle, wait_for_page_delay: int):
        capture_screenshot_option = dotnet_CaptureScreenShotOption()
        if mode == ScreenShotMode.Bounds:
            capture_screenshot_option.Mode = dotnet_CaptureScreenShotMode.Bounds
            if rect:
                screenshot_rect = dotnet_ScreenShotRect()
                screenshot_rect.Left = rect.Xoffset,
                screenshot_rect.Top = rect.Yoffset,
                screenshot_rect.Width = rect.Width,
                screenshot_rect.Height = rect.Height,
                capture_screenshot_option.Bounds = screenshot_rect
        elif mode == ScreenShotMode.Viewport:
            capture_screenshot_option.Mode = dotnet_CaptureScreenShotMode.Viewport
        else:
            capture_screenshot_option.Mode = dotnet_CaptureScreenShotMode.Full
            capture_screenshot_option.WaitForPageDelay = wait_for_page_delay * 1000
        return capture_screenshot_option

    @staticmethod
    def convert_open_browser_option(userdata_folder_mode, userdata_folder_path = "", args: List[str] = None):
        open_browser_option = dotnet_OpenBrowserOption()
        open_browser_option.UserDataFolderMode = _ConvertEnumService.convert_webuser_datafolder_mode_method(WebUserDataMode(userdata_folder_mode))
        if args:
            open_browser_option.Arguments = _ConvertBaseTypeService.convert_list(args)
        open_browser_option.UserDataFolderPath = userdata_folder_path
        return open_browser_option

    @staticmethod
    def convert_event_data(type, properties):
        event_data = EventData()
        event_data.Type = _ConvertEnumService.convert_event_type(type)
        event_data.Properties = _ConvertBaseTypeService.convert_dict_str(properties)
        return event_data

    @staticmethod
    def convert_scrolloption(x = 0, y = 0):
        scroll_option = dotnet_ScrollOption()
        scroll_option.X = x
        scroll_option.Y = y
        return scroll_option


class _ConvertEnumService:

    @staticmethod
    def convert_browser_type_enum(browser_type):
        if browser_type == BrowserType.IE:
            return dotnet_BrowserType.IE
        elif browser_type == BrowserType.Chrome:
            return dotnet_BrowserType.Chrome
        elif browser_type == BrowserType.FireFox:
            return dotnet_BrowserType.FireFox
        elif browser_type == BrowserType.Edge:
            return dotnet_BrowserType.Edge

    @staticmethod
    def convert_click_type_enum(click_type):
        if click_type == ClickType.Click:
            return dotnet_ClickType.SingleClick
        elif click_type == ClickType.DoubleClick:
            return dotnet_ClickType.DoubleClick
        elif click_type == ClickType.Down:
            return dotnet_ClickType.DownClick
        elif click_type == ClickType.Up:
            return dotnet_ClickType.UpClick

    @staticmethod
    def convert_mouse_button_enum(mouse_button):
        if mouse_button == MouseButton.Left:
            return dotnet_MouseButton.LeftButton
        elif mouse_button == MouseButton.Middle:
            return dotnet_MouseButton.MiddleButton
        elif mouse_button == MouseButton.Right:
            return dotnet_MouseButton.RightButton

    @staticmethod
    def convert_click_location_enum(click_location):
        if click_location == Location.Center:
            return dotnet_ClickLocation.Center
        elif click_location == Location.LeftTop:
            return dotnet_ClickLocation.LeftTop
        elif click_location == Location.LeftBottom:
            return dotnet_ClickLocation.LeftBottom
        elif click_location == Location.RightTop:
            return dotnet_ClickLocation.RightTop
        elif click_location == Location.RightBottom:
            return dotnet_ClickLocation.RightBottom

    @staticmethod
    def convert_click_method_enum(click_method):
        if click_method == MouseActionBy.Default:
            return dotnet_ClickMethod.Default
        elif click_method == MouseActionBy.MouseEmulation:
            return dotnet_ClickMethod.MouseEmulation
        elif click_method == MouseActionBy.ControlInvocation:
            return dotnet_ClickMethod.ControlInvocation
        elif click_method == MouseActionBy.DomEventInvocation:
            return dotnet_ClickMethod.DomEventInvocation

    @staticmethod
    def convert_modifier_key_enum(modifier_key):
        if modifier_key == ModifierKey.NoneKey:
            return dotnet_ModifierKeysEnum.NoneKey
        elif modifier_key == ModifierKey.Alt:
            return dotnet_ModifierKeysEnum.Alt
        elif modifier_key == ModifierKey.Ctrl:
            return dotnet_ModifierKeysEnum.Ctrl
        elif modifier_key == ModifierKey.Shift:
            return dotnet_ModifierKeysEnum.Shift
        elif modifier_key == ModifierKey.Win:
            return dotnet_ModifierKeysEnum.Win

    @staticmethod
    def convert_window_mode_enum(window_mode):
        if window_mode == WindowMode.Auto:
            return dotnet_BringWindowType.Auto
        elif window_mode == WindowMode.TopMost:
            return dotnet_BringWindowType.TopMost
        elif window_mode == WindowMode.NoAction:
            return dotnet_BringWindowType.NoAction

    @staticmethod
    def convert_input_method(input_method):
        if input_method == InputTextBy.Default:
            return dotnet_InputMethod.Default
        elif input_method == InputTextBy.SetText:
            return dotnet_InputMethod.ControlSetValue
        elif input_method == InputTextBy.SendKeyAfterClick:
            return dotnet_InputMethod.KeyboardSimulationWithClick
        elif input_method == InputTextBy.SendKeyAfterFocus:
            return dotnet_InputMethod.KeyboardSimulationWithFocus

    @staticmethod
    def convert_clear_method(clear_method):
        if clear_method == ClearTextBy.SetText:
            return dotnet_ClearMethod.ControlClearValue
        elif clear_method == ClearTextBy.SendHotKey:
            return dotnet_ClearMethod.SendHotKey

    @staticmethod
    def convert_clear_hotkey_method(clear_hotkey):
        if clear_hotkey == ClearHotKey.CtrlA_Delete:
            return dotnet_ClearHotKey.CtrlA_Delete
        elif clear_hotkey == ClearHotKey.Home_ShiftEnd_Delete:
            return dotnet_ClearHotKey.Home_ShiftEnd_Delete
        elif clear_hotkey == ClearHotKey.End_ShiftHome_Delete:
            return dotnet_ClearHotKey.End_ShiftHome_Delete

    @staticmethod
    def convert_preaction_method(preaction):
        if preaction == PreAction.SetFocus:
            return dotnet_PrefixAction.SetFocus
        elif preaction == PreAction.Click:
            return dotnet_PrefixAction.Click

    @staticmethod
    def convert_checktype_method(check_type):
        if check_type == CheckType.Check:
            return dotnet_CheckType.Check
        elif check_type == CheckType.UnCheck:
            return dotnet_CheckType.UnCheck
        elif check_type == CheckType.Toggle:
            return dotnet_CheckType.Toggle

    @staticmethod
    def convert_webuser_datafolder_mode_method(webuser_datafolder_mode):
        if webuser_datafolder_mode == WebUserDataMode.Automatic:
            return dotnet_WebUserDataFolderMode.Automatic
        elif webuser_datafolder_mode == WebUserDataMode.Default:
            return dotnet_WebUserDataFolderMode.DefaultFolder
        elif webuser_datafolder_mode == WebUserDataMode.Custom:
            return dotnet_WebUserDataFolderMode.CustomFolder

    @staticmethod
    def convert_event_type(type):
        if type == EventTypes.ApiCall:
            return dotnet_EventTypes.ApiCall
        elif type == EventTypes.ExceptionReport:
            return dotnet_EventTypes.ExceptionReport

    @staticmethod
    def convert_by_method(by):
        if by == By.XPath :
            return dotnet_WebInlineSelectorType.XPath
        elif by == By.CssSelector:
            return dotnet_WebInlineSelectorType.CssSelector

        
class _ConvertDotnetEnumService:

    @staticmethod
    def convert_automatiom_tech_method(automation):
        if(automation == dotnet_AutomationTech.Uia):
            return AutomationTech.Uia
        elif(automation == dotnet_AutomationTech.Java):
            return AutomationTech.Java
        elif(automation == dotnet_AutomationTech.IE):
            return AutomationTech.IE
        elif(automation == dotnet_AutomationTech.Chrome):
            return AutomationTech.Chrome
        elif(automation == dotnet_AutomationTech.Firefox):
            return AutomationTech.Firefox
        elif(automation == dotnet_AutomationTech.Sap):
            return AutomationTech.Sap
        elif(automation == dotnet_AutomationTech.Edge):
            return AutomationTech.Edge
        elif(automation == dotnet_AutomationTech.IA):
            return AutomationTech.IA

    @staticmethod
    def convert_browser_type_method(browser_type):
        if(browser_type == dotnet_BrowserType.IE):
            return BrowserType.IE
        elif(browser_type == dotnet_BrowserType.Chrome):
            return BrowserType.Chrome
        elif(browser_type == dotnet_BrowserType.FireFox):
            return BrowserType.FireFox
        elif(browser_type == dotnet_BrowserType.Edge):
            return BrowserType.Edge
        else:
            if browser_type:
                return str(browser_type)