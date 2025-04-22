import qrcode
import base64
import mimetypes
from PIL import Image
from io import BytesIO
from .utils import validate_color, validate_size
from .exceptions import QRCodeXError

class QRCodeX:
    """Main QR code generator class"""
    
    def __init__(self, 
                 error_correction='H', 
                 box_size=10, 
                 border=4,
                 version=None):
        """
        Initialize QR code generator
        :param error_correction: Error correction level (L, M, Q, H)
        :param box_size: Pixel size of each QR code module
        :param border: Number of border modules
        :param version: QR code version (1-40), None for auto
        """
        self.error_correction = self._parse_error_correction(error_correction)
        self.box_size = validate_size(box_size)
        self.border = validate_size(border)
        self.version = version
        self._qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )

    def _parse_error_correction(self, level):
        """Convert error correction string to qrcode constant"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        if level.upper() not in levels:
            raise QRCodeXError(f"Invalid error correction level: {level}")
        return levels[level.upper()]

    def add_data(self, data, data_type='auto'):
        """
        Add data to QR code with automatic type detection
        Supported types: text, url, image, binary
        """
        if data_type == 'auto':
            data = self._auto_detect_data_type(data)
        else:
            data = self._process_data(data, data_type)
        
        self._qr.add_data(data)
        self._qr.make(fit=True if self.version is None else False)

    def _auto_detect_data_type(self, data):
        """Automatically detect data type"""
        if isinstance(data, bytes):
            return self._process_data(data, 'binary')
        elif data.startswith(('http://', 'https://')):
            return self._process_data(data, 'url')
        elif self._is_image_file(data):
            return self._process_data(data, 'image')
        return self._process_data(data, 'text')

    def _is_image_file(self, data):
        """Check if data is a valid image file path"""
        try:
            Image.open(data)
            return True
        except (IOError, FileNotFoundError):
            return False

    def _process_data(self, data, data_type):
        """Process data based on type"""
        if data_type == 'image':
            return self._image_to_data_uri(data)
        elif data_type == 'binary':
            return base64.b64encode(data).decode()
        return data

    def _image_to_data_uri(self, image_path):
        """Convert image to Data URI"""
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            raise QRCodeXError("Unsupported image format")
        
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        
        return f"data:{mime_type};base64,{encoded}"

    def generate(self, 
                 output, 
                 fill_color='black', 
                 back_color='white', 
                 format='png',
                 **kwargs):
        """
        Generate and save QR code
        :param output: Output file path or BytesIO buffer
        :param fill_color: QR code color
        :param back_color: Background color
        :param format: Output format (png, svg, pdf)
        :param kwargs: Format-specific parameters
        """
        validate_color(fill_color)
        validate_color(back_color)
        
        img = self._qr.make_image(
            fill_color=fill_color,
            back_color=back_color,
            image_factory=self._get_image_factory(format)
        )
        
        if format == 'svg':
            self._save_svg(img, output, **kwargs)
        else:
            img.save(output, format=format.upper(), **kwargs)

    def _get_image_factory(self, format):
        """Get appropriate image factory for format"""
        if format == 'svg':
            from qrcode.image.svg import SvgPathImage
            return SvgPathImage
        return None

    def _save_svg(self, img, output, **kwargs):
        """Handle SVG saving with proper encoding"""
        if isinstance(output, str):
            with open(output, 'w') as f:
                img.save(f)
        else:
            img.save(output)