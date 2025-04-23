import utils.DataView

parameters = [
    "CONTROL/SQS_KBS_CSLIT/MOTOR/SLIT_Y_BOTTOM/encoderPosition",
    "CONTROL/SQS_NQS_CRSC/TSYS/PARKER_TRIGGER/actualControl",
    "CONTROL/SQS_NQS_CSLIT/PMOTOR/RESERVED_4/actualVelocity",
    "CONTROL/SQS_TDK/POWER_SUPPLY/MV1/current/actual",
    "CONTROL/SQS_TDK/POWER_SUPPLY/MV1/voltage/actual",
    "CONTROL/SQS_RACK_MPOD-2/MDL/MPOD_MAPPER/XGMD_MP_gain/channelMeasurementCurrent",
    "CONTROL/SQS_RACK_MPOD-1/MDL/MPOD_MAPPER/strk_ret4_v1/channelSupervisionMaxTerminalVoltage",
    "CONTROL/XFEL_MAGNETS_MAGNETML/DOOCS/KSNEG_2787_T4/pollingInterval",
    "CONTROL/SQS_XTD10_ESLIT/MDL/MAIN/actualPosition",
    "CONTROL/SQS_DIAG1_XGMD/XGM/DOOCS/pulseEnergy/crossUsed",
    "CONTROL/SA3_XTD10_XGM/XGM/DOOCS/current/bottom/rangeCode",
    "CONTROL/SA3_XTD10_VAC/MDL/GATT_P_CELL/weightingCoefficientLR",
    "CONTROL/SQS_KBS_CSLIT/MOTOR/SLIT_Y_TOP/actualPosition",
    "CONTROL/SQS_KBS_CSLIT/MOTOR/SLIT_X_RIGHT/actualPosition",
    "CONTROL/SQS_KBS_CSLIT/MDL/MAIN/actualPositionX",
    "CONTROL/SQS_F3_MOV/MOTOR/Y_US_L/actualVelocity",
    "CONTROL/SQS_RACK_MPOD-2/MDL/MPOD_MAPPER/state/value"
]


def h5_list():
    home = Path.home()
    root_data_path = home / 'gpfs/exfel/data/scs'
    filename = 'RAW-R0007-DA01-S00001.h5'
    file_path = root_data_path / filename

    # Scan all run folders within the data path
    files_list = [f for f in root_data_path.iterdir() if f.suffix == ".h5"]

    print(f"List of files in {root_data_path}:\n{files_list}")

    file_view = H5FileView()
    for file_path in files_list:
        try:
            print(f"List all datasets in the HDF5 file: {file_path}")
            file_view(file_path)
        except Exception as e:
            print(e)

    #  print(json.dumps(file_view, indent=4, cls=H5JsonEncoder))

    for filesname, data_view in file_view.data.items():
        for p in parameters:
            metadata = data_view.get_metadata(p)
            if metadata:
                print(f"{p} ==> {metadata}")


def h5_list_v0():
    home = Path.home()
    root_data_path = home / 'gpfs/exfel/data/scs'
    filename = 'RAW-R0007-DA01-S00001.h5'
    file_path = root_data_path / filename

    # Scan all run folders within the data path
    files_list = [f for f in root_data_path.iterdir() if f.suffix == ".h5"]

    print(f"List of files in {root_data_path}:\n{files_list}")

    h5_index = H5DataIndex('CONTROL')
    for file_path in files_list:
        try:
            print(f"List all datasets in the HDF5 file: {file_path}")
            h5_index.register_file(file_path)
            with h5py.File(file_path, 'r') as f:
                # this will visit all objects inside the hdf5 file and store datasets in h5_index object (ie names)
                f["CONTROL"].visititems(h5_index)
                f.close()
        except Exception as e:
            logger.error(e)

    print(json.dumps(h5_index.data, indent=4))

    paths = []
    for p in parameters:
        paths += [h5_index.get_metadata(p)]

    print(paths)

    compact = {}

    for p in paths:
        f = p["file"]
        compact[f] = compact.get(f, []) + [p["key"]]

    print(json.dumps(compact, indent=4))
