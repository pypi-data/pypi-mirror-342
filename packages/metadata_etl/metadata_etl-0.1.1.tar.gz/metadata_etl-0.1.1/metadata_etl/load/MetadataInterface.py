from http import HTTPStatus
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib.oauth2_session import OAuth2Session
import json
import inspect

from loguru import logger

import time
from datetime import datetime

from .defines import *

MODULE_NAME = DATA_GROUP_TYPE


class MetadataInterface:

    @staticmethod
    def build_fetch_token_kwargs(token_url, client_secret):
        return {
            'token_url': token_url,
            'client_secret': client_secret,
            'max_retries': MAX_RETRIES,
            'timeout': TIMEOUT,
            'verify': SSL_VERIFY
        }

    @staticmethod
    def build_app_urls(base_app_url):
        __suffix = {
            'base': '/',
            'token': 'oauth/token',
            'refresh': 'oauth/token',
            'authorize': 'oauth/authorize',
            'api': 'api',
        }
        base_url = base_app_url.rstrip('/')

        # dict([(x,y) for y,x in enumerate('cbad')])

        # return dict([{key : base_url + '/' +value} for key, value in __suffix])
        result_dict = {key + '_url': (base_url + '/' + value) for key, value in __suffix.items()}
        return result_dict

    @staticmethod
    def build_default_headers(client_email):
        return {
            'content-type': 'application/json',
            'Accept': 'application/json; version=1',
            'X-User-Email': client_email,
        }

    def __init__(self, client_id, client_secret, user_email, base_url, scope) -> None:

        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.user_email = user_email
        vars(self).update(MetadataInterface.build_app_urls(base_url))

        self.fetch_token_kwargs = MetadataInterface.build_fetch_token_kwargs(self.token_url, self.client_secret)
        self.headers = MetadataInterface.build_default_headers(self.user_email)

        self.oauth_client = BackendApplicationClient(self.client_id)

        self.oauth_session = OAuth2Session(client=self.oauth_client, scope=self.scope, auto_refresh_kwargs=self.fetch_token_kwargs)

    def get_session(self):
        self.oauth_session.fetch_token(**self.fetch_token_kwargs)
        return self.oauth_session

    def api_get(self, api_id, parameters={}):
        api_url = self.api_url + '/' + api_id + '/'
        kwargs = {'params': {'page': 1, 'page_size': -1}.update(parameters), 'allow_redirects': True}
        return self.get_session().get(api_url, headers=self.headers, **kwargs)

    def api_post(self, api_id, parameters={}):
        api_url = self.api_url + '/' + api_id + '/'

        kwargs = {'allow_redirects': True, "data": json.dumps(parameters), 'params': {'page': 1, 'page_size': -1, }}
        # kwargs = json.dumps(kwargs)
        # 'data_group_type': parameters |
        print(f'API URL: {api_url}')
        print(f'Input arguments: {parameters}')
        print(f'POST query arguments: {kwargs}')

        return self.get_session().post(api_url, headers=self.headers, **kwargs)

    def api_put(self, api_id, parameters={}):
        api_url = self.api_url + '/' + api_id + '/'
        kwargs = {'params': {'page': 1, 'page_size': -1}.update(parameters), 'allow_redirects': True}
        return self.get_session().put(api_url, **kwargs)

    def api_delete(self, api_id, parameters={}):
        api_url = self.api_url + '/' + api_id + '/' + str(parameters["id"])
        kwargs = {'allow_redirects': True, "data": json.dumps(parameters), 'params': {'page': 1, 'page_size': -1, }}
        return self.get_session().delete(api_url, headers=self.headers, **kwargs)


def default_headers(user_email):
    return {
        'content-type': 'application/json',
        'Accept': 'application/json; version=1',
    }


def log_debug(c_name, m_name, r_content):
    msg = '*** {0}.{1} (content) => {2}'.format(c_name, m_name, r_content)
    logger.debug(msg)


def string_to_json(hash_str):
    return {} if hash_str in ['', '[]'] else json.loads(hash_str)


def response_to_json(response):
    return string_to_json(response.content.decode('utf8'))


def load_json_from_headers(response):
    headers = {}
    if response.headers:
        headers['Date'] = response.headers.get('Date')
        headers['X-Total-Pages'] = response.headers.get('X-Total-Pages')
        headers['X-Count-Per-Page'] = response.headers.get('X-Count-Per-Page')
        headers['X-Current-Page'] = response.headers.get('X-Current-Page')
        headers['X-Total-Count'] = response.headers.get('X-Total-Count')
    return headers


class ActionType:
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    GET = 'GET'
    DELETE = 'DELETE'
    SET = 'SET'


def response_success(module_name, action, r_pagination, r_content):
    action_messages = {
        ActionType.CREATE: f'{module_name} created successfully',
        ActionType.UPDATE: f'{module_name} updated successfully',
        ActionType.GET: f'Got {module_name} successfully',
        ActionType.DELETE: f'{module_name} deleted successfully',
        ActionType.SET: f'{module_name} set successfully',
    }

    msg = action_messages.get(action, '')
    if not msg:
        return response_error(module_name, action, r_content)

    res = {
        'success': True,
        'info': msg,
        'app_info': {},
        'pagination': r_pagination,
        'data': r_content
    }

    logger.info(f'response_success => {res}')
    return res


def response_error(module_name, action, app_info):
    action_messages = {
        ActionType.CREATE: f'Error creating {module_name}',
        ActionType.UPDATE: f'Error updating {module_name}',
        ActionType.GET: f'Error getting {module_name}',
        ActionType.DELETE: f'Error deleting {module_name}',
        ActionType.SET: f'Error setting {module_name}',
    }

    msg = action_messages.get(action, 'ACTION is not correct!')
    res = {
        'success': False,
        'info': msg,
        'app_info': app_info,
        'pagination': {},
        'data': {}
    }

    logger.error('response_error => {res}')
    return res


def handle_response(response, action, success_code, module_name):
    content = response_to_json(response)
    pagination = load_json_from_headers(response)

    if response.status_code == HTTPStatus.NO_CONTENT and not content:
        formatted_response = response_success(module_name, action, pagination, content)
    elif response.status_code == success_code:
        if content or content == []:
            formatted_response = response_success(module_name, action, pagination, content)
        else:
            formatted_response = response_error(module_name, action, content)
    else:
        app_info = content.get('info', f'HTTP request status code: {response.status_code}')
        formatted_response = response_error(module_name, action, app_info)

    return formatted_response


def setup_oauth_session():
    fetch_token_kwargs = {
        'token_url': OAUTH_TOKEN_URL,
        'client_secret': OAUTH_USER_SECRET,
        'max_retries': MAX_RETRIES,
        'timeout': TIMEOUT,
        'verify': SSL_VERIFY
    }

    client = BackendApplicationClient(OAUTH_USER_ID)
    session = OAuth2Session(
        client=client,
        scope=OAUTH_SCOPE,
        auto_refresh_kwargs=fetch_token_kwargs
    )

    session.fetch_token(**fetch_token_kwargs)
    return session


def setupClient(app_info, user_info):
    logger.add("etl.log", rotation="500MB", level="DEBUG",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    logger.info("Setup metadata interface.")

    metadata_interface = MetadataInterface(app_info.id, app_info.secret, user_info.email, app_info.url, app_info.scope)
    logger.info("Retrieve information.")

    logger.info("Create new data group type.")

    data_group_type = {
        'data_group_type': {
            'name': "Space gate",
            'identifier': "SAGA",
            'flg_available': 'false',
            'description': 'desc 01'
        }
    }

    response = metadata_interface.api_post('data_group_types', data_group_type)  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)

    json_obj = json.loads(response.text) if len(response.text) else {}
    logger.info(json_obj)

    # time.sleep(5)

    data_group_type_id = json_obj['id']
    # data_group_type_id = 156
    logger.info(f"Delete existing data group type: {data_group_type_id}.")

    response = metadata_interface.api_delete('data_group_types', {"id": data_group_type_id})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})

    json_obj = json.loads(response.text) if len(response.text) else {}
    logger.info(json_obj)
    # logger.info (response.content)

    curr_method_name = inspect.currentframe().f_code.co_name
    log_debug(MODULE_NAME, curr_method_name, response)
    resp = handle_response(response, GET, OK, MODULE_NAME)

    json_obj = json.loads(response.text) if len(response.text) else {}

    logger.info(json_obj)
    logger.info(('resp: {0}'.format(resp)))

    return

    logger.info(json.dumps(MetadataInterface.build_app_urls(metadata_interface.base_url)))

    # Setup OAuth session
    # oauth_session = setup_oauth_session()

    headers = default_headers(OAUTH_USER_EMAIL)
    base_api_url = OAUTH_BASE_API_URL.rstrip('/') + '/'
    api_url = base_api_url + 'experiments/'

    kwargs = {'params': {'proposal_id': 4, 'page': 1, 'page_size': -1}, 'allow_redirects': True}
    response = oauth_session.get(api_url, headers=headers, **kwargs)

    logger.info('=' * 100)
