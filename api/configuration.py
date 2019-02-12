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

service_account_ids = [u'102925455101661417546', u'101129016229136729278']
