from pylexibench.matrix_formats import catg


def test_multi(matrix):
    res = catg.multi(matrix)
    assert res.strip() == """3 2
l1 l2 l3
011 1.0,1.0,1.0 1.0,1.0,1.0 0.5,0.5,0.5
-00 1.0,1.0,1.0 1.0,0.0,0.0 1.0,0.0,0.0
""".strip()


def test_bin(matrix):
    res = catg.bin(matrix, polymorphism_is_zero=True)
    assert res.strip() == """3 4
l1 l2 l3
100 0.0,1.0 1.0,0.0 1.0,0.0
010 1.0,0.0 0.0,1.0 0.5,0.5
000 1.0,0.0 1.0,0.0 0.5,0.5
-11 1.0,1.0 0.0,1.0 0.0,1.0
""".strip(), "Polymorphic doculect l3 not set to zero for character 1"
