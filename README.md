## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
pip3 install -r requirements.txt # Depending on your system settings
```

## Script Overview

### Imports

- `requests`: For making HTTP requests to fetch web pages.
- `BeautifulSoup` from `bs4`: For parsing HTML and extracting data.
- `csv`: For writing the extracted data to a CSV file.
- `urljoin` from `urllib.parse`: For constructing absolute URLs.

### Constants

- `BASE_URL`: The base URL of the Tecnoma Help Center's FAQ category page.
- `HEADERS`: HTTP headers to simulate a browser request and avoid being blocked by the website.

### Functions

1. **`fetch_page(url)`**: Fetches the HTML content of a given URL. Returns the HTML text if successful, otherwise prints an error message and returns `None`.

2. **`parse_category_page(html)`**: Parses the category page HTML to extract links to individual question pages. Returns a list of URLs.

3. **`parse_question_page(html)`**: Parses an individual question page HTML to extract links to answer pages. Returns a list of URLs.

4. **`parse_answer_page(html)`**: Parses an answer page HTML to extract the question and answer. Returns a tuple of the question and answer text.

5. **`scrape()`**: Orchestrates the scraping process:
   - Fetches the main category page.
   - Extracts links to individual question pages.
   - Fetches each question page and extracts links to answer pages.
   - Fetches each answer page, extracts the question and answer, and appends them to a list.
   - Writes the collected data to `output.csv` with `question` and `answer` columns.

### Execution

To run the script, simply position yourself in the `src` folder and execute it from the command line:

```bash
python scraper.py
python3 scraper.py  # Depending on your system settings
```

The scraped data will be saved to `output.csv` in the same directory as the script. Be aware that re-launching it is going to overwrite the existing file.

## Notes

- Adjust `HEADERS` and `timeout` values as needed to handle potential rate limiting.

## Troubleshooting

- If you encounter any issues with fetching pages or parsing HTML, check the URL structure and HTML elements of the website, as they may have changed.
