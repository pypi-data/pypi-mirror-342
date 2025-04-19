from ._async_cache import acache
from ._async_cache import setup as a_setup
from ._sync_cache import cache, setup

__all__ = ["cache", "setup", "a_setup", "acache"]
