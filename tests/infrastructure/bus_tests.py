# -*- coding: utf-8 -*-

from nose.tools import *
from unittest import TestCase

from api.infrastructure.bus import Bus, BusError


class BusTestCase(TestCase):
    def test_can_execute_a_query(self):
        handler = FakeQueryHandler()
        bus = bus_with_handler(handler)
        query = FakeQuery()

        bus.send_and_wait_response(query)

        assert_equal(query, handler.query_received)

    def test_the_result_of_the_query_is_returned(self):
        handler = FakeQueryHandler()
        bus = bus_with_handler(handler)

        result = bus.send_and_wait_response(FakeQuery())

        assert_equals(True, result.is_success())
        assert_equals(u'This is a yoke', result.response)

    def test_a_result_is_also_returned_on_error(self):
        handler = FakeQueryHandler()
        handler.raise_exception = True
        bus = bus_with_handler(handler)

        result = bus.send_and_wait_response(FakeQuery())

        assert_equals(True, result.is_error())
        assert_equals(RuntimeError, type(result.error))
        assert_equals(u'This is an error', result.error.message)

    def test_an_error_is_raised_if_no_handler_is_available_for_the_query(self):
        bus = empty_bus()

        result = bus.send_and_wait_response(FakeQuery())

        assert_equals(True, result.is_error())
        assert_equals(BusError, type(result.error))

    def test_can_execute_multiple_handlers_for_a_query(self):
        handler1 = FakeQueryHandler()
        handler2 = FakeQueryHandler()
        bus = bus_with_handlers([handler1, handler2])
        query = FakeQuery()

        bus.send_and_wait_response(query)

        assert_equals(query, handler1.query_received)
        assert_equals(query, handler2.query_received)


def bus_with_handler(handler):
    return bus_with_handlers([handler])


def bus_with_handlers(handlers):
    return Bus(handlers)


def empty_bus():
    return bus_with_handlers([])


class FakeQuery:
    def __init__(self):
        pass


class FakeQueryHandler:
    def __init__(self):
        self.message_type = FakeQuery
        self.raise_exception = False
        self.query_received = None

    def execute(self, query):
        self.query_received = query
        if self.raise_exception:
            raise RuntimeError(u'This is an error')
        return u'This is a yoke'
