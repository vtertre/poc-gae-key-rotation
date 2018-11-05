# -*- coding: utf-8 -*-

from flask_restful import Resource
from injector import inject

from api.infrastructure.bus import QueryBus
from api.query import dummy_query


class IndexResource(Resource):
    @inject(query_bus=QueryBus)
    def __init__(self, query_bus):
        self.query_bus = query_bus

    def get(self):
        result = self.query_bus.send_and_wait_response(dummy_query.DummyQuery())
        return result.response
