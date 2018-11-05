# -*- coding: utf-8 -*-

import errno
import logging
import socket
import time
from functools import partial
from random import randint

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from api.configuration import http_configuration

logger = logging.getLogger(__name__)

socket.setdefaulttimeout(60)


class WithExponentialBackoff(object):
    NUMBER_OF_RETRIES = http_configuration[u'number_of_retries']
    MAXIMUM_RETRY_DELAY = http_configuration[u'maximum_retry_delay_in_seconds']

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        logger.debug(u'Executing function %s with exponential backoff', self.function.__name__)
        for retry_count in xrange(0, 1 + self.NUMBER_OF_RETRIES):
            try:
                return self.function(*args, **kwargs)
            except Exception, exception:
                logger.error(u'Failed to execute %s (%d)', self.function.__name__, retry_count + 1, exc_info=1)
                if retry_count < self.NUMBER_OF_RETRIES and self._is_retryable(exception):
                    retry_delay = self._compute_retry_delay(retry_count)
                    logger.info(u'Retrying in %ss', str(retry_delay))
                    time.sleep(retry_delay)
                else:
                    raise

    def __get__(self, instance, owner=None):
        if instance:
            partial_function = partial(self, instance)
            partial_function.__wrapped__ = self.function
            return partial_function
        else:
            self.__wrapped__ = self.function
            return self

    def _compute_retry_delay(self, retry_count):
        potential_delay = 2 ** retry_count + randint(0, 1000) / 1000.0
        return min(potential_delay, self.MAXIMUM_RETRY_DELAY)

    def _is_retryable(self, error):
        is_broken_pipe_error = hasattr(error, u'errno') and error.errno == errno.EPIPE
        return is_broken_pipe_error or self._is_retryable_http_error(error)

    @staticmethod
    def _is_retryable_http_error(error):
        is_http_error = hasattr(error, u'resp') and hasattr(error.resp, u'status')
        if is_http_error:
            status = error.resp.status
            return status == 429 or 500 <= status < 600
        return False


def build_api_resource(keyfile_path, api, version, scopes=None, delegated_account=None):
    credentials = Credentials.from_service_account_file(keyfile_path, scopes=scopes or [], subject=delegated_account)
    return build_api_resource_from(credentials, api, version)


def build_api_resource_from(credentials, api, version):
    return build(api, version, credentials=credentials)


def results_generator(request, function_get_next, callback=None):
    get_next_page_and_request = partial(execution_result_and_next_request, request, function_get_next)
    while get_next_page_and_request:
        result_batch, get_next_page_and_request = get_next_page_and_request()
        if callback:
            result_batch = callback(result_batch)
        yield result_batch


@WithExponentialBackoff
def execution_result_and_next_request(request, function_get_next):
    result = request.execute()
    next_request = function_get_next(request, result)
    get_next_page_and_request = None if next_request is None else partial(
        execution_result_and_next_request,
        next_request,
        function_get_next
    )
    return result, get_next_page_and_request
