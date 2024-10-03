# .github/scripts/update_readme.py

import os
import subprocess
from datetime import datetime
from urllib.parse import quote
from collections import defaultdict

def get_last_commit_date(filepath):
    """
    Retrieves the last commit date for a given file using git.
    
    Args:
        filepath (str): The relative path to the file.
        
    Returns:
        datetime: The datetime of the last commit.
    """
    try:
        # Execute git log to get the last commit date for the file
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cd', '--date=iso', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        commit_date_str = result.stdout.strip()
        commit_datetime = datetime.strptime(commit_date_str, '%Y-%m-%d %H:%M:%S %z')
        # Return date in YYYY-MM-DD format
        return commit_datetime.date()
    except subprocess.CalledProcessError:
        # If the file has no commits, return today's date
        return datetime.utcnow().date()

def main():
    # Define the posts directory
    posts_directory = 'posts'
    
    # Excluded files (if any)
    excluded_files = {'README.md', '.github/scripts/update_readme.py'}
    
    # Initialize a dictionary to hold files grouped by commit date
    files_by_date = defaultdict(list)
    
    # Walk through the posts directory
    for root, _, filenames in os.walk(posts_directory):
        for filename in filenames:
            if filename.endswith(('.md', '.pdf')) and filename not in excluded_files:
                filepath = os.path.join(root, filename)
                # Convert to GitHub-friendly path
                relative_path = os.path.relpath(filepath, '.')  # Relative to repo root
                relative_path = relative_path.replace('\\', '/')
                
                # Get the last commit date
                commit_date = get_last_commit_date(relative_path)
                commit_date_str = commit_date.strftime('%Y-%m-%d')
                
                # URL-encode the relative path to handle spaces and special characters
                encoded_path = quote(relative_path)
                
                # Extract the base name without extension for display
                name = os.path.splitext(os.path.basename(filepath))[0]
                
                # Append to the corresponding date group with commit time for ordering
                # We'll store the commit datetime to sort later
                files_by_date[commit_date_str].append({
                    'name': name,
                    'path': encoded_path,
                    'commit_datetime': commit_date  # Using date only for grouping
                })
    
    # Sort the dates in descending order
    sorted_dates = sorted(files_by_date.keys(), reverse=True)
    
    # Generate README.md content
    readme_content = "# Blog Posts\n\n"
    
    for date in sorted_dates:
        readme_content += f"## {date}\n\n"
        # Sort the files within the date by commit time descending
        sorted_files = sorted(files_by_date[date], key=lambda x: x['commit_datetime'], reverse=True)
        for file in sorted_files:
            readme_content += f"- [{file['name']}]({file['path']})\n"
        readme_content += "\n"  # Add an empty line after each date section
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
