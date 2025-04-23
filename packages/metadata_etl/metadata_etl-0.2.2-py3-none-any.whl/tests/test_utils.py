import unittest
from unittest.mock import mock_open, patch
from utils.utils import flatten_list, load_data_from_file, store_data_to_file, create_parameter_data, create_metadata_client

import json
from loguru import logger


class TestFlattenList(unittest.TestCase):
    def test_flat_list(self):
        self.assertEqual(flatten_list([1, 2, 3]), [1, 2, 3])

    def test_nested_list(self):
        self.assertEqual(flatten_list([1, [2, 3], 4]), [1, 2, 3, 4])

    def test_deeply_nested_list(self):
        self.assertEqual(flatten_list([1, [2, [3, [4, 5]], 6], 7]), [1, 2, 3, 4, 5, 6, 7])

    def test_empty_list(self):
        self.assertEqual(flatten_list([]), [])

    def test_list_with_empty_nested_lists(self):
        self.assertEqual(flatten_list([[], [1, [], 2], 3]), [1, 2, 3])

    def test_list_with_non_integer_elements(self):
        self.assertEqual(flatten_list(["a", ["b", ["c"]], "d"]), ["a", "b", "c", "d"])

    def test_list_with_mixed_data_types(self):
        self.assertEqual(flatten_list([1, ["a", [3.14, [True]]], None]), [1, "a", 3.14, True, None])

    def test_lists_with_concatenations(self):

        l1 = [1, 2, 3, 4]
        l2 = ['a', l1, 'b']
        l3 = ['x', l2, 'y', l1, 'z']
        l4 = [[l1, [l2, [l3]]], [[[l1], l2], l3]]

        fl1 = flatten_list(l1)
        fl2 = flatten_list(l2)
        fl3 = flatten_list(l3)
        fl4 = flatten_list(l4)

        self.assertEqual(fl1, l1)
        self.assertEqual(fl2, ['a'] + fl1 + ['b'])
        self.assertEqual(fl3, ['x'] + fl2 + ['y'] + fl1 + ['z'])
        self.assertEqual(fl4, fl1 + fl2 + fl3 + fl1 + fl2 + fl3)


class TestLoadStoreDataFromAndToFile(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_valid_json_file(self, mock_file):
        self.assertEqual(load_data_from_file("dummy.json"), {"key": "value"})

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("loguru.logger.error")
    def test_invalid_json_file(self, mock_logger, mock_file):
        self.assertIsNone(load_data_from_file("dummy.json"))
        mock_logger.assert_called()

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    @patch("loguru.logger.error")
    def test_file_not_found(self, mock_logger, mock_file):
        self.assertIsNone(load_data_from_file("nonexistent.json"))
        mock_logger.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data='{"name": "Dj", "age": 76, "height":12345}')
    def test_store_data_to_file(self, mock_file):
        data = {"name": "Dj", "age": 76, "height": 12345}
        store_data_to_file(data, "test.json")
        mock_file.assert_called_once_with("test.json", 'w', encoding='utf-8')
        handle = mock_file()
        handle.write.assert_called()
        self.assertEqual(load_data_from_file("test.json"), data)


class TestCreateParameterData(unittest.TestCase):
    @patch("loguru.logger.warning")
    @patch("loguru.logger.error")
    def test_create_parameter_data_valid(self, mock_error, mock_warning):
        key = "param1"
        data = {'med': 50, 'min': 40, 'max': 60, 'mean': 50, 'std': 5}
        attrs = {'device': 'DS/1', 'name': 'Temperature', 'unit_id': 1, 'unit_prefix_name': 'C', 'alias': 'Temp'}

        expected = {
            'data_source': 'DS/1', 'name': 'Temperature', 'value': 50, 'minimum': 40, 'maximum': 60,
            'mean': 50, 'standard_deviation': 5, 'data_type_id': 20, 'parameter_type_id': 1, 'unit_id': 1,
            'unit_prefix': 'C', 'flg_available': True, 'description': 'Temp'
        }

        result = create_parameter_data(key, data, attrs)

        self.assertEqual(result, expected)
        mock_warning.assert_not_called()  # No warning should be logged
        mock_error.assert_not_called()  # No error should be logged

    @patch("loguru.logger.warning")
    @patch("loguru.logger.error")
    def test_create_parameter_data_invalid_mean(self, mock_error, mock_warning):
        key = "param2"
        data = {'med': 45, 'min': 40, 'max': 60, 'mean': 70, 'std': 5}
        attrs = {'device': 'DS/2', 'name': 'Pressure', 'unit_id': 2, 'unit_prefix_name': 'Pa', 'alias': 'Pres'}

        expected = {
            'data_source': 'DS/2', 'name': 'Pressure', 'value': 45, 'minimum': 40, 'maximum': 60,
            'mean': 45, 'standard_deviation': 5, 'data_type_id': 20, 'parameter_type_id': 1, 'unit_id': 2,
            'unit_prefix': 'Pa', 'flg_available': True, 'description': 'Pres'
        }

        result = create_parameter_data(key, data, attrs)

        self.assertEqual(result, expected)
        mock_warning.assert_called()  # Warning should be logged
        mock_error.assert_not_called()  # No error should be logged

    @patch("loguru.logger.warning")
    @patch("loguru.logger.error")
    def test_create_parameter_data_with_error(self, mock_error, mock_warning):
        key = "param3"
        data = {'med': 30, 'min': 20, 'max': 40, 'mean': 30, 'std': 2}
        attrs = {'device': 'DS/3', 'name': 'Humidity', 'unit_id': 3, 'unit_prefix_name': 'g/m³'}

        # Simulate an error scenario where 'device' attribute is missing
        attrs_missing = {'name': 'Humidity', 'unit_id': 3, 'unit_prefix_name': 'g/m³'}

        # This should raise an error due to missing 'device' in attrs
        result = create_parameter_data(key, data, attrs_missing)

        self.assertIsNone(result)  # The result should be None because of the error
        mock_warning.assert_not_called()  # No warning should be logged
        mock_error.assert_called()  # An error should be logged


if __name__ == "__main__":
    unittest.main()
