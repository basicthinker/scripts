#! /usr/bin/env python

from __future__ import print_function
from os import path
from datetime import datetime
import sys
import subprocess
import time

import parameters
import redis_config

PATH_TO_REDIS = '~/Projects/redis/'
PATH_TO_YCSB = '~/Projects/ycsb/'

def usage(main_command):
    print('Usage:', main_command, 'aof=[none, everysec, always]')

results = { }

def parse_result(output):
    for line in output.split('\n'):
        if line.startswith('[OVERALL]'):
            print(line)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].lower().startswith('aof='):
        print(sys.argv[0] + ':', 'Invalid command line args!', file=sys.stderr);
        usage(sys.argv[0])
        exit(-1)

    redis_dir = path.expanduser(PATH_TO_REDIS)
    ycsb_dir = path.expanduser(PATH_TO_YCSB)

    aof = sys.argv[1].lower().split('=')[1]
    time_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log = open('ycsb-redis@' + time_str + '.log', 'a')
    redis = path.join(redis_dir, 'src/redis-server')
    assert path.isfile(redis)
    ycsb = path.join(ycsb_dir, 'bin/ycsb')
    assert path.isfile(ycsb)

    redis_args = [redis] + redis_config.server_args(aof)
    redis_process = subprocess.Popen(redis_args, stdout=log)
    time.sleep(1)
    for param in parameters.full_list(path.join(ycsb_dir, 'workloads')):
        try:
            args = [ycsb, param['command'], 'redis']
            args += redis_config.client_args()
            args += parameters.command_args(param)
            print(args)
            output = subprocess.check_output(args)
            log.write(output)
            parse_result(output)
        except Exception as e:
            print(e)
            break
    redis_process.terminate();

if __name__ == '__main__':
    main()

