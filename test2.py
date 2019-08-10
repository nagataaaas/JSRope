test = {"w": {"y": {"z": 1}}, "ww": 1, "www": {"yy": 1}}


# test= {"x":2}

def allkeys(a, parent=''):
    for key, value in a.items():
        if not isinstance(value, dict):
            yield parent + key
        if isinstance(value, dict):
            yield from allkeys(value, parent + key + '.')


r = list(allkeys(test))
print(r)
