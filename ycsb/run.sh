#!/bin/bash

sudo sh -c 'echo 512 > /proc/sys/net/core/somaxconn'
sudo sh -c 'sysctl vm.overcommit_memory=1'
sudo sh -c 'echo never > /sys/kernel/mm/transparent_hugepage/enabled'

cd ~/Projects/hdd
pwd
for ((i=0; i<5; ++i)); do
  ~/Projects/scripts/ycsb/eval_redis.py aof=everysec
  sleep 30
done
for ((i=0; i<5; ++i)); do
  ~/Projects/scripts/ycsb/eval_redis.py aof=always
  sleep 30
done

