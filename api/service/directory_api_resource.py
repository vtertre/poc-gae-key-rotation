# -*- coding: utf-8 -*-
from injector import inject, Key

from api.http_utils import WithExponentialBackoff

GoogleDirectoryApiResource = Key(u'google_directory_api_resource')


class DirectoryApiResource(object):
    @inject(api_resource=GoogleDirectoryApiResource)
    def __init__(self, api_resource):
        self.__api_resource = api_resource

    @WithExponentialBackoff
    def list_users(self, **kwargs):
        return self.__api_resource.users().list(**kwargs).execute()
