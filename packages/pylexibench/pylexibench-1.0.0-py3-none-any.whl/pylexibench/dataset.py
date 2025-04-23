import shutil
import typing
import logging
import pathlib
import functools
import collections
import dataclasses

import pycldf
from clldutils.jsonlib import load
from clldutils.misc import slug
from lingpy.compare import sanity
from lingpy import Wordlist
import cldfzenodo
import nameparser

from pylexibench.util import clean_wordlist, clean_cognacy

CORRECT_FAMILY_NAME = {
    "Austroasiatic": "Austro-Asiatic",
}


@dataclasses.dataclass
class Dataset:
    """
    A `Dataset` object correponds to a Lexibank dataset, i.e. a set of lexical data curated within
    the Lexibank framework.
    """
    dir: pathlib.Path
    ID: str
    Concepts: int
    Concepticon: int
    Dataset: str
    Organization: str
    Source: str
    Zenodo: str
    ClicsCore: bool
    LexiCore: bool
    CogCore: bool
    ProtoCore: bool
    Version: str

    @classmethod
    def from_row(cls, row: dict, dir: pathlib.Path) -> "Dataset":
        """
        Factory method to initialize a `Dataset` object from a row in the repository's catalog.
        """
        def val(k, v):
            if k.endswith('Core'):
                return bool(v == 'x')
            if k in ['Concepts', 'Concepticon']:
                return int(v)
            return v
        return cls(dir=dir, **{k: val(k, v) for k, v in row.items()})

    @property
    def doi(self) -> str:
        return 'https://doi.org/' + self.Zenodo

    def __str__(self):
        return self.ID

    @property
    def markdown(self):
        return '[{}]({})'.format(self.ID, self.doi)

    @functools.cached_property
    def metadata_json(self) -> dict:
        return load(self.dir / 'metadata.json')

    @functools.cached_property
    def zenodo_json(self) -> dict:
        return load(self.dir / '.zenodo.json')

    @functools.cached_property
    def cldf_metadata_path(self) -> pathlib.Path:
        return self.dir / 'cldf' / 'cldf-metadata.json'

    def download(self, force=False, upgrade=False, log=None) -> pycldf.Source:
        """
        Download the data of a dataset to its directory (relative to the repository).

        :return: A `pycldf.Source` object with reference information for the dataset.
        """
        log = log or logging.getLogger(__name__)

        if self.dir.exists() and force:
            log.info('Removing old download in {}'.format(self.dir))
            shutil.rmtree(self.dir)

        record = cldfzenodo.API.get_record(self.Zenodo)
        # check if record is most recent one
        rec_new = record.from_concept_doi(record.concept_doi)
        if rec_new.doi != record.doi:
            if upgrade:
                record = rec_new
                if self.dir.exists():
                    log.info(f'DOI for dataset {self.ID} is not the latest version, removing old '
                             f'download!')
                    shutil.rmtree(self.dir)

        if not self.dir.exists():
            log.info(f"Downloading {self.ID} to {self.dir}")
            record.download(self.dir)

        editors = [c["name"] for c in self.zenodo_json["contributors"] if c["type"] == "Editor"]
        for i, editor in enumerate(editors):
            name = nameparser.HumanName(editor)
            first = name.first
            if name.middle:
                first = " " + name.middle
            editors[i] = f"{name.last}, {first}"

        description = self.metadata_json["citation"]
        # create bibtex and write to new file
        bib = dict(
            author=" and ".join(record.creators),
            title=record.title,
            publisher="Zenodo",
            year=record.year,
            address="Geneva",
            doi=record.doi)
        if editors:
            bib["editor"] = " and ".join(editors)
        if description:
            bib["citation"] = description
        return pycldf.Source("book", self.ID, **bib)

    def get_lingpy_wordlist_and_cognacy_col(self) \
            -> typing.Tuple[Wordlist, typing.Union[str, None], int]:
        """
        Read the dataset's data into a (corrected) LingPy Wordlist.
        """
        wl = Wordlist.from_cldf(
            self.cldf_metadata_path,
            columns=(
                'parameter_id', 'concept_name', 'language_id', 'language_name', "language_family",
                'value', 'form', 'segments', 'language_glottocode', 'concept_concepticon_id',
                'language_latitude', 'language_longitude', 'cognacy', 'partial_cognacy',
                "cogid_cognateset_id"),
            namespace=(
                ('concept_name', 'concept'),
                ('language_id', 'doculect'),
                ("language_family", "family"),
                ('segments', 'tokens'),
                ('language_glottocode', 'glottolog'),
                ('concept_concepticon_id', 'concepticon'),
                ('language_latitude', 'latitude'),
                ('language_longitude', 'longitude'),
                ('cognacy', 'cognacy'),
                ('partial_cognacy', 'partial_cognacy'),
                ('cogid_cognateset_id', 'cldf_cogid')))
        for col in ['cognacy', 'cldf_cogid', 'partial_cognacy']:
            if any(cog for _, cog in wl.iter_rows(col)):
                break
        else:  # pragma: no cover
            col = None  # Wordlist does not have cognacy annotations (in known places).
        cogid = 0
        if col:
            # We turn dataset-specific cognacy markers into integers.
            cogids, updates = {}, {}
            for idx, concept, cognacy in wl.iter_rows("concept", col):
                # make sure cognacy is resolved to something unique if set to 0 or left empty - why
                # not keep None?
                cc = clean_cognacy(cognacy, col=col)
                entry = '{}--{}'.format(slug(concept), cc) if cc else None
                if entry and entry not in cogids:
                    cogid += 1
                    cogids[entry] = cogid
                updates[idx] = cogids[entry] if entry else None

            wl.add_entries("cogid", updates, lambda x: x)
        return wl, col, cogid

    def iter_wordlists(self,
                       language_threshold,
                       concept_threshold,
                       coverage_threshold,
                       wldir,
                       log,
                       ) -> typing.Generator[typing.Tuple[pathlib.Path, typing.Tuple], None, None]:
        """
        Split the dataset into per-family lingpy_wordlists.

        These lingpy_wordlists are written to a file and summary statistics about them are yielded.
        """
        def warn(msg):  # pragma: no cover
            if isinstance(msg, list):
                msg = '\t'.join(str(m) for m in msg)
            (log.warning if warn else log.warn)('Dataset {}\t{}'.format(self.ID, msg))

        wl, cognacy_column, cogsets = self.get_lingpy_wordlist_and_cognacy_col()
        if not cognacy_column:  # pragma: no cover
            warn(["skipping", "no cognacy annotation."])
            return

        families = collections.defaultdict(list)
        for idx, family in wl.iter_rows("family"):
            if family:
                # correct erroneous family names
                families[CORRECT_FAMILY_NAME.get(family, family)].append(idx)
        for i, (family, idxs) in enumerate(families.items()):
            wln = Wordlist({idx: wl.columns if idx == 0 else wl[idx] for idx in [0] + idxs})
            if wln.width < language_threshold:  # pragma: no cover
                warn(['skipping', family, 'not enough languages', wln.width])
                continue
            elif wln.height < concept_threshold:  # pragma: no cover
                warn(['skipping', family, 'not enough concepts', wln.height])
                continue  # pragma: no cover

            wln, orig_items, edited, unsegmentable, uncoded = clean_wordlist(wln)
            ac = sanity.average_coverage(wln)
            if ac < coverage_threshold:  # pragma: no cover
                warn(['skipping', family, 'not enough mutual coverage', ac])
            else:
                wlname = self.ID + "-" + slug(family)
                lingpy_logger = logging.getLogger('lingpy')
                lingpy_logger.disabled = True
                wln.calculate("diversity")
                wln.output("tsv", filename=str(wldir / wlname), ignore="all", prettify=False)
                lingpy_logger.disabled = False
                yield wldir / '{}.tsv'.format(wlname), (
                    wlname,
                    family,
                    wln.height,
                    wln.width,
                    len(wln),
                    ac,
                    wln.diversity,
                    len(wln.get_etymdict(ref="cogid")),
                    orig_items,
                    edited,
                    unsegmentable,
                    uncoded,
                )
