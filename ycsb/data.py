# Created on Jan 12 2015

import statistics
import math
import os

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"


RESULTS_FILE = 'ycsb-redis.results'

def parse(output):
    run = {}
    for line in output.split('\n'):
        segs = [seg.strip() for seg in line.split(',')]
        if len(segs) < 3:
            continue 
        if segs[1] == 'RunTime(ms)' or segs[1] == 'Throughput(ops/sec)':
            assert segs[0] == '[OVERALL]'
            run[segs[1]] = float(segs[2])
        elif segs[1] == 'AverageLatency(us)':
            run[segs[0].strip('[]') + segs[1]] = float(segs[2])
    assert len(run) >= 3
    return run

def append(results, param, aof, run):
    workload = param['command'] + '-' + os.path.basename(param['workload'])
    if not workload in results:
        results[workload] = {}
    if not aof in results[workload]:
        results[workload][aof] = []
    results[workload][aof].append(run)

def calculate(runs):
    throughputs = []
    for run in runs:
        throughputs.append(run['Throughput(ops/sec)'])
    mean = statistics.mean(throughputs)
    stderr = 0
    if len(throughputs) >= 2:
        stderr = statistics.stdev(throughputs) / math.sqrt(len(runs))
    return [mean, stderr]

