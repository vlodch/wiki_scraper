# Link to the google doc format document with the scripts details and explanations:
https://github.com/vlodch/wiki_scraper/blob/main/wiki_scrapper_script.py - script with a Web Scraping through the Wikipedia,
https://docs.google.com/document/d/19qD9YLflF8npkKV2q6LH5mJm5_KmdjjM6PIitLHBhOg/edit#heading=h.wudrgb4gcu0u - document with the detailed explanation of each function from the script

# The project was developed with the goal of facilitating potential future extensions. By using Docker and Docker Compose, I demonstrated the opportunity to scale the project with additional dependencies or functionalities. This approach makes it much easier to manage and demonstrate all dependencies, as they are described within the Dockerfile and Docker Compose file, enabling more extensive functionality options. The script allows for quick setup and execution, while the Docker environment ensures consistency and ease of scaling.

# Dockerized WikiScraper

This project scrapes Wikipedia links and saves the results to CSV and JSON files.

## Prerequisites

- Docker
- Docker Compose

## Project Structure
 ```
│
├── app/
│ ├── src/
│ │ ├── init.py
│ │ ├── scraper.py
│ ├── tests/
│ │ ├── init.py
│ │ └── test_scraper.py
│ ├── Dockerfile
│ ├── requirements.txt
├── docker-compose.yml
├── .gitignore
├── README.md
├── output/
 ```

## Functionality Description

### 1. Link Validation
The function `is_valid_wiki_link(url)` checks if a given URL is a valid Wikipedia link. It uses a regular expression to ensure that the link follows the format of a typical Wikipedia page URL.

### 2. Link Scraping
The function `get_wiki_links(url, limit=MAX_LINKS_PER_PAGE)` scrapes a specified number of links from a given Wikipedia page URL. It performs the following steps:
- Initializes sets to track links to be scraped, links already scraped, and links that have been visited.
- Iteratively fetches links from the current URL, ensuring no duplicates and adherence to the specified limit.
- Handles exceptions during HTTP requests to ensure robust scraping.

### 3. Data Storage
The `main` function orchestrates the scraping process, starting from a base Wikipedia URL. It stores the scraped links in both CSV and JSON formats:
- `wiki_links.csv`: Contains all unique links found, with a summary row indicating the total and unique links found.
- `wiki_links.json`: Stores the total and unique links found, along with the list of links in JSON format.

### 4. Unit Testing
The project includes a suite of unit tests located in `app/tests/test_scraper.py` to verify the following:
- Valid and invalid Wikipedia links.
- Correct handling of valid and invalid input numbers.
- Proper functioning of the link scraping mechanism.
- Ensuring no revisiting of links during the scraping process.

## How to Build and Run

1. **Clone the repository:**
   ```sh
   git clone <repository_url>
   cd dockerized_wikiscraper
2. **Build and run the application:**

 ```
docker-compose up --build
 ```
**Run Tests:**
 ```
docker-compose run tests
 ```
**Check Files Generated in the output directory:**
 ```
wiki_links.csv
wiki_links.json
 ```

**Output Examples:**
**For CSV file types**
 ```
Link
https://en.wikipedia.org/wiki/Wikipedia:File_upload_wizard
https://en.wikipedia.org/wiki/Portal:Current_events
https://en.wikipedia.org/wiki/Main_Page
https://en.wikipedia.org/wiki/Special:Random
https://en.wikipedia.org/wiki/Wikipedia:Contents
https://en.wikipedia.org/wiki/Wikipedia:About
https://en.wikipedia.org/wiki/Help:Contents
https://en.wikipedia.org/wiki/Wikipedia:Community_portal
https://en.wikipedia.org/wiki/Special:RecentChanges
https://en.wikipedia.org/wiki/Help:Introduction

Total links found:,10
Unique links found:,10
 ```

**Output Examples:**
**For JSON file types**
 ```
{
    "total_links": 10,
    "unique_links": 10,
    "links": [
        "https://en.wikipedia.org/wiki/Wikipedia:File_upload_wizard",
        "https://en.wikipedia.org/wiki/Portal:Current_events",
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://en.wikipedia.org/wiki/Special:Random",
        "https://en.wikipedia.org/wiki/Wikipedia:Contents",
        "https://en.wikipedia.org/wiki/Wikipedia:About",
        "https://en.wikipedia.org/wiki/Help:Contents",
        "https://en.wikipedia.org/wiki/Wikipedia:Community_portal",
        "https://en.wikipedia.org/wiki/Special:RecentChanges",
        "https://en.wikipedia.org/wiki/Help:Introduction"
    ]
}
 ```
