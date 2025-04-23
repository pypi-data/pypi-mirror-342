from importlib.resources import files

leapseconds = files("naif_leapseconds").joinpath("latest_leapseconds.tls").as_posix()
_leapseconds_md5 = files("naif_leapseconds").joinpath("latest_leapseconds.md5").as_posix()
