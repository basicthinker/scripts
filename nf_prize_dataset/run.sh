#!/bin/bash

dirs=(./tmpfs ./f2fs ./ext4 ./hdd)
mbs="256 512 1024 2048"

for dir in ${dirs[@]}; do
  cur_dir=`pwd`
  cd $dir
  for mb in $mbs; do
    ~/Projects/scripts/nf_prize_dataset/run_graphchi.sh nf_prize_dataset.mm $mb
  done
  cd $cur_dir
done

