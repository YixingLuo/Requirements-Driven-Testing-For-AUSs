#!/usr/bin/python
# -*- coding: utf-8 -*-

def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        # print("there is a value:", name)
        return _global_dict[name]
    except KeyError:
        # print("there is no a value:", name)
        return defValue