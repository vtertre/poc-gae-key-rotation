# -*- coding: utf-8 -*-
from injector import inject

from api.service.iam_api_resource import IAMApiResource


class IAMService(object):
    @inject(iam_api_resource=IAMApiResource)
    def __init__(self, iam_api_resource):
        self.__iam_api_resource = iam_api_resource

    def list_keys_of(self, service_account_name, key_types=None):
        service_account_resource_name = u'projects/-/serviceAccounts/{}'.format(service_account_name)
        return self.__iam_api_resource.list_keys_of(service_account_resource_name, key_types)
