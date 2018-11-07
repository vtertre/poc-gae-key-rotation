# -*- coding: utf-8 -*-
from injector import inject

from api.infrastructure.messages import QueryHandler
from api.service.directory_service import DirectoryService


class DummyQuery(object):
    def __init__(self):
        self.message = u'The first query'


class DummyQueryHandler(QueryHandler):
    @inject(directory_service=DirectoryService)
    def __init__(self, directory_service):
        self.__directory_service = directory_service

    @property
    def message_type(self):
        return DummyQuery

    def execute(self, query):
        return self.__directory_service.list_users()
