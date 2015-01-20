#! /bin/bash

NUM_WAREHOUSES=20
NUM_CLIENTS=8
RAMPUP_TIME=10 # sec
MEASURE_TIME=1200 #sec

cd tpcc-mysql

mysql -u root -p -e "DROP DATABASE IF EXISTS tpcc; CREATE DATABASE tpcc;"
mysql -u root -p tpcc < create_table_memory.sql
mysql -u root -p tpcc < add_fkey_idx.sql

./tpcc_load 127.0.0.1 tpcc root "" $NUM_WAREHOUSES
./tpcc_start -h127.0.0.1 -dtpcc -uroot -w$NUM_WAREHOUSES -c$NUM_CLIENTS -r$RAMPUP_TIME -l$MEASURE_TIME > tpcc-output-memory.log

mysql -u root -p -e "DROP DATABASE IF EXISTS tpcc; CREATE DATABASE tpcc;"
mysql -u root -p tpcc < create_table.sql
mysql -u root -p tpcc < add_fkey_idx.sql

./tpcc_load 127.0.0.1 tpcc root "" $NUM_WAREHOUSES
./tpcc_start -h127.0.0.1 -dtpcc -uroot -w$NUM_WAREHOUSES -c$NUM_CLIENTS -r$RAMPUP_TIME -l$MEASURE_TIME > tpcc-output.log

./tpcc-output-analyze.sh tpcc-output-memory.log > tpcc-memory-data.txt
./tpcc-output-analyze.sh tpcc-output.log > tpcc-data.txt

paste tpcc-data.txt tpcc-memory-data.txt > tpcc-graph-data.txt

./tpcc-graph-build.sh tpcc-graph-data.txt tpcc-graph.jpg

