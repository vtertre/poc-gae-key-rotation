# -*- coding: utf-8 -*-

import mock
from nose.tools import *
from unittest import TestCase

from api.resource.index_resource import *


class IndexResourceTestCase(TestCase):
    def test_a_message_is_returned(self):
        result = FakeResult(u'hello')
        bus = mock.Mock()
        bus.send_and_wait_response.return_value = result

        response = IndexResource(query_bus=bus).get()

        assert_equals(u'hello', response)


class FakeResult:
    def __init__(self, response):
        self.response = response
