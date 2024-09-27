# Fetch Web Pages CLI

## Build Docker Image
        docker build -t fetch_webpage .

## Run the Fetch Website Function
                  docker run fetcher-app <...>
        Example : docker run fetcher-app https://www.google.com https://autify.com

## Run the Fetch MetaData Function

                  docker run fetcher-app --metadata <...>
        Example : docker run fetcher-app --metadata https://www.google.com https://autify.com
