from pathlib import Path
import subprocess
import requests


class ReadmeGetter:
    def __init__(self):
        self.temp_folder = Path("./temp_readme")

    def get_default_branch_name(self, repo_url):
        # This uses git ls-remote to get references from the remote repo
        result = subprocess.run(['git', 'ls-remote', '--symref', repo_url, 'HEAD'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if 'ref:' in line:
                    # Line format is: ref: refs/heads/main HEAD
                    return line.split()[1].split('/')[-1]
        return None

    def extract_readme(self, repo_url):
        default_branch = self.get_default_branch_name(repo_url)

        if default_branch is None:
            return False  # Return False because we couldn't get the default branch name

        # Correctly form the URL to the README.md file
        url = f"https://raw.githubusercontent.com/{'/'.join(repo_url.split('/')[-2:])}/{default_branch}/README.md"
        response = requests.get(url)
        if response.status_code == 200:
            # Write the content of the README.md to a local file
            with open('support/Downloaded_README.txt', 'w', encoding='utf-8') as file:
                file.write(response.text)
            return True
        else:
            return False
