import re

from CJKhyperradicals.dir import database_path


class Decompose:
    def __init__(self):
        self.entries = dict()
        self.super_entries = dict()
        with open(database_path('cjk-decomp.txt')) as f:
            for row in f:
                entry, _, components = re.match('(.+):(.+)\((.*)\)', row).groups()
                comp_list = components.split(',')
                self.entries[entry] = comp_list
                for comp in comp_list:
                    self.super_entries.setdefault(comp, []).append(entry)

    def get_sub(self, char):
        return self.entries.get(char, [])

    def get_super(self, char):
        return self.super_entries.get(char, [])
