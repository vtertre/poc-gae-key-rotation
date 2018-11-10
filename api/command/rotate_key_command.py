# -*- coding: utf-8 -*-
from injector import inject

from api.infrastructure.messages import CommandHandler
from api.service.iam_service import IAMService
from api.service.storage_service import StorageService


class RotateKeyCommand(object):
    def __init__(self, service_account_id, key_id):
        self.service_account_id = service_account_id
        self.key_id = key_id


class RotateKeyCommandHandler(CommandHandler):
    @inject(iam_service=IAMService, storage_service=StorageService)
    def __init__(self, iam_service, storage_service):
        self.__iam_service = iam_service
        self.__storage_service = storage_service

    @property
    def message_type(self):
        return RotateKeyCommand

    def execute(self, command):
        key_resource = self.__iam_service.create_key(command.service_account_id)
        key_data = key_resource[u'privateKeyData'].decode(u'base64')
        storage_resource = self.__storage_service.insert_key(key_data, u'sandbox-vincent.appspot.com',
                                                             u'keys/data-key.json')
        self.__iam_service.delete_key(command.service_account_id, command.key_id)
        return storage_resource
