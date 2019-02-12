# -*- coding: utf-8 -*-
from injector import inject

from api.infrastructure.messages import CommandHandler
from api.service.iam_service import IAMService
from api.service.storage_service import StorageService


class CreateDefaultKeyCommand(object):
    def __init__(self, service_account_id):
        self.service_account_id = service_account_id


class CreateDefaultKeyCommandHandler(CommandHandler):
    @inject(iam_service=IAMService, storage_service=StorageService)
    def __init__(self, iam_service, storage_service):
        self.__iam_service = iam_service
        self.__storage_service = storage_service

    @property
    def message_type(self):
        return CreateDefaultKeyCommand

    def execute(self, command):
        key_resource = self.__iam_service.create_key(command.service_account_id)
        key_data = key_resource[u'privateKeyData'].decode(u'base64')
        key_filepath = u'keys/{}.json'.format(command.service_account_id)
        self.__storage_service.insert_key(key_data, u'sandbox-vincent.appspot.com', key_filepath)
        return key_data
