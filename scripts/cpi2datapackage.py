#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
import csv
import json
import zipfile
import urllib.request

# API URI for CPI information from The World Bank (in csv format)
cpi_source = 'https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=csv'
file_name = 'cpi.csv'

def get_csv(source):
    """
    Get the inflation data as a CSV from a ZIP file. Returns a tuple where the
    first item is the header row and the second item is the rows of the CSV.
    """

    response = urllib.request.urlopen(source)
    zip_file = zipfile.ZipFile(io.BytesIO(response.read()))

    csv_filename = next(f for f in zip_file.namelist()
                        if f.startswith('API_'))

    with zip_file.open(csv_filename) as csvfile:
        csvreader = csv.reader(io.TextIOWrapper(csvfile,
                               encoding='ISO-8859-1'))
        next(csvreader)
        next(csvreader)
        updated_date = next(csvreader)
        next(csvreader)
        header = next(csvreader)
        updated_date = re.search(r'(\d{4}-\d{2}-\d{2})', ''.join(updated_date))
        return header, list(csvreader), updated_date.group(1)


def process(headers, rows):
    """
    Process rows from the source CSV and yield rows for the output CSV.
    The output CSV includes country, country code, year, and CPI value.
    """
    yield ['Country', 'Country Code', 'Year', 'CPI']

    for row in rows:
        for (index, cpi) in enumerate(row[2:]):
            if cpi and index > 1:

                # We yield the country and the country code then we lookup
                # the corresponding year in the header (we add 2 since we're
                # enumerating from the third column)
                yield row[:2] + [headers[index + 2], cpi]

def write_csv(rows, filename=None):
    """
    Write rows to a CSV file. Use default dialect for the CSV. If a file name
    is not provided, but source is, the rows will be printed to standard output
    """

    with open('data/' + filename, 'w') as output:
        csvwriter = csv.writer(output)
        for row in rows:
            csvwriter.writerow(row)

def update_datapackage(updated_date):
    """
    Update the data package with the new CPI data.
    """
    with open('datapackage.json', 'r') as f:
        datapackage = json.load(f)
    datapackage['last_updated'] = updated_date
    with open('datapackage.json', 'w') as f:
        json.dump(datapackage, f, indent=2)

if __name__ == '__main__':
    header, row, updated_date = get_csv(cpi_source)
    write_csv(process(header, row), file_name)
    update_datapackage(updated_date)