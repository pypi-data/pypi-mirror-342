from importlib.resources import files

de440 = files("naif_de440").joinpath("de440.bsp").as_posix()
_de440_md5 = files("naif_de440").joinpath("de440.md5").as_posix()
