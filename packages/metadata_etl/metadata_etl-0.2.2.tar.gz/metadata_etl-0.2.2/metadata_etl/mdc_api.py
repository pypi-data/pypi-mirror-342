from loguru import logger
from load.ServiceInterface import ServiceInterface
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def retrieve_proposal_info_by_number(service_interface, proposal_numer):
    response = service_interface.api_get(f'proposals/by_number/{proposal_numer}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def retrieve_proposal_info_by_id(service_interface, proposal_id):
    response = service_interface.api_get(f'proposals/{proposal_id}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def retrieve_run_info(service_interface, proposal_id, run_number):
    response = service_interface.api_get(f'proposals/by_number/{proposal_id}/runs/{run_number}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def retrieve_run_info_by_id(service_interface, run_id):
    response = service_interface.api_get(f'runs/{run_id}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def fetch_all_parameters(service_interface):
    response = []


# /dev_metadata/proposals/:proposal_id/runs/:id/parameters
def fetch_all_records(service_interface, api_id):
    response = []

    for page in range(1, 100):
        res = service_interface.api_get(api_id, {'page': page, 'page_size': -1})

        try:
            lst = res.json()
            if isinstance(lst, list) and len(lst):
                response.extend(lst)
            else:
                break
        except (ValueError, TypeError):
            break

    return response


def extract_parameters_with_data_groups(parameters, key="data_groups_parameters"):
    return [param for param in parameters if isinstance(param[key], list) and len(param[key])]


def extract_parameters_by_data_group_id(parameters, data_group_id, key="data_groups_parameters"):
    return [param for param in parameters if isinstance(param[key], list) and len(param[key]) > 0 and param[key][0]['data_group_id'] == data_group_id]


def extract_files_by_data_group_id(files, data_group_id, key="data_group_id"):
    return [file for file in files if file[key] == data_group_id]


def retrieve_units(service_interface):
    response = service_interface.api_get(f'units')
    return response.json()


def retrieve_unit_info(service_interface, unit_id):
    response = service_interface.api_get(f'units/{unit_id}')
    return response.json()


def inject_parameter(service_interface, parameter):
    response = service_interface.api_post('parameters', parameter)
    # print(response)
    return response.json()


def retrieve_parameter(service_interface, parameter_id):
    # response = service_interface.api_get(f'../proposals/{proposal_id}/runs/{run_id}/data_groups', {'run_id': run_id}) # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    response = service_interface.api_get(f'parameters/{parameter_id}')  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def update_parameter(service_interface, parameter_id, parameter):
    # response = service_interface.api_get(f'../proposals/{proposal_id}/runs/{run_id}/data_groups', {'run_id': run_id}) # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    response = service_interface.api_put(f'parameters/{parameter_id}', parameter)  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def delete_parameter(service_interface, parameter_id):
    response = service_interface.api_delete(f'parameters', {'id': parameter_id})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response  # .json()


def inject_run_paramter(service_interface, run_id, parameter_id):
    return {}


def get_proposal_details(proposal_number):
    pass


def retrieve_data_group(service_interface, data_group_id):
    response = service_interface.api_get(f'data_groups/{data_group_id}')  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    return response.json()


def connect_to_service(app_info, user_info):
    service_interface = ServiceInterface(app_info['id'], app_info['secret'], user_info['email'], app_info['url'], app_info['scope'])

    auth = HTTPBasicAuth(app_info['id'], app_info['secret'])

    return service_interface
    req_proposal = {
        'number': 990390
    }

    response = service_interface.api_get(f'proposals/by_number/{2}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)
    trace(json.dumps(json.loads(response.text), indent=4))

    response = service_interface.api_get(f'proposals/by_number/{2}/runs', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)
    trace(json.dumps(json.loads(response.text), indent=4))

    response = service_interface.api_get(f'proposals/by_number/{2}/runs/{3}', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)
    trace(json.dumps(json.loads(response.text), indent=4))

    parameter = {
        'parameter': {
            'data_source': 'MID/XTD9/XGM/MAIN/DESY',
            'name': 'PhotonFlux',
            'value': 15.6,
            'minimum': 35.0,
            'maximum': 106.0,
            'mean': 45.5,
            'standard_deviation': 7.5,
            'data_type_id': 20,
            'parameter_type_id': 1,
            'unit_id': 1,
            'unit_prefix': '',
            'flg_available': True,
            'description': 'desc 01'
        }
    }

    response = service_interface.api_post('parameters', parameter)  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)
    trace(json.dumps(json.loads(response.text), indent=4))

    response = service_interface.api_get(f'parameters', {})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)
    trace(json.dumps(json.loads(response.text), indent=4))

    return

    data_group_type = {
        'data_group_type': {
            'name': "Gamma",
            'identifier': "GAMMA",
            'flg_available': 'false',
            'description': 'desc 01'
        }
    }

    response = service_interface.api_post('data_group_types', data_group_type)  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})
    logger.info(response.content)

    json_obj = json.loads(response.text) if len(response.text) else {}
    logger.info(json_obj)
    data_group_type_id = json_obj['id']
    # data_group_type_id = 156
    logger.info(f"Delete existing data group type: {data_group_type_id}.")

    response = service_interface.api_delete('data_group_types', {"id": data_group_type_id})  # {'data_source': "data_source", 'name': "name"}) #, {'proposal_id': 4})

    json_obj = json.loads(response.text) if len(response.text) else {}
    logger.info(json_obj)
    # logger.info (response.content)

    curr_method_name = inspect.currentframe().f_code.co_name
    trace(f'{MODULE_NAME}.{curr_method_name} ==> {response}')

    resp = handle_response(response, GET, OK, MODULE_NAME)

    json_obj = json.loads(response.text) if len(response.text) else {}

    logger.info(json_obj)

    logger.info(('resp: {0}'.format(resp)))
