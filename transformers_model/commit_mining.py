from pydriller import Repository
import os
"""
Helper script for mining label data.
"""

# List of repository URLs
repositories = [
    "https://github.com/greenrobot/greendao",
    "https://github.com/objectbox/objectbox-java",
    "https://github.com/Red5/red5-server"
]


def download_commit_messages(repo_url):
    # Extract the repository name from the URL to use as the filename
    repo_name = repo_url.split('/')[-1]
    # Specify the directory where to save the files
    output_directory = "commit_messages"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, f"{repo_name}_commit_messages.txt")
    readme_file_path = os.path.join(output_directory, f"{repo_name}_readme.txt")

    output_directory_files = "file_paths"
    os.makedirs(output_directory_files, exist_ok=True)
    file_paths = os.path.join(output_directory_files, f"{repo_name}_files.txt")

    # Set to store unique file paths
    unique_file_paths = set()

    # Initialize README content
    readme_content = None

    # Open the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # Iterate through all commits of the repository
        for commit in Repository(repo_url).traverse_commits():
            # Write each commit message to the file
            file.write(f"\"{commit.msg}\",\"\"\n")

            # Collect unique file paths
            for modified_file in commit.modified_files:
                unique_file_paths.add(modified_file.new_path)
                if modified_file.filename.lower() == "readme.md":
                    readme_content = modified_file.source_code

    with open(readme_file_path, 'w', encoding='utf-8') as file:
        if readme_content is not None:
            file.write(readme_content)
        else:
            file.write("No readme content.")

    # Write unique file paths to file
    with open(file_paths, 'w', encoding='utf-8') as file:
        for path in unique_file_paths:
            if path is not None:  # Ensure there are no None entries
                file.write(f"\"{path}\",\"\"\n")


# Loop through the repository URLs
for repo_url in repositories:
    print(f"Downloading commit messages for {repo_url}...")
    download_commit_messages(repo_url)
    print(f"Completed downloading commit messages for {repo_url}.\n")

print("All commit messages have been downloaded.")
