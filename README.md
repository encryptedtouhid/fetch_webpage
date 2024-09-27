# Fetch Web Pages CLI

## Build Docker Image
        docker build -t fetch .

## Section 1:  Run the Fetch Website Function
                  docker run fetch <...>
        Example : docker run fetch https://www.google.com https://autify.com

## Section 2: Run the Fetch MetaData Function ( including local mirror )

                  docker run fetch --metadata <...>
        Example : docker run fetch --metadata https://www.google.com https://autify.com

## Output Directory 
        /app/output

## Demo 
![Demo](demo.gif)
