import os
import spiceypy as spice


def test_eop_predict():
    from naif_eop_predict import eop_predict

    assert os.path.isfile(eop_predict)

def test_eop_predict_load():
    from naif_eop_predict import eop_predict

    spice.furnsh(eop_predict)
    spice.unload(eop_predict)

def test__eop_predict_md5():
    from naif_eop_predict import _eop_predict_md5

    assert os.path.isfile(_eop_predict_md5)
