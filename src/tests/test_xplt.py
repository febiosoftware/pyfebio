from pathlib import Path
from pyfebio import xplt


def test_read_xplt(tmp_path):
    xplt.to_hdf5(Path(__file__).parent.joinpath("../../assets/elastic_hex20.xplt").as_posix(), tmp_path/"elastic_hex20.hdf5")
