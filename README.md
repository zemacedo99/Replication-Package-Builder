# Replication Package Builder

This Replication Package Builder effectively compiles scientific publications from multiple sources, including Scopus, IEEE Xplore, Engineering Village (Inspec), Science Direct, HAL Open Science, Springer Nature, and the ACM Digital Library. It utilizes Crossref for enhanced data integration.

The package aids in extracting key details like titles, authors, years of publication, venues, and types of venues, as well as providing direct links to the articles.

Moreover, it offers a feature to create a focused research query using specific terms from a CSV file. This solution is instrumental in refining search results by filtering out duplicates and omitting non-English publications. Additionally, the package supports the visual presentation of the data analyzed.

## Prerequisites

### Installing Python

Before you set up this project, you will need to install Python on your system. If you haven't already installed Python, follow these instructions:

#### Windows

1. Visit the [official Python website](https://www.python.org/downloads/windows/).
2. Download the latest version of Python for Windows.
3. Run the installer. Check the box that says "Add Python to PATH" during installation. This will make it easier to run Python from the command line.

#### MacOS

1. Visit the [official Python website](https://www.python.org/downloads/mac-osx/).
2. Download the latest version of Python for macOS.
3. Follow the installation instructions.

#### Linux

Most Linux distributions come with Python pre-installed. If not, you can install Python in your distribution's package manager. For example, on Ubuntu:

```bash
sudo apt update
sudo apt install python3
```

### Installing pip

`pip` is the package installer for Python. It usually comes pre-installed with Python installations. However, if you need to install it:

#### Windows or MacOS

Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer. Open a command prompt from that folder and run:

```bash
python get-pip.py
```

#### Linux

Using your distribution's package manager, you can install pip. For example, on Ubuntu:

```bash
sudo apt install python3-pip
```

## Setup and Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/zemacedo99/Replication-Package.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd Replication-Package
    ```

3. **Virtual Environment Setup (Windows)**

    Using a virtual environment is recommended to avoid package conflicts between projects. If you're on Windows, here's how to set it up:

    1. Create a virtual environment:

        ```bash
        python -m venv myenv
        ```

    2. Activate the virtual environment:

        ```bash
        .\myenv\Scripts\Activate
        ```

    3. When done, deactivate with:
        ```bash
        deactivate
        ```

4. **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Setup API Keys**:
    - Obtain your API keys from:
      - [IEEE Xplore API Provider](https://developer.ieee.org/member/register)
      - [Springer Nature API Provider](https://dev.springernature.com/)
      - [Elsevier API Provider](https://dev.elsevier.com/apikey/manage) *Works for Scopus, Engineering Village (Inspec) and ScienceDirect*
      - *Setting up a key for accessing HAL Open Science and the ACM Digital Library is unnecessary.*

6. **Navigate to the source code**:

    ```bash
    cd src/
    ```

    - Rename `config_template.py` inside the search folder to `config.py`.
    - Open `config.py` and replace placeholders (e.g., `YOUR_SCOPUS_API_KEY_HERE`, `YOUR_IEEE_API_KEY_HERE`, `YOUR_EV_API_KEY_HERE`) with the respective API keys.

   **Note**: The `config.py` file contains sensitive information (your API keys) and is gitignored to ensure it isn't accidentally committed to the repository. Please make sure you don't manually add this file to version control.

7. **Run the Application**:

    ```bash
    python replication_package.py
    ```

8. **Troubleshooting**:
    - Ensure you're using a compatible version of Python and pip. Check using `python --version` and `pip --version`.
    - Consider using a virtual environment like `venv` to avoid package conflicts.
    - If a specific package causes an error, try installing it separately using `pip install <package-name>`.
    - For SSL or proxy issues, try: `pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt`.
    - If all else fails, check the internet connection, ensure [PyPI](https://pypi.org/) is accessible, and look for specific error messages for more detailed guidance.
    - **Institutional Restrictions:** If you cannot run the application due to restrictions from your institution's internet connection or VPN, consider obtaining an institutional token from the API Provider support.

## How to Use the Solution

### Customizing Your Search Queries

- **Modify query_terms.csv:**
  - This CSV file contains categories and terms used to create search queries.
  - Personalize the search strings by editing or adding terms according to your research needs.
  - Ensure that the format of the file remains consistent for seamless processing.

### Processing Retrieved Data

- **Change data_process.py:**
  - This script processes the data fetched from the APIs.
  - It generates individual CSV files for each API with the retrieved information.
  - The script also compiles a final CSV file with filtered results, removing duplicates, non-English articles, and publications after a specified date.
  - You can modify the script to change the filtering criteria based on your requirements.

### Narrowing Down the Search Scope

- **Update venues_to_exclude.txt:**
  - This text file lists the venues (journals, conferences, etc.) excluded from the search.
  - Modify this file to reflect the scope of your literature review.
  - Removing specific venues can help focus the search results more relevantly to your study.

### Validating Search Completeness

- **Update titles_to_validate.txt:**
  - This file should be updated with the titles of papers the solution needs to find.
  - This step ensures the comprehensive search process captures all relevant literature.
  - Regularly updating this file is crucial for maintaining the accuracy and completeness of the research.

## Features

- **Multiple Data Sources Integration:**
  - **Scopus**
  - **IEEE Xplore**
  - **Engineering Village (Inspec)**
  - **Science Direct**
  - **HAL Open Science**
  - **ACM Digital Library via Crossref**
  - **Springer Nature**

- **CSV-based Queries:** The ability to create a research query from a CSV file with terms.
  - **Enhanced Query Flexibility:** Now includes the capability to specify terms to exclude from the search, allowing for more precise and tailored query results.

- **Data Visualization:** After gathering and processing the data, the solution offers functionality for its visualization, providing insights and easy-to-understand graphics.

- **Error Handling:** Gracefully handles potential issues during data retrieval and extraction, ensuring consistent results.

- **Query Validation Process:** Introduces a validation step to verify if all the relevant papers have been identified and included in the search results, enhancing the thoroughness and accuracy of the research.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you want to change. As the project interacts with various data sources, please ensure any modifications don't disrupt the existing integrations.

## Credits and Acknowledgments

If you find this solution useful and decide to use it in your projects, please give appropriate credit to the original authors. We kindly request that you acknowledge the contributions of:

- J. Eduardo Ferreira Ribeiro
- J. Antonio Dantas Macedo

For citation or acknowledgment, please refer to their contributions: *"We want to thank J. Eduardo Ferreira Ribeiro and J. Antonio Dantas Macedo for their substantial contributions in developing and providing this replication package builder."*

Your support in crediting our work helps in promoting open and collaborative development. Thank you for respecting our contributions!
