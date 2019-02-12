# -*- coding: utf-8 -*-

from injector import inject

from api.command.initiate_key_rotation_command import InitiateKeyRotationCommand
from api.infrastructure.bus import CommandBus
from api.resource.base_resource import BaseResource


class InitiateKeyRotationResource(BaseResource):
    @inject(command_bus=CommandBus)
    def __init__(self, command_bus):
        super(InitiateKeyRotationResource, self).__init__()
        self.command_bus = command_bus

    def get(self):
        command = InitiateKeyRotationCommand()
        result = self.command_bus.send_and_wait_response(command)
        return result.response
