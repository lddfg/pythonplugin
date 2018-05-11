# -*- coding: utf-8 -*-

def make_uppercase(s):
    return s.upper()


def setup(app):
    app.register_formatter('uppercase', make_uppercase)
