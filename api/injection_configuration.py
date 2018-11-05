# -*- coding: utf-8 -*-

import logging
from injector import singleton, Module, Injector

from api.infrastructure.bus import CommandBus, QueryBus, CommandHandlers, QueryHandlers
from api.infrastructure.messages import CommandHandler, QueryHandler
from api.model.error import ErrorResolver, ErrorResolvers
from utils import find_implementations_of

logger = logging.getLogger(__name__)


def create_injector():
    return Injector([InjectionModule()])


class InjectionModule(Module):
    def configure(self, binder):
        self.__configure_commands(binder)
        self.__configure_queries(binder)
        self.__configure_resolvers(binder)

    def __configure_commands(self, binder):
        command_handlers = self.__implementations_of(CommandHandler)
        binder.multibind(CommandHandlers, to=command_handlers, scope=singleton)
        binder.bind(CommandBus, scope=singleton)

    def __configure_queries(self, binder):
        query_handlers = self.__implementations_of(QueryHandler)
        binder.multibind(QueryHandlers, to=query_handlers, scope=singleton)
        binder.bind(QueryBus, scope=singleton)

    def __configure_resolvers(self, binder):
        resolvers = self.__implementations_of(ErrorResolver)
        binder.multibind(ErrorResolvers, to=resolvers, scope=singleton)

    def __implementations_of(self, clazz):
        query_handlers = []
        implementations = find_implementations_of(clazz)
        for implementation in implementations:
            logger.debug(u'Found implementation for %s => %s', clazz.__name__, implementation.__name__)
            query_handlers.append(self.__injector__.get(implementation))
        return query_handlers
