# .github/scripts/update_readme.py

import os
from datetime import datetime
from urllib.parse import quote
from collections import defaultdict

def main():
    # Define the posts directory
    posts_directory = 'posts'
    
    # Excluded files
    excluded_files = {'README.md', '.github/scripts/update_readme.py'}
    
    # Dictionary to hold files grouped by modified date
    files_by_date = defaultdict(list)
    
    # Walk through the posts directory
    for root, _, filenames in os.walk(posts_directory):
        for filename in filenames:
            if filename.endswith(('.md', '.pdf')) and filename not in excluded_files:
                filepath = os.path.join(root, filename)
                
                # Relative path to repo root
                relative_path = os.path.relpath(filepath, '.')  # e.g., 'posts/My Post.md'
                relative_path = relative_path.replace('\\', '/')  # For Windows compatibility
                
                # Get the last modified time
                timestamp = os.path.getmtime(filepath)
                modified_datetime = datetime.fromtimestamp(timestamp)
                modified_date_str = modified_datetime.strftime('%Y-%m-%d')
                
                # URL-encode the relative path to handle spaces and special characters
                encoded_path = quote(relative_path)
                
                # Extract the base name without extension for display
                name = os.path.splitext(os.path.basename(filepath))[0]
                
                # Append to the corresponding date group
                files_by_date[modified_date_str].append({
                    'name': name,
                    'path': encoded_path,
                    'modified_datetime': modified_datetime  # For sorting within the group
                })
    
    # Sort the dates in descending order
    sorted_dates = sorted(files_by_date.keys(), reverse=True)
    
    # Generate README.md content
    readme_content = "# Blog Posts\n\n"
    
    for date in sorted_dates:
        readme_content += f"## {date}\n\n"
        
        # Sort the files within the date by modified time descendingly
        sorted_files = sorted(
            files_by_date[date],
            key=lambda x: x['modified_datetime'],
            reverse=True
        )
        
        for file in sorted_files:
            readme_content += f"- [{file['name']}]({file['path']})\n"
        
        readme_content += "\n"  # Add an empty line after each date section
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
