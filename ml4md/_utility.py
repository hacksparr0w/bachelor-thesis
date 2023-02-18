def flatten(outer):
    return [item for inner in outer for item in inner]


def unique(items):
    return list(dict.fromkeys(items))
