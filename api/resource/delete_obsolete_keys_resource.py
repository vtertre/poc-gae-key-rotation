# -*- coding: utf-8 -*-

from injector import inject

from api.command.delete_obsolete_keys_command import DeleteObsoleteKeysCommand
from api.infrastructure.bus import CommandBus
from api.resource.base_resource import BaseResource


class DeleteObsoleteKeysResource(BaseResource):
    @inject(command_bus=CommandBus)
    def __init__(self, command_bus):
        super(DeleteObsoleteKeysResource, self).__init__()
        self.command_bus = command_bus

    def post(self, service_account_id):
        command = DeleteObsoleteKeysCommand(service_account_id)
        result = self.command_bus.send_and_wait_response(command)
        return result.response
