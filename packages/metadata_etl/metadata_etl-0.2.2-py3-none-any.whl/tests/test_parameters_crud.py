
import unittest

from utils.utils import create_parameter_data, create_metadata_client, fetch_proposal_details, fetch_run_details
from unittest.mock import mock_open, patch
from .secrets import *
from metadata_api import MetadataClient
from loguru import logger
from .mdc_api_responses_mock import *
import json

import unittest
from unittest.mock import MagicMock, patch

# Import the function from your module
# from your_module import fetch_proposal_details


class TestFetchProposalDetails(unittest.TestCase):

    def setUp(self):
        """Set up common test data."""
        self.mock_client = MagicMock()  # Mock the client connection
        self.client_api = MagicMock()  # create_metadata_client(APP_INFO, USER_INFO)
        self.proposal_number = 900390
        self.run_number = 704

    def test_fetch_proposal_details_valid(self):
        """Test fetch_proposal_details with a valid proposal response."""
        proposal_number = "12345"
        expected_response = proposal_info_response  # {"id": 1, "name": "Test Proposal", "status": "Approved"}

        # Mock the API call response
        self.mock_client.get_proposal_by_number_api.return_value.json.return_value = expected_response

        result = fetch_proposal_details(self.mock_client, proposal_number)

        self.mock_client.get_proposal_by_number_api.assert_called_once_with(proposal_number)
        self.assertEqual(result, expected_response)

    def test_fetch_proposal_details_valid_api(self):
        """Test fetch_proposal_details with a valid proposal response."""
        # Mock the API call response
        res_api = self.client_api.get_proposal_by_number_api(self.proposal_number).json()

        self.proposal_details = fetch_proposal_details(self.client_api, self.proposal_number)
        self.assertIsNotNone(self.proposal_details)

        self.assertEqual(res_api, self.proposal_details)

    def test_fetch_proposal_details_valid_api(self):
        expected_response = run_info_response
        self.mock_client.get_runs_by_proposal_number_api.return_value.json.return_value = proposal_runs_response
        self.mock_client.get_run_by_id_api.return_value.json.return_value = run_info_response
        self.run_info = fetch_run_details(self.mock_client, self.proposal_number, self.run_number)
        self.assertIsNotNone(self.run_info)
        self.assertEqual(self.run_info, expected_response)

        return
        self.mock_client.get_proposal_by_number_api.assert_called_once_with(proposal_number)
        self.assertEqual(result, expected_response)

    # @patch('loguru.logger.error')  # Mock logger to prevent real logging
    # def test_fetch_proposal_details_missing_id(self, mock_error):
    #     """Test when 'id' is missing from the API response."""
    #     proposal_number = "67890"
    #     error_response = {"info": f"Proposal number {proposal_number} not found"}

    #     # Mock API call returning an invalid response (missing 'id')
    #     self.mock_client.get_proposal_by_number_api.return_value.json.return_value = error_response
    #     # ex = ValueError(error_response["info"])

    #     # with self.assertRaises(ValueError) as context:
    #     result = fetch_proposal_details(self.mock_client, proposal_number)

    #     #self.assertEqual(str(context.exception), error_response["info"])
    #     self.mock_client.get_proposal_by_number_api.assert_called_once_with(proposal_number)
    #     mock_error.assert_called_once()
    #     self.assertIsNone(result)

    @patch('loguru.logger.error')  # Mock logger to prevent real logging
    def test_fetch_proposal_details_exception_handling(self, mock_error):
        """Test fetch_proposal_details when an exception occurs."""
        proposal_number = "9999999"

        error_response = {"info": f"Proposal number {proposal_number} not found"}

        # Mock API call raising an exception, proposal not found
        self.mock_client.get_proposal_by_number_api.side_effect = ValueError(error_response["info"])

        result = fetch_proposal_details(self.mock_client, proposal_number)

        self.mock_client.get_proposal_by_number_api.assert_called_once_with(proposal_number)
        # mock_error.error.assert_called_once()
        print("Calls are: ", mock_error.mock_calls)

        calls = mock_error.mock_calls
        assert len(calls) == 1
        # Unpack call
        function_called, args, kwargs = calls[0]
        # assert(function_called == "error")
        value_error = args[0]

        assert isinstance(value_error, ValueError)
        assert value_error.args[0] == error_response["info"]

        self.assertIsNone(result)


class TestParameterCRUD(unittest.TestCase):

    def setUp(self):
        self.mock_client_api = MagicMock()
        self.client_api = create_metadata_client(APP_INFO, USER_INFO)

    def tearDown(self):
        pass  # cls.client_api.destroy()

    @staticmethod
    def create_dummy_parameter(key):
        data = {'count': 6000.0,
                'mean': 111.57698059082031,
                'std': 2.211357831954956,
                'min': 106.80351257324219,
                'max': 116.29515075683594,
                'med': 111.6604995727539}

        attrs = {
            'device': key,
            'name': 'Test device',
            'unit_id': '12',
            'unit_prefix_name': '',
            'alias': "test device",
        }

        return create_parameter_data(key, data, attrs)

    @patch("loguru.logger.warning")
    @patch("loguru.logger.error")
    def test_inject_parameter(self, mock_error, mock_warning):
        self.client_api = create_metadata_client(APP_INFO, USER_INFO)
        self.assertIsNotNone(self.client_api)  # The result should be None because of the error
        param = self.create_dummy_parameter("LOCATION/CLASS/PARAM/00")
        expected_result = {"id": int()} | param

        self.mock_client_api.get_all_units_api.return_value.json.return_value = get_all_units_reponse
        units = self.client_api.get_all_units_api(0).json()
        self.assertIsNotNone(units)  # The units should not be None

        self.assertIsNotNone(param)  # The result should be None because of the error

        self.mock_client_api.create_parameter_api.return_value.json.return_value = expected_result
        res = self.client_api.create_parameter_api(param).json()
        print(json.dumps(res, indent=4))
        print(json.dumps(param, indent=4))

        self.assertIsNotNone(res)  # The result should be None because of the error
        mock_warning.assert_not_called()  # No warning should be logged
        mock_error.assert_not_called()  # An error should be logged

        assert 'id' in res
        param_id = res['id']
        res = self.client_api.get_parameter_by_id_api(param_id)
        res = self.client_api.delete_parameter_api(param_id)
        res = self.client_api.get_parameter_by_id_api(param_id)


if __name__ == "__main__":
    unittest.main()
