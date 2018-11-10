# -*- coding: utf-8 -*-
from StringIO import StringIO

from googleapiclient.http import MediaIoBaseUpload
from injector import inject

from api.service.storage_api_resource import StorageApiResource


class StorageService(object):
    @inject(api_resource=StorageApiResource)
    def __init__(self, api_resource):
        self.__api_resource = api_resource

    def insert_key(self, json_private_key, bucket, path):
        media_file = MediaIoBaseUpload(StringIO(json_private_key), u'application/json')
        return self.__api_resource.insert_object(bucket=bucket, name=path, media_body=media_file)
