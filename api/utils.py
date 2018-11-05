# -*- coding: utf-8 -*-

from inspect import isabstract


def find_implementations_of(clazz):
    implementations = []
    for subclass in clazz.__subclasses__():
        if isabstract(subclass):
            implementations.extend(find_implementations_of(subclass))
        else:
            implementations.append(subclass)
    return implementations
