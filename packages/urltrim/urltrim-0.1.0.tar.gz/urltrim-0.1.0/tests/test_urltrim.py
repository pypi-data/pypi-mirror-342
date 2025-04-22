# tests/test_urltrim.py
import unittest
from urltrim import URLTrim

class TestURLTrim(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.example.com/some/very/long/path?query=123"

    def test_default_mode(self):
        link = URLTrim(self.url)
        self.assertEqual(str(link), "example.com/some")
        self.assertEqual(link.get_full_url(), self.url)

    def test_domain_mode(self):
        link = URLTrim(self.url, mode="domain")
        self.assertEqual(str(link), "example.com")

    def test_full_path_mode(self):
        link = URLTrim(self.url, mode="full_path")
        self.assertEqual(str(link), "example.com/some/very/long/path")

    def test_validation_invalid(self):
        with self.assertRaises(ValueError):
            URLTrim("invalid-url", validate=True)

    def test_validation_valid(self):
        link = URLTrim("https://google.com", validate=True)
        self.assertEqual(str(link), "google.com")

    def test_caching(self):
        link1 = URLTrim(self.url, mode="domain")
        link2 = URLTrim(self.url, mode="domain")
        self.assertIs(link1.parsed_url, link2.parsed_url)  # Same object from cache

if __name__ == "__main__":
    unittest.main()