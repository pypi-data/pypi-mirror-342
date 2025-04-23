from loguru import logger

# Check if required libraries are imported
try:
    import pandas as pd
except ImportError:
    raise ImportError("Pandas library is required for this function.")

from utils.defines import Scope
from utils.Trace import enable_trace


class MetadataExtractor:

    def __init__(self, operators) -> None:
        self.operators = operators

    @enable_trace
    def process(self, data_view):

        #  trace(f'Data view : {data_view}')

        scope = data_view.get('scope', Scope.PROPOSAL)

        match scope:
            case Scope.RUN:
                runs = data_view['runs']
                for run in runs:
                    data = run['data']
                    run['parameters'] = MetadataExtractor.describe_data(data, self.operators)
                    del run['data']
            case Scope.FILE:
                data_files = data_view['files']
                for file in data_files:
                    data = file['data']
                    file['parameters'] = MetadataExtractor.describe_data(data, self.operators)
                    del file['data']

            case _:  # Scope.PROPOSAL
                data = data_view['data']
                data_view['parameters'] = MetadataExtractor.describe_data(data, self.operators)
                del data_view['data']

        return data_view

    @staticmethod
    def describe_data(datasets, operators):
        """
        Describe the given datasets and return the result as a dictionary.

        Parameters:
        - datasets (dict): A dictionary containing datasets, where keys are paths and values
                        are dictionaries with 'data' (numpy array) and 'metadata' keys.

        Returns:
        - dict: A dictionary with paths as keys and values as dictionaries containing
                'data' (descriptive statistics) and 'metadata'.
        """

        result = {}

        for path, data in datasets.items():
            df_describe = pd.DataFrame(data['data'])
            df_describe.dropna(inplace=True)
            percentiles = [.50]

            # Generate descriptive statistics and update the result dictionary
            desc = df_describe.describe(percentiles=percentiles).to_dict()[0]
            desc['med'] = desc['50%']
            del desc['50%']

            summary = {k: v for k, v in desc.items() if k in operators}

            result[path] = {'data': summary, 'attributes': data['attributes'], 'run_number': data['run_number'], 'proposal_number': data['proposal_number']}

        return result
