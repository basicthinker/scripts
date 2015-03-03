#! /bin/bash

sudo apt-get install -y bzr gnuplot
bzr branch lp:~percona-dev/perconatools/tpcc-mysql

sudo apt-get install -y mysql-server libmysqlclient-dev
sudo cp memory_table.cnf /etc/mysql/conf.d/
sudo service mysql restart

cd tpcc-mysql/
make -C src

sed "s/Engine=InnoDB/Engine=MEMORY/g" create_table.sql > create_table_memory.sql
sed -i "s/ text,/ varchar(2048),/g" create_table_memory.sql
sed "s/ ON / USING BTREE ON /g" add_fkey_idx.sql > add_fkey_idx_memory.sql

