import os
import requests
from urllib.parse import urljoin, urlparse
from src.utils import save_html

class Fetcher:
    def __init__(self, url):
        self.url = url
        self.base_url = urljoin(url, '/')

    def fetch(self):
        try:
            # Fetch the webpage content
            response = requests.get(self.url)
            response.raise_for_status()

            # Generate a valid filename by stripping the scheme and replacing any slashes
            domain = self.get_domain()
            filename = f"{domain}.html"

            # Save the HTML content to disk
            save_html(filename, response.text)


            # Download assets
            self.download_assets(response.text, domain)

            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {self.url}: {e}")
            return None

    def get_domain(self):
        # Extract domain from URL
        return urlparse(self.url).netloc.replace("www.", "")  # Remove 'www.' for simplicity

    def download_assets(self, html_content, domain):
        # Create a directory for the domain if it doesn't exist
        os.makedirs(domain, exist_ok=True)

        # Parse the HTML content to find assets
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and download images
        for img in soup.find_all('img'):
            img_url = urljoin(self.base_url, img['src'])
            self.download_file(img_url, domain)

        # Find and download CSS files
        for link in soup.find_all('link', href=True):
            if 'stylesheet' in link.get('rel', []):
                css_url = urljoin(self.base_url, link['href'])
                self.download_file(css_url, domain)

        # Find and download JavaScript files
        for script in soup.find_all('script', src=True):
            js_url = urljoin(self.base_url, script['src'])
            self.download_file(js_url, domain)

    def download_file(self, file_url, domain):
        try:
            response = requests.get(file_url)
            response.raise_for_status()

            # Create a valid filename for the asset
            asset_name = os.path.basename(urlparse(file_url).path)
            file_path = os.path.join(domain, asset_name)

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(f"Saved asset {file_url} to {file_path}")

        except requests.RequestException as e:
            print(f"Failed to download {file_url}: {e}")
import os
import requests
from urllib.parse import urljoin, urlparse
from src.utils import save_html

class Fetcher:
    def __init__(self, url):
        self.url = url
        self.base_url = urljoin(url, '/')

    def fetch(self):
        try:
            # Fetch the webpage content
            response = requests.get(self.url)
            response.raise_for_status()

            # Generate a valid filename by stripping the scheme and replacing any slashes
            domain = self.get_domain()
            filename = f"{domain}.html"

            # Save the HTML content to disk
            save_html(filename, response.text)
            print(f"Saved {self.url} to {filename}")

            # Download assets
            self.download_assets(response.text, domain)

            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {self.url}: {e}")
            return None

    def get_domain(self):
        # Extract domain from URL
        return urlparse(self.url).netloc.replace("www.", "")  # Remove 'www.' for simplicity

    def download_assets(self, html_content, domain):
        # Create a directory for the domain if it doesn't exist
        os.makedirs(domain, exist_ok=True)

        # Parse the HTML content to find assets
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find and download images
        for img in soup.find_all('img'):
            img_url = urljoin(self.base_url, img['src'])
            self.download_file(img_url, domain)

        # Find and download CSS files
        for link in soup.find_all('link', href=True):
            if 'stylesheet' in link.get('rel', []):
                css_url = urljoin(self.base_url, link['href'])
                self.download_file(css_url, domain)

        # Find and download JavaScript files
        for script in soup.find_all('script', src=True):
            js_url = urljoin(self.base_url, script['src'])
            self.download_file(js_url, domain)

    def download_file(self, file_url, domain):
        try:
            response = requests.get(file_url)
            response.raise_for_status()

            # Create a valid filename for the asset
            asset_name = os.path.basename(urlparse(file_url).path)
            file_path = os.path.join(domain, asset_name)

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(response.content)


        except requests.RequestException as e:
            print(f"Failed to download {file_url}: {e}")
