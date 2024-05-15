# DevAnalyzer

This tool is part of a bachelor's thesis written by Emma Pesjak and Ebba Nimér. The DevAnalyzer is a tool for summarizing Java software projects, giving a comprehensive overview of who is doing what and where when inputting a GitHub repository. It utilizes 3 different transformers models for:

- **Summarizing the root README.md.**

- **Classifying Git commit messages into the categories:**
  1. **Adaptive** - Adaptive activities are functional activities and involve making modifications to the software to ensure it remains compatible with new environments. Examples of these are feature additions and test cases.
  2. **Perfective** - Perfective activities encompass modifications aimed at improving the software's overall quality, structure, and efficiency, such as refactoring, renaming, cleaning up redundant segments, and improving algorithms and performance.
  3. **Corrective** - Corrective activities address and correct software problems such as bugs, defects, errors, and faults that negatively impact the system.
  4. **Administrative** - Administrative activities include working on documentation such as README.md files, javadocs, or commenting the code.
  5. **Other** - This activity includes Git operations such as merges and pull requests. It also includes vague and unspecified tasks.

- **Classifying changed files in commits by their file path into the categories:**
  1. **Source Code** - Core application code typically involving back-end (server-side logic, APIs, database interactions) and front-end (user interface, client-side logic).
  2. **Tests** - Code files in a test directory or containing "test".
  3. **Resources** - Assets and other resources (images, stylesheets, etc.).
  4. **Configuration** - Configuration files and scripts (build scripts, manifests, shell scripts).
  5. **Documentation** - Software documentation (README files, package-info, license, notice files).

The DevAnalyzer consists of a Graphical User Interface (GUI) and follows a Model-View-Controller (MVC) architecture. The GUI provides the user the option to enter a URL to a GitHub repository. The repository data is then collected from GitHub with PyDriller, and then stored in a SQLite database. The trained models are loaded from Hugging Face and used for analyzing the Git commit message, README.md, and file path data, and the output is displayed in the user interface with diagrams and summaries. The user can also select a specific contributor to get an overview of their specific contribution.

This repository also contains the `transformers_model` directory, which includes the code for training and fine-tuning the BERT models, producing evaluation loss diagrams, commit mining, and other helpful scripts used in this project. As well as the datasets used during training and the results. For more details, see the Transformers_README.md.