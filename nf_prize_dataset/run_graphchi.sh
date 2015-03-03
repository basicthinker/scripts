#!/bin/bash

cleanup() {
  graph=$1
  if [ ! -f "$graph" ]; then
    echo "Error: $graph is not a file!"
    exit -2
  fi
  rm -rf "$graph".*
  rm -f "$graph"_*
}

if [ $# -ne 2 ]; then
  echo "Usage: $0 [GRAPH] [MEM MB]"
  exit -1
fi

graph=$1
mem_mb=$2

for (( i=1; i<=3; ++i ))
do
  cleanup $graph
  sleep 1
  $GRAPHCHI_ROOT/bin/example_apps/matrix_factorization/als_edgefactors file $graph membudget_mb $mem_mb >> als.output.$mem_mb
done

