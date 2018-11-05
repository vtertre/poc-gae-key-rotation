# -*- coding: utf-8 -*-

import logging

from injector import inject, Key

logger = logging.getLogger(__name__)
QueryHandlers = Key(u'query_handlers')
CommandHandlers = Key(u'command_handlers')


class ExecutionResult(object):
    def __init__(self, response=None, error=None, success=False):
        self.response = response
        self.error = error
        self.success = success

    @staticmethod
    def success(response):
        return ExecutionResult(response=response, success=True)

    @staticmethod
    def error(error):
        return ExecutionResult(error=error)

    def is_success(self):
        return self.success

    def is_error(self):
        return not self.success


class Bus(object):
    def __init__(self, handlers):
        self.message_handlers = {}
        for handler in handlers:
            if self.message_handlers.get(handler.message_type) is None:
                self.message_handlers[handler.message_type] = []
            self.message_handlers[handler.message_type].append(handler)

    def send_and_wait_response(self, message):
        handlers = self.message_handlers.get(message.__class__, [])
        if len(handlers) == 0:
            logger.warning(u'Impossible to find a handler for %s', message.__class__.__name__)
            return ExecutionResult.error(BusError(u'Impossible to find a handler for current message'))

        logger.debug(u'New message: %s', message.__class__.__name__)
        results = []
        for handler in handlers:
            results.append(self._execute(message, handler))
        return results[0]

    @staticmethod
    def _execute(message, handler):
        try:
            logger.debug(u'Executing handler %s', handler.__class__.__name__)
            return ExecutionResult.success(handler.execute(message))
        except Exception as e:
            logger.exception(e)
            return ExecutionResult.error(e)


class CommandBus(Bus):
    @inject(handlers=CommandHandlers)
    def __init__(self, handlers):
        super(CommandBus, self).__init__(handlers)


class QueryBus(Bus):
    @inject(handlers=QueryHandlers)
    def __init__(self, handlers):
        super(QueryBus, self).__init__(handlers)


class BusError(RuntimeError):
    def __init__(self, message):
        self.message = message
