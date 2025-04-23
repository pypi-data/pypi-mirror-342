import functools
import collections
import math

from pylexibench.matrix import Matrix
from .catg import MULTISTATE_SYMBOLS

__all__ = ['bin', 'multi']


def _format(row_factory, matrix: Matrix, **kw) -> str:
    return '\n'.join(row_factory(matrix, **kw))


def iter_lines(sequences):
    line_offset = max(len(doculect) for doculect in sequences) + 2
    nchars = len(list(sequences.values())[0])
    block_size, unit_size = 50, 10
    yield ' {} {}'.format(len(sequences), nchars)
    for char_offset in range(0, nchars, block_size):
        if char_offset:
            yield ''
        for doculect, sequence in sequences.items():
            label = doculect.ljust(line_offset) if char_offset == 0 else ''.ljust(line_offset)
            chunks = []
            block = sequence[char_offset:char_offset + block_size]
            for i in range(0, len(block), unit_size):
                chunks.append(''.join(block[i:i + unit_size]))
            yield label + ' '.join(chunks)


def binary_value(entry, char):
    if not entry:
        return '-'
    return '1' if char in entry else '0'


def _bin(matrix, part_cs=-1, **kw):
    sequences = collections.OrderedDict()
    for doculect in matrix.doculects:
        sequences[doculect] = []
        for concept, charset in matrix.charsets.items():
            if part_cs != -1 and len(charset) != part_cs:
                continue
            entry = matrix[concept][doculect]
            for char in charset:
                sequences[doculect].append(binary_value(entry, char))
    if max([len(sequences[doculect]) for doculect in matrix.doculects]) == 0:
        raise ValueError('Empty matrix')
    yield from iter_lines(sequences)


def _multi(matrix, **kw):
    if matrix.max_charset_size > len(MULTISTATE_SYMBOLS):
        raise ValueError(
            'Cannot encode more than {} different cognate sets for one concept as '
            'multistate character.'.format(len(MULTISTATE_SYMBOLS)))

    if matrix.max_charset_size < 2:
        raise ValueError('multi MSA cannot be created for dataset in which all concepts yield '
                         'less than 2 cognate classes')

    if matrix.is_polymorphic:
        raise ValueError('multi MSA cannot be created for polymorphic dataset')

    def multistate_value(concept, doculect, symbol_dict):
        return "-" if not matrix[concept][doculect] \
            else symbol_dict[next(iter(matrix[concept][doculect]))]

    sequences = collections.OrderedDict()
    for doculect in matrix.doculects:
        sequences[doculect] = []
        for concept, charset in matrix.charsets.items():
            symbol_dict = dict(zip(charset, MULTISTATE_SYMBOLS))
            sequences[doculect].append(multistate_value(concept, doculect, symbol_dict))
    if max([len(sequences[doculect]) for doculect in matrix.doculects]) == 0:
        raise ValueError('Empty matrix')
    yield from iter_lines(sequences)


def _bv(matrix, part_cs=-1, **kw):
    if part_cs == -1:
        cs = matrix.max_charset_size
    else:
        cs = part_cs
    upper_bound = math.floor(math.log(len(MULTISTATE_SYMBOLS), 2))
    if cs > upper_bound:
        raise ValueError(
            'Cannot encode more than {} different cognate sets for one concept as '
            'bv character.'.format(upper_bound))

    sequences = collections.OrderedDict()
    for doculect in matrix.doculects:
        sequences[doculect] = []
        for concept, charset in matrix.charsets.items():
            if part_cs != -1 and len(charset) != cs:
                continue
            entry = matrix[concept][doculect]
            binary_code = "". join([binary_value(entry, char) for char in charset])
            if binary_code.startswith("-"):
                sequences[doculect].append("-")
            else:
                sequences[doculect].append(
                    MULTISTATE_SYMBOLS[int(("0" * (cs - len(binary_code))) + binary_code, 2) - 1])
    if max([len(sequences[doculect]) for doculect in matrix.doculects]) == 0:
        raise ValueError('Empty matrix')
    yield from iter_lines(sequences)


multi = functools.partial(_format, _multi)
bin = functools.partial(_format, _bin, part_cs=-1)
bin_part_2 = functools.partial(_format, _bin, part_cs=2)
bin_part_3 = functools.partial(_format, _bin, part_cs=3)
bin_part_4 = functools.partial(_format, _bin, part_cs=4)
bin_part_5 = functools.partial(_format, _bin, part_cs=5)
bin_part_6 = functools.partial(_format, _bin, part_cs=6)
bv = functools.partial(_format, _bv, part_cs=-1)
bv_part_2 = functools.partial(_format, _bv, part_cs=2)
bv_part_3 = functools.partial(_format, _bv, part_cs=3)
bv_part_4 = functools.partial(_format, _bv, part_cs=4)
bv_part_5 = functools.partial(_format, _bv, part_cs=5)
bv_part_6 = functools.partial(_format, _bv, part_cs=6)
