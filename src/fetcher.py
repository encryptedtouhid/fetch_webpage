import os
import requests
from urllib.parse import urljoin, urlparse
from src.utils import save_html
from bs4 import BeautifulSoup

class Fetcher:
    def __init__(self, url):
        self.url = url
        self.base_url = urljoin(url, '/')
        # Set output directory from environment variable, with a fallback to 'output'
        self.output_dir = os.environ.get('OUTPUT_DIR', 'output')

    def fetch(self):
        try:
            # Fetch the webpage content
            response = requests.get(self.url)
            response.raise_for_status()

            # Generate a valid filename by stripping the scheme and replacing any slashes
            domain = self.get_domain()
            filename = f"{domain}.html"

            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)

            # Parse HTML content
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Download assets and replace URLs
            soup = self.download_assets(soup, domain)

            # Save the modified HTML content to disk
            html_path = os.path.join(self.output_dir, filename)
            save_html(html_path, str(soup))  # Save as string to include modified content
            print(f"Saved {self.url} to {html_path}")

            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {self.url}: {e}")
            return None

    def get_domain(self):
        # Extract domain from URL
        return urlparse(self.url).netloc.replace("www.", "")  # Remove 'www.' for simplicity

    def download_assets(self, soup, domain):
        # Create a directory for the domain within the output directory
        domain_dir = os.path.join(self.output_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)

        # Mapping to replace URLs in HTML
        url_map = {}

        # Download images and replace their URLs
        for img in soup.find_all('img'):
            img_url = urljoin(self.base_url, img['src'])
            local_img_path = self.download_file(img_url, domain_dir)
            if local_img_path:
                img['src'] = local_img_path  # Replace URL with local path

        # Download CSS files and replace their URLs
        for link in soup.find_all('link', href=True):
            if 'stylesheet' in link.get('rel', []):
                css_url = urljoin(self.base_url, link['href'])
                local_css_path = self.download_file(css_url, domain_dir)
                if local_css_path:
                    link['href'] = local_css_path  # Replace URL with local path

        # Download JavaScript files and replace their URLs
        for script in soup.find_all('script', src=True):
            js_url = urljoin(self.base_url, script['src'])
            local_js_path = self.download_file(js_url, domain_dir)
            if local_js_path:
                script['src'] = local_js_path  # Replace URL with local path

        return soup

    def download_file(self, file_url, domain_dir):
        try:
            response = requests.get(file_url)
            response.raise_for_status()

            # Create a valid filename for the asset
            asset_name = os.path.basename(urlparse(file_url).path)
            if not asset_name:  # Handle cases where the asset_name might be empty
                asset_name = "index.html"
            file_path = os.path.join(domain_dir, asset_name)

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Return the relative path to be used in HTML
            return os.path.relpath(file_path, self.output_dir)

        except requests.RequestException as e:
            print(f"Failed to download {file_url}: {e}")
            return None
