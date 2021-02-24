# cve_ids_search

## Installation
1. Clone the repository and set up the CVE database from instructions: https://github.com/cve-search/cve-search
2. Move the files from this repository to the cve-search folder
3. Run the script `get_cve_ids.py`

## Requirements
1. python 3.8.5
2. CSV file with two columns - Package name, Version

## Example
`python3 get_cve_ids.py --initial rpm_devs.csv --output result.csv --versions`

#### If you want to just search the packages without versions, omit the `--versions` flag.

`python3 get_cve_ids.py --initial rpm_devs.csv --output result.csv`

#### To filter the found CVE IDs from the results.csv file to the matching versions in the CVE ID run the script `filter_cve_ids_versions.py`. 

`python3 filter_cve_ids_versions.py --file results.csv --initial rpm_devs.csv --output filtered_cve.csv`
