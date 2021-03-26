TPCDS benchmark
===============

Based on [https://github.com/pivotal/gp-performance-testing.git](https://github.com/pivotal/gp-performance-testing.git)

## Generate the data

[https://perf.ci.gpdb.pivotal.io/teams/main/pipelines/data-gen-tpc-ds-1t-master/jobs/generate-data-tpc-ds-1000/builds/10](https://perf.ci.gpdb.pivotal.io/teams/main/pipelines/data-gen-tpc-ds-1t-master/jobs/generate-data-tpc-ds-1000/builds/10)

TPC-DS tools: `gs://gp-perf-framework/test-suites/tpc-ds-tool.zip#1531432561966019`

You can download the tools and repos and the upload to the server where you generate data.

Apply the patch to the script gen_data.sh.

## Create tables and ext-tables

first move data

python3 tpcds.py 

## Load into Greenplum

## Set GUCs

## Run the benchmark