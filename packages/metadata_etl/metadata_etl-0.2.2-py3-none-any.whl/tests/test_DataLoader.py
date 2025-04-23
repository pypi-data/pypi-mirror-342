import os
from extract.DataLoader import DataLoader
import datadir


def test_load_data(datadir):
    assert set(os.listdir(str(datadir))) == {
        "data",
        "parameters.json",
        "dataset.data",
        "specs.txt",
    }
    with (datadir / "specs.txt").open() as fp:
        contents = fp.read()
    assert contents == "Hello, world!\n"

    base_dir = datadir / "data"
    filename = "RAW-R0190-DA03-S00000.h5"

    assert set(os.listdir(str(base_dir))) == {
        filename,
    }
