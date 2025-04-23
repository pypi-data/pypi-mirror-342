import os

import spiceypy as spice


def test_jpl_small_bodies_de441_n16():
    from jpl_small_bodies_de441_n16 import de441_n16

    assert os.path.isfile(de441_n16)

def test_jpl_small_bodies_de441_n16_load():
    from jpl_small_bodies_de441_n16 import de441_n16

    spice.furnsh(de441_n16)
    spice.unload(de441_n16)

def test__jpl_small_bodies_de441_n16_md5():
    from jpl_small_bodies_de441_n16 import _de441_n16_md5

    assert os.path.isfile(_de441_n16_md5)
