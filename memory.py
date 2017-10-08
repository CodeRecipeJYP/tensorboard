import os

import resource

_proc_status = '/proc/%d/status' % os.getpid()

_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0*1024.0}
firsttime_checkplatform = True

def _VmB(VmKey):
    '''Private.
    '''
    global _proc_status, _scale
     # get pseudo file  /proc/<pid>/status
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0  # non-Linux?
     # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
    i = v.index(VmKey)
    v = v[i:].split(None, 3)  # whitespace
    if len(v) < 3:
        return 0.0  # invalid format?
     # convert Vm value to bytes
    return float(v[1]) * _scale[v[2]]


def memory_in_osx(since=0.0):
    '''Return memory usage in bytes.
    '''
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # return _VmB('VmSize:') - since


def resident(since=0.0):
    '''Return resident memory usage in bytes.
    '''
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    '''Return stack size in bytes.
    '''
    return _VmB('VmStk:') - since


def memory_in_linux():
    return _VmB('VmSize:')


def memory():
    from sys import platform
    global firsttime_checkplatform

    if firsttime_checkplatform:
        print(platform)
        firsttime_checkplatform = False

    if platform == "linux" or platform == "linux2":
        return memory_in_linux()
    elif platform == "darwin":
        return memory_in_osx()


def printMemory():
    memoryusage = memory()
    memoryinmb = memoryusage / 1024 / 1024
    return print("memory:%d mbs" % memoryinmb)