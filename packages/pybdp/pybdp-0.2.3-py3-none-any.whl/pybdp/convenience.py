from collections import Counter


def find_duplicates(objects):
    counter = Counter([x.id for x in objects])
    duplicates = [item for item, count in counter.items() if count > 1]
    return duplicates
