# Metadata ETL (Extract-Transform-Load)

The ETL is a service for ingesting metadata the into the central metadata data catalogue (aka **myMDC**).

Basically, the ETL application **extracts** metadata about scientific data, **transforms** the input data into a structure and format that is expected by the Metadata service API and **loads** the final result to myMDC using the provided API/Library.

The ETL design aims to provide a uniform API to integrate with different sources of metadata, such as DAMNIT (https://github.com/European-XFEL/DAMNIT), File system DB, etc.

As a proof-of-concept, the current version implements the extraction component that reads the raw data and extracts metadata from.
In addition, the transform and load components design is flexible enough to ingesting metadata from different sources.

_Repository:_

- https://git.xfel.eu/ITDM/metadata_etl

_Dependencies:_

- metadata_api (https://git.xfel.eu/ITDM/metadata_api)

## Installation

1. Install Python and all required dependencies (eg. Python, poetry, metadata_api, etc.)

   **TBD**

## Usage

1. Run the main application from the command-line with the help argument:

`   poetry run metadata_etl --help`

2. You should get the this output:

```
   usage: MetadataETL [-h] [-b BASE_FOLDER] [-p PROPOSAL] [-r RUN] [-s {proposal,file,run}] [-d DATA] 
          [-g {config,extract,transform,load}] [-v] [files ...]

   Extract metadata from research data and load it into the metadata catalog.

   positional arguments:
   files List of data file(s)

   options:
   -h, --help show this help message and exit
   -b BASE_FOLDER, --base_folder BASE_FOLDER
   Base folder (default: $PWD)
   -p PROPOSAL, --proposal PROPOSAL
   Full proposal number
   -r RUN, --run RUN Run numbers
   -s {proposal,file,run}, --scope {proposal,file,run}
   -d DATA, --data DATA Input file for data and metadata specifications
   -g {config,extract,transform,load}, --stage {config,extract,transform,load}
   -v, --verbose Verbose mode
```
