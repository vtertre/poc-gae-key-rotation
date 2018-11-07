# -*- coding: utf-8 -*-
from injector import inject

from api.service.directory_api_resource import DirectoryApiResource


class DirectoryService(object):
    @inject(directory_api_resource=DirectoryApiResource)
    def __init__(self, directory_api_resource):
        self.__directory_api_resource = directory_api_resource

    def list_users(self):
        arguments = {
            u'customer': u'my_customer',
            u'viewType': u'admin_view',
            u'fields': u'users(id, primaryEmail, orgUnitPath, lastLoginTime), nextPageToken',
            u'maxResults': 10
        }
        return self.__directory_api_resource.list_users(**arguments)
