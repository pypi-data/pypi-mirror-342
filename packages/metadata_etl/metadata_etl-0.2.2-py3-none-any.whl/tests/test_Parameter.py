from extract.DataLoader import DataLoader
from mdc_api import connect_to_service, retrieve_units, retrieve_unit_info, ServiceInterface, inject_parameter, retrieve_parameter, delete_parameter
import unittest
import requests
from http import HTTPStatus

app_info = {
    "id": "6TqGFOWg0PzEXsHCs9baMmGQ7Hc6UhpU7YztJz7Y9OI",
    "secret": "N1_qi7Zt7ElHhJksM5ocnkGsvHS0jnp03WOMS9Hpzz8",
    "url": "https://192.168.56.101:3000/dev_metadata",
    "scope": ""
}

user_info = {
    "name": "Djelloul Boukhelef",
    "email": "djelloul.boukhelef@xfel.eu",
    "provider": "ldap",
    "uid": "boukhele"
}


class ParameterApiTest(unittest.TestCase):
    def setUp(self) -> None:
        # need to setup mdc for testing
        return
        self.service_interface = connect_to_service(app_info, user_info)
        self.client = self.service_interface.oauth_client
        self.session = self.service_interface.oauth_session
        assert (self.service_interface is not None)
        assert (self.client is not None)
        assert (self.session is not None)

        res = ServiceInterface.get_access_token(app_info["url"] + "/oauth/token", self.service_interface.client_id, self.service_interface.client_secret)
        assert (res.get("expires_in", None))

    def test_retrieve_units(self):
        # need to setup mdc for testing
        return
        service_interface = self.service_interface

        units = retrieve_units(service_interface)
        unit = retrieve_unit_info(service_interface, 10)

        assert unit['id'] == 10
        assert unit['name'] == "Hertz"
        assert unit['identifier'] == "HERTZ"
        assert unit['symbol'] == "Hz"

        assert unit in units

        unit = retrieve_unit_info(service_interface, 400)
        assert unit["info"] == "Resource not found!"

    def test_create_parameter(self):
        # need to setup mdc for testing
        return
        service_interface = self.service_interface
        parameter = {
            'data_source': 'MID/XTD9/XGM/MAIN/CAR',
            'name': 'Liquid velocity',
            'value': 445.6,
            'minimum': 305.0,
            'maximum': 1064.0,
            'mean': 750.5,
            'standard_deviation': 7.5,
            'data_type_id': 20,
            'parameter_type_id': 1,
            'unit_id': 1,
            'unit_prefix': '',
            'flg_available': True,
            'description': 'Dummy parameter for testing purpose only!!',
            'data_groups_parameters_attributes': [{'data_group_id': 4}]
            #  'runs_parameters_attributes': [{'run_id': 4}]
        }

        #  Test inject new parameter
        res = inject_parameter(service_interface, parameter)
        assert "id" in res
        parameter_id = res['id']

        #  Test retrieve new parameter
        parameter_data = retrieve_parameter(service_interface, parameter_id)

        assert parameter_id == parameter_data["id"]

        #  Test delete parameter
        res = delete_parameter(service_interface, parameter_id)
        assert res.status_code == HTTPStatus.NO_CONTENT

        #  Make sure that the parameter no longer exists after the deletion
        res = retrieve_parameter(service_interface, parameter_id)
        assert "id" not in res
        assert "info" in res
