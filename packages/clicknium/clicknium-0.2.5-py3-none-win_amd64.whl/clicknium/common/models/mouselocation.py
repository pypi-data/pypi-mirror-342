from clicknium.common.enums import Location
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else: 
    from typing_extensions import Literal

class MouseLocation:

    def __init__(self, 
    location: Literal["center", "left-top", "left-bottom", "right-top","right-bottom"] = Location.Center, 
    xoffset=0, yoffset=0, xrate=0, yrate=0):
        self.Location = location
        self.Xoffset = xoffset
        self.Yoffset = yoffset
        self.Xrate = xrate
        self.Yrate = yrate