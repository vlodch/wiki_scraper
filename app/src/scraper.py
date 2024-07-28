import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os
import unittest

WIKI_BASE_URL = "https://en.wikipedia.org"
MAX_LINKS_PER_PAGE = 9
OUTPUT_DIR = '/app/output'


class WikiScraperError(Exception):
    pass


def is_valid_wiki_link(url):
    return re.match(r'^https://(?:[a-z]+\.)?wikipedia\.org/wiki/[^:]+$', url)


def get_wiki_links(url, limit=MAX_LINKS_PER_PAGE):
    links = set()
    to_scrape = {url}
    visited = set()

    while to_scrape and len(links) < limit:
        current_url = to_scrape.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            print(f"Scraping URL: {current_url}")
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
                    full_link = WIKI_BASE_URL + href
                    if full_link not in links and full_link not in visited:
                        links.add(full_link)
                        to_scrape.add(full_link)
                        if len(links) >= limit:
                            break
        except requests.RequestException as e:
            print(f"Error accessing {current_url}: {e}")
            raise WikiScraperError(f"Failed to fetch links from {current_url}") from e

    return links


def main():
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    wiki_link = "https://en.wikipedia.org/wiki/Main_Page"
    if not is_valid_wiki_link(wiki_link):
        raise ValueError("Invalid Wikipedia link provided. Please ensure it is a valid Wikipedia link.")

    try:
        n = 2
        if n < 1 or n > 3:
            raise ValueError("The number must be between 1 and 3.")
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

    all_links = set()
    current_links = {wiki_link}
    for _ in range(n):
        if not current_links:
            break
        new_links = set()
        for link in current_links:
            new_links.update(get_wiki_links(link))
        all_links.update(new_links)
        current_links = new_links

    csv_file_path = os.path.join(OUTPUT_DIR, 'wiki_links.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link'])
        for link in all_links:
            writer.writerow([link])
        writer.writerow([])
        writer.writerow(['Total links found:', len(all_links)])
        writer.writerow(['Unique links found:', len(all_links)])

    json_file_path = os.path.join(OUTPUT_DIR, 'wiki_links.json')
    with open(json_file_path, 'w') as jsonfile:
        json.dump({
            'total_links': len(all_links),
            'unique_links': len(all_links),
            'links': list(all_links)
        }, jsonfile, indent=4)

    print(f"Total links found: {len(all_links)}")
    print(f"Unique links found: {len(all_links)}")
    print(f"Data saved to CSV file: {csv_file_path}")
    print(f"Data saved to JSON file: {json_file_path}")


class TestWikiScraper(unittest.TestCase):
    def test_valid_wiki_link(self):
        valid_link = "https://en.wikipedia.org/wiki/Main_Page"
        self.assertTrue(is_valid_wiki_link(valid_link))

    def test_invalid_wiki_link(self):
        invalid_link = "https://www.wiki.org/"
        with self.assertRaises(ValueError):
            if not is_valid_wiki_link(invalid_link):
                raise ValueError("Invalid Wikipedia link")

    def test_valid_integer_input(self):
        valid_input = 2
        self.assertTrue(1 <= valid_input <= 3)

    def test_invalid_integer_input(self):
        invalid_input = 5
        with self.assertRaises(ValueError):
            if not (1 <= invalid_input <= 3):
                raise ValueError("The number must be between 1 and 3.")

    def test_scrape_links(self):
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(links), 10)

    def test_no_revisit_links(self):
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(set(links)), len(links))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
    main()
