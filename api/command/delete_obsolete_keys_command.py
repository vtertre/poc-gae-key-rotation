# -*- coding: utf-8 -*-

from datetime import datetime

from injector import inject
import logging

from api.infrastructure.messages import CommandHandler
from api.service.iam_service import IAMService
from api.service.storage_service import StorageService

logger = logging.getLogger(__name__)


class DeleteObsoleteKeysCommand(object):
    def __init__(self, service_account_id):
        self.service_account_id = service_account_id


class DeleteObsoleteKeysCommandHandler(CommandHandler):
    @inject(iam_service=IAMService, storage_service=StorageService)
    def __init__(self, iam_service, storage_service):
        self.__iam_service = iam_service
        self.__storage_service = storage_service

    @property
    def message_type(self):
        return DeleteObsoleteKeysCommand

    def execute(self, command):
        current_datetime = datetime.utcnow()
        available_keys = self.__iam_service.list_keys_of(command.service_account_id).get(u'keys', [])
        obsolete_keys = []
        for key in available_keys:
            if self.__is_obsolete(key, current_datetime):
                obsolete_keys.append(key)
        self.__delete(obsolete_keys)
        return None

    def __delete(self, obsolete_keys):
        obsolete_keys_count = len(obsolete_keys)
        if obsolete_keys_count > 1:
            self.__batch_delete(obsolete_keys)
        elif obsolete_keys_count == 1:
            key = obsolete_keys.pop()
            self.__iam_service.delete_key_from_name(key[u'name'])

    def __batch_delete(self, obsolete_keys):
        batch_request = self.__iam_service.create_batch_request(callback=self.__deletion_callback)
        for key in obsolete_keys:
            request = self.__iam_service.delete_key_from_name(key[u'name'], execute=False)
            batch_request.add(request)
        batch_request.execute()

    @staticmethod
    def __deletion_callback(request_id, response, error):
        if error:
            logger.warning(u'Failed to delete key: %s', error)

    @staticmethod
    def __is_obsolete(key, current_datetime):
        key_creation_time = datetime.strptime(key[u'validAfterTime'], u'%Y-%m-%dT%H:%M:%SZ')
        diff_time = current_datetime - key_creation_time
        return diff_time.days >= 14
