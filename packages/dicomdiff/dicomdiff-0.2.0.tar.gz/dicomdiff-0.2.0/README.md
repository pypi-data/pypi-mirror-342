[![CI](https://github.com/ResearchBureau/dicomdiff/actions/workflows/build.yml/badge.svg)](https://github.com/ResearchBureau/dicomdiff/actions/workflows/build.yml)
[![PyPI](https://img.shields.io/pypi/v/dicomdiff)](https://pypi.org/project/dicomdiff/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicomdiff)](https://pypi.org/project/dicomdiff/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Dicomdiff
A Python module that accepts an original DICOM file and its de-identified version as input, and compares them to detect any differences.
## Installation
Install the module with pip

```bash
  pip install dicomdiff
```

## Usage
```python
from dicomdiff.main import compare_dicom_files, print_differences

original_file = "path to original dcm file"
deidentified_file = "path to de-identified dcm file"

result = compare_dicom_files(original_file, deidentified_file) # compare the files
print_differences(result) # print the results
```