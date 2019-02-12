# -*- coding: utf-8 -*-

from injector import inject

from api.command.create_default_key_command import CreateDefaultKeyCommand
from api.infrastructure.bus import CommandBus
from api.resource.base_resource import BaseResource


class CreateDefaultKeyResource(BaseResource):
    @inject(command_bus=CommandBus)
    def __init__(self, command_bus):
        super(CreateDefaultKeyResource, self).__init__()
        self.command_bus = command_bus

    def post(self, service_account_id):
        command = CreateDefaultKeyCommand(service_account_id)
        result = self.command_bus.send_and_wait_response(command)
        return result.response
