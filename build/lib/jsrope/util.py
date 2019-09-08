# -*- coding: utf-8 -*-
import jsrope


def substitute(left, right, define="let"):
    return jsrope.Expression("{} {} = {}".format(define, left, right))


def negative(statement):
    return type(statement)("!({})".format(statement))


def escape(obj):
    if isinstance(obj, dict):
        return "{{{}}}".format(", ".join(["{}: {}".format(repr(k), escape(v)) for k, v in obj.items()]))
    elif isinstance(obj, jsrope.Code):
        return str(obj)
    elif isinstance(obj, str):
        return '"{}"'.format(obj.replace('"', r'\"'))
    elif isinstance(obj, (tuple, set, list)):
        return "[{}]".format(", ".join([escape(x) for x in obj]))
    return str(obj)


jquery3_url = "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"
jquery3_script = """<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>"""

jquery2_url = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"
jquery2_script = """<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>"""
