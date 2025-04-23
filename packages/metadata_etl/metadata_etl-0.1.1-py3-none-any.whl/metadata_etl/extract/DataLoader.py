from copy import deepcopy
from loguru import logger
import h5py as h5
import numpy as np

from utils.defines import Scope
from utils.Trace import enable_trace


class DataLoader:

    def __init__(self, data_view):
        self.data_view = data_view
        self.scope = data_view.get('scope', Scope.PROPOSAL)

    @enable_trace
    def process(self, data_parameters, data_attributes):
        """
        Load specified parameters and attributes for the data_view provided above.

        First, we validates the parameters, load the data and processes it accordingly
        based on the specified scope (RUN, FILE, or PROPOSAL).

        Parameters:
        - data_parameters (dict): Parameters specifying the list of parameters to extract from the files.
        - data_attributes (dict): Additional attributes associated with the data to be extracted also.

        Returns:
        dict: The raw data associated with each member of the list of data_parameters.

        """

        #  trace(f'Data parameters specs: {data_parameters}')

        validated_data_parameters = DataLoader.validate_data_parameters(data_parameters)
        logger.debug(f'Load data parameters: {validated_data_parameters}')

        match self.scope:
            case Scope.RUN:
                runs = self.data_view['runs']
                for run in runs:
                    data_files = run['files']
                    run['data'] = DataLoader.batch_process(data_files, validated_data_parameters, data_attributes)

            case Scope.FILE:
                data_files = self.data_view['files']
                for file in data_files:
                    file['data'] = DataLoader.process_file(file['file'], validated_data_parameters, data_attributes)

            case _:  # Scope.PROPOSAL
                data_files = self.data_view['files']
                self.data_view['data'] = DataLoader.batch_process(data_files, validated_data_parameters, data_attributes)

        return self.data_view

    @staticmethod
    def validate_data_parameters(data_parameters):
        required_keys = ['section', 'group', 'value']
        result = []

        for param in data_parameters:
            if not all(name in param for name in required_keys):
                raise ValueError(f"Wrong description of the parameter: {param}")

            value = param['value']

            if isinstance(value, str):
                result.append(param)
            elif isinstance(value, list):
                result.extend(deepcopy(param) | {'value': v} for v in value)
            else:
                raise TypeError(f"Value type error: {value}")

        return result

    @staticmethod
    def create_data_path(param_desc, has_value_suffix=True):
        """
        Create a data path based on the given parameter description.

        Parameters:
        - param_desc (dict): Dictionary containing 'section', 'group', and 'value'.
        - has_value (bool): Indicates whether to include '/value' as prefix to the path.

        Returns:
        - str: Constructed data path.
        """
        required_keys = ['section', 'group', 'value']
        if not all(name in param_desc for name in required_keys):
            raise ValueError("Wrong description of the parameter")

        section = param_desc['section']
        group = param_desc['group']
        value = param_desc['value']

        # value_suffix = '/value' if has_value_suffix else ''
        # return '{}/{}/{}/{}{}'.format(section, path, group, property_name, value_suffix)
        return f'{section}/{group}/{value}' + ('/value' if has_value_suffix else '')

    @staticmethod
    def process_file(filename, data_params, data_attributes):
        """
        Extract dataset from an HDF5 file based on the provided data parameters.

        Parameters:
        - filename (str): Path to the HDF5 file.
        - data_params (list): List of parameter descriptions for creating data paths.
        - data_attributes (list): List of attributes keys to extract for each dataset.

        Returns:
        - dict: Dictionary containing data paths, datasets, and attributes.
        """
        result = {}

        with h5.File(filename, 'r') as f:
            run_number = f["METADATA/runNumber"][()][0]
            proposal_number = f["METADATA/proposalNumber"][()][0]
            for param in data_params:
                try:
                    data_path = DataLoader.create_data_path(param)
                    if data_path not in f:
                        logger.warning(f"Dataset not found: {data_path}")
                        continue

                    dataset = f[data_path][()]

                    # Check if attributes exist before accessing
                    all_attrs = f[data_path].attrs if hasattr(f[data_path], 'attrs') else {}

                    # Extract dataset attribues based on data_attributes
                    attributes = {k: v for k, v in all_attrs.items() if k in data_attributes}

                    for k, v in {"section": "section", "device": "group", "name": "value"}.items():
                        attributes[k] = param[v]

                    #  trace(attributes)
                    # Update the result dictionary with both data and attributes
                    result[data_path] = {'data': dataset, 'attributes': attributes, 'run_number': run_number, 'proposal_number': proposal_number}
                except Exception as error:
                    logger.error(f'{error}. Dataset: {data_path}')

        return result

    @staticmethod
    def batch_process(data_files, data_params, data_attributes):
        """
        Aggregate datasets from multiple HDF5 files.

        Parameters:
        - data_files (list): List of file paths.
        - data_params (dict): List of parameters.
        - data_attributes (list): List of attributes to extract.

        Returns:
        - dict: Aggregated datasets.
        """
        # Use a list for temporary storage
        data_list = {}

        for param in data_params:
            data_path = DataLoader.create_data_path(param)
            data_list[data_path] = {'data': [], 'attributes': {}, 'run_number': None, 'proposal_number': None}

        for filename in data_files:
            data = DataLoader.process_file(filename, data_params, data_attributes)

            for p, v in data.items():
                data_list[p]['data'].append(v['data'])
                data_list[p]['attributes'] = v['attributes']
                data_list[p]['run_number'] = v['run_number']
                data_list[p]['proposal_number'] = v['proposal_number']

        result = {}
        for path, data in data_list.items():
            if not data['data']:
                continue
            aggregated_data = np.concatenate(data['data'])
            result.update({path: {'data': aggregated_data, 'attributes': data['attributes'], 'run_number': int(data['run_number']), 'proposal_number': int(data['proposal_number'])}})

        return result
