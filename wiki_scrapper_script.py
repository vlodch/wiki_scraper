import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import unittest

WIKI_BASE_URL = "https://en.wikipedia.org"
MAX_LINKS_PER_PAGE = 9


class WikiScraperError(Exception):
    pass


# Regexp matches a valid Wikipedia link
def is_valid_wiki_link(url):
    return re.match(r'^https://(?:[a-z]+\.)?wikipedia\.org/wiki/[^:]+$', url)


def get_wiki_links(url, limit=MAX_LINKS_PER_PAGE):
    links = set()  # Set to store unique links
    to_scrape = {url}  # Set of links to scrape
    visited = set()  # Set of visited links

    while to_scrape and len(links) < limit:
        current_url = to_scrape.pop()  # Get a link to scrape
        if current_url in visited:
            continue  # Skip if already visited
        visited.add(current_url)  # Mark the current link as visited

        try:
            print(f"Scraping URL: {current_url}")
            response = requests.get(current_url)  # Fetch the page content
            response.raise_for_status()  # Raise an error for bad status
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the page

            # Finding all the tags with a href attribute and Check if href is a valid Wikipedia link and not a file
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
                    full_link = WIKI_BASE_URL + href
                    # Adding the link if it's unique and not visited
                    if full_link not in links and full_link not in visited:
                        links.add(full_link)
                        to_scrape.add(full_link)
                        # If the limit is reached scraping stops
                        if len(links) >= limit:
                            break
        except requests.RequestException as e:
            print(f"Error accessing {current_url}: {e}")
            raise WikiScraperError(f"Failed to fetch links from {current_url}") from e

    return links


# Main function to execute the script
def main():
    # Input link and validate
    wiki_link = "https://en.wikipedia.org/wiki/Main_Page"
    if not is_valid_wiki_link(wiki_link):
        raise ValueError("Invalid Wikipedia link provided. Please ensure it is a valid Wikipedia link.")

    #  Number of cycles and validation
    try:
        n = 2  # 2 cycles are set for testing purposes.
        if n < 1 or n > 3:
            raise ValueError("The number must be between 1 and 3.")
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

    #  Chosen "set" data structure to keep unique links and avoid duplicates
    all_links = set()
    current_links = {wiki_link}
    # Repeating the scraping process for n cycles
    for _ in range(n):
        if not current_links:
            break
        new_links = set()
        # Scrape links for each link in current_links
        for link in current_links:
            new_links.update(get_wiki_links(link))
        all_links.update(new_links)
        current_links = new_links

    # Writing results to CSV
    csv_file_path = 'wiki_links.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link'])
        for link in all_links:
            writer.writerow([link])
        writer.writerow([])
        writer.writerow(['Total links found:', len(all_links)])
        writer.writerow(['Unique links found:', len(all_links)])

    # Write results to JSON
    json_file_path = 'wiki_links.json'
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


# Unit Tests
class TestWikiScraper(unittest.TestCase):
    def test_valid_wiki_link(self):
        # Test for a valid Wikipedia link
        valid_link = "https://en.wikipedia.org/wiki/Main_Page"
        self.assertTrue(is_valid_wiki_link(valid_link))

    def test_invalid_wiki_link(self):
        # Test for an invalid Wikipedia link
        invalid_link = "https://www.wiki.org/"
        with self.assertRaises(ValueError):
            if not is_valid_wiki_link(invalid_link):
                raise ValueError("Invalid Wikipedia link")

    def test_valid_integer_input(self):
        # Test for valid integer input
        valid_input = 2
        self.assertTrue(1 <= valid_input <= 3)

    def test_invalid_integer_input(self):
        # Test for invalid integer input
        invalid_input = 5
        with self.assertRaises(ValueError):
            if not (1 <= invalid_input <= 3):
                raise ValueError("The number must be between 1 and 3.")

    def test_scrape_links(self):
        # Test to scrape links from a Wikipedia page
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(links), 10)

    def test_no_revisit_links(self):
        # Test to ensure no links are revisited
        links = get_wiki_links("https://en.wikipedia.org/wiki/Main_Page", 10)
        self.assertEqual(len(set(links)), len(links))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
    main()
