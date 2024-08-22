from enum import Enum, auto


# setup selectors such as xpath, accessibility id
class Selector(Enum):
    XPATH = "xpath"
    AID = "accessibility_id"


class XpathType(Enum):
    AID = "accessibility_id"
    XPATH = "xpath"
    NAME = "name"
    CONTAINS = "contains"
    DIRECT_AID = "direct_accessibility_id"
    DIRECT_VALUE = "direct_value"


class ScreenshotPosition(Enum):
    PRE = auto()
    POST = auto()
