# -*- coding: utf-8 -*-
from injector import inject

from api.service.iam_api_resource import IAMApiResource


class IAMService(object):
    SERVICE_ACCOUNT_RESOURCE_ID_TEMPLATE = u'projects/-/serviceAccounts/{}'
    KEY_RESOURCE_ID_TEMPLATE = u'projects/-/serviceAccounts/{}/keys/{}'

    @inject(iam_api_resource=IAMApiResource)
    def __init__(self, iam_api_resource):
        self.__iam_api_resource = iam_api_resource

    def create_key(self, service_account_id):
        service_account_resource_id = self.SERVICE_ACCOUNT_RESOURCE_ID_TEMPLATE.format(service_account_id)
        key_data = {
            u'privateKeyType': u'TYPE_GOOGLE_CREDENTIALS_FILE',
            u'keyAlgorithm': u'KEY_ALG_RSA_2048'
        }
        return self.__iam_api_resource.create_key(service_account_resource_id, key_data)

    def delete_key(self, service_account_id, key_id):
        key_resource_id = self.KEY_RESOURCE_ID_TEMPLATE.format(service_account_id, key_id)
        return self.__iam_api_resource.delete_key(key_resource_id)

    def get_key(self, service_account_id, key_id):
        key_resource_id = self.KEY_RESOURCE_ID_TEMPLATE.format(service_account_id, key_id)
        return self.__iam_api_resource.get_key(key_resource_id)

    def list_keys_of(self, service_account_id):
        service_account_resource_id = self.SERVICE_ACCOUNT_RESOURCE_ID_TEMPLATE.format(service_account_id)
        return self.__iam_api_resource.list_keys_of(service_account_resource_id, key_types=u'USER_MANAGED')
