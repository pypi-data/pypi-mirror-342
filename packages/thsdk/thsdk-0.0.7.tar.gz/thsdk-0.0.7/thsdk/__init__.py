from .ths_api import *  # Import everything from ths_api
from .ths_api import __all__ as ths_api_all  # Import __all__ from ths_api

__all__ = (
    *ths_api_all,
    "ThsQuote",
    "ZhuThsQuote",
    "FuThsQuote",
    "InfoThsQuote",
    "BlockThsQuote",
)

# Aliases for compatibility
ThsQuote = THS
ZhuThsQuote = ZhuTHS
FuThsQuote = FuTHS
InfoThsQuote = InfoTHS
BlockThsQuote = BlockTHS

__version__ = '1.0.0'
