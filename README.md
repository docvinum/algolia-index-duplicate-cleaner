# Algolia Custom Duplicate Cleaner

## Overview
This Python script is designed for cleaning up duplicate entries in an Algolia index with enhanced flexibility. It allows users to specify which attributes should be considered when detecting duplicates, offering a tailored approach to maintaining the integrity and relevance of your Algolia data.

## Features
- **Dynamic Attribute Listing**: Automatically lists all attributes present in the records of the specified Algolia index.
- **Custom Duplicate Detection**: Users can specify one or multiple attributes based on which the script identifies duplicates.
- **Interactive Duplicate Review**: Allows users to review the identified duplicates in batches of 10 and decide on their deletion.
- **JSON Backup Option**: Offers an option to save a backup of the current index and identified duplicates in JSON format.
- **Safe Deletion with Confirmation**: Ensures that duplicates are only deleted after user confirmation to prevent accidental data loss.

## Prerequisites
- Python 3.x
- Algolia account and API credentials

## Installation
1. Clone the repository or download the script directly.
2. Ensure Python 3.x is installed on your system.
3. Install the `algoliasearch` Python package if not already installed:
   ```bash
   pip install algoliasearch
   ```

## Usage
Run the script in your Python environment:
```bash
python algolia_clean_duplicate.py
```
Follow the on-screen prompts to enter your Algolia credentials, choose the attributes for duplicate detection, and manage duplicates in your index.

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/your-github-username/algolia-custom-duplicate-cleaner/issues) if you want to contribute.

## License
Distributed under the MIT License. See `LICENSE` for more information.
