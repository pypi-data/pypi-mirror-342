import typing
import pathlib
import functools

from csvw.dsv import reader

from pylexibench.dataset import Dataset
from pylexibench.wordlist import Wordlist


class Repository:
    """
    A `Repository` is the top-level organizational unit of data in lexibench.
    It holds a catalog of individual Lexibank datasets from which data might be retrieved for
    analysis.
    """
    def __init__(self, path: pathlib.Path):
        assert path.exists() and path.is_dir()
        self.path = path
        self.etc_dir = self.path / 'etc'
        self.dataset_list = self.etc_dir.joinpath('lexibank.tsv')
        assert self.dataset_list.exists()
        self.download_dir = self.path / 'download'
        self.wordlists_dir = self.path / 'lingpy_wordlists'
        self.cognates_dir = self.path / 'lingpy_cognates'
        self.trees_dir = self.path / 'glottolog_trees'
        self.matrices_dir = self.path / 'character_matrices'
        self.compatible_matrices_dir = self.path / 'character_matrices_compatible'
        self.cross_validation_dir = self.path / 'bin_cross_validation'

    @functools.cached_property
    def datasets(self) -> typing.List[Dataset]:
        return [
            Dataset.from_row(r, self.download_dir / r['ID'])
            for r in reader(self.dataset_list, delimiter='\t', dicts=True)]

    def iter_wordlists(self,
                       predicate: typing.Union[None, typing.Callable[[pathlib.Path], bool]] = None
                       ) -> typing.Generator[pathlib.Path, None, None]:
        """
        Generator of paths for family-specific LingPy Wordlists extracted from the repository's
        datasets.

        A predicate can be used to filter only matching paths.
        """
        for p in sorted(self.wordlists_dir.glob('*.tsv'), key=lambda _p: _p.stem):
            if p.name in {'data.tsv', 'stats.tsv'}:
                continue
            if not predicate or predicate(p):
                yield Wordlist(p)
