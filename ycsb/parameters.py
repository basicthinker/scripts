# Created on Jan 11 2015

from os import path

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"


NUM_THREADS = 16
NUM_RECORDS = 2000
NUM_OPERATIONS = 1000

def __single_run(command, workload):
    param = { }
    param['command'] = command
    param['workload'] = workload
    assert path.isfile(workload)
    param['threads'] = str(NUM_THREADS)
    param['records'] = str(NUM_RECORDS)
    param['operations'] = str(NUM_OPERATIONS)
    return param

def full_list(workloads_dir):
    runs = []
    workload = path.join(workloads_dir, 'workload')
    runs.append(__single_run('load', workload + 'a'))
    runs.append(__single_run('run', workload + 'a'))
    runs.append(__single_run('run', workload + 'b'))
    runs.append(__single_run('run', workload + 'c'))
    runs.append(__single_run('run', workload + 'f'))
    runs.append(__single_run('run', workload + 'd'))
    return runs

def command_args(param):
    args = ['-P', param['workload']]
    args += ['-threads', param['threads']]
    args += ['-p',  'recordcount=' + param['records']]
    args += ['-p',  'operationcount=' + param['operations']]
    return args

