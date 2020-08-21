import os

from xml_generator.utils import safe_bool

LDCAD = 'LDCad'
ONLY_NEW: bool = safe_bool(os.environ.get('ONLY_NEW', True))


class ColumnNames:
    PART_NUMBER = 'part_number'
    COLOR_NUMBER = 'color_number'
    COLOR_DESCRIPTION = 'color_description'
    QUANTITY = 'quantity'
    PART_DESCRIPTION = 'part_description'


ColorNumberMapping = {
    'white': 1,
    'light grey': 9,
    'light bluish grey': 86,
    'dark grey': 10,
    'dark bluish grey': 85,
    'black': 11,
    'dark red': 59,
    'red': 5,
    'rust': 27,
    'reddish brown': 88,
    'brown': 8,
    'dark brown': 120,
    'dark tan': 69,
    'tan': 2,
    'medium brown': 91,
    'orange': 4,
    'yellow': 3,
    'lime': 34,
    'olive green': 155,
    'dark green': 80,
    'green': 6,
    'bright green': 36,
    'blue': 7,
    'dark azure': 153,
    'medium azure': 42,
    'trans clear': 12,
    'trans black': 13,
    'trans red': 17,
    'trans neon orange': 18,
    'trans orange': 98
}