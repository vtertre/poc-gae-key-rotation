# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from injector import Key

ErrorResolvers = Key(u'error_resolvers')


class ErrorResolver(object):
    __metaclass__ = ABCMeta

    def can_resolve(self, error):
        error_type = error.__class__ if error else None
        return error is not None and error_type is not None and self.error_type == error_type

    @property
    @abstractmethod
    def error_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self):
        raise NotImplementedError

    @abstractmethod
    def representation(self, error):
        return None
