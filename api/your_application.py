# -*- coding: utf-8 -*-

from injector import inject

from api.resource.synchronous_rotation_resource import SynchronousRotationResource
from injection_configuration import create_injector
from model.error import ErrorResolvers
from resource.index_resource import IndexResource


class YourApplication(object):
    def __init__(self):
        self.injector = create_injector()

    @staticmethod
    def routes():
        return [
            Route(u'/', IndexResource),
            Route(u'/serviceAccounts/<string:service_account_id>/keys/<string:key_id>:rotate',
                  SynchronousRotationResource)
        ]


class Route(object):
    def __init__(self, uri, resource, requires_admin_privileges=False):
        self.uri = uri
        self.resource = resource
        self.requires_admin_privileges = requires_admin_privileges


class ApplicationStatusService(object):
    @inject(resolvers=ErrorResolvers)
    def __init__(self, resolvers):
        self.resolvers = resolvers

    def get_status(self, error):
        resolver = self._resolver(error)
        return resolver.status if resolver else 500

    def get_representation(self, error):
        resolver = self._resolver(error)
        return resolver.representation(error) if resolver else None

    def _resolver(self, error):
        resolvers = filter(lambda resolver: resolver.can_resolve(error), self.resolvers)
        return resolvers[0] if len(resolvers) > 0 else None
