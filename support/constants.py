MODE_DARK = "dark"
MODE_LIGHT = "light"
DEFAULT_THEME = "green"  # blue green or dark-blue
WINDOW_TITLE = "DevAnalyzer"
WINDOW_GEOMETRY = "1275x675"
TEXT_COLOR = "#3FA27B"
PADDING = 10
HELP_TEXT = """
        Welcome to DevAnalyzer!

        This tool allows you to analyze the development activities
            within a Git repository.

        Instructions:
        1. Click on 'Select repository' to input the repository URL.
        2. The analysis will begin automatically and display 
            various statistics and visualizations about
            the repository's commit history. Keep in mind 
            that large repositories with many commits
            may take a while to load.
        3. Use the dropdown menu to select specific users and 
            view detailed analysis.

            """
HELP_INFO = "Help - DevAnalyzer"
CAT_TEXT = """
            Git commit messages are categorized into the
            following categories:
                1. Adaptive - Adaptive activities are functional
                   activities and involve making modifications 
                   to the software to ensure it remains compatible 
                   with new environments. Examples of these are 
                   feature additions and test cases.
                2. Perfective - Perfective activities encompass 
                   modifications aimed at improving the software's 
                   overall quality, structure, and efficiency, 
                   such as refactoring, renaming, cleaning up 
                   redundant segments, and improving algorithms 
                   and performance.
                3. Corrective - Corrective activities address 
                   and correct software problems such as bugs, 
                   defects, errors, and faults that negatively 
                   impact the system. 
                4. Administrative - Administrative activities 
                   include working on documentation such as 
                   README.md files, javadocs, or commenting
                   the code.
                5. Other - This activity include Git operations 
                   such as merges and pull requests. It also include 
                   vague and unspecified tasks.

            Changed files are categorized into the
             following categories:
                1. Source Code - Core application code typically 
                   involving back-end (server-side logic, APIs, 
                   database interactions) and front-end (user 
                   interface, client-side logic).
                2. Tests - Code files in a test directory or 
                   containing "test".
                3. Resources - Assets and other resources (images, 
                   stylesheets).
                4. Configuration - Configuration files and scripts 
                   (build scripts, manifests, shell scripts).
                5. Documentation - Software documentation 
                   (README files, package-info, license, notice 
                   files).
                """
CAT_INFO = "Categories - DevAnalyzer"
APP_MODE = "Appearance mode"
EXIT = "Exit"
SELECT_REPO = "Select repository"
SELECT_REPO_TEXT = "No repository is selected, please select one with the 'Select repository' button."
ENTER_REPO = "Enter you repository link:"
REPO = "Repository"
LOADING = "Loading, please wait... Large repositories might take a while."
SELECT_USER = "Select user"
HELP = "Help"
CATEGORIES = "Categories"
NONE = "None"
NO_DATA = "No data available for analysis, please select another repository."
