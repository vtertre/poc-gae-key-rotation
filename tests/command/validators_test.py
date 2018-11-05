# -*- coding: utf-8 -*-

from nose.tools import *
from unittest import TestCase

from api.command.validators import CommandValidator, ValidationError, ValidateBeforeWith


class ValidatorsTestCase(TestCase):
    def test_executes_a_valid_command(self):
        command = FakeCommand(u'number', 3, u'RUNNING')

        result = FakeCommandHandler().execute(command)

        assert_equals(13, result)

    def test_raises_all_the_violations_of_an_invalid_command(self):
        command = FakeCommand(u'string', 7, u'RUNNING')

        with assert_raises(ValidationError) as context:
            FakeCommandHandler().execute(command)

        error = context.exception
        assert_list_equal([u'BAD_TYPE', u'BAD_VALUE'], error.messages)

    def test_a_validation_error_is_a_bad_request(self):
        assert_equals(400, ValidationError.status_code)


class FakeCommand:
    def __init__(self, kind, value, state):
        self.kind = kind
        self.value = value
        self.state = state


class FakeCommandValidator(CommandValidator):
    def validate(self, command):
        violations = []
        if command.kind != u'number':
            violations.append(u'BAD_TYPE')
        if command.value < 0 or command.value > 5:
            violations.append(u'BAD_VALUE')
        if command.state != u'RUNNING':
            violations.append(u'BAD_STATE')
        return violations


class FakeCommandHandler:
    def __init__(self):
        pass

    @ValidateBeforeWith(FakeCommandValidator())
    def execute(self, command):
        return command.value + 10
