import csv
import json
from app.src.scraper import get_wiki_links, is_valid_wiki_link, WikiScraperError


def main():
    # Input link and validate
    wiki_link = "https://en.wikipedia.org/wiki/Main_Page"
    if not is_valid_wiki_link(wiki_link):
        raise ValueError("Invalid Wikipedia link provided. Please ensure it is a valid Wikipedia link.")

    # Input number of cycles and validate
    n = 2  # For testing purposes, let's use 2 cycles.
    if n < 1 or n > 3:
        raise ValueError("The number must be between 1 and 3.")

    # Initialize data structure
    all_links = set()
    current_links = {wiki_link}
    # Repeat the scraping process for n cycles
    for _ in range(n):
        if not current_links:
            break
        new_links = set()
        # Scrape links for each link in current_links
        for link in current_links:
            new_links.update(get_wiki_links(link))
        all_links.update(new_links)
        current_links = new_links

    # Write results to CSV
    csv_file_path = 'wiki_links.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Link'])
        # Write each link to the CSV file
        for link in all_links:
            writer.writerow([link])
        writer.writerow([])
        writer.writerow(['Total links found:', len(all_links)])
        writer.writerow(['Unique links found:', len(all_links)])

    # Write results to JSON
    json_file_path = 'wiki_links.json'
    with open(json_file_path, 'w') as jsonfile:
        # Dump the results to the JSON file
        json.dump({
            'total_links': len(all_links),
            'unique_links': len(all_links),
            'links': list(all_links)
        }, jsonfile, indent=4)

    print(f"Total links found: {len(all_links)}")
    print(f"Unique links found: {len(all_links)}")
    print(f"Data saved to CSV file: {csv_file_path}")
    print(f"Data saved to JSON file: {json_file_path}")


if __name__ == "__main__":
    main()
