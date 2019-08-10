# -*- coding: utf-8 -*-

import datetime
import collections

import jsbeautifier

from .util import Escape

element_by_methods = ("css_selector", "id", "tag")


def find_element_by(method, key):
    if method not in element_by_methods:
        raise ValueError("Invalid argument '{}' for 'method' of jsrope.find_element_by".format(method))
    if method == "id":
        return Element("#{}".format(key))
    elif method == "css_selector":
        return Element(key)
    elif method == "tag":
        return Element(key)


def Return(value=None):
    if isinstance(value, JS):
        return Code("return {}".format(value))
    elif value:
        return Code("return {}".format(repr(value)))
    else:
        return Code("return")


def If(condition, flow):
    return Code("if ({}){{{}}}".format(condition, flow))


def For(init="", condition="", after="", flow=""):
    return Code("for({};{};{}){{{}}}".format(init, condition, after, flow))


def While(condition="", flow=""):
    return Code("while({}){{{}}}".format(condition, flow))


class JS:
    def __hash__(self):
        return hash(self)


class Switch(dict, JS):
    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def to_code(self):
        return Code(str(self))

    def __hash__(self):
        return id(self)

    def __str__(self):
        code = ""
        for condition, action in self.items():
            if isinstance(condition, JS):
                condition = condition.to_code()
            if isinstance(action, JS):
                action = action.to_code()
            if not code:
                code += "if ({}){{{}}}".format(condition, action)
            elif condition != "else":
                code += "else if ({}){{{}}}".format(condition, action)
            else:
                code += "else {{{}}}".format(action)
        return code

    def __repr__(self):
        return "{}({})".format(type(self).__name__, dict(self))

    def prettify(self):
        return jsbeautifier.beautify(str(self))


class Code(str, JS):
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

    def _operation(self, operation, *args):
        args = [x.to_code() if isinstance(x, JS) else str(x) for x in args]
        return Code("{}({})".format(operation, ", ".join([self, *args])))

    def _operation_with_operator(self, operation, other):
        if isinstance(other, JS):
            return Code("{} {} {}".format(self, operation, other))
        else:
            return Code("{} {} {}".format(self, operation, repr(other)))

    def __add__(self, other):
        """
        self + other
        """
        return self._operation_with_operator(operation="+", other=other)

    def __sub__(self, other):
        return self._operation_with_operator(operation="-", other=other)

    def __mul__(self, other):
        return self._operation_with_operator(operation="*", other=other)

    def __mod__(self, other):
        return self._operation_with_operator(operation="%", other=other)

    def __pow__(self, power, modulo=None):
        if modulo:
            return self._operation_with_operator("**", power).__mod__(modulo)
        else:
            return self._operation_with_operator("**", power)

    def __truediv__(self, other):
        return self._operation_with_operator(operation="/", other=other)

    def __floordiv__(self, other):
        return self.__truediv__(other=other)._operation("Math.floor")

    def iadd(self, other):
        return self._operation_with_operator(operation="+=", other=other)

    def isub(self, other):
        return self._operation_with_operator(operation="-=", other=other)

    def imul(self, other):
        return self._operation_with_operator(operation="*=", other=other)

    def idiv(self, other):
        return self._operation_with_operator(operation="/=", other=other)

    def ipow(self, other):
        return self._operation_with_operator(operation="**=", other=other)

    def __iadd__(self, other):
        return self._operation_with_operator(operation="+=", other=other)

    def __isub__(self, other):
        return self._operation_with_operator(operation="-=", other=other)

    def __imul__(self, other):
        return self._operation_with_operator(operation="*=", other=other)

    def __idiv__(self, other):
        return self._operation_with_operator(operation="/=", other=other)

    def __ipow__(self, other):
        return self._operation_with_operator(operation="**=", other=other)

    def __eq__(self, other):
        return self._operation_with_operator(operation="===", other=other)

    def __ge__(self, other):
        return self._operation_with_operator(operation=">=", other=other)

    def __le__(self, other):
        return self._operation_with_operator(operation="<=", other=other)

    def __gt__(self, other):
        return self._operation_with_operator(operation=">", other=other)

    def __lt__(self, other):
        return self._operation_with_operator(operation="<", other=other)

    def abstract_eq(self, other):
        return self._operation_with_operator(operation="==", other=other)

    def int(self):
        return self._operation("parseInt")

    def float(self):
        return self._operation("parseFloat")

    def str(self):
        return self._operation("String")

    def __neg__(self):
        return Code("-" + self.to_code())

    def __abs__(self):
        return self._operation("Math.abs")

    def to_code(self):
        return self

    def prettify(self):
        return Code(jsbeautifier.beautify(self.to_code()))

    def __hash__(self):
        return id(self)


class Function(JS):
    def __init__(self, name, arguments, flow):
        assert isinstance(name, str)
        assert isinstance(arguments, collections.abc.Mapping)
        assert isinstance(flow, (Flow, str))

        self.name = name
        self.arguments = arguments
        self.flow = flow

    def __call__(self, *args, **kwargs):
        argument = dict(self.arguments)
        edited = set()

        for k, v in zip(argument.keys(), args):
            argument[k] = v
            edited.add(k)

        for k, v in kwargs.items():
            if k in edited:
                raise TypeError("argument {} is already given".format(k))
            argument[k] = v
            edited.add(k)

        argument_str = ", ".join([v if v is not None else "" for v in argument.values()])

        if self.name:
            return Code("{}({})".format(self.name, argument_str))
        else:
            return Code("({})({})".format(self.to_code(), argument_str))

    def _argument_to_code(self):
        args = []
        for k, v in self.arguments.items():
            if v is None:
                args.append(k)
            else:
                args.append("{}={}".format(k, v))
        return ", ".join(args)

    def to_code(self):
        return Code(str(self))

    def prettify(self):
        return Code(self.to_code().prettify())

    def __str__(self):
        if self.name:
            return "function {}({}) {{{}}}".format(self.name, self._argument_to_code(), self.flow)
        else:
            return "function({}) {{{}}}".format(self._argument_to_code(), self.flow)

    def __repr__(self):
        return "{}({}, {}, {})".format(type(self).__name__, repr(self.name), repr(self.arguments), repr(self.flow))


class Date(JS):
    def __init__(self, dt=None):
        if isinstance(dt, datetime.datetime):
            self.dt = dt
            self.time = dt.timestamp() * 1000

        elif isinstance(dt, (int, float)):
            self.dt = datetime.datetime.utcfromtimestamp(dt / 1000)
            self.time = dt

        else:
            self.dt = None
            self.time = None

    def to_code(self):
        return Code(str(self))

    @classmethod
    def now(cls):
        return Code("Date.now()")

    def __call__(self):
        if self.time:
            return Code("new Date({})".format(self.time))
        else:
            return Code("new Date()")

    def __hash__(self):
        return id(self)

    def __str__(self):
        if self.time:
            return "Date({})".format(self.time)
        else:
            return "Date()"

    def __repr__(self):
        if self.dt:
            return "{}({})".format(type(self).__name__, self.time)
        else:
            return "{}()".format(type(self).__name__)


class Element:
    def __init__(self, selector=""):
        if selector:
            self.element = "$('{}')".format(selector)

    @classmethod
    def by(cls, method, key):
        try:
            elem = cls()
            elem.element = find_element_by(method, key)
            return elem
        except ValueError:
            raise ValueError("Invalid argument '{}' for 'method' of jsrope.Element.by".format(method))

    @classmethod
    def by_id(cls, key):
        elem = cls()
        elem.element = find_element_by("id", key)
        return elem

    @classmethod
    def by_css_selector(cls, key):
        elem = cls()
        elem.element = find_element_by("css_selector", key)
        return elem

    @classmethod
    def by_tag(cls, key):
        elem = cls()
        elem.element = find_element_by("tag", key)
        return elem

    def on(self, event, flow):
        return EventHandler(self, event, flow)

    def _change_attr(self, attr, value):
        if isinstance(value, Code):
            return Code("{}.{}({})".format(self.to_code(), attr, value))
        elif isinstance(value, str):
            return Code("{}.{}('{}')".format(self.to_code(), attr, value.replace("'", "\\'")))

    def _get_attr(self, attr):
        return Code("{}.{}()".format(self.to_code(), attr))

    def change_value(self, value):
        """
        change Element's value to 'value'

        :param value: str
        :return: str
        """
        return self._change_attr(attr="val", value=value)

    def get_value(self):
        """
        get Element's value

        :return: str
        """
        return self._get_attr("val")

    def change_inner_html(self, html):
        """
        change Element's inner_html to 'html'

        :param html: str
        :return: str
        """
        return self._change_attr(attr="html", value=html)

    def get_inner_html(self):
        """
        get Element's inner_html

        :return: str
        """
        return self._get_attr("html")

    def to_code(self):
        return Code(str(self))

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.element))

    def __str__(self):
        return str(self.element)


class Flow(JS):
    def __init__(self, *actions):
        self.events = []
        self.events.extend([*actions])

    def add(self, action):
        """
        add action to Event Handler's job
        :param action: str
        :return: None
        """
        if not isinstance(action, str):
            raise TypeError("action has to be str")
        self.events.append(action)

    def to_code(self):
        return Code(str(self))

    def __hash__(self):
        return id(self)

    def __str__(self):
        return ";".join([e.to_code() if isinstance(e, JS) else e for e in self.events])

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.events))


class EventHandler(JS):
    def __init__(self, element, event, handler):
        self.element = element
        self.event = event
        self.handler = handler

    def to_code(self):
        return Code(str(self))

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return "{}({},{},{})".format(type(self).__name__, repr(self.element), repr(self.event), repr(self.handler))

    def __str__(self):
        return "{}.on('{}',function(e){{{}}})".format(self.element.to_code(), self.event, self.handler.to_code())

    def prettify(self):
        return jsbeautifier.beautify(str(self))


class Ajax(JS):
    def __init__(self, url, settings, done=None, fail=None, always=None, ignore_error=True):
        self.url = url
        assert isinstance(settings, dict)
        self.settings = settings
        self.done = done
        self.fail = fail
        self.always = always
        self.ignore_error = ignore_error

    def parse_setting(self):
        def bool_handler(_k, _v):
            return "{}: {}".format(_k, "true" if _v else "false")

        def str_handler(_k, _v):
            return "{}: {}".format(_k, Escape(_v))

        handler = {"accepts": str_handler, "async": bool_handler, "beforeSend": str_handler,
                   "cache": bool_handler, "contents": str_handler, "contentType": str_handler,
                   "context": str_handler, "converters": False, "crossDomain": bool_handler,
                   "data": str_handler, "dataFilter": str_handler, "dataType": str_handler,
                   "global": bool_handler, "headers": str_handler, "ifModified": bool_handler,
                   "isLocal": bool_handler, "jsonp": str_handler, "jsonpCallback": str_handler,
                   "mimeType": str_handler, "password": str_handler, "processData": bool_handler,
                   "scriptCharset": str_handler, "statusCode": False, "timeout": str_handler,
                   "traditional": bool_handler, "username": str_handler, "xhr": str_handler,
                   "xhrFields": str_handler, "method": str_handler}
        for k, v in self.settings.items():
            if k not in handler and not self.ignore_error:
                raise ValueError("{} for the key of {}.settings is not allowed".format(k, type(self).__name__))
            c_handler = handler[k]
            if c_handler:
                yield c_handler(k, v)
            elif k == "converters":
                yield "converters: {}".format(
                    "{{{}}}".format(", ".join(["{}: {}".format(repr(kk), vv) for kk, vv in v.items()])))
            elif k == "statusCode":
                yield "statusCode: {}".format(str({kk: str(vv) for kk, vv in v.items()}))

    def to_code(self):
        return Code(str(self))

    def __str__(self):
        params = ",".join(self.parse_setting())
        code = """$.ajax({{url: "{}",{}}})""".format(self.url, params)
        if self.done:
            code += ".done({})".format(str(self.done))
        if self.fail:
            code += ".fail({})".format(str(self.fail))
        if self.always:
            code += ".always({})".format(str(self.always))
        return code

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.url)

    def prettify(self):
        return jsbeautifier.beautify(str(self))


class Boolean(Code):
    def __new__(cls, *args, **kwargs):
        return Code.__new__(cls, *args, **kwargs)

    def __bool__(self):
        return True if str(self) == "true" else False


class Console:
    @staticmethod
    def Assert(boolean=""):
        return Code("console.assert({})".format(Escape(boolean)))

    @staticmethod
    def Clear():
        return Code("console.clear()")

    @staticmethod
    def Count():
        return Code("console.count()")

    def Debug(self, obj=""):
        return self.Log(obj)

    @staticmethod
    def Dir(obj=""):
        return Code("console.dir({})".format(Escape(obj)))

    @staticmethod
    def Dirxml(obj=""):
        return Code("console.dirxml({})".format(Escape(obj)))

    @staticmethod
    def Error(e=""):
        return Code("console.error({})".format(Escape(e)))

    @staticmethod
    def Group():
        return Code("console.group()")

    @staticmethod
    def GroupCollapsed():
        return Code("console.groupCollapsed()")

    @staticmethod
    def GroupEnd():
        return Code("console.groupEnd()")

    @staticmethod
    def Info():
        return Code("console.info()")

    @staticmethod
    def Log(obj=""):
        return Code("console.log({})".format(Escape(obj)))

    @staticmethod
    def Profile():
        return Code("console.profile()")

    @staticmethod
    def ProfileEnd():
        return Code("console.profileEnd()")

    @staticmethod
    def Table(obj=""):
        return Code("console.table({})".format(Escape(obj)))

    @staticmethod
    def Time(name=""):
        return Code("console.time({})".format(Escape(name)))

    @staticmethod
    def TimeEnd(name=""):
        return Code("console.timeEnd({})".format(Escape(name)))

    @staticmethod
    def TimeStamp(name=""):
        return Code("console.timeStamp({})".format(Escape(name)))

    @staticmethod
    def Trace():
        return Code("console.trace()")

    @staticmethod
    def Warn(warn=""):
        return Code("console.warn({})".format(Escape(warn)))


class Util:
    @staticmethod
    def Alert(obj=""):
        return Code("alert({})".format(Escape(obj)))

    @staticmethod
    def Confirm(text):
        return Code("confirm({})".format(Escape(text)))


true = Boolean("true")
false = Boolean("false")
