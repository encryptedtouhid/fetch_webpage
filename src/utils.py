import os


def save_html(filename, content):
    # Get the output directory from an environment variable, default to 'output' if not set
    output_dir = os.environ.get('OUTPUT_DIR', 'output')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the full path for the file
    full_path = os.path.join(output_dir, filename)

    # Save the HTML content to the specified file
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"HTML content saved to {full_path}")
