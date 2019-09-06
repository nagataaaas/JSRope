# -*- coding: utf-8 -*-

import datetime
import collections

import jsbeautifier

from .util import escape

element_by_methods = ("css_selector", "id", "tag")


class JS:
    """
    The best base class for JavaScript.
    All class that related to JavaScript should inherit this class.
    """

    def __init__(self, code=""):
        self.code = code

    def prettify(self):
        return jsbeautifier.beautify(self.to_code())

    def to_code(self):
        return self.code

    def _operation(self, operation, *args):
        args = [x.__str__() for x in args]
        return self.__class__("{}({})".format(operation, ", ".join([self.to_code(), *args])))

    def _operation_with_operator(self, operation, other):
        return self.__class__("{} {} {}".format(self.to_code(), operation, other))

    def __add__(self, other):
        """
        self + other
        """
        return self._operation_with_operator(operation="+", other=other)

    def __sub__(self, other):
        """
        self - other
        """
        return self._operation_with_operator(operation="-", other=other)

    def __mul__(self, other):
        """
        self * other
        """
        return self._operation_with_operator(operation="*", other=other)

    def __mod__(self, other):
        """
        self % other
        """
        return self._operation_with_operator(operation="%", other=other)

    def __pow__(self, power, modulo=None):
        """
        self ** other
        """
        if modulo:
            return self._operation_with_operator("**", power).__mod__(modulo)
        else:
            return self._operation_with_operator("**", power)

    def __truediv__(self, other):
        """
        self / other
        """
        return self._operation_with_operator(operation="/", other=other)

    def __floordiv__(self, other):
        """
        self // other
        """
        return self.__truediv__(other=other)._operation("Math.floor")

    def iadd(self, other):
        """
        self += other
        """
        return self._operation_with_operator(operation="+=", other=other)

    def isub(self, other):
        """
        self -= other
        """
        return self._operation_with_operator(operation="-=", other=other)

    def imul(self, other):
        """
        self *= other
        """
        return self._operation_with_operator(operation="*=", other=other)

    def idiv(self, other):
        """
        self /= other
        """
        return self._operation_with_operator(operation="/=", other=other)

    def ipow(self, other):
        """
        self **= other
        """
        return self._operation_with_operator(operation="**=", other=other)

    def __iadd__(self, other):
        """
        self += other
        """
        return self._operation_with_operator(operation="+=", other=other)

    def __isub__(self, other):
        """
        self -= other
        """
        return self._operation_with_operator(operation="-=", other=other)

    def __imul__(self, other):
        """
        self *= other
        """
        return self._operation_with_operator(operation="*=", other=other)

    def __idiv__(self, other):
        """
        self /= other
        """
        return self._operation_with_operator(operation="/=", other=other)

    def __ipow__(self, other):
        """
        self **= other
        """
        return self._operation_with_operator(operation="**=", other=other)

    def __eq__(self, other):
        """
        self === other
        """
        return Bool(self._operation_with_operator(operation="===", other=other).to_code(), explicit=False)

    def __ge__(self, other):
        """
        self >= other
        """
        return Bool(self._operation_with_operator(operation=">=", other=other).to_code(), explicit=False)

    def __le__(self, other):
        """
        self <= other
        """
        return Bool(self._operation_with_operator(operation="<=", other=other).to_code(), explicit=False)

    def __gt__(self, other):
        """
        self > other
        """
        return Bool(self._operation_with_operator(operation=">", other=other).to_code(), explicit=False)

    def __lt__(self, other):
        """
        self < other
        """
        return Bool(self._operation_with_operator(operation="<", other=other).to_code(), explicit=False)

    def abstract_eq(self, other):
        """
        self == other
        """
        return Bool(self._operation_with_operator(operation="==", other=other).to_code(), explicit=False)

    def __neg__(self):
        """
        -self
        """
        return self.__class__("-" + self.to_code())

    def __abs__(self):
        """
        abs(self)
        """
        return self._operation("Math.abs")

    def __str__(self):
        """
        Return self.code
        """
        return self.to_code()


class Code(str, JS):
    """
    The main class that express Code of JavaScript.
    Use just like `str`.
    """

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

    def prettify(self):
        return Code(jsbeautifier.beautify(self))

    def to_code(self):
        return self


class Expression(Code):
    def __init__(self, code):
        super().__init__(code=code)


class EventHandler(JS):
    def __init__(self, element, event, handler):
        super().__init__()
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


class BaseJS(JS):
    """
    The base class that express JavaScript Data.

    Attributes
    -------------------------------------------
    code: The code which instance going to have
    explicit: Whether this instance made with explicit type declaration.

    """

    def __init__(self, code="", explicit=False):
        """
        :param code: The code which instance going to have
        :param explicit: Whether this instance made with explicit type declaration.
        """
        super().__init__()
        self.code = Code(code)
        self.explicit = explicit

    def to_int(self):
        """
        Returns jsrope.Int object made with self.code and explicit type declaration
        :return: Int()
        """
        return Int(self._operation("parseInt").to_code(), True)

    def to_str(self):
        """
        Returns jsrope.Str object made with self.code and explicit type declaration
        :return: Int()
        """
        return Str(self._operation("String").to_code(), True)

    def to_float(self):
        """
        Returns jsrope.Float object made with self.code and explicit type declaration
        :return: Int()
        """
        return Float(self._operation("parseFloat").to_code(), True)

    def prettify(self):
        """
        Return prettified self.code
        """
        return Code(jsbeautifier.beautify(self.to_code()))

    def to_code(self):
        return self.code

    def __str__(self):
        """
        Return self.code
        """
        return self.to_code()

    def __hash__(self):
        return id(self.__class__) + self.to_code().__hash__()


class Object(BaseJS):
    def __init__(self, code, explicit=False):
        super().__init__(code=code, explicit=explicit)


class Element(BaseJS):
    def __init__(self, selector=""):
        super().__init__()
        self.is_selector = False
        if selector:
            self.element = "$('{}')".format(selector)
            self.is_selector = True

        self.param = {"class": None, "id": None, "name": None, "content": None, "tag": None}

        self.other_param = None

    @classmethod
    def new(cls, tag, content=None, class_=None, id_=None, name=None, **kwargs):
        assert isinstance(tag, str)
        assert content is None or isinstance(content, str)
        assert class_ is None or isinstance(class_, (str, list, tuple, set))
        assert id_ is None or isinstance(id_, str)
        assert name is None or isinstance(name, str)

        elem = cls()
        elem.param = {"class": None, "id": None, "name": None, "content": None, "tag": None}

        elem.is_selector = False
        elem.param["tag"] = tag
        elem.param["content"] = content
        elem.param["class"] = class_
        elem.param["id"] = id_
        elem.param["name"] = name
        elem.other_param = kwargs

        return elem

    @classmethod
    def by(cls, method, key):
        try:
            elem = cls()
            elem.element = find_element_by(method, key)
            elem.is_selector = True
            return elem
        except ValueError:
            raise ValueError("Invalid argument '{}' for 'method' of jsrope.Element.by".format(method))

    @classmethod
    def by_id(cls, key):
        elem = cls()
        elem.element = find_element_by("id", key)
        elem.is_selector = True
        return elem

    @classmethod
    def by_css_selector(cls, key):
        elem = cls()
        elem.element = find_element_by("css_selector", key)
        elem.is_selector = True
        return elem

    @classmethod
    def by_tag(cls, key):
        elem = cls()
        elem.element = find_element_by("tag", key)
        elem.is_selector = True
        return elem

    def on(self, event, flow):
        return EventHandler(self, event, flow)

    def _change_attr(self, attr, value):
        if isinstance(value, Code):
            return Expression("{}.{}({})".format(self.to_code(), attr, value))
        elif isinstance(value, str):
            return Expression("{}.{}('{}')".format(self.to_code(), attr, value.replace("'", "\\'")))

    def _get_attr(self, attr):
        return Object("{}.{}()".format(self.to_code(), attr))

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

    def serialize(self):
        """
        get Element.serialize()

        :return: str
        """
        return self._get_attr("serialize")

    def to_code(self):
        return Code(str(self))

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.element))

    def generate_tag(self):
        assert self.is_selector is False
        param = self.param.copy()
        tag, _ = param.pop("tag"), param.pop("content")

        if self.param["class"]:
            if isinstance(self.param["class"], str):
                param["class"] = self.param["class"]
            else:
                param["class"] = escape(self.param["class"])
        else:
            param["class"] = None

        for k, v in self.other_param.items():
            param[k] = escape(v)

        for k, v in param.items():
            if isinstance(v, str):
                param[k] = v.replace("\"", "&quot;")
        tag = tag.replace("\"", "&quot;")

        return "<{} {}>".format(tag, " ".join(
            ["{}={}".format(k, v) for k, v in param.items() if v is not None])), "</{}>".format(tag)

    def create_element(self):
        assert self.is_selector is False
        o, e = self.generate_tag()
        content = "" if self.param["content"] is None else self.param["content"]
        return "\"{}\"+{}{}\"{}\"".format(o, content, "+" if content else "", e)

    def append(self, obj):
        return "{}.append({})".format(str(self), escape(obj))

    def __str__(self):
        if self.is_selector:
            return str(self.element)
        else:
            return self.create_element()


def find_element_by(method, key):
    if method not in element_by_methods:
        raise ValueError("Invalid argument '{}' for 'method' of jsrope.find_element_by".format(method))
    if method == "id":
        return Element("#{}".format(key))
    elif method == "css_selector":
        return Element(key)
    elif method == "tag":
        return Element(key)


class Bool(Object):
    """
    The class that express Boolean object.
    """

    def __init__(self, code="", explicit=False):
        super().__init__(code)
        if isinstance(code, (str, BaseJS)):
            if not explicit and code[:1] + code[-1:] != "()" and not code.startswith("Boolean("):
                self.code = Code("({})".format(code))
            else:
                self.code = Code(code)
        else:
            if code:
                self.code = Code("true")
            else:
                self.code = Code("false")

    def negative(self):
        """
        return negative of self
        """
        return self.__neg__()

    def __neg__(self):
        """
        return negative of self
        """
        return Bool("!" + self.to_code(), explicit=False)


class Int(Object):
    """
    The class that express Integer object.
    """

    def __init__(self, code="", explicit=False):
        super().__init__(code, explicit)


class Str(Object):
    """
    The class that express String object.
    """

    def __init__(self, code="", explicit=False):
        super().__init__(code, explicit)

    def __neg__(self):
        return Code("-" + self.to_code())

    def __str__(self):
        if self.explicit:
            return self.to_code()

        else:
            return "'{}'".format(self.to_code())


class Float(Object):
    """
    The class that express Float object.
    """

    def __init__(self, code="", explicit=False):
        super().__init__(code, explicit)


class Return(BaseJS):
    """
    The class for express return expression

    Attributes
    -----------
    code: The JavaScript code
    value: What to return
    """

    def __init__(self, value=None):
        super().__init__()
        self.value = value
        if isinstance(value, JS):
            self.code = Expression("return {}".format(value))
        elif value:
            self.code = Expression("return {}".format(repr(value)))
        else:
            self.code = Expression("return")


class If(JS):
    """
    The class for express if expression

    Attributes
    -----------
    code: The JavaScript code
    condition: condition for if
    flow: What to do if condition was truthy
    """

    def __init__(self, condition, flow):
        super().__init__()
        self.code = Expression("if ({}){{{}}}".format(condition, flow))
        self.condition = condition
        self.flow = flow


class For(JS):
    """
    The class for express for expression

    Attributes
    -----------
    code: The JavaScript code
    init: What to do as initialize
    condition: condition for for
    after: WHat to do after running flow
    flow: What to do if condition was truthy
    """

    def __init__(self, init="", condition="", after="", flow=""):
        super().__init__()
        self.code = Expression("for({};{};{}){{{}}}".format(init, condition, after, flow))
        self.init = init
        self.condition = condition
        self.after = after
        self.flow = flow


class While(JS):
    """
    The class for express while while

    Attributes
    -----------
    code: The JavaScript code
    condition: condition for while
    flow: What to do if condition was truthy
    """

    def __init__(self, condition="", flow=""):
        super().__init__()
        self.code = Expression("while({}){{{}}}".format(condition, flow))


class Switch(dict, JS):
    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def to_code(self):
        return Code(str(self))

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


class Flow(JS):
    def __init__(self, *actions):
        super().__init__()
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

    def prettify(self):
        return Code(self.to_code().prettify())

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.events))


class Function(JS):
    def __init__(self, name, arguments, flow):
        super().__init__()
        assert isinstance(name, str)
        assert isinstance(arguments, collections.abc.Mapping)
        assert isinstance(flow, (Flow, str))

        self.name = name
        self.arguments = arguments
        self.flow = flow
        self.code = self.to_code()

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

        argument_str = ", ".join([str(v) if v is not None else "" for v in argument.values()])

        if self.name:
            return Object("{}({})".format(self.name, argument_str))
        else:
            return Object("({})({})".format(self.to_code(), argument_str))

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


class Ajax(JS):
    def __init__(self, url, settings, done=None, fail=None, always=None, ignore_error=True):
        super().__init__()
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
            return "{}: {}".format(_k, escape(_v))

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


class Date(JS):
    def __init__(self, dt=None):
        super().__init__()
        if isinstance(dt, datetime.datetime):
            self.dt = dt
            self.time = dt.timestamp() * 1000

        elif isinstance(dt, (int, float)):
            self.dt = datetime.datetime.utcfromtimestamp(dt / 1000)
            self.time = dt

        else:
            self.dt = None
            self.time = None
        self.code = self.to_code()

    def to_code(self):
        return Code(str(self))

    @classmethod
    def now(cls):
        return Object("Date.now()")

    def __call__(self):
        if self.time:
            return Object("new Date({})".format(self.time))
        else:
            return Object("new Date()")

    def __str__(self):
        if self.time:
            return "Date({})".format(self.time)
        else:
            return "Date()"

    def prettify(self):
        return Code(self.to_code().prettify())

    def __repr__(self):
        if self.dt:
            return "{}({})".format(type(self).__name__, self.time)
        else:
            return "{}()".format(type(self).__name__)


class Array(list, JS):
    def __new__(cls, *args, **kwargs):
        return list.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(args)

    def __hash__(self):
        return id(self)

    def to_code(self):
        return Code(str(self))

    def __str__(self):
        return "[{}]".format(",".join(list(map(escape, list(self)))))

    def __repr__(self):
        return "{}({})".format(type(self).__name__, list(self.__iter__()))

    def prettify(self):
        return jsbeautifier.beautify(str(self))


class Util:
    @staticmethod
    def alert(obj=""):
        return Expression("alert({})".format(escape(obj)))

    @staticmethod
    def confirm(text):
        return Expression("confirm({})".format(escape(text)))


true = Bool(True)
false = Bool(False)
