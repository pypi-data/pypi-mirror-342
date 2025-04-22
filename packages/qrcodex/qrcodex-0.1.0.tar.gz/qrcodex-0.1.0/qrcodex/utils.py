import re
from PIL import ImageColor
from .exceptions import QRCodeXError

def validate_color(color):
    """Validate color format"""
    if not (re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color) or 
            color in ImageColor.colormap):
        raise QRCodeXError(f"Invalid color format: {color}")

def validate_size(size):
    """Validate numeric size values"""
    if not isinstance(size, int) or size < 1:
        raise QRCodeXError("Size must be a positive integer")
    return size