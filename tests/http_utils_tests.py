# -*- coding: utf-8 -*-

from mock import MagicMock, Mock
from nose.tools import *
from unittest import TestCase

from api.http_utils import *


class WithExponentialBackoffTestCase(TestCase):
    def setUp(self):
        time.sleep = MagicMock()
        self.calls = 0

    def test_calls_the_wrapped_function_once_if_no_error_occurs(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            return u'hello'

        assert_equals(u'hello', function_to_call())
        assert_equals(1, self.calls)

    def test_can_retry_for_five_times_by_default(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            raise FakeError(500)

        with assert_raises(FakeError):
            function_to_call()
            assert_equals(6, self.calls)

    def test_the_delay_increases_on_each_retry(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            raise FakeError(500)

        with assert_raises(FakeError):
            function_to_call()

        assert_equals(5, len(time.sleep.mock_calls))
        assert_between(time.sleep.mock_calls[0][1][0], 1, 2)
        assert_between(time.sleep.mock_calls[1][1][0], 2, 3)
        assert_between(time.sleep.mock_calls[2][1][0], 4, 5)
        assert_between(time.sleep.mock_calls[3][1][0], 8, 9)
        assert_between(time.sleep.mock_calls[4][1][0], 16, 17)

    def test_retries_on_429_5xx_errors(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            if self.calls == 1:
                raise FakeError(503)
            elif self.calls == 2:
                raise FakeError(429)
            elif self.calls == 3:
                raise FakeError(404)
            else:
                return u'hello'

        with assert_raises(FakeError):
            function_to_call()
            assert_equals(3, self.calls)

    def test_retries_on_broken_pipe_error(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            if self.calls == 1:
                raise FakeBrokenPipeError()
            elif self.calls == 2:
                raise FakeError(404)
            else:
                return u'hello'

        with assert_raises(FakeError):
            function_to_call()
            assert_equals(2, self.calls)

    def test_propagates_the_error_immediately_if_it_is_not_retryable(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            raise FakeError(404)

        with assert_raises(FakeError):
            function_to_call()
            assert_equals(1, self.calls)

    def test_propagates_the_last_error_on_too_many_retries(self):
        @WithExponentialBackoff
        def function_to_call():
            self.calls += 1
            if self.calls <= WithExponentialBackoff.NUMBER_OF_RETRIES:
                raise FakeError(500)
            raise FakeError(503)

        with assert_raises(FakeError) as error:
            function_to_call()
            assert_equals(503, error.status_code)

    def test_the_wrapped_function_can_have_parameters(self):
        @WithExponentialBackoff
        def function_to_call(param, optional_param=u'hey'):
            return param + optional_param

        result = function_to_call(u'hello ', optional_param=u'world')

        assert_equals(u'hello world', result)


class GlobalFunctionsTestCase(TestCase):
    def test_can_build_a_results_generator(self):
        request = Mock()
        request.execute.return_value = u'hello'
        request2 = Mock()
        request2.execute.return_value = u'hey'
        get_next_function = Mock(return_value=request2)

        generator = results_generator(request, get_next_function)

        assert_equals(u'hello', generator.next())
        assert_equals(u'hey', generator.next())

    def test_can_execute_a_callback_on_each_batch(self):
        request = Mock()
        request.execute.return_value = u'hello'
        request2 = Mock()
        request2.execute.return_value = u'hey'
        get_next_function = Mock(return_value=request2)

        generator = results_generator(request, get_next_function, lambda batch: batch + u' world')

        assert_equals(u'hello world', generator.next())
        assert_equals(u'hey world', generator.next())

    def test_execution_result_and_next_request(self):
        request = Mock()
        request.execute.return_value = u'hello'
        next_request = Mock()
        get_next_function = Mock(return_value=next_request)

        result, get_next = execution_result_and_next_request(request, get_next_function)

        get_next_function.assert_called_with(request, u'hello')
        assert_equals(u'hello', result)
        assert_equals(next_request, get_next.args[0])
        assert_is_instance(get_next, partial)

    def test_execution_result_and_next_request_is_executed_with_exponential_backoff(self):
        assert_equals(u'execution_result_and_next_request', execution_result_and_next_request.function.__name__)


def assert_between(instance, a, b):
    assert_greater_equal(instance, a)
    assert_less_equal(instance, b)


class FakeError(RuntimeError):
    def __init__(self, status_code):
        self.status_code = status_code
        self.resp = FakeResponse(status_code)


class FakeBrokenPipeError(RuntimeError):
    def __init__(self):
        self.errno = 32


class FakeResponse(object):
    def __init__(self, status_code):
        self.status = status_code
