import os
import spiceypy as spice

from ..compare import calculate_md5


def test_leapseconds():
    from naif_leapseconds import leapseconds

    assert os.path.isfile(leapseconds)

def test_leapseconds_load():
    from naif_leapseconds import leapseconds

    spice.furnsh(leapseconds)
    spice.unload(leapseconds)

def test__leapseconds_md5():
    from naif_leapseconds import _leapseconds_md5

    assert os.path.isfile(_leapseconds_md5)


def test__leapseconds_md5_matches():
    from naif_leapseconds import _leapseconds_md5, leapseconds

    # Read the MD5 hash from the file that comes with the
    # package
    with open(_leapseconds_md5, "r") as f:
        md5_hash = f.read().split()[0]

    # Compare to the MD5 calculated from the naif_leapseconds file
    assert calculate_md5(leapseconds) == md5_hash
