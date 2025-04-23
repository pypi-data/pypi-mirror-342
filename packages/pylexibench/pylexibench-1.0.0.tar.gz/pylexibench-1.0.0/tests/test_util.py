import pytest
from lingpy import Wordlist

from pylexibench.util import *


@pytest.mark.parametrize(
    'cogid,clean',
    [
        ('a', 'a'),
        ('1 ', '1'),
        ('0', None),
        ('', None),
        ('?', None),
        ('1?', '1'),
        ('1, 2', '1'),
        ('1?, 2', '1'),
    ]
)
def test_clean_cognacy(cogid, clean):
    assert clean_cognacy(cogid) == clean


def test_empty_dir(tmp_path):
    tmp_path.joinpath('d').mkdir()
    assert list(tmp_path.iterdir())
    empty_dir(tmp_path)
    assert not list(tmp_path.iterdir())


def test_cleanup_wordlist(tmp_path):
    data = {
        0: ['tokens', 'concept', 'doculect'],
        1: ['a b # *', 'c', 'l'],
        2: [list('a b c'), '"abc', 'l'],
    }
    wl, _, purged, excluded, uncoded = clean_wordlist(Wordlist(data))
    assert purged == 1
    assert excluded == 0
    assert uncoded == 2
