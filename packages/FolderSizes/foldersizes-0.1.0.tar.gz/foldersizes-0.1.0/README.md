# FolderSizes Project

## Description
FolderSizes is a Python package that provides a command-line interface for displaying the sizes of directories and files in a human-readable format. It allows users to easily visualize the space usage of their file system.

## Features
- Recursively calculates the total size of directories.
- Displays sizes in both human-readable format and in bytes.
- Optionally includes files in the size listing.
- Sorts entries by size, largest first.

## Installation
To install FolderSizes, you can use pip. First, ensure you have Python and pip installed on your system. Then, run the following command:

```
pip install FolderSizes
```

## Usage
After installation, you can use the `foldersizes` command in your terminal. Here are some examples of how to use it:

1. To display sizes of subdirectories in the current directory:
   ```
   foldersizes
   ```

2. To display sizes in a human-readable format:
   ```
   foldersizes -H
   ```

3. To include files in the listing:
   ```
   foldersizes --files
   ```

4. To sort entries by size, largest first:
   ```
   foldersizes -s
   ```

## Requirements
This package requires the `click` library. It will be installed automatically when you install FolderSizes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Author
Carter Struck

## Acknowledgments
- Thanks to the contributors of the `click` library for making command-line interfaces easier to implement.