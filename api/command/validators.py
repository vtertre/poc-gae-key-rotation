# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from functools import wraps


class CommandValidator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self, command):
        raise NotImplementedError


class ValidateBeforeWith(object):
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, wrapped_function):
        @wraps(wrapped_function)
        def validate_and_execute(*args, **kwargs):
            command = args[1]
            violations = self.validator.validate(command)
            if len(violations) > 0:
                raise ValidationError(violations)
            return wrapped_function(*args, **kwargs)
        return validate_and_execute


class ValidationError(RuntimeError):
    status_code = 400

    def __init__(self, messages):
        self.messages = messages
