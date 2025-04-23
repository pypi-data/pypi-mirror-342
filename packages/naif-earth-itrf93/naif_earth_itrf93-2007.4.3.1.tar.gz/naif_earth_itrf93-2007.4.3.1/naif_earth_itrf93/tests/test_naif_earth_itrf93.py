import os
import spiceypy as spice


def test_earth_itrf93():
    from naif_earth_itrf93 import earth_itrf93

    assert os.path.isfile(earth_itrf93)

def test_earth_itrf93_load():
    from naif_earth_itrf93 import earth_itrf93

    spice.furnsh(earth_itrf93)
    spice.unload(earth_itrf93)

def test__earth_itrf93_md5():
    from naif_earth_itrf93 import _earth_itrf93_md5

    assert os.path.isfile(_earth_itrf93_md5)
