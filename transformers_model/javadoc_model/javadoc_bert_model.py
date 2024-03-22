from pydriller import Repository
import re

# def extract_javadocs(file_content):
#     javadoc_pattern = re.compile(r'/\*\*.*?\*/', re.DOTALL)
#     javadocs = javadoc_pattern.findall(file_content)
#     return javadocs
#
# def analyze_repository(repo_path):
#     # Iterate through commits in the repository
#     for commit in Repository(repo_path).traverse_commits():
#         # For each commit, find modified .java files
#         for file in commit.modified_files:
#             if file.filename.endswith('.java'):
#                 # Fetch the file content for this specific commit
#                 file_content = file.source_code
#                 if file_content:
#                     # Extract JavaDocs from the file content
#                     javadocs = extract_javadocs(file_content)
#                     # Here, you can further analyze the extracted JavaDocs
#                     for javadoc in javadocs:
#                         print(f"Commit message: {commit.msg}, Javadoc: {javadoc}")  # Or apply more sophisticated analysis

def analyze_repository(repo_path):
    javadoc_pattern = re.compile(r'/\*\*(.+?)\*/', re.DOTALL)  # Updated regex for capturing JavaDoc
    for commit in Repository(repo_path).traverse_commits():
        for file in commit.modified_files:
            if file.filename.endswith('.java'):
                diffs = file.diff_parsed['added']  # Focus on added lines
                diff_text = "\n".join([line[1] for line in diffs])  # Combine added lines into a single string

                # Check for JavaDoc in the added diff text
                javadocs = javadoc_pattern.findall(diff_text)
                if javadocs:  # If at least one JavaDoc block found
                    for javadoc in javadocs:
                        print(f"Commit message: {commit.msg}, file: {file.filename}, Added Javadoc: {javadoc}")
                else:
                    print(f"Commit message: {commit.msg}, file: {file.filename}, No entire JavaDoc added.")
            elif file.filename.lower() == "readme.md":
                diffs = file.diff_parsed['added']  # Focus on added lines
                diff_text = "\n".join([line[1] for line in diffs])  # Combine added lines into a single string
                print(f"Diff text: {diff_text}")

analyze_repository('https://github.com/ebbanimer/adventofcode')