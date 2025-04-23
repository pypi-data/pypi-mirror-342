from importlib.resources import files

earth_itrf93 = files("naif_earth_itrf93").joinpath("earth_assoc_itrf93.tf").as_posix()
_earth_itrf93_md5 = files("naif_earth_itrf93").joinpath("earth_assoc_itrf93.md5").as_posix()
