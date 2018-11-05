# -*- coding: utf-8 -*-

import flask
import logging
from flask_restful import Resource

logger = logging.getLogger(__name__)


class BaseResource(Resource):
    def __init__(self):
        pass

    @staticmethod
    def _get_query_parameter_value_for(key, type=None):
        return flask.request.args.get(key, None, type)

    @staticmethod
    def _get_json_body_value_for(key):
        return flask.request.json.get(key, None)

    @staticmethod
    def _get_form_value_for(key, type=None):
        return flask.request.form.get(key, None, type)

    @staticmethod
    def _get_form_values_for(key, type=None):
        return flask.request.form.getlist(key, type) if key in flask.request.form else None

    @staticmethod
    def _get_file(key):
        return flask.request.files.get(key, None)

    @staticmethod
    def _get_data_or_fail(execution_result):
        if not execution_result:
            return None
        if execution_result.is_error():
            raise execution_result.error
        return execution_result.response
