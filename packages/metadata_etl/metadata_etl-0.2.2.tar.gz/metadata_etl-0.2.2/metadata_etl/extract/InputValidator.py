import os
from pathlib import Path
from utils.utils import flatten_list


def MSG_FILE_NOT_FOUND(name, obj):
    return f'{name} does not exist or it is not a directory: {obj}'


class InputValidator:
    INVALID_VALUE = -1

    @staticmethod
    def validate_input(base_folder, scope, proposal, run=None, files=[], **kwargs):

        data_view = {'scope': scope}

        # If the base folder is not specified then use the current working directory,
        # Otherwise make sure that the base folder exist and is a folder
        base_folder = Path(base_folder or os.getcwd()).resolve()
        if not base_folder.is_dir():
            raise FileNotFoundError(MSG_FILE_NOT_FOUND('Base folder', base_folder))

        data_view["base_folder"] = str(base_folder)

        # Validata the proposal information
        proposal = InputValidator.validate_numerical_input(proposal, 'p')

        if proposal == InputValidator.INVALID_VALUE:
            raise ValueError(f'Invalid proposal number')

        # Construct data path
        if proposal is not None:
            # proposal = f'p{proposal}'
            data_path = base_folder / f'p{proposal}' / 'raw'

            # Make sure that the proposal folder exists
            if not data_path.is_dir():
                raise FileNotFoundError(MSG_FILE_NOT_FOUND('Proposal folder', data_path))

            data_view["proposal_number"] = proposal
        else:
            data_path = base_folder

        data_view["data_path"] = str(data_path)

        # Validate and construct runs list
        if run is not None:
            # Validate the run information
            run = InputValidator.validate_numerical_input(run, 'r')

            if run == InputValidator.INVALID_VALUE:
                raise ValueError(f'Invalid run number')

            path_list = [data_path / f'r{run:04}']
        else:
            # Scan all run folders within the data path
            path_list = [f for f in data_path.iterdir()
                         if InputValidator.validate_numerical_input(f.stem, 'r') != InputValidator.INVALID_VALUE]

        data_view['runs'] = [{'run_number': path.stem,
                              'path': str(path),
                              'files': InputValidator.discover_run_data(path)
                              } for path in path_list if path.is_dir()]

        # Make sure that all specified files exists
        # Filter and remove duplicate file paths
        data_view['files'] = list(set(f for f in files if Path(f).is_file())) if files is not None else []

        return data_view

    @staticmethod
    def discover_all_run_data(data_view):
        for run in data_view['runs']:
            run['data_files'] = [str(f) for f in list(Path(f'{run["path"]}').rglob("*.h5"))]

    @staticmethod
    def discover_run_data(path, pattern='*.h5'):
        return [str(f) for f in list(Path(path).rglob(pattern))]

    @staticmethod
    def validate_numerical_input(val, prefix='', type=int):
        """
        Validates and extracts an integer input after removing a specified prefix.

        Parameters:
        - val: The input value to be validated (can be any type).
        - prefix: The prefix to be removed from the input value (default is an empty string).

        Returns:
        - An integer if the modified input consists only of digits, otherwise returns None.
        """
        if val is None:
            return None
        # Convert the input value to a string
        tmp = str(val)

        # Check if the string starts with the specified prefix
        if tmp.startswith(prefix):
            # If it does, remove the prefix
            tmp = tmp[len(prefix):]

        # Check if the modified string consists only of digits
        return type(tmp) if tmp.isdigit() else InputValidator.INVALID_VALUE
