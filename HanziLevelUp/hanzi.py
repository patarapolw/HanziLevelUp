import regex

from HanziLevelUp.dir import database_path


def generate_hanzi_level_dict():
    entries = dict()
    level = 0
    with open(database_path('hanzi_level.txt')) as f:
        for row in f:
            if regex.match(r'[\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', row):
                level += 1
                for char in row.strip():
                    entries[char] = level

    return entries


hanzi_level_dict = generate_hanzi_level_dict()


def get_hanzi_level(hanzi):
    return hanzi_level_dict.get(hanzi, 0)
