from csvw.dsv import UnicodeWriter

from pylexibench.wordlist import Wordlist


def test_Wordlist(glottolog, tmp_path):
    with UnicodeWriter(tmp_path / "wordlist.tsv", delimiter="\t") as writer:
        writer.writerows([
            ['GLOTTOLOG', 'DOCULECT'],
            ('', 'l1'),  # Glottocode missing.
            ('book1243', 'l2'),  # A Glottocode in the Bookkeeping pseudo-family.
            ('invalid', 'l2'),  # An invalid Glottocode.
            ('tupi1275', 'l3'),  # A family-level Glottocode.
            ('arik1264', 'l4'),
            ('arik1264', 'l5'),
        ])

    lgs = {lg.id: lg for lg in glottolog.languoids()}
    wl = Wordlist(tmp_path / "wordlist.tsv")
    m, problems = wl.glottocode2doculects(lgs, glottolog)
    assert len(m) == 1 and len(m['arik1264']) == 2
    assert problems.invalid and problems.family and problems.bookkeeping

    m, problems = wl.glottocode2doculects(
        lgs, glottolog, include_family_level=True, include_bookkeeping=True)
    assert len(m) == 3 and not problems.bookkeeping
