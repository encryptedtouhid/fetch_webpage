import sys
import argparse
import requests
from src.fetcher import Fetcher
from src.metadata import Metadata  # Assuming you have a Metadata class


def is_valid_url(url):
    # Simple URL validation (you can expand this with regex if needed)
    return url.startswith("http://") or url.startswith("https://")


def check_internet_connection():
    try:
        # Attempt to connect to a known host to check for internet connectivity
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def is_valid_website(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def fetch_with_retry(fetcher, retries=3):
    for attempt in range(retries):
        try:
            html_content = fetcher.fetch()
            return html_content
        except requests.exceptions.Timeout:
            print(f"Timeout occurred. Attempt {attempt + 1} of {retries}...")
            if attempt == retries - 1:
                print("Failed to fetch the webpage after multiple attempts.")
                return None


def main(urls, metadata_flag):
    if not check_internet_connection():
        print("No internet connection. Please connect to the internet and retry.")
        sys.exit(1)

    # Loop through each provided URL
    for url in urls:
        if not is_valid_url(url):
            print(f"Invalid URL: {url}. Please enter a valid URL.")
            continue  # Skip to the next URL

        if not is_valid_website(url):
            print(f"Website is not valid or not reachable: {url}. Please check the URL and retry.")
            continue  # Skip to the next URL

        if metadata_flag:
            # Call the Metadata analyze function if the flag is set
            metadata = Metadata(url)
            metadata.analyze()  # Assuming this method processes the metadata
            print(f"Successfully analyzed metadata for {url}")
        else:
            fetcher = Fetcher(url)
            html_content = fetch_with_retry(fetcher)
            if html_content:
                print(f"Successfully fetched and saved {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch or analyze web pages.')
    parser.add_argument('urls', nargs='+', help='List of URLs to fetch or analyze.')
    parser.add_argument('--metadata', action='store_true', help='Analyze metadata of the provided URLs.')

    args = parser.parse_args()

    main(args.urls, args.metadata)
