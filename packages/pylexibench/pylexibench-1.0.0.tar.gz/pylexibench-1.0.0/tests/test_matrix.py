from pylexibench.matrix import Matrix
from pylexibench.repository import Repository


def test_matrix(tmp_repos):
    for wl in Repository(tmp_repos).iter_wordlists():
        m = Matrix.from_wordlist(wl)
        break
    assert m.is_polymorphic
    assert m.max_charset_size == 18

    m = Matrix.from_items([dict(DOCULECT='d', CONCEPT='c', COGID='1')])
    assert not m.is_polymorphic
