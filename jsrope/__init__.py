"""
    Japanera
    -----------

    Easy japanese era tool
    All Information's source is [Wikipedia Page](https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC))
    Powered by [Yamato Nagata](https://twitter.com/514YJ)

    [GitHub](https://github.com/delta114514/Japanera)
    [ReadTheDocs](https://japanera.readthedocs.io/en/latest/)

    :copyright: (c) 2019 by Yamato Nagata.
    :license: MIT.
"""

from .__about__ import __version__

from .jsrope import (Element, find_element_by, Flow, EventHandler, Code, Date, If, Switch, For, Return, While, Function,
                    true, false, Ajax, Boolean, Util)

from .util import Not, substitute, Escape
