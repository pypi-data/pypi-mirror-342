from enum import Enum


class ORIGIN_VALUES(str, Enum):
    EXISTING = "existing"
    APPENDING = "appending"
    # APPENDED = "appended"  # Uncomment if needed later


class BASIC_TYPE_VALUES(str, Enum):
    FLOAT = "float"
    INT = "int"
    TEXT = "text"
    BOOLEAN = "boolean"
    DATE = "date"
    FILE = "blob"
    JSON = "json"


class MEASURE_VALUES(str, Enum):
    CONSTRAINT = "constraint"
    YDATA = "y-data"


class CONVERSION_VALUES(str, Enum):
    HTML = "html"
    PDF = "pdf"
