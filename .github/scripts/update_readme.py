# update_readme.py

import os
from datetime import datetime
from urllib.parse import quote
from collections import defaultdict

# Define the posts directory
posts_directory = 'posts'

# Excluded files (if any)
excluded_files = {'README.md', 'update_readme.py'}

# Initialize a dictionary to hold files grouped by date
files_by_date = defaultdict(list)

# Walk through the posts directory
for root, _, filenames in os.walk(posts_directory):
    for filename in filenames:
        if filename.endswith(('.md', '.pdf')) and filename not in excluded_files:
            filepath = os.path.join(root, filename)
            # Convert to GitHub-friendly path
            relative_path = os.path.relpath(filepath, '.')  # Relative to repo root
            relative_path = relative_path.replace('\\', '/')
            # Get the last modified time
            timestamp = os.path.getmtime(filepath)
            last_modified = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            # URL-encode the relative path to handle spaces and special characters
            encoded_path = quote(relative_path)
            # Extract the base name without extension for display
            name = os.path.splitext(os.path.basename(filepath))[0]
            # Append to the corresponding date group
            files_by_date[last_modified].append((name, encoded_path))

# Sort the dates in descending order
sorted_dates = sorted(files_by_date.keys(), reverse=True)

# Generate README.md content
readme_content = "# Blog Posts\n\n"

for date in sorted_dates:
    readme_content += f"## {date}\n\n"
    for name, path in files_by_date[date]:
        readme_content += f"- [{name}]({path})\n"
    readme_content += "\n"  # Add an empty line after each date section

# Write to README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)
