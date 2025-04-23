"""
Download lexibank datasets as specified in the repository's dataset list and write a corresponding
BibTeX file for reference.
"""
from pycldf import Dataset as CLDFDataset

from pylexibench.util import output

README_TEMPLATE = """\n
# Datasets

{table}

BibTeX records for the downloaded datasets are available in [sources.bib](sources.bib).
"""


def register(parser):
    parser.add_argument(
        '-f', '--force',
        default=False,
        action='store_true',
        help='Force download of a dataset even if it already exists.')
    parser.add_argument(
        '-u', '--upgrade',
        default=False,
        action='store_true',
        help='Download newest release of a dataset.')


def run(args):
    if not args.repos.download_dir.exists():
        args.repos.download_dir.mkdir()
    sources, table = [], []
    for dataset in args.repos.datasets:
        args.log.info('Downloading dataset {} to {}'.format(dataset.ID, dataset.dir))
        sources.append(dataset.download(force=args.force, upgrade=args.upgrade, log=args.log))
        cldf = CLDFDataset.from_metadata(dataset.cldf_metadata_path)
        table.append([
            dataset,
            len(list(cldf.iter_rows('LanguageTable'))),
            len(list(cldf.iter_rows('ParameterTable'))),
            len(list(cldf.iter_rows('FormTable'))),
            str(sources[-1]),
        ])
    args.repos.download_dir.joinpath('sources.bib').write_text(
        '\n\n'.join(source.bibtex() for source in sources))

    output(
        args,
        ['Dataset', 'Languages', 'Concepts', 'Forms', 'Citation'],
        table,
        args.repos.download_dir,
        README_TEMPLATE,
    )
