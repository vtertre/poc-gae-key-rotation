# -*- coding: utf-8 -*-
from injector import inject

from api.infrastructure.messages import QueryHandler
from api.service.directory_api_service import DirectoryApiService


class DummyQuery(object):
    def __init__(self):
        self.message = u'The first query'


class DummyQueryHandler(QueryHandler):
    @inject(directory_api_service=DirectoryApiService)
    def __init__(self, directory_api_service):
        self.__directory_api_service = directory_api_service

    @property
    def message_type(self):
        return DummyQuery

    def execute(self, query):
        return self.__directory_api_service.list_users()
