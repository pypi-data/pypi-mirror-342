from collections.abc import Mapping, Sequence
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL.TiffImagePlugin import IFDRational
from .abstract import ImagePlugin
from ....exceptions import ComponentError, DataNotFound


def _json_safe(obj):
    """Return a structure containing only JSON‑serialisable scalar types,
    no IFDRational, no bytes, and **no NUL characters**."""
    if isinstance(obj, IFDRational):
        return float(obj)

    if isinstance(obj, bytes):
        # bytes -> str *and* strip embedded NULs
        return obj.decode(errors="replace").replace('\x00', '')

    if isinstance(obj, str):
        # Remove NUL chars from normal strings too
        return obj.replace('\x00', '')

    if isinstance(obj, Mapping):
        return {k: _json_safe(v) for k, v in obj.items()}

    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
        return [_json_safe(v) for v in obj]

    return obj


def _make_serialisable(val):
    if isinstance(val, IFDRational):
        return float(val)
    if isinstance(val, bytes):
        return val.decode(errors="replace")
    return val


class EXIFPlugin(ImagePlugin):
    """
    EXIFPlugin is a plugin for extracting EXIF data from images.
    It extends the ImagePlugin class and implements the analyze method to extract EXIF data.
    """
    column_name: str = "exif_data"

    def __init__(self, *args, **kwargs):
        self.extract_geoloc: bool = kwargs.get("extract_geoloc", False)
        super().__init__(*args, **kwargs)

    def convert_to_degrees(self, value):
        try:
            # Handles case where value is tuple of Rational objects
            def to_float(r):
                return float(r.num) / float(r.den) if hasattr(r, "num") else float(r)

            d = to_float(value[0])
            m = to_float(value[1])
            s = to_float(value[2])

            return d + (m / 60.0) + (s / 3600.0)
        except Exception as e:
            print(f"Error converting GPS value to degrees: {e}")
            return None

    def extract_gps_datetime(self, exif: dict):
        gps = exif.get("GPSInfo", {})
        datetime = exif.get("DateTimeOriginal") or exif.get("DateTime")

        latitude = longitude = None

        if gps:
            lat = gps.get("GPSLatitude")
            lat_ref = gps.get("GPSLatitudeRef")
            lon = gps.get("GPSLongitude")
            lon_ref = gps.get("GPSLongitudeRef")

            if lat and lat_ref and lon and lon_ref:
                latitude = self.convert_to_degrees(lat)
                if lat_ref != "N":
                    latitude = -latitude

                longitude = self.convert_to_degrees(lon)
                if lon_ref != "E":
                    longitude = -longitude

        return {
            "datetime": datetime,
            "latitude": latitude,
            "longitude": longitude
        }

    async def extract_exif_data(self, image) -> dict:
        """
        Extract EXIF data from the image file object.

        Args:
            file_obj: The file object containing the image.
        """
        try:
            # Extract EXIF data
            exif_data = image._getexif()
            if not exif_data:
                return

            exif = {}
            gps_info = {}

            for tag, value in exif_data.items():
                # Convert EXIF data to a readable format
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_info[sub_decoded] = value[t]
                    exif["GPSInfo"] = gps_info
                else:
                    exif[decoded] = _make_serialisable(value)
            # Extract GPS datetime if available
            if self.extract_geoloc:
                gps_datetime = self.extract_gps_datetime(exif)
                if gps_datetime:
                    exif['gps_info'] = gps_datetime
            return _json_safe(exif)
        except OSError as e:
            print(f'Error opening image file: {e}')
            raise e
        except (AttributeError, KeyError) as e:
            print(f'Error extracting EXIF data: {e}')
            raise e
        except Exception as e:
            print(f'Fail extracting EXIF data: {e}')
            raise e

    async def analyze(self, image: Image.Image) -> dict:
        """
        Extract EXIF data from the given image.

        :param image: Image Bytes opened with PIL Image.open
        :return: Dictionary containing EXIF data.
        """
        try:
            if image is None:
                return {}
            exif_data = await self.extract_exif_data(image)
            if not exif_data:
                return {}
            return exif_data
        except Exception as e:
            raise ComponentError(
                f"Error in EXIF analysis: {str(e)}"
            ) from e
