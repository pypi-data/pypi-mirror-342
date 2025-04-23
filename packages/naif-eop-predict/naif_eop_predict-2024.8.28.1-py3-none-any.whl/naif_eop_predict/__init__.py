from importlib.resources import files

eop_predict = files("naif_eop_predict").joinpath("earth_200101_990827_predict.bpc").as_posix()
_eop_predict_md5 = files("naif_eop_predict").joinpath("earth_200101_990827_predict.md5").as_posix()
