import pytest

from pylexibench.repository import Repository


@pytest.fixture
def repos(tests_dir):
    return Repository(tests_dir / 'repos')


def test_iter_wordlists(repos):
    assert len(list(repos.iter_wordlists())) == 1
    assert len(list(repos.iter_wordlists(lambda wl: wl.stem == 'abc'))) == 0
    assert len(list(repos.iter_wordlists(lambda wl: wl.stem.startswith('gal')))) == 1