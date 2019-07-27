import flask

from jsrope import Element, Flow, Switch, Code, For, Return, Function, If, true, false, Ajax, Util
from jsrope.util import substitute, Not

app = flask.Flask(__name__)


@app.route("/")
def main():
    input_box = Element.by("id", "name_input")
    p = Element.by("tag", "p")
    number = Code("num")
    i = Code("i")
    is_prime = Function("is_prime", {"num": None},
                        Flow(For(substitute(i, 2), i < (number ** 0.5).int() + 1, i.iadd(1),
                                 Flow(If(Not(number % i), Flow(Return(false))))
                                 ), Return(true)
                             )
                        )
    input_box_event = input_box.on("keyup",
                                   Flow(Ajax("/", {"method": "GET", "data": {"data": input_box.get_value()}},
                                        done=Flow(Util.Alert(input_box.get_value().int()))),
                                        Switch({is_prime(input_box.get_value().int()): p.change_inner_html("prime"),
                                                "else": p.change_inner_html("not prime")})
                                        )).prettify()
    return flask.render_template("index.html", sc=Flow(input_box_event, is_prime.prettify()))


app.run(port=8888)
