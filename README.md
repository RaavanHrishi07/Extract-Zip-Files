# Extract ZIP Files

A lightweight and secure Python utility for extracting ZIP archives with input validation, error handling, and protection against path traversal attacks.

## Features

- Extract ZIP archives into a folder named after the archive.
- Choose a custom extraction destination.
- Validate input file paths and ZIP file extensions.
- Detect invalid or corrupted ZIP archives.
- Reject unsafe archive paths, including common directory traversal attempts.
- Automated tests using Python's built-in `unittest` framework.
- No third-party dependencies required.

## Requirements

- Python 3.11 or a compatible Python 3 version.
- Git (optional, for cloning the repository).

## Installation

Clone the repository:

```bash
git clone https://github.com/RaavanHrishi07/Extract-Zip-Files.git
cd Extract-Zip-Files
```

## Usage

### Extract into the default folder

```bash
python extract_zip_files.py -l "archive.zip"
```

The archive will be extracted into a sibling folder named after the ZIP file.

For example, `archive.zip` will be extracted into `archive/`.

### Choose a custom destination

```bash
python extract_zip_files.py -l "archive.zip" -o "output_folder"
```

You can also use the short option:

```bash
python extract_zip_files.py -l "archive.zip" -o "D:/ExtractedFiles"
```

### View command-line help

```bash
python extract_zip_files.py --help
```

## Running Tests

Run the automated test suite from the project directory:

```bash
python -m unittest -v test_extract_zip_files.py
```

The tests cover valid extraction, custom destinations, missing files, invalid ZIP archives, and unsafe paths.

## Project Structure

```text
Extract-Zip-Files/
├── extract_zip_files.py
├── test_extract_zip_files.py
├── README.md
└── .gitignore
```

## Security Note

The utility checks archive member paths before extraction to help prevent directory traversal attacks. As with any archive extraction tool, use trusted archives where possible and keep your Python installation updated.

## Author

**Hrishikesh Sharma**

GitHub: [@RaavanHrishi07](https://github.com/RaavanHrishi07)

## License

No license has been added yet. Contact the author for permission before reusing or distributing this project.