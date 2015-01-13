# Created on Jan 11 2015

__author__ = "Jinglei Ren"
__copyright__ = "Copyright (c) 2015 Jinglei Ren"
__email__ = "jinglei@ren.systems"


def server_args(aof):
    args = ['--save', '""']
    if aof == 'everysec' or aof == 'always':
        args += ['--appendonly', 'yes']
        args += ['--appendfsync', aof]
    else:
        assert aof == 'none'
    return args

def client_args():
    args = ['-p', 'redis.host=localhost']
    args += ['-p', 'redis.port=6379']
    return args

