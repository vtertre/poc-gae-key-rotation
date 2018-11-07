# -*- coding: utf-8 -*-
from injector import inject, Key

from api.http_utils import WithExponentialBackoff

GoogleIAMApiResource = Key(u'google_iam_api_resource')


class IAMApiResource(object):
    @inject(api_resource=GoogleIAMApiResource)
    def __init__(self, api_resource):
        self.__keys_resource = api_resource.projects().serviceAccounts().keys()

    @WithExponentialBackoff
    def list_keys_of(self, service_account_name, key_types=None):
        return self.__keys_resource.list(name=service_account_name, keyTypes=key_types).execute()
