from importlib.resources import files

eop_historical = files("naif_eop_historical").joinpath("earth_620120_240827.bpc").as_posix()
_eop_historical_md5 = files("naif_eop_historical").joinpath("earth_620120_240827.md5").as_posix()
