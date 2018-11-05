# -*- coding: utf-8 -*-

import logging

logging_configuration = {
    u'level': logging.DEBUG,
    u'pattern': u'[%(name)s] | %(message)s'
}

http_configuration = {
    u'number_of_retries': 5,
    u'maximum_retry_delay_in_seconds': 32
}
