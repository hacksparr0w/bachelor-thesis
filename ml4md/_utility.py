def flatten(outer):
    return [item for inner in outer for item in inner]


def ls_files(dir):
    return [x for x in dir.glob("**/*") if x.is_file()]


def unique(items):
    return list(dict.fromkeys(items))
