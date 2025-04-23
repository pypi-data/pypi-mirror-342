import types
import typing
import pathlib
import functools
import collections

from csvw.dsv import reader
from pyglottolog import Glottolog
from pyglottolog.languoids import Languoid


class Wordlist(type(pathlib.Path())):
    """
    Wordlists are the smallest organizational unit in a lexibench repository.

    These are single-family LingPy Wordlists extracted from the datasets in a repository via the
    `lexibench write_lingpy_wordlist` command.
    """
    @property
    def markdown(self):
        return '[{}]({})'.format(self.stem, self.name)

    def read_items(self) -> typing.Generator[typing.Dict[str, typing.Any], None, None]:
        yield from reader(self, delimiter="\t", dicts=True)

    @functools.cached_property
    def doculects(self):
        return sorted(set(i['DOCULECT'] for i in self.read_items()))

    def glottocode2doculects(self,
                             lgs: typing.Dict[str, Languoid],
                             gl: Glottolog,
                             include_family_level=False,
                             include_bookkeeping=False
                             ) -> typing.Tuple[
            typing.Dict[str, typing.Set[str]],
            types.SimpleNamespace]:
        """
        Compute a mapping from Glottocodes to a Wordlist's Doculects.
        """
        glottocode_problems = types.SimpleNamespace(invalid=set(), family=set(), bookkeeping=set())
        res = collections.defaultdict(set)
        for item in self.read_items():
            if item['GLOTTOLOG']:
                if item['GLOTTOLOG'] not in lgs:
                    glottocode_problems.invalid.add(item['GLOTTOLOG'])
                    continue
                lg = lgs[item['GLOTTOLOG']]
                if lg.level == gl.languoid_levels.family and not include_family_level:
                    # We don't want top-level family nodes in the tree. Family-level data might
                    # be present in datasets with reconstructed proto-forms.
                    glottocode_problems.family.add(item['GLOTTOLOG'])
                    continue
                if lg.lineage and lg.lineage[0][1] == 'book1242' and not include_bookkeeping:
                    glottocode_problems.bookkeeping.add(item['GLOTTOLOG'])
                    continue
                res[item["GLOTTOLOG"]].add(item["DOCULECT"])
        return res, glottocode_problems

    def doculects_with_glottocodes(
            self,
            lgs: typing.Dict[str, Languoid],
            gl: Glottolog,
            include_family_level=False,
            include_bookkeeping=False
    ) -> typing.Tuple[typing.List[str], types.SimpleNamespace]:
        """
        Compute a subset of doculects for which there are Glottocodes available
        """
        glottocode_problems = types.SimpleNamespace(invalid=set(), family=set(), bookkeeping=set())
        res = set()
        for item in self.read_items():
            if item['GLOTTOLOG']:
                if item['GLOTTOLOG'] not in lgs:
                    glottocode_problems.invalid.add(item['GLOTTOLOG'])
                    continue
                lg = lgs[item['GLOTTOLOG']]
                if lg.level == gl.languoid_levels.family and not include_family_level:
                    # We don't want top-level family nodes in the tree. Family-level data might
                    # be present in datasets with reconstructed proto-forms.
                    glottocode_problems.family.add(item['GLOTTOLOG'])
                    continue
                if lg.lineage and lg.lineage[0][1] == 'book1242' and not include_bookkeeping:
                    glottocode_problems.bookkeeping.add(item['GLOTTOLOG'])
                    continue
                res.add(item["DOCULECT"])
        return list(res), glottocode_problems
