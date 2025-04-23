import collections

import pytest

from pylexibench.matrix_formats import phy
from pylexibench.matrix import Matrix


def test_chunking():
    res = '\n'.join(phy.iter_lines({'l1': 61*'1'}))
    assert res == """ 1 61
l1  1111111111 1111111111 1111111111 1111111111 1111111111

    1111111111 1"""


def test_multi_errors(matrix):
    assert matrix.is_polymorphic
    with pytest.raises(ValueError):
        _ = phy.multi(matrix)

    m = Matrix.from_items([
        dict(CONCEPT='c', DOCULECT='l{}'.format(i + 1), COGID=str(i + 1))
        for i in range(100)])
    with pytest.raises(ValueError) as e:
        _ = phy.multi(m)
    assert 'more than' in str(e)

    m = Matrix.from_items([
        dict(CONCEPT='c{}'.format(i + 1), DOCULECT='l{}'.format(i + 1), COGID=str(i + 1))
        for i in range(100)])
    with pytest.raises(ValueError) as e:
        _ = phy.multi(m)
    assert 'less than' in str(e)


def test_multi(matrix):
    # Make matrix non-polymorphic:
    items = []
    for k, v in matrix.matrix.items():
        for kk, vv in v.items():
            if vv:
                items.append(dict(CONCEPT=k, DOCULECT=kk, COGID=vv.pop()))
    m = Matrix.from_items(items)
    assert not m.is_polymorphic
    res = phy.multi(m)
    assert res == """ 3 2
l1  0-
l2  10
l3  10"""


def test_bin(matrix):
    res = phy.bin(matrix)
    assert res.strip() == """3 4
l1  100-
l2  0101
l3  0111"""
