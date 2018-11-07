# -*- coding: utf-8 -*-
from injector import inject

from api.infrastructure.messages import CommandHandler
from api.service.iam_service import IAMService


class RotateKeyCommand(object):
    def __init__(self, service_account_name):
        self.service_account_name = service_account_name


class RotateKeyCommandHandler(CommandHandler):
    @inject(iam_service=IAMService)
    def __init__(self, iam_service):
        self.__iam_service = iam_service

    @property
    def message_type(self):
        return RotateKeyCommand

    def execute(self, command):
        return self.__iam_service.list_keys_of(command.service_account_name)
