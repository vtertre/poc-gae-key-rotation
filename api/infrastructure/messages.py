# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class Query(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.per_page_request = 0
        self.page_request = 0

    def per_page(self, per_page):
        self.per_page_request = per_page
        return self

    def page(self, page):
        self.page_request = page
        return self

    def skip(self):
        return (self.page_request - 1) * self.per_page_request


class MessageHandler(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def message_type(self):
        raise AttributeError

    @abstractmethod
    def execute(self, query):
        raise NotImplementedError


class CommandHandler(MessageHandler):
    __metaclass__ = ABCMeta


class QueryHandler(MessageHandler):
    __metaclass__ = ABCMeta
