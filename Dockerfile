# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to ensure Python can find modules in src/
ENV PYTHONPATH=/app/src

# Define the output directory environment variable (default is 'output')
ENV OUTPUT_DIR=/app/output
# You can change this to whatever default you prefer

# Make sure the fetcher script is executable
RUN chmod +x run_fetcher.py

# Define a volume for the output directory to persist output files
VOLUME ["/app/output"]

# Use Python to run the script and pass command-line arguments to it
ENTRYPOINT ["python", "./run_fetcher.py"]
