#!/usr/bin/python3

from utils.CommandLine import process_arguments
from extract.InputValidator import InputValidator
from extract.InputProcessor import InputProcessor
from extract.DataLoader import DataLoader
from transform.MetadataExtractor import MetadataExtractor
from utils.Trace import Trace, enable_trace
from utils.utils import load_data_from_file, resolve_unit_info, create_parameter_data, create_metadata_client, load_configuration
from utils.defines import STAT_OPERATORS
from loguru import logger
import json
from utils.DataView import H5FileView, H5JsonEncoder

from metadata_api import MetadataClient
from utils.defines import MAX_RETRIES, TIMEOUT, SSL_VERIFY

PROC_STAGE = ['config', 'extract', 'transform', 'load']


@enable_trace
def main(args=None):

    # Process the list of the command line arguments
    arguments = process_arguments()

    # Setup logger and trace
    logger.debug(f'Command line arguments: {arguments}')
    trace = Trace().setup(False)  # arguments.verbose

    proc_stage = arguments.stage
    try:
        app_info, user_info = load_configuration()
        if not (user_info and app_info):
            raise ValueError('Invalid application or user information')

        logger.info(f'Application info: {json.dumps(app_info, indent=4)}')
        logger.info(f'User info: {json.dumps(user_info, indent=4)}')

        logger.info(f'Connecting to Metadata service {app_info["url"]} ...')
        client_conn = create_metadata_client(app_info, user_info)
    except Exception as e:
        logger.error(e)
        return

    logger.info(f'Successfuly connected to Metadata service')

    # Dump data from MDC to JSON files
    #  dump_data_from_mdc(service_interface)

    proposal_number = arguments.proposal
    run_number = arguments.run

    try:
        proposal_info = client_conn.get_proposal_by_number_api(proposal_number).json()

        if 'id' not in proposal_info:
            raise ValueError(f"Unable to retrieve proposl info: {proposal_info}")

        proposal_id = proposal_info['id']
        logger.info(f'Proposal details by id ({proposal_id}):\n{json.dumps(proposal_info, indent=4)}')

        run_info = client_conn.get_runs_by_proposal_number_api(proposal_number, run_number).json()

        if 'runs' not in run_info:
            raise ValueError(run_info)  # ValueError(f"Unable to retrieve proposal info: {proposal_info}")

        run_id = run_info['runs'][0]['id']
        logger.info(f'Run details by id ({run_id}):\n{json.dumps(run_info, indent=4)}')

        try:
            logger.info("Retrieve run data using mdc client")
            run_info = client_conn.get_run_by_id_api(run_id).json()
            logger.info(f'Run details by id ({run_id}):\n{json.dumps(run_info, indent=4)}')
        except Exception as e:
            logger.error(e)

        logger.info(f'Run details by id:\n{json.dumps(run_info, indent=4)}')
        data_groups_repositories = run_info['data_groups_repositories']

        if isinstance(data_groups_repositories, list) and len(data_groups_repositories):
            data_group_id = data_groups_repositories[0]['id']

            logger.debug(f'Retrieve data group info {data_group_id}')
            data_group_info = client_conn.get_data_group_by_id_api(data_group_id).json()
            logger.info(f'Data group:\n{json.dumps(data_group_info, indent=4)}')

        data_group_parameters = []
        for id in data_group_info["parameter_ids"]:
            data_group_parameters.append(client_conn.get_parameter_by_id_api(id).json())

        data_files = client_conn.get_all_data_files_by_data_group_id_api(data_group_id).json()
        logger.debug(f"Data files:\n{json.dumps(data_files, indent=4)}")

        list_of_files = []
        for f in data_files:
            list_of_files.extend(eval(f['files']) if isinstance(f['files'], str) else f['files'])

        logger.info(f'Data files per group ({data_group_id}):\n{json.dumps(list_of_files, indent=4)}')

        prefix_path = data_group_info["prefix_path"]
        run_data_files = [prefix_path + f["relative_path"] for f in list_of_files]

        logger.info(f'Data files per run/data group ({run_number}/{data_group_id}):\n{json.dumps(run_data_files, indent=4)}')

    except Exception as e:
        logger.error(e)

    with open(arguments.data, 'r') as f:
        specs = json.load(f)

    if proc_stage == 'config':
        return

    logger.debug(f'Metadata specifications:\n{json.dumps(specs, indent=4)}')

    data_parameters = specs.get('parameters', {})
    data_attributes = specs.get('attributes', {})

    operators = set(specs.get('operators', STAT_OPERATORS))
    if "*" in operators:
        operators = STAT_OPERATORS

    parameters = InputValidator.validate_input(**dict(vars(arguments)))
    data_view = InputProcessor.process_input(parameters)

    logger.info(f'Data view: {json.dumps(data_view, indent=4)}')

    # ETL process for extracting metadata from HDF5 files

    # Extract (specific) data from files:
    data_loader = DataLoader(data_view)
    data = data_loader.process(data_parameters, data_attributes)

    # Transform data intp summary (metadata)
    metadata = MetadataExtractor(operators).process(data)

    logger.info(f'Metadata: {json.dumps(metadata, indent=4)}')

    if proc_stage == 'extract':
        return

    #  Load metadata into metadata catalog
    parameters = metadata['parameters']

    list_of_parameters = {}

    for key, value in parameters.items():
        attrs = value.get("attributes")
        list_of_parameters.update({attrs["device"] + '/' + attrs["name"]: key})

    logger.info(f"List of parameters from MDC: {json.dumps(data_group_parameters, indent=4)}")
    logger.debug(f"List of requested parameters: {json.dumps(list_of_parameters, indent=4)}")

    if proc_stage == 'transform':
        return

    units = client_conn.get_all_units_api(0).json()

    logger.info(f"Units:\n{units}")

    mdc_ops_summary = []

    for param in data_group_parameters:
        try:
            logger.debug(f'Process parameter:\n{json.dumps(param, indent=4)}')

            full_name = param["data_source"] + '/' + param["name"]
            if full_name in list_of_parameters:
                value = list_of_parameters[full_name]
                parameter_id = param["id"]
                param = parameters[value]
                data = param['data']
                attrs = param['attributes']

                unit_info = resolve_unit_info(units, attrs)
                attrs |= unit_info
                param = create_parameter_data(value, data, attrs)

                res = client_conn.update_parameter_api(parameter_id, param).json()
                if 'id' in res:
                    # logger.info(f'Updated parameter (id:{parameter_id}) successful:\n{json.dumps(res, indent=4)}')
                    mdc_ops_summary.append({"action": "update", "id": res["id"], "device": res["data_source"], "property": res["name"]})
                    list_of_parameters.pop(full_name)
                else:
                    raise RuntimeError(f'Update parameter (id:{parameter_id}) failed:\n{res}')
            else:
                trace(f"Delete parameter: {full_name}")
                parameter_id = param["id"]
                res = client_conn.delete_parameter_api(parameter_id)
                logger.info(f'Delete parameter ({param}):\n{res.status_code}')
                if res.status_code in [200, 204]:
                    mdc_ops_summary.append({"action": "delete", "id": param["id"], "device": param["data_source"], "property": param["name"]})
                else:
                    raise RuntimeError(f'Delete parameter (id:{parameter_id}) failed:\n{res}')
        except Exception as e:
            logger.warning(e)

    for key, value in list_of_parameters.items():
        param = parameters[value]
        trace(f"Add parameter: {key}\n{param}")

        data = param['data']
        attrs = param['attributes']
        unit_info = resolve_unit_info(units, attrs)
        attrs |= unit_info
        param = create_parameter_data(value, data, attrs)

        param['data_groups_parameters_attributes'] = [{'data_group_id': data_group_id}]
        # param['runs_parameters_attributes'] = [{'run_id': 2004}]

        res = client_conn.create_parameter_api(param).json()
        # logger.info(f'Insert parameter successful:\n{res}')
        mdc_ops_summary.append({"action": "create", "id": res["id"], "device": res["data_source"], "property": res["name"]})

    logger.info(f'Summary list of new/updated parameters:\n{json.dumps(mdc_ops_summary, indent=4)}')


if __name__ == "__main__":
    main()
