from functools import wraps, reduce

import flask

import jsrope


def ajax_handler(ajax, data_name="ajax_data"):
    def _wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "dataType" in ajax.settings and ajax.settings["dataType"] == "script":
                method = "GET"
            elif "type" in ajax.settings:
                method = ajax.settings["type"]
            elif "method" in ajax.settings:
                method = ajax.settings["method"]
            else:
                method = "GET"

            if "data" in ajax.settings:
                data = dig_nest(ajax.settings["data"], method)
                kwargs.update({data_name: data})
            return f(*args, **kwargs)

        return wrapper

    return _wrapper


def dig_nest(target, method):
    keys = list(all_keys(target))
    data = target
    for k, t in keys:
        if len(k) > 1:
            _k = "{}[{}]".format(k[0], "][".join(k[1:]))
        else:
            _k = k[0]
        if t == "array":
            _k = _k + "[]"
            if method == "GET":
                update(data, reduce(lambda x, y: {y: x}, reversed(k), flask.request.args.getlist(_k)))
            else:
                update(data, reduce(lambda x, y: {y: x}, reversed(k), flask.request.form.getlist(_k)))
        else:
            if method == "GET":
                update(data, reduce(lambda x, y: {y: x}, reversed(k), flask.request.args.get(_k)))
            else:
                update(data, reduce(lambda x, y: {y: x}, reversed(k), flask.request.form.get(_k)))
    return data


def all_keys(a, parent=[]):
    for k, v in a.items():
        if isinstance(v, (jsrope.Array, list)):
            yield (parent + [k], "array")
        elif isinstance(v, dict):
            yield from all_keys(v, parent + [k])
        else:
            yield (parent + [k], "other")


def update(dict_base, other):
    for k, v in other.items():
        if isinstance(v, dict) and k in dict_base:
            update(dict_base[k], v)
        else:
            dict_base[k] = v
