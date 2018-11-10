# -*- coding: utf-8 -*-

from injector import inject, Key

from api.http_utils import WithExponentialBackoff

GoogleStorageApiResource = Key(u'google_storage_api_resource')


class StorageApiResource(object):
    @inject(api_resource=GoogleStorageApiResource)
    def __init__(self, api_resource):
        self.__objects_resource = api_resource.objects()

    @WithExponentialBackoff
    def insert_object(self, **kwargs):
        return self.__objects_resource.insert(**kwargs).execute()
