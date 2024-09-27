# Fetch Web Pages CLI

## Build Docker Image
        docker build -t fetch .

## Run the Fetch Website Function
                  docker run fetch <...>
        Example : docker run fetch https://www.google.com https://autify.com

## Run the Fetch MetaData Function

                  docker run fetch --metadata <...>
        Example : docker run fetch --metadata https://www.google.com https://autify.com

## Output Directory 
        /app/output
