
proposal_info_response = {
    "id": 923,
    "number": 900390,
    "title": "FXE commissioning",
    "abstract": None,
    "proposal_folder": "p900390",
    "def_proposal_path": "/gpfs/exfel/exp/FXE/202331/p900390/raw",
    "doi": "10.22003/XFEL.EU-DATA-900390-00",
    "url": None,
    "instrument_id": 2,
    "instrument_cycle_id": 341,
    "principal_investigator_id": 658,
    "main_proposer_id": 180,
    "local_contact_id": 180,
    "local_data_contact_id": None,
    "experiment_data_contact_id": 180,
    "orig_repository_id": 103,
    "last_run": 704,
    "begin_at": "2023-07-01T00:02:00.000+02:00",
    "end_at": "2025-01-31T23:58:00.000+01:00",
    "release_at": "2028-12-31T23:58:00.000+01:00",
    "num_delivered_shifts": None,
    "num_preparation_shifts": None,
    "flg_public": False,
    "flg_proposal_system": "L",
    "flg_preferred_data_output": "P",
    "flg_available": True,
    "flg_auto_run_quality": 1,
    "flg_beamtime_status": "R",
    "beamtime_start_at": None,
    "beamtime_end_at": None,
    "flg_cloneable_status": "SC",
    "flg_data_archived_notification": "R",
    "expected_data_archive_at": "2027-02-12T00:00:00.000+01:00",
    "data_archived_at": None,
    "description": None,
    "data_plan_comments": None,
    "flg_visibility_status": "",
    "logbook_info": {
    },
    "beamtimes": [
        {
            "id": 1064,
            "begin_at": "2023-07-01T00:02:00.000+02:00",
            "end_at": "2026-12-31T23:58:00.000+01:00",
            "flg_available": True,
            "description": None
        }
    ],
    "instrument_identifier": "FXE",
    "meeting": None,
    "team": [
        {
            "id": 19191,
            "user_id": 1234,
            "data_access_role": 1,
            "flg_lab_access": False,
            "flg_support": False
        },
    ],
    "users_ids": [
        [
            1234,
            "jbald",
            "ldap"
        ],
    ],
    "openly_released_at": None,
    "techniques": [],
    "users_info": [
        {
            "user_id": 1234,
            "data_access_role": 2,
            "flg_lab_access": False,
            "flg_support": False,
            "uid": "jbald",
            "provider": "ldap",
            "name": "John Bald",
            "email": "jonh.bald@example.com",
            "flg_upex_acceptances": True
        },
    ]
}


proposal_runs_response = {
    "proposal": {
        "id": 923,
        "number": 900390,
        "title": "FXE commissioning"
    },
    "runs": [
        {
            "id": 214026,
            "run_number": 704,
            "run_folder": "r0704",
            "run_alias": "",
            "experiment_id": 4462,
            "sample_id": 4962,
            "begin_at": "2024-01-31T13:30:27.000+01:00",
            "end_at": "2024-01-31T13:31:04.000+01:00",
            "first_train": 1919430548,
            "last_train": 1919430895,
            "flg_available": True,
            "flg_status": 2,
            "original_format": "",
            "system_msg": "",
            "description": "",
            "created_at": "2024-01-31T13:30:27.000+01:00",
            "updated_at": "2024-01-31T13:33:26.000+01:00",
            "flg_run_quality": 1,
            "size": 5779619840,
            "num_files": 34,
            "flg_cal_data_status": "E",
            "cal_pipeline_reply": "Succeeded: none; Failed: FXE_DET_LPD1M-1",
            "migration_request_at": "2024-01-31T13:31:38.000+01:00",
            "migration_begin_at": "2024-01-31T13:31:48.000+01:00",
            "migration_end_at": "2024-01-31T13:32:07.000+01:00",
            "cal_num_requests": 1,
            "cal_last_request_at": "2024-01-31T13:31:38.000+01:00",
            "cal_last_begin_at": "2024-01-31T13:32:11.000+01:00",
            "cal_last_end_at": "2024-01-31T13:33:26.000+01:00",
            "flg_auto_run_quality": None,
            "run_technique_snapshot": None,
            "cal_input_path": None,
            "cal_output_path": None,
            "repositories": {
                "XFEL_GPFS_OFFLINE_RAW_CC": {
                    "identifier": "XFEL_GPFS_OFFLINE_RAW_CC",
                    "name": "XFEL GPFS offline Raw data in DESY CC",
                    "mount_point": "/gpfs/exfel/d/raw",
                    "data_groups": 1,
                    "flg_available": False
                },
                "DESY_DCACHE_RAW_CC": {
                    "identifier": "DESY_DCACHE_RAW_CC",
                    "name": "dCache Raw Data in DESY CC",
                    "mount_point": "/pnfs/desy.de/exfel/archive/XFEL/raw",
                    "data_groups": 1,
                    "flg_available": True
                }
            }
        }
    ]
}


run_info_response = {
    "id": 214026,
    "run_number": 704,
    "run_folder": "r0704",
    "run_alias": "",
    "experiment_id": 4462,
    "sample_id": 4962,
    "begin_at": "2024-01-31T13:30:27.000+01:00",
    "end_at": "2024-01-31T13:31:04.000+01:00",
    "first_train": 1919430548,
    "last_train": 1919430895,
    "migration_request_at": "2024-01-31T13:31:38.000+01:00",
    "migration_begin_at": "2024-01-31T13:31:48.000+01:00",
    "migration_end_at": "2024-01-31T13:32:07.000+01:00",
    "flg_available": True,
    "flg_status": 2,
    "flg_run_quality": 1,
    "size": 5779619840,
    "num_files": 34,
    "flg_cal_data_status": "E",
    "cal_pipeline_reply": "Succeeded: none; Failed: FXE_DET_LPD1M-1",
    "cal_num_requests": 1,
    "cal_last_request_at": "2024-01-31T13:31:38.000+01:00",
    "cal_last_begin_at": "2024-01-31T13:32:11.000+01:00",
    "cal_last_end_at": "2024-01-31T13:33:26.000+01:00",
    "original_format": "",
    "system_msg": "",
    "description": "",
    "experiment": {
        "id": 4462,
        "name": "Test DAQ",
        "doi": "xfel.mdc.exp.4462",
        "abstract": None,
        "experiment_folder": "e0001",
        "experiment_type_id": 10,
        "proposal_id": 923,
        "first_prefix_path": "/gpfs/exfel/exp/FXE/202331/p900390/raw/e0001/",
        "flg_available": True,
        "publisher": "XFEL",
        "contributor": "XFEL",
        "description": None
    },
    "sample": {
        "id": 4962,
        "name": "No sample",
        "url": None,
        "sample_type_id": 7,
        "flg_proposal_system": None,
        "proposal_system_id": None,
        "flg_available": True,
        "description": None
    },
    "data_groups_repositories": [
        {
            "id": 213902,
            "name": "raw_e0001_n0489",
            "language": "en",
            "doi": "xfel.mdc.dg.213902",
            "format": "",
            "data_passport": "",
            "experiment": {
                "id": 4462,
                "name": "Test DAQ",
                "doi": "xfel.mdc.exp.4462"
            },
            "data_group_type": {
                "id": 1,
                "name": "Raw",
                "identifier": "RAW"
            },
            "repositories": [
                {
                    "id": 11,
                    "name": "XFEL GPFS offline Raw data in DESY CC",
                    "identifier": "XFEL_GPFS_OFFLINE_RAW_CC",
                    "mount_point": "/gpfs/exfel/d/raw",
                    "transfer_agent_identifier": "offline_raw",
                    "transfer_agent_server_url": None,
                    "flg_context": "Global",
                    "flg_available": True,
                    "rank": 11,
                    "data_group_type_id": 1,
                    "description": "European XFEL GPFS offline Raw Data instance in DESY Computer Center"
                },
                {
                    "id": 21,
                    "name": "dCache Raw Data in DESY CC",
                    "identifier": "DESY_DCACHE_RAW_CC",
                    "mount_point": "/pnfs/desy.de/exfel/archive/XFEL/raw",
                    "transfer_agent_identifier": "dcache_raw",
                    "transfer_agent_server_url": "",
                    "flg_context": "Global",
                    "flg_available": True,
                    "rank": 21,
                    "data_group_type_id": 1,
                    "description": "DESY dCACHE Raw Data instance in DESY Computer Center"
                }
            ]
        }
    ],
    "techniques": [],
    "raw_repositories": [
        {
            "id": 11,
            "name": "XFEL GPFS offline Raw data in DESY CC",
            "identifier": "XFEL_GPFS_OFFLINE_RAW_CC",
            "img_url": "https://in.xfel.eu/metadata/assets/repos_host_logo/desy_logo_rgb-911077061ae7089b93c512ee0a396e4139e0a4d9dff3cf23fcb4d2a7f44eaf3b.jpg",
            "transfer_agent_identifier": "offline_raw",
            "transfer_agent_server_url": None,
            "mount_point": "/gpfs/exfel/d/raw",
            "flg_available": True,
            "flg_context": "Global",
            "data_group_type_id": 1,
            "rank": 11,
            "description": "European XFEL GPFS offline Raw Data instance in DESY Computer Center"
        },
        {
            "id": 21,
            "name": "dCache Raw Data in DESY CC",
            "identifier": "DESY_DCACHE_RAW_CC",
            "img_url": "https://in.xfel.eu/metadata/assets/repos_host_logo/desy_logo_rgb-911077061ae7089b93c512ee0a396e4139e0a4d9dff3cf23fcb4d2a7f44eaf3b.jpg",
            "transfer_agent_identifier": "dcache_raw",
            "transfer_agent_server_url": "",
            "mount_point": "/pnfs/desy.de/exfel/archive/XFEL/raw",
            "flg_available": True,
            "flg_context": "Global",
            "data_group_type_id": 1,
            "rank": 21,
            "description": "DESY dCACHE Raw Data instance in DESY Computer Center"
        }
    ],
    "reports": [
        {
            "id": 41,
            "name": "FXE_DET_LPD1M-1_correct_900390_r0704_240131_123138_453943.pdf",
            "cal_report_path": "/gpfs/exfel/exp/FXE/202331/p900390/usr/Reports/r0704/",
            "cal_report_at": "2024-01-31T13:31:38.453+01:00",
            "run_id": 214026,
            "description": "FXE_DET_LPD1M-1 detector corrections (errors occurred)"
        }
    ]
}


get_all_units_reponse = [{'id': 1, 'name': 'Number', 'identifier': 'NUMBER', 'symbol': '№', 'origin': 'Other', 'flg_available': True, 'description': 'Values without a clearly defined unit'}, {'id': 2, 'name': 'Count', 'identifier': 'COUNT', 'symbol': '#', 'origin': 'Other', 'flg_available': True, 'description': 'Counters, iteration variable'}, {'id': 3, 'name': 'Meter', 'identifier': 'METER', 'symbol': 'm', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of length'}, {'id': 4, 'name': 'Gram', 'identifier': 'GRAM', 'symbol': 'g', 'origin': 'SI base unit Kg * 0.001', 'flg_available': True, 'description': 'Unit of mass'}, {'id': 5, 'name': 'Second', 'identifier': 'SECOND', 'symbol': 's', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of time'}, {'id': 6, 'name': 'Ampere', 'identifier': 'AMPERE', 'symbol': 'A', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of electric current'}, {'id': 7, 'name': 'Kelvin', 'identifier': 'KELVIN', 'symbol': 'K', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of thermodynamic temperature'}, {'id': 8, 'name': 'Mole', 'identifier': 'MOLE', 'symbol': 'mol', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of amount of substance'}, {'id': 9, 'name': 'Candela', 'identifier': 'CANDELA', 'symbol': 'cd', 'origin': 'SI base unit', 'flg_available': True, 'description': 'Unit of luminous intensity'}, {'id': 10, 'name': 'Hertz', 'identifier': 'HERTZ', 'symbol': 'Hz', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of frequency (s-1)'}, {'id': 11, 'name': 'Radian', 'identifier': 'RADIAN', 'symbol': 'rad', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of plane angle (2D angle)'}, {'id': 12, 'name': 'Degree', 'identifier': 'DEGREE', 'symbol': 'deg', 'origin': 'Non-SI unit mentioned in the SI', 'flg_available': True, 'description': 'Unit of plane angle (2D angle)'}, {'id': 13, 'name': 'Steradian', 'identifier': 'STERADIAN', 'symbol': 'sr', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of solid angle (3D angle)'}, {'id': 14, 'name': 'Newton', 'identifier': 'NEWTON', 'symbol': 'N', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Mechanics unit of force, weight (kg·m·s-2)'}, {'id': 15, 'name': 'Pascal', 'identifier': 'PASCAL', 'symbol': 'Pa', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Mechanics unit of pressure, stress (kg·m-1·s-2)'}, {'id': 16, 'name': 'Joule', 'identifier': 'JOULE', 'symbol': 'J', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Mechanics unit of energy, work, heat (kg·m2·s-2)'}, {'id': 17, 'name': 'Electronvolt', 'identifier': 'ELECTRONVOLT', 'symbol': 'eV', 'origin': 'Non-SI unit mentioned in the SI', 'flg_available': True, 'description': 'Physics unit of energy'}, {'id': 18, 'name': 'Watt', 'identifier': 'WATT', 'symbol': 'W', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Mechanics unit of power (kg·m2·s-3)'}, {'id': 19, 'name': 'Coulomb', 'identifier': 'COULOMB', 'symbol': 'C', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of charge (A·s)'}, {'id': 20, 'name': 'Volt', 'identifier': 'VOLT', 'symbol': 'V', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of voltage (kg·m2·s-3·A-1)'}, {'id': 21, 'name': 'Farad', 'identifier': 'FARAD', 'symbol': 'F', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of electric capacitance (kg-1·m-2·s4·A2)'}, {'id': 22, 'name': 'Ohm', 'identifier': 'OHM', 'symbol': 'Ω', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of electric resistance (kg·m2·s-3·A-3)'}, {'id': 23, 'name': 'Siemens', 'identifier': 'SIEMENS', 'symbol': 'S', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of electrical conductance (kg-1·m-2·s3·A2)'}, {'id': 24, 'name': 'Weber', 'identifier': 'WEBER', 'symbol': 'Wb', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of magnetic flux (kg·m2·s-2·A-1)'}, {'id': 25, 'name': 'Tesla', 'identifier': 'TESLA', 'symbol': 'T', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of magnetic Field (kg·s-2·A-1)'}, {'id': 26, 'name': 'Henry', 'identifier': 'HENRY', 'symbol': 'H', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Electromagnetism unit of inductance (kg·m2·s-2·A-2)'}, {'id': 27, 'name': 'Degree Celsius', 'identifier': 'DEGREE_CELSIUS', 'symbol': 'degC', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of temperature'}, {'id': 28, 'name': 'Lumen', 'identifier': 'LUMEN', 'symbol': 'lm', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Optics unit of luminous flux (cd·sr)'}, {'id': 29, 'name': 'Lux', 'identifier': 'LUX', 'symbol': 'lx', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Optics unit of illuminance (cd·sr·m-2)'}, {'id': 30, 'name': 'Becquerel', 'identifier': 'BECQUEREL', 'symbol': 'Bq', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Radioactivity unit of radioactivity (s-1)'}, {'id': 31, 'name': 'Gray', 'identifier': 'GRAY', 'symbol': 'Gy', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Radioactivity unit of absorbed dose (m2·s-1)'}, {'id': 32, 'name': 'Sievert', 'identifier': 'SIEVERT', 'symbol': 'Sv', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Radioactivity unit of equivalent dose (m2·s-1)'}, {'id': 33, 'name': 'Katal', 'identifier': 'KATAL', 'symbol': 'kat', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of catalytic activity (mol·s-1)'}, {'id': 34, 'name': 'Minute', 'identifier': 'MINUTE', 'symbol': 'min', 'origin': 'Non-SI unit mentioned in the SI', 'flg_available': True, 'description': 'Unit of time'}, {'id': 35, 'name': 'Hour', 'identifier': 'HOUR', 'symbol': 'h', 'origin': 'Non-SI unit mentioned in the SI', 'flg_available': True, 'description': 'Unit of time'}, {'id': 36, 'name': 'Day', 'identifier': 'DAY', 'symbol': 'd', 'origin': 'Non-SI unit mentioned in the SI', 'flg_available': True, 'description': 'Unit of time'}, {'id': 37, 'name': 'Year', 'identifier': 'YEAR', 'symbol': 'a', 'origin': 'Other', 'flg_available': True, 'description': 'Unit of time (equal to either 365 or 366 days)'}, {'id': 38, 'name': 'Bar', 'identifier': 'BAR', 'symbol': 'bar', 'origin': 'Common unit not officially sanctioned', 'flg_available': True, 'description': 'Metric unit of pressure'}, {'id': 39, 'name': 'Pixel', 'identifier': 'PIXEL', 'symbol': 'px', 'origin': 'Other', 'flg_available': True, 'description': 'Unit of programmable color on a computer display or in a computer image'}, {'id': 40, 'name': 'Byte', 'identifier': 'BYTE', 'symbol': 'B', 'origin': 'Other', 'flg_available': True, 'description': 'Unit of information'}, {'id': 41, 'name': 'Bit', 'identifier': 'BIT', 'symbol': 'bit', 'origin': 'Other', 'flg_available': True, 'description': 'Unit of information'}, {'id': 42, 'name': 'Metre per second', 'identifier': 'METER_PER_SECOND', 'symbol': 'm/s', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'SI derived unit of both speed (scalar) and velocity (vector quantity which specifies both magnitude and a specific direction), defined by distance in metres divided by time in seconds.'}, {'id': 43, 'name': 'Volts per second', 'identifier': 'VOLT_PER_SECOND', 'symbol': 'V/s', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'SI derived rate unit of change of Voltage'}, {'id': 44, 'name': 'Ampere per second', 'identifier': 'AMPERE_PER_SECOND', 'symbol': 'A/s', 'origin': 'SI derived unit', 'flg_available': True, 'description': 'Unit of electrical charge'}, {'id': 45, 'name': 'Percentage', 'identifier': 'PERCENT', 'symbol': '%', 'origin': 'Other', 'flg_available': True, 'description': ''}, {'id': 46, 'name': 'Unknown', 'identifier': 'NOT_ASSIGNED', 'symbol': 'N_A', 'origin': 'Other', 'flg_available': True, 'description': ''}]


create_parameter_api_response = {'id': 1234, 'data_source': 'LOCATION/CLASS/PARAM/00', 'name': 'Test device', 'value': 111.6604995727539, 'minimum': 106.80351257324219, 'maximum': 116.29515075683594, 'mean': 111.57698059082031, 'standard_deviation': 2.211357831954956, 'data_type_id': 20, 'parameter_type_id': 1, 'unit_id': 12, 'unit_prefix': '', 'flg_available': True, 'description': 'test device', 'data_groups_parameters': []}
