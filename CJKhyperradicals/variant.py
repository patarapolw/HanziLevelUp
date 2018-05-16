import re

from CJKhyperradicals.dir import database_path


class Variant:
    def __init__(self):
        self.entries = dict(self._load(database_path('Unihan_Variants.txt')))

    @staticmethod
    def _load(database):
        with open(database) as f:
            for row in f:
                _ = re.match(r'U\+([0-9A-F]{4,})\t(\w+)\t(.+)\n', row)
                if _ is not None:
                    char, variant_type, variants = _.groups()
                    yield chr(int(char, 16)), [chr(int(item.group(1) , 16))
                                               for item in re.finditer(r'U\+([0-9A-F]{4,})', variants)]
                else:
                    # print(row)
                    pass

    def get(self, character):
        return self.entries.get(character, [])


if __name__ == '__main__':
    print(Variant().entries)
