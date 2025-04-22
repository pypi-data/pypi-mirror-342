from enum import Enum


class WindowMode(Enum):
    Auto = "auto"
    TopMost = "topmost"
    NoAction = "noaction"

class ClickType(Enum):
    Click = "click"
    DoubleClick = "double-click"
    Up = "up"
    Down = "down"

class PreAction(Enum):
    SetFocus = "setfocus"
    Click = "click"

class MouseButton(Enum):
    Left = "left"
    Right = "right"
    Middle = "middle"

class Location(Enum):
    Center = "center"
    LeftTop = "left-top"
    LeftBottom = "left-bottom"
    RightTop = "right-top"
    RightBottom = "right-bottom"

class ModifierKey(Enum):
    NoneKey = "nonekey"
    Alt = "alt"
    Ctrl = "ctrl"
    Shift = "shift"
    Win = "win"

class CheckType(Enum):
    Check = "check"
    UnCheck = "uncheck"
    Toggle = "toggle"

class Color(object):
    Black = "#000000"
    Blue = "#0000ff"
    Green = "#008000"
    Orange = "#ffa500"
    Pink = "#ffcocb"
    Purple = "#800080"
    Red = "#ff0000"
    Yellow = "#ffff00"

class WebUserDataMode(Enum):
    Automatic = "automatic"
    Default = "default"
    Custom = "custom"

class InputTextBy(Enum):
    Default = "default"
    SetText = "set-text"
    SendKeyAfterClick = "sendkey-after-click"
    SendKeyAfterFocus = "sendkey-after-focus"

class MouseActionBy(Enum):
    Default = "default"
    MouseEmulation = "mouse-emulation"
    ControlInvocation = "control-invocation"
    DomEventInvocation = "dom-event-invocation"

class ClearTextBy(Enum):
    SetText = "set-text"
    SendHotKey = "send-hotkey"

class ClearHotKey(Enum):    
    CtrlA_Delete = "CAD"
    End_ShiftHome_Delete = "ESHD"
    Home_ShiftEnd_Delete = "HSED"

class ScreenShotMode(Enum):
    Bounds = "bounds"
    Viewport = "viewport"
    Full = "full"

class BrowserType:
    IE = "ie"
    Chrome = "chrome"
    FireFox = "firefox"
    Edge = "edge"

class AutomationTech:
    Uia = "uia"
    Java ="java"
    IE ="ie"
    Chrome = "chrome"
    Firefox = "firefox"
    Sap = "sap"
    Edge = "edge"
    IA = "ia"

class EventTypes:
    ApiCall = 0
    ExceptionReport = 1

class ExtensionStatus:
    NotInstalled = "NotInstalled"
    NeedUpdate = "NeedUpdate"
    Installed = "Installed"    

class By:
    XPath = "xpath"
    CssSelector = "css-selector"