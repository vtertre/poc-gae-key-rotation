# -*- coding: utf-8 -*-

import logging
from json import loads
from os import environ

from google.auth import app_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from injector import singleton, Module, Injector, provides

from api.http_utils import build_api_resource_from
from api.infrastructure.bus import CommandBus, QueryBus, CommandHandlers, QueryHandlers
from api.infrastructure.messages import CommandHandler, QueryHandler
from api.model.error import ErrorResolver, ErrorResolvers
from api.service.directory_api_resource import GoogleDirectoryApiResource, DirectoryApiResource
from api.service.directory_service import DirectoryService
from api.service.iam_api_resource import GoogleIAMApiResource
from api.service.iam_service import IAMService
from utils import find_implementations_of

logger = logging.getLogger(__name__)


def create_injector():
    return Injector([InjectionModule()])


class InjectionModule(Module):
    def configure(self, binder):
        self.__configure_commands(binder)
        self.__configure_queries(binder)
        self.__configure_resolvers(binder)
        binder.bind(DirectoryApiResource, scope=singleton)
        binder.bind(DirectoryService, scope=singleton)
        binder.bind(IAMService, scope=singleton)

    @singleton
    @provides(GoogleIAMApiResource)
    def provide_google_iam_api_resource(self):
        # TODO: use created service account
        credentials = app_engine.Credentials()
        return build_api_resource_from(credentials, u'iam', u'v1')

    @singleton
    @provides(GoogleDirectoryApiResource)
    def provide_google_directory_api_resource(self):
        # TODO: use created service account
        scopes = [u'https://www.googleapis.com/auth/admin.directory.user.readonly']
        if environ.get(u'GOOGLE_APPLICATION_CREDENTIALS'):
            keyfile_path = environ.get(u'GOOGLE_APPLICATION_CREDENTIALS')
            credentials = Credentials.from_service_account_file(keyfile_path, scopes=scopes,
                                                                subject=u'vtertre@test.gpartner.eu')
        else:
            # service_account_id = u'cloud-storage-key-rotator@sandbox-vincent.iam.gserviceaccount.com'
            # storage_credentials = app_engine.Credentials(service_account_id=service_account_id)
            storage_credentials = app_engine.Credentials()
            storage_client = build(u'storage', u'v1', credentials=storage_credentials)
            key_data = storage_client.objects().get_media(bucket=u'sandbox-vincent.appspot.com',
                                                          object=u'keys/data-key.json').execute()
            keyfile_dict = loads(key_data)
            credentials = Credentials.from_service_account_info(keyfile_dict, scopes=scopes,
                                                                subject=u'vtertre@test.gpartner.eu')
        return build(u'admin', u'directory_v1', credentials=credentials)

    def __configure_commands(self, binder):
        command_handlers = self.__implementations_of(CommandHandler)
        binder.multibind(CommandHandlers, to=command_handlers, scope=singleton)
        binder.bind(CommandBus, scope=singleton)

    def __configure_queries(self, binder):
        query_handlers = self.__implementations_of(QueryHandler)
        binder.multibind(QueryHandlers, to=query_handlers, scope=singleton)
        binder.bind(QueryBus, scope=singleton)

    def __configure_resolvers(self, binder):
        resolvers = self.__implementations_of(ErrorResolver)
        binder.multibind(ErrorResolvers, to=resolvers, scope=singleton)

    def __implementations_of(self, clazz):
        query_handlers = []
        implementations = find_implementations_of(clazz)
        for implementation in implementations:
            logger.debug(u'Found implementation for %s => %s', clazz.__name__, implementation.__name__)
            query_handlers.append(self.__injector__.get(implementation))
        return query_handlers
