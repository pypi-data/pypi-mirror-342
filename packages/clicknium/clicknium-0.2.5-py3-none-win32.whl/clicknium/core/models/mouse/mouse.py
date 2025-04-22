import sys
from typing import Tuple
from clicknium.common.enums import *
from clicknium.core.service.invokerservice import _ExceptionHandle, _InvokerService, _ConvertBaseTypeService, _ConvertEnumService
if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal

class Mouse(object):

    def __init__(self):
        self.mouse_driver = _InvokerService.get_mousedriver()

    @_ExceptionHandle.try_except
    def click(
        self, 
        x: int, 
        y: int, 
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey,
        delay: int = 0
    ) -> None:
        '''
            Perform a single click with the specified mouse button.

            Parameters:
                x[Required]: Defines the X integer coordinate.

                y[Required]: Defines the Y integer coordinate.

                mouse_button: Define the position of the mouse button, and default is left button.

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with the action, and default is none.  

                delay: Defines the time to wait between mouse down and mouse up, the unit is second, and default is set to 0 seconds.

            Returns:
                None
        '''
        point = _ConvertBaseTypeService.convert_point(x,y)
        button = _ConvertEnumService.convert_mouse_button_enum(MouseButton(mouse_button))
        modifier_key = _ConvertEnumService.convert_modifier_key_enum(ModifierKey(modifier_key))
        self.mouse_driver.MouseClick(point, button, modifier_key, delay)

    @_ExceptionHandle.try_except
    def double_click(
        self, 
        x: int, 
        y: int, 
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey
    ) -> None:
        '''
            Perform a double click with the specified mouse button.

            Parameters:
                x[Required]: Defines the X integer coordinate.

                y[Required]: Defines the Y integer coordinate.

                mouse_button: Define the position of the mouse button, and default is left button.

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with the action, and default is none.  

            Returns:
                None
        '''
        point = _ConvertBaseTypeService.convert_point(x,y)
        button = _ConvertEnumService.convert_mouse_button_enum(MouseButton(mouse_button))
        modifier_key = _ConvertEnumService.convert_modifier_key_enum(ModifierKey(modifier_key))
        self.mouse_driver.MouseDoubleClick(point, button, modifier_key)

    @_ExceptionHandle.try_except
    def up(
        self,
        x: int, 
        y: int, 
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left
    ) -> None:
        '''
            Move the mouse cursor to the X and Y integer coordinates, and release the mouse button back up.

            Parameters:
                x[Required]: Defines the X integer coordinate.

                y[Required]: Defines the Y integer coordinate.

                mouse_button: Define the position of the mouse button, and default is left button.

            Returns:
                None
        '''
        point = _ConvertBaseTypeService.convert_point(x,y)
        button = _ConvertEnumService.convert_mouse_button_enum(MouseButton(mouse_button))
        self.mouse_driver.MouseUp(point, button)

    @_ExceptionHandle.try_except
    def down(
        self,
        x: int, 
        y: int, 
        mouse_button: Literal["left", "middle", "right"] = MouseButton.Left
    ) -> None:
        '''
            Move the mouse cursor to the X and Y integer coordinates, and press the mouse button down.

            Parameters:
                x[Required]: Defines the X integer coordinate.

                y[Required]: Defines the Y integer coordinate.

                mouse_button: Define the position of the mouse button, and default is left button.

            Returns:
                None
        '''
        point = _ConvertBaseTypeService.convert_point(x,y)
        button = _ConvertEnumService.convert_mouse_button_enum(MouseButton(mouse_button))
        self.mouse_driver.MouseDown(point, button)

    @_ExceptionHandle.try_except
    def move(
        self,
        x: int, 
        y: int
    ) -> None:
        '''
            Move the mouse cursor to the X and Y integer coordinates.

            Parameters:
                x[Required]: Defines the X integer coordinate.

                y[Required]: Defines the Y integer coordinate.

            Returns:
                None
        '''
        point = _ConvertBaseTypeService.convert_point(x,y)
        self.mouse_driver.MouseMoveTo(point)

    @_ExceptionHandle.try_except
    def scroll(
        self,
        times = 1,
        modifier_key: Literal["nonekey", "alt", "ctrl", "shift","win"]  = ModifierKey.NoneKey
    ) -> None:
        '''
            Do the mouse scroll wheel.

            Parameters:
                times: An integer number of times to scroll, and default is 1. When the value is greater than zero means scroll up, others means scroll down.

                modifier_key: The modifier key("alt", "ctrl", "shift", "win") to be pressed along with the action, and default is none.  

            Returns:
                None
        '''
        modifier_key = _ConvertEnumService.convert_modifier_key_enum(ModifierKey(modifier_key))
        self.mouse_driver.ScrollWheel(times, modifier_key)    

    def position(
        self
    ) -> Tuple[int,int]:
        '''
            Get the position of the mouse cursor.

            Returns:
                The current X and Y coordinates of the mouse cursor.
        '''
        point = self.mouse_driver.GetMousePosition()
        return (point.X, point.Y)

