import flask

from jsrope import Element, Flow, Switch, Int, For, Return, Function, If, true, false, Ajax, Util
from jsrope.util import substitute, negative, jquery3_script

app = flask.Flask(__name__)


@app.route("/")
def main():
    input_box = Element.by_id("name_input")
    p = Element.by_tag("p")
    number = Int("num")
    i = Int("i")
    is_prime = Function("is_prime", {"num": None},
                        Flow(For(substitute(i, 2), (i < (number ** 0.5)).to_int() + 1, i.iadd(1),
                                 Flow(If(negative(number % i), Flow(Return(false))))
                                 ), Return(true)
                             )
                        )
    input_box_event = input_box.on("keyup",
                                   Flow(Ajax("/", {"method": "GET", "data": {"data": input_box.get_value()}},
                                             done=Util.alert(input_box.get_value())),
                                        Switch({is_prime(input_box.get_value().to_int()): p.change_inner_html("prime"),
                                                "else": p.change_inner_html("not prime")})
                                        )).prettify()

    return flask.render_template_string("""
       <input id="name_input" type="text" style="width: 300px; height: 300px">
       <p>inner</p>
       {{ jquery3_url | safe}}
       <script> {{ sc | safe }} </script>""", jquery3_url=jquery3_script, sc=Flow(input_box_event, is_prime.prettify()))


app.run(port=8888)
