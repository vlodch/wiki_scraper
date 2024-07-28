# app/tests/test_scraper.py
import unittest
from app.src.scraper import is_valid_wiki_link, get_wiki_links


class TestWikiScraper(unittest.TestCase):
    def test_valid_wiki_link(self):
        valid_link = "https://en.wikipedia.org/wiki/Main_Page"
        self.assertTrue(is_valid_wiki_link(valid_link))

    def test_invalid_wiki_link(self):
        invalid_link = "https://www.wiki.org/"
        self.assertFalse(is_valid_wiki_link(invalid_link))

    def test_scrape_links(self):
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(links), 10)

    def test_no_revisit_links(self):
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(set(links)), len(links))


if __name__ == "__main__":
    unittest.main()
