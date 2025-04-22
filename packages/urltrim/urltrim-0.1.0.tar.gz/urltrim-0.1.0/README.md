# URLTrim

A Python library to trim long URLs in your code while retaining their full functionality.

## Installation

```bash
pip install urltrim
```

from urltrim import URLTrim

url = "https://www.example.com/some/very/long/path?query=123"
link = URLTrim(url) # Default mode: domain + first path segment
print(link) # Outputs: example.com/some
print(link.get_full_url()) # Outputs: the full URL

# Custom modes

link_domain = URLTrim(url, mode="domain") # Domain only
print(link_domain) # Outputs: example.com

link_full = URLTrim(url, mode="full_path") # Full path
print(link_full) # Outputs: example.com/some/very/long/path
