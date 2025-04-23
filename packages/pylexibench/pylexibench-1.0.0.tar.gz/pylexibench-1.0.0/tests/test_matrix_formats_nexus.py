from pylexibench.matrix_formats import nexus
from pylexibench.matrix import Matrix


def test_multi(matrix):
    res = nexus.multi(matrix)
    assert res.strip() == """#NEXUS
BEGIN CHARACTERS;
DIMENSIONS NCHAR=2;
FORMAT DATATYPE=STANDARD MISSING=? GAP=- SYMBOLS="ABC";
CHARSTATELABELS 
    1 1.c1, 
    2 2.c2;
MATRIX 
l1 A?
l2 BA
l3 (BC)A
;
END;"""

    res = nexus.multi(Matrix.from_items([
        dict(CONCEPT='c', DOCULECT='l1', COGID='1'),
        dict(CONCEPT='c', DOCULECT='l2', COGID='2'),
        dict(CONCEPT='c', DOCULECT='l3', COGID='3'),
    ]))
    assert res.strip() == """#NEXUS
BEGIN CHARACTERS;
DIMENSIONS NCHAR=1;
FORMAT DATATYPE=STANDARD MISSING=? GAP=- SYMBOLS="ABC";
CHARSTATELABELS 
    1 1.c;
MATRIX 
l1 A
l2 B
l3 C
;
END;"""


def test_bin(matrix):
    res = nexus.bin(matrix)
    assert res.strip() == """#NEXUS
BEGIN CHARACTERS;
DIMENSIONS NCHAR=4;
FORMAT DATATYPE=STANDARD MISSING=? GAP=- SYMBOLS="01";
CHARSTATELABELS 
    1 c1_1, 
    2 c1_2, 
    3 c1_3, 
    4 c2_4;
MATRIX 
l1 100?
l2 0101
l3 0111
;
END;"""
