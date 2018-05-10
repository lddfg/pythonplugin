# -*- coding: utf-8 -*-
import string


def make_g3(s):
    chars = list(s)
    for idx, char in enumerate(chars):
        if char not in string.punctuation and not char.isspace():
            chars[idx] = 'y'
    return ''.join(chars)


def setup(app):
    app.register_formatter('g3', make_g3)
