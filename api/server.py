# -*- coding: utf-8 -*-

import os

import uuid
from flask import Flask, request, jsonify
from flask_restful import Api
from google.appengine.api import users

from your_application import ApplicationStatusService


class ExtendedApi(Api):
    def __init__(self, app, status_service):
        super(ExtendedApi, self).__init__(app)
        self.status_service = status_service

    def handle_error(self, e):
        status_code = self.status_service.get_status(e)
        error_representation = self.status_service.get_representation(e)
        return self.make_response(error_representation, status_code)


class Server(object):
    def __init__(self, application):
        flask = Flask(__name__)
        flask.config.from_object(ServerConfiguration)
        self._application = application
        self._web_server = ExtendedApi(flask, self._application.injector.get(ApplicationStatusService))
        self._admin_routes = []
        self.add_routes(self._application.routes())
        flask.before_request(check_privileges_for(self._admin_routes))

    def start(self, port):
        self.flask.run(port=port)

    def add_routes(self, routes):
        for route in routes:
            if route.requires_admin_privileges:
                self._admin_routes.append(route.resource.__name__.lower())
            self._web_server.add_resource(route.resource, route.uri)

    def __call__(self, environ, start_response):
        return self.flask.wsgi_app(environ, start_response)

    @property
    def flask(self):
        return self._web_server.app


class ServerConfiguration(object):
    DEBUG = os.environ.get(u'env', u'dev') == u'dev'
    # SECRET_KEY = '' Generate a secret to use client side sessions with os.urandom(24)


def check_privileges_for(admin_endpoints):
    def check_if_admin_role_is_required():
        if request.endpoint in admin_endpoints:
            if not users.is_current_user_admin():
                return jsonify({u'message': u'ACCESS_FORBIDDEN'}), 403

    return check_if_admin_role_is_required
