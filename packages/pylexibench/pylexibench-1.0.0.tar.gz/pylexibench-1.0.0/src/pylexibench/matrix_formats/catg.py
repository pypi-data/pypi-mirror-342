import functools

from pylexibench.matrix import Matrix

__all__ = ['bin', 'multi']

MULTISTATE_SYMBOLS = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
    "Y", "Z", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "/", ":",
    ";", "<", "=", ">", "@", "[", "\\", "]", "^", "_", "{", "|", "}", "~"]


def _format(row_factory, matrix: Matrix, **kw) -> str:
    rows = list(row_factory(matrix, **kw))
    return '\n'.join(
        ['{} {}'.format(len(matrix.doculects), len(rows)), ' '.join(matrix.doculects)] + rows)


def _multi(matrix: Matrix, **kw):
    if matrix.max_charset_size > len(MULTISTATE_SYMBOLS):
        raise ValueError(
            'Cannot encode more than {} different cognate sets for one concept as '
            'multistate character.'.format(len(MULTISTATE_SYMBOLS)))  # pragma: no cover

    def multistate_value(concept, doculect, charset, symbol_dict):
        language_values = matrix[concept][doculect]
        if len(language_values) == 0:
            return "-", ','.join("1.0" for _ in range(matrix.max_charset_size))

        prob = str(round(1 / len(language_values), 3))
        prob_vec = [prob if i < len(charset) else "0.0" for i in range(matrix.max_charset_size)]
        for i, value in enumerate(charset):
            if value in language_values:  # First matching cognate set wins.
                return symbol_dict[value], ','.join(prob_vec)

    for concept, charset in matrix.charsets.items():
        symbol_dict = dict(zip(charset, MULTISTATE_SYMBOLS))
        symbols, probs = list(zip(*[multistate_value(concept, doculect, charset, symbol_dict)
                                    for doculect in matrix.doculects]))
        yield "{} {}".format(''.join(symbols), ' '.join(probs))


def _bin(matrix, **kw):
    missing_is_zero = kw.pop('missing_is_zero', False)
    polymorphism_is_zero = kw.pop('polymorphism_is_zero', False)

    def binary_value(concept, doculect, char):
        if not matrix[concept][doculect]:
            return '0' if missing_is_zero else '-'
        if polymorphism_is_zero and len(matrix[concept][doculect]) > 1:
            return '0'
        return '1' if char in matrix[concept][doculect] else '0'

    def probs(concept, doculect, char):
        vals = matrix[concept][doculect]
        if not vals:
            # alternative:
            # one_prob = 1 / len(possible_values)
            return '1.0,1.0'
        one_prob = 1 / len(vals) if char in vals else 0.0
        return "{},{}".format(round(1.0 - one_prob, 3), round(one_prob, 3))

    for concept, charset in matrix.charsets.items():
        for char in charset:
            yield "{} {}".format(
                ''.join(binary_value(concept, dl, char) for dl in matrix.doculects),
                ' '.join(probs(concept, dl, char) for dl in matrix.doculects))


multi = functools.partial(_format, _multi)
bin = functools.partial(_format, _bin)
