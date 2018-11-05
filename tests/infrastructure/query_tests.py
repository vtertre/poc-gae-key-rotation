# -*- coding: utf-8 -*-

from nose.tools import *
from unittest import TestCase

from api.infrastructure.messages import *


class QueryTestCase(TestCase):
    def test_calculates_the_skip_amount(self):
        query = DummyQuery()
        query.per_page(10).page(3)

        assert_equals(20, query.skip())


class DummyQuery(Query):
    pass
