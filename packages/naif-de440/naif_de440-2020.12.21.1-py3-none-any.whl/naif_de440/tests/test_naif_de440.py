import os
import spiceypy as spice


def test_de440():
    from naif_de440 import de440

    assert os.path.isfile(de440)

def test_de440_load():
    from naif_de440 import de440

    spice.furnsh(de440)
    spice.unload(de440)

def test__de440_md5():
    from naif_de440 import _de440_md5

    assert os.path.isfile(_de440_md5)
