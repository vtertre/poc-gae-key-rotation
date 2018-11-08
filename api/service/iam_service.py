# -*- coding: utf-8 -*-
from injector import inject

from api.service.iam_api_resource import IAMApiResource


class IAMService(object):
    @inject(iam_api_resource=IAMApiResource)
    def __init__(self, iam_api_resource):
        self.__iam_api_resource = iam_api_resource

    def get_key(self, service_account_id, key_id):
        key_resource_id = u'projects/-/serviceAccounts/{}/keys/{}'.format(service_account_id, key_id)
        return self.__iam_api_resource.get_key(key_resource_id)

    def list_keys_of(self, service_account_id):
        service_account_resource_id = u'projects/-/serviceAccounts/{}'.format(service_account_id)
        return self.__iam_api_resource.list_keys_of(service_account_resource_id, key_types=u'USER_MANAGED')
