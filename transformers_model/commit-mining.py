from pydriller import Repository
import os

# List of repository URLs
repositories = [
    "https://github.com/greenrobot/greendao",
    "https://github.com/pxb1988/dex2jar",
    "https://github.com/objectbox/objectbox-java",
    "https://github.com/EmmaPesjak/DevAnalyzer"
]


def download_commit_messages(repo_url):
    # Extract the repository name from the URL to use as the filename
    repo_name = repo_url.split('/')[-1]
    # Specify the directory where you want to save the files
    output_directory = "commit_messages"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, f"{repo_name}_commit_messages.txt")
    readme_file_path = os.path.join(output_directory, f"{repo_name}_readme.txt")

    # Open the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # Iterate through all commits of the repository
        for commit in Repository(repo_url).traverse_commits():
            # Write each commit message to the file
            file.write(f"\"{commit.msg}\",\"\"\n")

            for modified_file in commit.modified_files:
                if modified_file.filename.lower() == "readme.md":
                    readme_content = modified_file.source_code

    with open(readme_file_path, 'w', encoding='utf-8') as file:
        if readme_content is not None:
            file.write(readme_content)
        else:
            file.write("No readme content.")

# Loop through the repository URLs
for repo_url in repositories:
    print(f"Downloading commit messages for {repo_url}...")
    download_commit_messages(repo_url)
    print(f"Completed downloading commit messages for {repo_url}.\n")

print("All commit messages have been downloaded.")
