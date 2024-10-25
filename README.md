<a className="gh-badge" href="https://datahub.io/core/cpi"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Annual Consumer Price Index (CPI) for most countries in the world when it has been measured. The reference year is 2005 (meaning the value of CPI for all countries is 100 and all other CPI values are relative to that year).

## Data

The data comes from [The World Bank](http://data.worldbank.org/indicator/FP.CPI.TOTL) and is collected from 1960 to 2011. There are some values missing from data so users of the data will have to *guess* what should be in the empty slots.

The actual download happens via [The World Bank's API (with csv as the requested format)](http://api.worldbank.org/indicator/FP.CPI.TOTL?format=csv).

## Preparation

It is parsed via the script **cpi2datapackage.py**, located in scripts.

```cli-output
    usage: cpi2datapackage.py [-h] [-o filename] [source]
    
    convert WorldBank CPI data to a data package resource

    positional arguments:
      source                source file to generate output from
    
    optional arguments:
      -h, --help            show this help message and exit
      -o filename, --output filename
                            define output filename
```
                    
## License

This Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/