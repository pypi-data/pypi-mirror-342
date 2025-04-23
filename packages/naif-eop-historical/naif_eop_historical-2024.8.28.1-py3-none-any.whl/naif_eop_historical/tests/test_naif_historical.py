import os
import spiceypy as spice


def test_eop_historical():
    from naif_eop_historical import eop_historical

    assert os.path.isfile(eop_historical)

def test_eop_historical_load():
    from naif_eop_historical import eop_historical

    spice.furnsh(eop_historical)
    spice.unload(eop_historical)

def test__eop_historical_md5():
    from naif_eop_historical import _eop_historical_md5

    assert os.path.isfile(_eop_historical_md5)
