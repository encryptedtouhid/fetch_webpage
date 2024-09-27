import requests
from src.utils import save_html

class Fetcher:
    def __init__(self, url):
        self.url = url

    def fetch(self):
        try:
            # Fetch the webpage content
            response = requests.get(self.url)
            response.raise_for_status()

            # Generate a valid filename by stripping the scheme and replacing any slashes
            domain = self.url.split("//")[-1].split("/")[0]
            filename = domain + ".html"

            # Save the HTML content to disk
            save_html(filename, response.text)
            print(f"Saved {self.url} to {filename}")
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {self.url}: {e}")
            return None
