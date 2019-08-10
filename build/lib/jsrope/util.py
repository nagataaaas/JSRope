# -*- coding: utf-8 -*-
import jsrope


def substitute(left, right, define="let"):
    return "{} {} = {}".format(define, left, right)


def Not(statement):
    return type(statement)("!({})".format(statement))


def Escape(obj):
    if isinstance(obj, dict):
        return "{{{}}}".format(", ".join(["{}: {}".format(repr(k), Escape(v)) for k, v in obj.items()]))
    if isinstance(obj, jsrope.Code):
        return str(obj)
    elif isinstance(obj, str):
        return '"{}"'.format(obj.replace('"', r'\"'))
    return str(obj)
