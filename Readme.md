# WP3 MLIP schema and tools

This repository hosts the blueprints, pipelines, and examples for WP3 MLIP repository.

## Schema
The layout for the database for MLIPs, in excel format is present under the folder `schema`.  

## ETL pipeline
For each database record, there must be a corresponding `canonical_schema.yml file` which will be processed by the ETL pipeline. Users have the option to submit either:

- A `userform.yml` file with the  `vasprun.xml`, or

- A complete `canonical_schema` file.

## Public datasets
These contains filled `canonical_schema.yaml` files for commonly used public datasets:
 
 * MPtraj
 * SAlex
 * OC20

