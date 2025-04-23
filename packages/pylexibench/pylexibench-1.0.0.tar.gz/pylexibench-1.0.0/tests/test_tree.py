from pylexibench.tree import *


def test_get_tree(glottolog):
    lgs = {lg.id: lg for lg in glottolog.languoids()}
    tree = get_tree({'arik1263': ['l1', 'l2'], 'kari1311': ['l3']}, lgs)
    assert 'l2' in {n.name for n in tree.walk()}
