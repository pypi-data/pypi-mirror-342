'''
    element base operation
'''

import sys
from typing import Union
from clicknium.common.enums import *
from clicknium.common.constants import _Constants
from clicknium.common.models.mouselocation import MouseLocation
from clicknium.common.models.elementitem import ElementPosition, ElementSize
from clicknium.common.models.exceptions import ArgumentError
from clicknium.common.utils import Utils
from clicknium.core.service.invokerservice import _ConvertBaseTypeService, _ConvertOptionService, _ExceptionHandle

if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal

class UiElement(object):

    def __init__(self, element):
        self._element = element

    @property
    @_ExceptionHandle.try_except
    def parent(self):
        """
            Get parent element.
                                
            Returns:
                UiElement object if it was found, or None if not
        """
        if self._element.Parent:
            return UiElement(self._element.Parent)
        return None

    @property
    @_ExceptionHandle.try_except
    def children(self):
        """
            Get child elements.
                                
            Returns:
                list of UiElement object
        """
        child_list = []
        if self._element.Children:            
            for child in self._element.Children:
                child_list.append(UiElement(child))
        return child_list

    @property
    @_ExceptionHandle.try_except
    def next_sibling(self):
        """
            Get next sibling element.
                                
            Returns:
                UiElement object if it is found, or None if not
        """
        if self._element.NextSibling:
            return UiElement(self._element.NextSibling)
        return None

    @property
    @_ExceptionHandle.try_except
    def previous_sibling(self):
        """
            Get previous sibling element.
                                
            Returns:
                UiElement object if it is found, or None if not
        """
        if self._element.PreviousSibling:
            return UiElement(self._element.PreviousSibling)
        return None
    
    @_ExceptionHandle.try_except
    def child(self, index: int):
        """
            Get child element with index.

            Parameters:
                index[Required]: zero-based index.
                                
            Returns:
                UiElement object if it is found, or None if not
        """
        child_element = self._element.Child(index)
        if child_element:
            return UiElement(self._element.Child(index))
        return None

    @_ExceptionHandle.try_except
    def click(
        self,
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Union[Literal["default", "mouse-emulation", "control-invocation", "dom-event-invocation"], MouseActionBy] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        timeout: int = 30
    ) -> None:        
        """
            Single click the target element.

            Remarks: Import parameters' types with " from clicknium.common.enums import * "
 
            Parameters:

                mouse_button: The available values are: 'left', 'right' and 'center', default is 'left'.  

                mouse_location: it is set to define the position where the element to be clicked. Default position is center of element.  
 
                by: Defines the method to click the UI element.  
                    mouse-emulation: click the target UI element by simulating mouse.  
                    control-invocation: click the target UI element by invoking its UI method. It may not be supported if it is a Windows desktop element.  
                    dom-event-invocation: call event methods bound to the dom elements.
                    default: automatically choose method per element type. For Web element, use `control-invocation`; for Window element, use `mouse-emulation`.  

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with click, and default is none.  

                timeout: timeout for the operation, the unit is second, and default is set to 30 seconds.  
                            
            Returns:
                None
        """
        click_option = _ConvertOptionService.convert_clickoption(ClickType.Click, mouse_button, mouse_location.Location, by, modifier_key, mouse_location.Xoffset, mouse_location.Yoffset, mouse_location.Xrate, mouse_location.Yrate)
        self._element.Click(click_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def double_click(
        self,
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Union[Literal["default", "mouse-emulation", "control-invocation"], MouseActionBy] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        timeout: int = 30
    ) -> None:        
        """
            Double click the target element.  

            Remarks: Import parameters' types with " from clicknium.common.enums import * "
 
            Parameters:

                mouse_button: The available values are: 'left', 'right' and 'center', default is 'left'.  

                mouse_location: it is set to define the position where the element to be clicked. Default position is center of element.  
 
                by: Defines the method to double click the UI element.  
                    mouse-emulation: click the target UI element by simulating mouse.  
                    control-invocation: click the target UI element by invoking its UI method. It may not be supported if it is a Windows desktop element.  
                    default: automatically choose method per element type. For Web element, use `control-invocation`; for Window element, use `mouse-emulation`.  

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with click, and default is none.  

                timeout: timeout for the operation, the unit is second, and default is set to 30 seconds.  
                             
            Returns:
                None

        """
        click_option = _ConvertOptionService.convert_clickoption(ClickType.DoubleClick, mouse_button, mouse_location.Location, by, modifier_key, mouse_location.Xoffset, mouse_location.Yoffset, mouse_location.Xrate, mouse_location.Yrate)
        self._element.Click(click_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def mouse_up(
        self,
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Union[Literal["default", "mouse-emulation", "control-invocation"], MouseActionBy] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        timeout: int = 30
    ) -> None:        
        """
            Mouse button up on the target element.

            Remarks: Import parameters' types with " from clicknium.common.enums import * "
 
            Parameters:

                mouse_button: The available values are: 'left', 'right' and 'center', default is 'left'.  

                mouse_location: it is set to define the position of element where mouse button released. Default position is center of element.  
 
                by: Defines the method to perform releasing mouse button.  
                    mouse-emulation: perform the action by simulating mouse.  
                    control-invocation: perform the action by invoking its UI method. It may not be supported if it is a Windows desktop element.  
                    default: automatically choose method per element type. For Web element, use `control-invocation`; for Window element, use `mouse-emulation`.  

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with the action, and default is none.  

                timeout: timeout for the operation, the unit is second, and default is 30 seconds.  
                             
            Returns:
                None

        """
        click_option = _ConvertOptionService.convert_clickoption(ClickType.Up, mouse_button, mouse_location.Location, by, modifier_key, mouse_location.Xoffset, mouse_location.Yoffset, mouse_location.Xrate, mouse_location.Yrate)
        self._element.Click(click_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def mouse_down(
        self,
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        mouse_location: MouseLocation = MouseLocation(),
        by: Union[Literal["default", "mouse-emulation", "control-invocation"], MouseActionBy] = MouseActionBy.Default,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        timeout: int = 30
    ) -> None:        
        """
            Mouse key down on the target element.

            Remarks: Import parameters' types module with " from clicknium.common.enums import * "
 
            Parameters:

                mouse_button: The available values are: 'left', 'right' and 'center', default is 'left'.  

                mouse_location: it is set to define the position of element where mouse button pressed. Default position is center of element.  
 
                by: Defines the method to perform releasing mouse button.  
                    mouse-emulation: perform the action by simulating mouse.  
                    control-invocation: perform the action by invoking its UI method. It may not be supported if it is a Windows desktop element.  
                    default: automatically choose method per element type. For Web element, use `control-invocation`; for Window element, use `mouse-emulation`.  

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with the action, and default is none.  

                timeout: timeout for the operation, the unit of parameter is seconds, and default is 30 seconds. 
                                
            Returns:
                None

        """
        click_option = _ConvertOptionService.convert_clickoption(ClickType.Down, mouse_button, mouse_location.Location, by, modifier_key, mouse_location.Xoffset, mouse_location.Yoffset, mouse_location.Xrate, mouse_location.Yrate)
        self._element.Click(click_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def send_hotkey(
        self,
        hotkey: str,
        preaction: Literal["setfocus", "click"] = PreAction.SetFocus,
        timeout: int = 30
    ) -> None: 
        """
            Send hotkey to target element.

            Remarks: Import parameter's type with " from clicknium.common.enums import * "
 
            Parameters:

                hotkey[Required]: hotkey string represents one key or combined keys. For example, to represent the letter A, input string "A". To represent the letters A, B, and C, input paremeter "ABC". For special keys, please refer to [hotkeys](https://docs.microsoft.com/en-au/dotnet/api/system.windows.forms.sendkeys?view=windowsdesktop-6.0#remarks).  

                preaction: the action to be taken before sending hotkey.  

                timeout: timeout for the operation, the unit is second, and the default value is 30 seconds.  
                                
            Returns:
                None
        """
        sendhotkey_option = _ConvertOptionService.convert_sendhotkey_option(preaction)       
        self._element.SendHotKey(str(hotkey), sendhotkey_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def drag_drop(
        self,
        xpoint: int = 0,
        ypoint: int = 0,
        speed: int = 50,
        timeout: int = 30
    ) -> None:
        """
            Hold down the mouse left button on the source element, then move to the target offset and release the mouse button. 
 
            Parameters:

                xpoint: moved pixels in X-Axis.  

                ypoint: moved pixels in Y-Axis.  

                speed: drag speed. The unit is ms/10px. Default is 50.  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        dragdrop_option = _ConvertOptionService.convert_dragdrop_option(xpoint, ypoint, speed)
        self._element.DragDrop(dragdrop_option, timeout*1000)

    @_ExceptionHandle.try_except
    def hover(self, timeout: int = 30) -> None:
        """
            Hover over the element, and the mouse will move upon the element and stay for a while.
 
            Parameters:

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        self._element.Hover(timeout * 1000)

    @_ExceptionHandle.try_except
    def set_checkbox(
        self,
        check_type: Literal["check", "uncheck", "toggle"] = CheckType.Check,
        timeout: int = 30
    ) -> None:
        """
            Set check state for a checkbox control.

            Remarks: Import parameter's type with " from clicknium.common.enums import * "
 
            Parameters:

                check_type: the check action types: "check", "uncheck" or "toggle".  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        check_option = _ConvertOptionService.convert_check_option(check_type)
        self._element.Check(check_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def set_text(
        self,
        text: str,        
        by: Union[Literal["default", "set-text", "sendkey-after-click", "sendkey-after-focus"], InputTextBy]= InputTextBy.Default,
        overwrite: bool = True,
        timeout: int = 30
    ) -> None:
        """
            Set text for the target element, it can be used to input text to a system.  

            Remarks: Import parameter's type with " from clicknium.common.enums import * "
 
            Parameters:

                text[Requried]: text string to be input.                 

                by: the method to perform the text input operation. 
                    set-text: call system method to set text to the target element. Some Windows application elements may not be supported.  
                    sendkey-after-click: simulate mouse click to activate the element, then send keys by simulating keyboard.  
                    sendkey-after-focus: set the target element to focused state, then send keys by simulating keyboard.  
                    default: using different methods per target element type. `set-text` for web element and `sendkey-after-click` for desktop element.  

                overwrite: whether overwrite or append the text on the target element, default is True. 

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        settext_option = _ConvertOptionService.convert_settext_option(by, overwrite == False)
        self._element.SetText(str(text), settext_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def clear_text(
        self,
        by: Union[Literal["set-text", "send-hotkey"], ClearTextBy],
        clear_hotkey: Union[Literal["CAD", "ESHD", "HSED"], ClearHotKey] = ClearHotKey.CtrlA_Delete,
        preaction: Literal["setfocus", "click"] = PreAction.SetFocus,
        timeout: int = 30
    ) -> None:
        """
            Clear the element's text.

            Remarks: Import parameters' types with " from clicknium.common.enums import * "
 
            Parameters:

                by: clear method, the method to clear text for the target element  
                    set-text: clear the target element's text by calling system method.  
                    send-hotkey: clear text by sending hotkey to the target element. "clear_hotkey" and "preaction" parameters also need to be specified accordingly.   

                clear_hotkey: If clear_method is set to "send-hotkey", then specify hotkey with this parameter, default is `CAD`.  
                    CAD: {CTRL}{A}-{DELETE}, send the combined hotkey "{CTRL}{A}" first, then send hotkey "{DELETE}"
                    ESHD: {END}{SHIFT}{HOME}{DELETE}, send the hotkey "{END}" first, then send combined hotkey "{SHIFT}{HOME}, then send hotkey "{DELETE}"
                    HSED: {HOME}{SHIFT}{END}{DELETE}, send the hotkey "{HOME}" first, then send combined hotkey "{SHIFT}{END}, then send hotkey "{DELETE}"

                preaction: If clear_method is set to "send-hotkey", specify this parameter for the action to be taken before sending hotkey to clear text.   

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        cleartext_option = _ConvertOptionService.convert_cleartext_option(by, clear_hotkey, preaction)
        self._element.ClearText(cleartext_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def get_text(self, timeout: int = 30) -> str:
        """
            Get text of the element.
 
            Parameters:

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds

            Returns:
                str
        """
        return self._element.GetText(timeout * 1000)

    @_ExceptionHandle.try_except
    def get_property(
        self,
        name: str,
        timeout: int = 30
    ) -> str:
        """
            Get property value of the target element. 
 
            Parameters:

                name[Required]: property name, different UI elements may support different properties.  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds

            Returns:
                str
        """
        return self._element.GetProperty(name, timeout * 1000)

    @_ExceptionHandle.try_except
    def select_item(
        self,
        item: str,
        timeout: int = 30
    ) -> None:
        """
            Select one option for the target element when it is a dropdown type control.  
 
            Parameters:

                item[Required]: target option of the dropdown control.  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        self._element.SelectItem(str(item), timeout * 1000)

    @_ExceptionHandle.try_except
    def select_items(
        self,
        items: list,
        clear_selected: bool = True,
        timeout: int = 30
    ) -> None:
        """
            Select multiple options for the target element that can support multiple selections.
 
            Parameters:

                items[Required]: options to be selected.

                clear_selected: whether to clear existing selections, default is True.  

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        items_array = _ConvertBaseTypeService.convert_array(items)
        select_items_option = _ConvertOptionService.convert_select_items_option(clear_selected)
        self._element.SelectMultipleItem(items_array, select_items_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def save_to_image(
        self,
        image_file: str,
        img_width: int = 0,
        img_height: int = 0,
        xoffset: int = 0,
        yoffset: int  = 0,
        timeout: int = 30
    ) -> None:
        """
            Save target element's screenshot to file with the specified size and offset.
 
            Parameters:

                image_file[Required]: file path to save image

                img_width: specify the screenshot width. Default is the target element's width.  

                img_height: speficy the screenshot height. Default is the target element's height.  

                xoffset: offset of X-Axis from the target element's left-top corner.

                yoffset: offset of Y-Axis from the target element's left-top corner.

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """        
        save_image_option = _ConvertOptionService.convert_save_image_option(img_width, img_height, xoffset, yoffset)
        image = self._element.CaptureScreenShot(save_image_option, timeout * 1000)
        if not Utils.create_file(image_file):
            raise ArgumentError(_Constants.FilePathInvalidError)
        image.Save(image_file)

    @_ExceptionHandle.try_except
    def highlight(
        self,
        color: Union[str, Color] = Color.Yellow,
        duration: int = 3,        
        timeout: int = 30
    ) -> None: 
        """
            Highlight the element with specified color.

            Remarks: Import parameter's type with " from clicknium.common.enums import * "
 
            Parameters:

                color: the color of the highlighting rectangle, default is Yellow

                duration: the duration for highlighting the element. The unit is second. Default is set to 3 seconds                

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                                
            Returns:
                None
        """
        if len(color) != 7:
            raise ArgumentError(_Constants.InvalidColor)
        color = color.lower().replace("#","#ff")
        highlight_option = _ConvertOptionService.convert_highlight_option(duration, color)  
        self._element.Highlight(highlight_option, timeout * 1000)

    @_ExceptionHandle.try_except
    def set_focus(self, timeout: int = 30) -> None:
        """
            Set the target element to focused state.
 
            Parameters:

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds
                
            Returns:
                None
        """
        self._element.SetFocus(timeout * 1000)

    @_ExceptionHandle.try_except
    def get_position(self, timeout: int = 30) -> ElementPosition:
        """
            Get position of the target element.
 
            Parameters:

                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds

            Returns:
                ElementPosition
        """
        rectangle = self._element.GetLocation(timeout * 1000)
        return ElementPosition(rectangle.Left, rectangle.Top, rectangle.Right, rectangle.Bottom) if rectangle else None

    @_ExceptionHandle.try_except
    def get_size(self, timeout: int = 30) -> ElementSize:
        """
            Get element's size(height and width).
 
            Parameters:
                timeout: timeout for the operation. The unit of parameter is seconds. Default is set to 30 seconds

            Returns:
                ElementSize
        """
        rectangle = self._element.GetLocation(timeout * 1000)
        return ElementSize(rectangle.Width, rectangle.Height) if rectangle else None

    @_ExceptionHandle.try_except
    def wait_property(
        self,
        name: str, 
        value: str, 
        wait_timeout: int = 30
    ) -> bool:
        """
            Wait for the target element's property to be expected value within specified timeout. 
 
            Parameters:
                name[Required]: property name, different UI elements may support different properties.

                value[Required]: expected property value

                wait_timeout: wait timeout for the operation, unit is second, default value is 30 seconds
 
            Returns:
                bool, return True if UI element exist and the property value equals expected value, or return False
        """        
        result = self._element.WaitProperty(str(name), str(value), wait_timeout * 1000)
        return True if result else False