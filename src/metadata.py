import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Metadata:
    def __init__(self, url):
        self.url = url
        self.metadata = {
            'site': url,
            'num_links': 0,
            'images': 0,
            'last_fetch': None
        }

    def fetch_html(self):
        """Fetches the HTML content of the page."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")
            return None

    def analyze(self):
        """Analyzes the webpage and extracts metadata."""
        html_content = self.fetch_html()
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            self.extract_metadata(soup)

            # Update last_fetch with the current date and time
            self.metadata['last_fetch'] = datetime.utcnow().strftime('%a %b %d %Y %H:%M UTC')

            # Display the extracted metadata in the required format
            print(f"site: {self.metadata['site']}")
            print(f"num_links: {self.metadata['num_links']}")
            print(f"images: {self.metadata['images']}")
            print(f"last_fetch: {self.metadata['last_fetch']}")

    def extract_metadata(self, soup):
        """Extracts metadata from the BeautifulSoup object."""
        # Count links and images
        self.metadata['num_links'] = len(soup.find_all('a'))
        self.metadata['images'] = len(soup.find_all('img'))
