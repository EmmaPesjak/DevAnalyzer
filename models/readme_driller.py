import shutil
import subprocess
from pathlib import Path


class ReadmeDriller:
    def __init__(self):

        self.temp_folder = Path("./readme")

    def clone_and_extract_readme(self, repo_url):
        """
        Clones the repository, checks for a README file in the root, and writes it to a file if found.
        :return: Boolean indicating whether a README was found and written.
        """
        # Create a temporary directory for the repository
        self.temp_folder.mkdir(parents=True, exist_ok=True)

        try:
            # Clone the repository to the temporary directory
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(self.temp_folder)], check=True)

            # Check the root directory of the cloned repository for a README file
            readme_found = False
            for file in self.temp_folder.iterdir():
                if file.name.lower().startswith("readme") and file.is_file():
                    readme_found = True
                    print("hej")
                    # Read the README file and write its contents to a new file
                    readme_content = file.read_text(encoding="utf-8")
                    print(readme_content)
                    with open("README.md", "w", encoding="utf-8") as output_file:
                        output_file.write(readme_content)
                    break
        finally:
            # Remove the temporary directory
            shutil.rmtree(self.temp_folder, ignore_errors=True)

        return readme_found
