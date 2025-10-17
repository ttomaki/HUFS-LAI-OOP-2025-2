"""
cachekit: simple memory cache package
Provides a basic Cache class for temporary storage.
"""

VERSION = "1.0"


def print_version_info() -> None:
    """Print version information for cachekit."""
    print(f"cachekit version {VERSION}")


class Cache:
    """Simple in-memory cache backed by a dictionary."""

    def __init__(self) -> None:
        """Initialize an empty cache."""
        self._data = {}

    def put(self, key, value) -> None:
        """Store a key-value pair in the cache."""
        self._data[key] = value

    def get(self, key, default=None):
        """Retrieve a value from the cache, returning default if not found."""
        return self._data.get(key, default)

    def __len__(self) -> int:
        """Return the number of items in the cache."""
        return len(self._data)

    def clear(self) -> None:
        """Remove all items from the cache."""
        self._data.clear()


__all__ = ["Cache", "print_version_info", "VERSION"]