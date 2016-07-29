#!/usr/bin/python

from datetime import datetime

def parseTime(value):
    if value is None:
        return None

    idx = value.index('.')
    return datetime.strptime(value[:idx], '%Y-%m-%dT%H:%M:%S')

def tryCall(fn, arg):
    return None if arg is None else fn(arg)
