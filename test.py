import flask
from jsrope import Ajax, Function, Element, Flow, Code, Date
from jsrope.flask import ajax_handler

app = flask.Flask(__name__)

input_box = Element.by("id", "name_input")

number = input_box.get_value().to_int()
timestamp = Date.now().get_time()
timestamp.handler = Date.from_timestamp

ajax = Ajax("/data",
            {"method": "POST", "data": {"number": number, "timestamp": timestamp}},
            done=Function("done", {"e": None},
                          Flow(Element.by_tag("ul").append(Element.new("li", Code("e + ' sent'"))))))

input_box_event = input_box.on("keyup", ajax)


@app.route("/", methods=["GET", "POST"])
def main():
    return flask.render_template("index.html", sc=input_box_event.prettify())


@app.route("/data", methods=["GET", "POST"])
@ajax_handler(ajax)
def handler(ajax_data):
    print(ajax_data)
    return str(ajax_data["number"]), 200


app.run(port=8888)
