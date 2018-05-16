import os
import inspect

ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def database_path(data):
    return os.path.join(ROOT, 'database', data)


def chinese_path(data):
    return os.path.join(ROOT, 'database', 'chinese', data)
