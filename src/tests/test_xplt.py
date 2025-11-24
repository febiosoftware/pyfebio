from pathlib import Path

import pyfebio as feb


def test_read_xplt():
    feb.xplt.parse_xplt(Path(__file__).parent.joinpath("../examples/contact.xplt").as_posix())
