from urllib.parse import urlparse
import re
from typing import Optional

class URLTrim:
    """A class to simplify long URLs with customizable rules, validation, and caching."""
    
    # Class-level cache to store processed URLs
    _cache = {}

    def __init__(self, url: str, mode: str = "default", validate: bool = True):
        """
        Initialize with a URL, shortening mode, and validation option.
        
        Args:
            url (str): The full URL to trim.
            mode (str): Trimming mode - 'domain' (domain only), 'default' (domain + first path),
                        or 'full_path' (domain + full path).
            validate (bool): Whether to validate the URL before processing.
        """
        self.full_url = url.strip()
        self.mode = mode.lower()
        
        # Validate URL if requested
        if validate and not self._is_valid_url():
            raise ValueError(f"Invalid URL: {self.full_url}")
        
        # Check cache first
        cache_key = (self.full_url, self.mode)
        if cache_key in self._cache:
            self.parsed_url, self.short_url = self._cache[cache_key]
        else:
            self.parsed_url = urlparse(self.full_url)
            self.short_url = self._trim_url()
            self._cache[cache_key] = (self.parsed_url, self.short_url)

    def _is_valid_url(self) -> bool:
        """Validate if the URL is well-formed."""
        regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, self.full_url) is not None

    def _trim_url(self) -> str:
        """Generate a trimmed version of the URL based on the mode."""
        domain = self.parsed_url.netloc
        path = self.parsed_url.path.strip("/") if self.parsed_url.path else ""
        
        if domain.startswith("www."):
            domain = domain[4:]

        if self.mode == "domain":
            return domain
        elif self.mode == "full_path" and path:
            return f"{domain}/{path}"
        elif self.mode == "default" and path:
            first_segment = path.split("/")[0]
            return f"{domain}/{first_segment}"
        return domain

    def get_full_url(self) -> str:
        """Return the original full URL."""
        return self.full_url

    def __str__(self) -> str:
        """Return the trimmed URL when the object is printed."""
        return self.short_url