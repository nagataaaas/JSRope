You don't want to write JavaScript? Me, too. But, Let me handle it with Python.
===============================================================================
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/delta114514/JSRope)
```python
import flask

from jsrope import Element, Flow, Switch, Code, For, Return, Function, If, true, false, Ajax, Util
from jsrope.util import substitute, negative

app = flask.Flask(__name__)


@app.route("/")
def main():
    input_box = Element.by_id("name_input")
    p = Element.by_tag("p")
    number = Code("num")
    i = Code("i")
    is_prime = Function("is_prime", {"num": None},
                        Flow(For(substitute(i, 2), i < (number ** 0.5).int() + 1, i.iadd(1),
                                 Flow(If(negative(number % i), Flow(Return(false))))
                                 ), Return(true)
                             )
                        )
    input_box_event = input_box.on("keyup",
                                   Flow(Ajax("/", {"method": "GET", "data": {"data": input_box.get_value()}},
                                        done=Util.alert(input_box.get_value())),
                                        Switch({is_prime(input_box.get_value().int()): p.change_inner_html("prime"),
                                                "else": p.change_inner_html("not prime")})
                                        )).prettify()
    return flask.render_template_string("""
       <input id="name_input" type="text" style="width: 300px; height: 300px">
       <p>inner</p>
       <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
       <script> {{ sc | safe }} </script>""", sc=Flow(input_box_event, is_prime.prettify()))


app.run(port=8888)
```

Then this will return

```html
<html><head></head><body><input id="name_input" type="text" style="width: 300px; height: 300px">
<p>inner</p>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<script>
 $('#name_input').on('keyup', function(e) {
    $.ajax({
        url: "/",
        method: "GET",
        data: {
            'data': $('#name_input').val()
        }
    }).done(alert(parseInt($('#name_input').val())));
    if (is_prime(parseInt($('#name_input').val()))) {
        $('p').html('prime')
    } else {
        $('p').html('not prime')
    }
});
 function is_prime(num) {
    for (let i = 2; i < parseInt(num ** 0.5) + 1; i += 1) {
        if (!(num % i)) {
            return false
        }
    };
    return true
}

</script>
</body></html>
```


Instllation
===========

Install with pip
```
   $ pip install jsrope
```
Basic Usage
=======================

**Don't forget to load `jQuery`.**

You can use `Element` to select element.

You can find element by `id`, `css_selector` or `tag`.

```python
from jsrope import Element

Element.by_id("element_id")  # > $('#element_id')  
                             # Same as Element.by("id", id)
                             
Element.by_css_selector("input.input_numer")  # > $('input.input_numer')  
                                              # Same as Element.by("css_selector", selector)

Element.by_tag("input")  # > $('input')  
                         # Same as Element.by("tag", tag)
```

Others gonna be written in the future.

In End
======
Note this: **Writing code by yourself is always the best way.**

Sorry for my poor English.
I want **you** to join us and send many pull requests about Doc, code, features and more!!
