# -*- coding: utf-8 -*-
import os

ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)))


def data_path(filename):
    return os.path.join(ROOT, 'data', filename)
