import functools
import collections

from commonnexus import Nexus
from commonnexus.blocks import Characters
from commonnexus.tools.matrix import CharacterMatrix
from commonnexus.tools.combine import combine

__all__ = ['bin', 'multi']


def nexus(matrix, binary=True, **kw):
    charlabels = []
    for concept, charset in matrix.charsets.items():
        for char in charset:
            charlabels.append((concept, char))

    data = collections.OrderedDict(
        (doc, collections.OrderedDict((c, None) for c in charlabels)) for doc in matrix.doculects)

    for concept, charset in matrix.charsets.items():
        for doculect in matrix.doculects:
            vals = matrix[concept][doculect]
            if vals:
                for char in charset:
                    data[doculect][(concept, char)] = '1' if char in vals else '0'

    if binary:
        ndata = collections.OrderedDict()
        for k, row in data.items():
            ndata[k] = collections.OrderedDict(('{}_{}'.format(*k), v) for k, v in row.items())
        data = ndata
    else:
        if matrix.max_charset_size > 52:
            raise ValueError(
                'Cannot encode more than {} different cognate sets for one concept as '
                'multistate character.'.format(52))  # pragma: no cover
        try:
            data = multistate_nexus(data)
        except AssertionError as e:  # pragma: no cover
            raise ValueError(str(e))

    return str(Nexus.from_blocks(Characters.from_data(data)))


def multistate_nexus(matrix):
    # split matrix into partitions and multistatise each, then recombine.
    charpartitions = collections.defaultdict(list)
    for concept, char in list(matrix.values())[0]:
        charpartitions[concept].append((concept, char))
    matrices = [
        (key, CharacterMatrix.from_characters(matrix, drop_chars=chars, inverse=True))
        for key, chars in charpartitions.items()]
    ms = []
    for key, m in matrices:
        ms.append(CharacterMatrix.multistatised(m, multicharlabel=key))
    new = combine(*[Nexus.from_blocks(Characters.from_data(m)) for m in ms])
    return new.characters.get_matrix()


bin = functools.partial(nexus, binary=True)
multi = functools.partial(nexus, binary=False)
