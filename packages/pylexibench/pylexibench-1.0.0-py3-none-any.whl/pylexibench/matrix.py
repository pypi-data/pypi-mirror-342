import typing
import functools
import collections
import math
import random

from pylexibench.repository import Wordlist


class Matrix:
    """
    A `Matrix` object represents the cognate codings in a LingPy `Wordlist` as nested `dict`s.
    """
    def __init__(self, doculects, concepts, matrix):
        self.doculects = doculects
        self.concepts = concepts
        self.matrix = matrix

    @classmethod
    def from_items(cls, items):
        doculects = sorted({i['DOCULECT'] for i in items})
        concepts = sorted({i['CONCEPT'] for i in items})
        matrix = collections.OrderedDict(
            (con, collections.OrderedDict((doc, set()) for doc in doculects))
            for con in concepts)
        for item in items:
            matrix[item['CONCEPT']][item['DOCULECT']].add(int(item['COGID']))
        return cls(doculects, concepts, matrix)

    @classmethod
    def from_wordlist(cls, wordlist: Wordlist) -> "Matrix":
        items = list(wordlist.read_items())
        return cls.from_items(items)

    def __getitem__(self, item: str) -> typing.OrderedDict[str, typing.Set[str]]:
        """
        The cognate codings for one concept.
        """
        return self.matrix[item]

    def itervalues(self):
        for c, items in self.matrix.items():
            for d, val in items.items():
                yield c, d, val

    def restrict_matrix(self, new_doculects: typing.List[str]) -> "Matrix":
        """
        Returns a new matrix object which is a restriction of this matrix to the provided list of
        doculects
        """
        new_matrix = collections.OrderedDict(
            (con, collections.OrderedDict((doc, set()) for doc in new_doculects))
            for con in self.concepts)
        for concept in self.concepts:
            for doculect in new_doculects:
                new_matrix[concept][doculect] = self.matrix[concept][doculect]
        return Matrix(new_doculects, self.concepts, new_matrix)

    @functools.cached_property
    def is_polymorphic(self) -> bool:
        """
        Whether the matrix is polymorphic, i.e. whether at least one doculect has counterparts for
        the same concept in more than one cognate set.
        """
        for row in self.matrix.values():
            for cell in row.values():
                if len(cell) > 1:
                    return True
        return False

    @functools.cached_property
    def charsets(self) -> typing.OrderedDict[str, typing.List[str]]:
        """
        An ordered `dict` mapping concepts to the sorted list of cognate set IDs used to annotate
        cognacy.
        """
        return collections.OrderedDict(
            (concept, sorted(set().union(*[states for states in self[concept].values()])))
            for concept in self.concepts)

    @functools.cached_property
    def max_charset_size(self) -> int:
        """
        The maximal number of different cognate sets for counterparts of the same concept.
        """
        return max(len(charset) for charset in self.charsets.values())

    def split_train_test(self,
                         train_ratio: float,
                         min_concepts: int) -> typing.Tuple["Matrix", "Matrix"]:
        """
        Returns two Matrix objects which result from splitting the concepts in this matrix randomly
        in training and testing data according to train_ratio.
        If the smaller matrix contains fewer than min_concepts concepts the function raises a
        ValueError
        """
        num_concepts = len(self.concepts)
        smaller = min(train_ratio, 1 - train_ratio) * num_concepts
        if smaller < min_concepts:
            raise ValueError("Smaller partition has < " + str(min_concepts) + " concepts")
        num_concepts_train = math.ceil(train_ratio * num_concepts)
        l = [_ for _ in range(num_concepts)]  # noqa: E741
        random.shuffle(l)
        train_indices = l[:num_concepts_train]
        train_matrix = collections.OrderedDict()
        train_concepts = []
        test_matrix = collections.OrderedDict()
        test_concepts = []
        for i, concept in enumerate(self.concepts):
            if i in train_indices:
                train_concepts.append(concept)
                train_matrix[concept] = self.matrix[concept]
            else:
                test_concepts.append(concept)
                test_matrix[concept] = self.matrix[concept]
        train = Matrix(self.doculects, train_concepts, train_matrix)
        test = Matrix(self.doculects, test_concepts, test_matrix)
        return (train, test)
