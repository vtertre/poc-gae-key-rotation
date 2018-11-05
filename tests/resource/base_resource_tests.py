# -*- coding: utf-8 -*-

from mock import MagicMock
from nose.tools import *
from unittest import TestCase
from werkzeug.datastructures import MultiDict

from api.infrastructure.bus import ExecutionResult
from api.resource.base_resource import *


class BaseResourceTestCase(TestCase):
    def setUp(self):
        flask.request = MagicMock()
        flask.request.args = MultiDict()
        flask.request.json = {}
        flask.request.form = MultiDict()
        flask.request.files = {}

    def test_gets_arguments_from_the_request(self):
        flask.request.args[u'hello'] = u'5'
        resource = DummyResource()

        assert_equals(5, resource._get_query_parameter_value_for(u'hello', int))

    def test_gets_json_from_the_request(self):
        flask.request.json[u'hello'] = u'world'
        resource = DummyResource()

        assert_equals(u'world', resource._get_json_body_value_for(u'hello'))

    def test_gets_form_value_from_the_request(self):
        flask.request.form.add(u'hello', u'world')
        resource = DummyResource()

        assert_equals(u'world', resource._get_form_value_for(u'hello'))

    def test_gets_form_values_from_the_request(self):
        flask.request.form.setlist(u'hello', [u'world', u'bump'])
        resource = DummyResource()

        assert_list_equal([u'world', u'bump'], resource._get_form_values_for(u'hello'))

    def test_gets_file_from_the_request(self):
        flask.request.files[u'hello'] = u'world'
        resource = DummyResource()

        assert_equals(u'world', resource._get_file(u'hello'))

    def test_returns_none_if_execution_result_is_empty(self):
        resource = DummyResource()

        assert_equals(None, resource._get_data_or_fail(None))

    def test_returns_none_if_execution_result_is_empty(self):
        resource = DummyResource()

        assert_equals(None, resource._get_data_or_fail(None))

    def test_raises_the_error_if_execution_result_is_an_error(self):
        result = ExecutionResult.error(FakeError(500))
        resource = DummyResource()

        with assert_raises(FakeError) as error:
            resource._get_data_or_fail(result)
            assert_equals(500, error.status_code)

    def test_passes_the_result_if_everything_is_ok(self):
        result = ExecutionResult.success(u'success')
        resource = DummyResource()

        assert_equals(u'success', resource._get_data_or_fail(result))


class DummyResource(BaseResource):
    pass


class FakeError(RuntimeError):
    def __init__(self, status_code):
        self.status_code = status_code
