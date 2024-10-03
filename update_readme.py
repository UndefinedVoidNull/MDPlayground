# update_readme.py

import os
from datetime import datetime

# Define the posts directory
posts_directory = 'posts'

# Excluded files (if any)
excluded_files = {'README.md', 'update_readme.py'}

# Initialize list to hold file info
files = []

# Walk through the posts directory
for root, _, filenames in os.walk(posts_directory):
    for filename in filenames:
        if filename.endswith(('.md', '.pdf')) and filename not in excluded_files:
            filepath = os.path.join(root, filename)
            # Convert to GitHub-friendly path
            filepath = filepath.replace('\\', '/')
            # Get the last modified time
            timestamp = os.path.getmtime(filepath)
            last_modified = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            files.append((filepath, last_modified))

# Sort files by last modified date descending
files.sort(key=lambda x: x[1], reverse=True)

# Generate README.md content
readme_content = "# Blog Posts\n\n"

for file, date in files:
    name = os.path.splitext(os.path.basename(file))[0]
    # Format the link to be relative
    readme_content += f"- [{name}]({file}) - *Last updated: {date}*\n"

# Write to README.md
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)
