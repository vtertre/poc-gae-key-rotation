# -*- coding: utf-8 -*-
from injector import inject, Key

from api.http_utils import WithExponentialBackoff

GoogleIAMApiResource = Key(u'google_iam_api_resource')


class IAMApiResource(object):
    @inject(api_resource=GoogleIAMApiResource)
    def __init__(self, api_resource):
        self.__api_resource = api_resource
        self.__keys_resource = api_resource.projects().serviceAccounts().keys()

    @WithExponentialBackoff
    def create_key(self, service_account_resource_id, key_data):
        return self.__keys_resource.create(name=service_account_resource_id, body=key_data).execute()

    @WithExponentialBackoff
    def delete_key(self, key_resource_id, execute=True):
        request = self.__keys_resource.delete(name=key_resource_id)
        return request.execute() if execute else request

    @WithExponentialBackoff
    def get_key(self, key_resource_id, public_key_type=None):
        return self.__keys_resource.get(name=key_resource_id, publicKeyType=public_key_type).execute()

    @WithExponentialBackoff
    def list_keys_of(self, service_account_resource_id, key_types=None):
        return self.__keys_resource.list(name=service_account_resource_id, keyTypes=key_types).execute()

    def create_batch_request(self, callback=None):
        return self.__api_resource.new_batch_http_request(callback=callback)
