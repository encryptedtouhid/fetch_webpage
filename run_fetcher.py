import sys
import argparse
from src.fetcher import Fetcher
from src.metadata import Metadata  # Assuming you have a Metadata class


def main(urls, metadata_flag):
    # Loop through each provided URL
    for url in urls:
        if metadata_flag:
            # Call the Metadata analyze function if the flag is set
            metadata = Metadata(url)
            metadata.analyze()  # Assuming this method processes the metadata
            print(f"Successfully analyzed metadata for {url}")
        else:
            fetcher = Fetcher(url)
            html_content = fetcher.fetch()  # Fetch the webpage content
            if html_content:
                print(f"Successfully fetched and saved {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch or analyze web pages.')
    parser.add_argument('urls', nargs='+', help='List of URLs to fetch or analyze.')
    parser.add_argument('--metadata', action='store_true', help='Analyze metadata of the provided URLs.')

    args = parser.parse_args()

    main(args.urls, args.metadata)
