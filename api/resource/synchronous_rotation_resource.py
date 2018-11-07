# -*- coding: utf-8 -*-

from injector import inject

from api.command.rotate_key_command import RotateKeyCommand
from api.infrastructure.bus import CommandBus
from api.resource.base_resource import BaseResource


class SynchronousRotationResource(BaseResource):
    @inject(command_bus=CommandBus)
    def __init__(self, command_bus):
        super(SynchronousRotationResource, self).__init__()
        self.command_bus = command_bus

    def post(self):
        service_account_name = self._get_json_body_value_for(u'name')
        command = RotateKeyCommand(service_account_name)
        result = self.command_bus.send_and_wait_response(command)
        return result.response
