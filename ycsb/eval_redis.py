#! /usr/bin/env python3
# Created on Jan 11 2015

from os import path
from datetime import datetime
import ast
import sys
import os
import subprocess
import time
import traceback

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"


import parameters
import redis_config
import data

PATH_TO_REDIS = '~/Projects/redis/'
PATH_TO_YCSB = '~/Projects/ycsb/'

AOF_FILE = 'appendonly.aof'

def usage(main_command):
    print('Usage:', main_command, 'aof=[none, everysec, always]')

def main():
    if len(sys.argv) != 2 or not sys.argv[1].lower().startswith('aof='):
        print(sys.argv[0] + ':', 'Invalid command line args!', file=sys.stderr);
        usage(sys.argv[0])
        exit(-1)

    redis_dir = path.expanduser(PATH_TO_REDIS)
    ycsb_dir = path.expanduser(PATH_TO_YCSB)

    aof = sys.argv[1].lower().split('=')[1]

    time_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log_file = open('ycsb-redis@' + time_str + '.log', 'ab')

    results = { }
    if path.isfile(data.RESULTS_FILE):
        existing = open(data.RESULTS_FILE, 'r')
        lines = existing.read()
        if len(lines) > 0:
            results = ast.literal_eval(lines)
        existing.close()

    redis = path.join(redis_dir, 'src/redis-server')
    assert path.isfile(redis)
    ycsb = path.join(ycsb_dir, 'bin/ycsb')
    assert path.isfile(ycsb)

    redis_args = [redis] + redis_config.server_args(aof)
    redis_process = subprocess.Popen(redis_args, stdout=log_file)
    time.sleep(1)
    for param in parameters.full_list(path.join(ycsb_dir, 'workloads')):
        try:
            args = [ycsb, param['command'], 'redis']
            args += redis_config.client_args()
            args += parameters.command_args(param)
            output = subprocess.check_output(args)
            log_file.write(output)
            run_result = data.parse(output.decode('UTF-8'))
            data.append(results, param, aof, run_result)
        except Exception as e:
            print(traceback.format_exc())
            break
    redis_process.terminate();
    if aof != 'none':
        assert path.isfile(AOF_FILE)
        size = path.getsize(AOF_FILE)
        log_file.write(bytes(AOF_FILE + ' size: ' + str(size), 'UTF-8'))
        os.remove(AOF_FILE)

    results_file = open(data.RESULTS_FILE, 'w')
    results_file.write(str(results))
    results_file.close()

if __name__ == '__main__':
    main()

