# -*- coding: utf-8 -*-

import logging
from flask_injector import FlaskInjector

from configuration import logging_configuration
from server import Server
from your_application import YourApplication

formatter = logging.Formatter(logging_configuration[u'pattern'])
root_logger = logging.getLogger()
handler = root_logger.handlers[0] if root_logger.handlers else logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging_configuration[u'level'])
root_logger.addHandler(handler)
root_logger.setLevel(logging_configuration[u'level'])

application = YourApplication()
server = Server(application)

FlaskInjector(app=server.flask, injector=application.injector)
