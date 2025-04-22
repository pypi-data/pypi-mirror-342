import datetime
import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class ExifStat(IntEnum):
    UnknownErr = 0
    FileNotFound = 1
    Unsupported = 2
    NoExif = 3
    NoDateTime = 4
    InvalidDateTime = 5
    ValidExif = 6


ExifRaw = dict
Goff = int | None | bool


@dataclass
class ExifClass:
    # class MyExif(NamedTuple):
    # File Type                       : JPEG
    # Date/Time Original              : 2020:04:24 12:07:46
    # Create Date                     : 2020:04:24 12:07:46
    # Make                            : samsung
    # Camera Model Name               : SM-G975F
    # Image Size                      : 2944x2208
    # GPS Latitude                    : 32 deg 34' 13.22" N
    # GPS Longitude                   : 34 deg 56' 29.58" E
    ext: str
    backend: str
    dt: datetime.datetime | None = None
    t_org: str | None = None
    t_dig: str | None = None
    t_img: str | None = None

    goff: Goff = None
    goff_dig: Goff = None
    goff_img: Goff = None

    make: str | None = None
    model: str | None = None
    x: int | None = None
    y: int | None = None
    w: int | None = None
    h: int | None = None
    lat: float | None = None
    lon: float | None = None

    # all: dict | None = None

    # @classmethod
    # def is_supported(cls, filename: Path):
    #     return filename.suffix.lower() in ['.jpg', '.jpeg', '.tif', '.tiff']
    def get_exif_kwargs(self, none_value=None):
        return dict(
            make=self.make or none_value,
            model=self.model or none_value,
            x=self.x or none_value,
            y=self.y or none_value,
            w=self.w or none_value,
            h=self.h or none_value,
            lat=self.lat or none_value,
            lon=self.lon or none_value,
        )


makers = {
    'Hewlett-Packard': 'HP',
    'Samsung': 'Samsung',
    'FUJIFILM': 'Fujifilm',
    'FUJI': 'Fujifilm',
    'NIKON': 'Nikon',
    'OLYMPUS': 'Olympus',
}
makers = {str(k).lower(): v for k, v in makers.items()}


def nice_model(model: str) -> str:
    spam_words = ('SAMSUNG-',)
    for spam in spam_words:
        model = model.replace(spam, '')
    return model


def nice_make(make: str) -> str:
    # makes = ['Canon', 'HP', 'NIKON CORPORATION', 'OLYMPUS OPTICAL CO.,LTD', 'Google', 'FUJIFILM', 'SONY',
    # 'Panasonic', 'SAMSUNG', 'samsung', 'MOTOROLA', 'Hewlett-Packard', 'EASTMAN KODAK COMPANY', 'Apple',
    # 'NIKON', 'SANYO Electric Co.,Ltd',
    # 'OLYMPUS_IMAGING_CORP.', 'KONICA MINOLTA', 'LGE', 'PENTAX Corporation', 'OLYMPUS IMAGING CORP.', 'DSCimg',
    # 'CASIO COMPUTER CO.,LTD.', 'Research In Motion', 'Minolta Co., Ltd.', 'Samsung Techwin', 'OLYMPUS CORPORATION',
    # 'Toshiba', 'LG Electronics', 'Nokia', 'Microtek', 'DIGITAL', 'AgfaPhoto GmbH', 'Xiaomi',
    # 'Hewlett-Packard Company', 'Sony Ericsson', 'Zoran Corporation', 'FUJI PHOTO FILM CO., LTD.']

    spam_words = (
        'CORPORATION', 'CO.,LTD', 'CO,', 'LTD', 'EASTMAN', 'COMPANY', 'Electric', 'IMAGING', 'CORP', 'Electronics',
        'COMPUTER', 'PHOTO', 'FILM', 'OPTICAL')

    parts = make.split(sep=' ')
    maker_parts = []
    for part in parts:
        if part not in spam_words:
            nice_part = makers.get(part.lower(), part)
            maker_parts.append(nice_part)
    make = ' '.join(maker_parts)
    return make


def tag_friendly(s: str) -> str:
    return s.replace(' ', '-').replace('_', '-')


def fix_make_model(make: str | None, model: str | None) -> tuple[str | None, str | None]:
    make = fix_make_model_base(make)
    model = fix_make_model_base(model)
    if make:
        make = nice_make(make)
        if model:
            model = nice_make(model)
            model_parts = model.split(' ')
            make_parts = [s.lower() for s in make.split(' ')]
            new_parts = []
            for part in model_parts:
                if part.lower() not in make_parts:
                    new_parts.append(part)
            model = ' '.join(new_parts)
            model = nice_model(model)
    make = tag_friendly(make)
    model = tag_friendly(model)
    return make, model


def filename_friendly(s: str, keep=(' ','.','_','-')) -> str:
    s = "".join(c for c in s if c.isalnum() or c in keep).rstrip()
    return s


def fix_make_model_base(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip().strip('\x00').replace('_', ' ')
    s = filename_friendly(s)
    return s


OrgExifDict = dict[dict[str, Any]]


def exif_dict_decode(d: OrgExifDict):
    for tags in d.values():
        for k, tag in tags.items():
            if isinstance(tag, bytes):
                tags[k] = tag.decode("ascii")


# GPS Latitude                    : 32 deg 33' 56.49" N
# GPS Longitude                   : 34 deg 56' 12.15" E
# ((32, 1), (33, 1), (56494080, 1000000))

def parse_gps(p) -> float | None:
    if not p:
        return None
    d = p[0][0] / p[0][1]
    m = p[1][0] / p[1][1]
    s = p[2][0] / p[2][1]
    dms = d + m / 60 + s / 3600
    return dms


def extract_piexif(path: str, logger: logging.Logger) -> tuple[datetime.datetime | None, Goff]:
    pass

def parse_offset(goff: str, logger: logging.Logger) -> int:
    try:
        goff_len = 6
        if len(goff) >= goff_len:
            sign = 1 if goff[-6] == '+' else -1
            hours = int(goff[-5:-3])
            minutes = int(goff[-2:])
            return sign * (hours * 60 + minutes)
    except Exception as e:
        logger.debug(f"Could not parse offset {goff}: {e}")
    return None

def extract_datetime_utc(date_str: str, logger: logging.Logger) -> tuple[datetime.datetime | None, Goff]:
    dt, goff = None, None
    dt_len = 19
    if len(date_str) >= dt_len:
        if len(date_str) > dt_len:
            goff = date_str[dt_len:]
            date_str = date_str[:dt_len]
        if goff:
            goff = parse_offset(goff, logger)
        dt = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    return dt, goff

def extract_datetime_local(date_str: str, logger: logging.Logger) -> tuple[datetime.datetime | None, Goff]:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), True


def parse_exif_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y:%m:%d %H:%M:%S")

def is_timestamp_valid(s: str) -> bool:
    try:
        datetime.datetime.strptime(s, "%Y:%m:%d %H:%M:%S")
        return True
    except Exception:
        return False


# def exif_parse_datetime(s: str) -> str:
#     obj = datetime.strptime(s, "%Y:%m:%d %H:%M:%S")
#     s = obj.strftime("%Y.%m.%d-%H.%M.%S")
#     return s


# import piexif
# import pyheif
#
# # from exif import Image
# #
# # with open('grand_canyon.jpg', 'rb') as image_file:
# #     my_image = Image(image_file)
# #     my_image.has_exif
# #     my_image.list_all()
#
# exif_dict = piexif.load("foo1.jpg")
# for ifd in ("0th", "Exif", "GPS", "1st"):
#     for tag in exif_dict[ifd]:
#         print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
#
#
#
# # Using a file path:
# heif_file = pyheif.read("IMG_7424.HEIC")
# # Or using bytes directly:
# heif_file = pyheif.read(open("IMG_7424.HEIC", "rb").read())
