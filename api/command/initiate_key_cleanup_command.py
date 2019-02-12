# -*- coding: utf-8 -*-

from google.appengine.api import taskqueue

from api.infrastructure.messages import CommandHandler
from api.configuration import service_account_ids


class InitiateKeyCleanupCommand(object):
    def __init__(self):
        pass


class InitiateKeyCleanupCommandHandler(CommandHandler):
    def __init__(self):
        self.queue = taskqueue.Queue(name=u'key-rotation-queue')

    @property
    def message_type(self):
        return InitiateKeyCleanupCommand

    def execute(self, command):
        for service_account in service_account_ids:
            self.__create_task_for(service_account)
        return {u'count': len(service_account_ids)}

    def __create_task_for(self, service_account_id):
        url = u'/keyRotation/serviceAccounts/{}/keys:deleteObsoleteKeys'.format(service_account_id)
        task = taskqueue.Task(method=u'POST', url=url)
        self.queue.add(task)
