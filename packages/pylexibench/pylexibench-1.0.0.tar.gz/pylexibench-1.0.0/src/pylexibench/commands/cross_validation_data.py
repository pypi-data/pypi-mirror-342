"""
Write character matrix_formats for cognate data encoded in the lingpy_wordlists.
"""
import pathlib
import random

from pylexibench.matrix import Matrix
from pylexibench.matrix_formats import phy
from pylexibench.util import empty_dir

README_TEMPLATE = """\
# Character matrices

Character matrices encode cognate data in formats suitable for phylogenetic software.
This directory contains character matrices derived from the cognate data in the
[lingpy_wordlists](../lingpy_wordlists).

## Available matrices

The following table shows available matrix formats as well as some summary statistics about the
character matrices.

{table}

- **cs_max**: For a concept, the charset size corresponds the number of cognate classes that exist
  for this concept in all languages under study. This is equal to the number of columns
  representing this concept in the binary character matrix and to the number of symbols required to
  represent this concept in the multi-valued character matrix. By **cs_max** we denote the
  maximum charset size over all concepts in the dataset.
- **cs_mean**: Ratio of columns in the binary character matrix (= overall number of cognate classes)
  and number of concepts in the dataset. Average number of columns representing a concept in the
  binary character matrix / average number of symbols required per concept in the multi-valued
  character matrix.
- **polymorphic_cell_ratio**: Ratio of language-concept pairs for which there are words from more
  than one cognate class provided
- **polymorphic_concept_ratio**: Ratio of concepts for which there exist languages for which word
  from more than one cognate class are provided
- **concepts_per_language**: Average number of concepts for which there is at least one word
  provided for the languages under study


## Polymorphism

*Polymorphism* in cognate data means that a dataset lists multiple counterparts for a concept in a
language, which are assigned to a different cognate sets. Some analysis methods are sensitive to
polymorphism. The following plot shows the prevalence of polymorphism in our character matrices.

The prevalence of polymorphism in the character matrices is shown in the plot below.

![](stats.svg)
    """


class MatrixFile(type(pathlib.Path())):
    @property
    def markdown(self):
        return '[{}]({}/{})'.format(self.name, self.parent.name, self.name)


def register(parser):
    parser.add_argument(
        '--missing-is-zero',
        action='store_true',
        help='Code a missing counterpart for a concept in a doculect as 0 rather than as missing '
             'data',
        default=False)
    parser.add_argument(
        '--polymorphism-is-zero',
        action='store_true',
        help='Code the case of multiple counterparts (in different cognate sets) for a concept in '
             'a doculect as 0',
        default=False)
    parser.add_argument(
        '--wordlist',
        help='Name of a specific wordlist to process',
        default=None)
    parser.add_argument(
        '--num-samples',
        type=int,
        help='Number cross validation samples to be created',
        default=10)
    parser.add_argument(
        '--train-ratios',
        type=float,
        nargs='+',
        help='Ratios how the data is to be split, providing the relative size of the training '
             'partition',
        default=[0.5, 0.6, 0.7, 0.8, 0.9])
    parser.add_argument(
        '--min-concepts',
        type=int,
        help='Minimum number of concepts that need to be in the smaller partiion for a splitting '
             'to be created',
        default=10)


def run(args):
    if not args.repos.wordlists_dir.exists():
        args.log.error('Run lingpy_wordlists before cross_validation_data')
        return
    empty_dir(args.repos.cross_validation_dir)

    for wordlist in args.repos.iter_wordlists(
            lambda wl: not args.wordlist or wl.stem == args.wordlist):
        args.log.info(wordlist.stem)
        m = Matrix.from_wordlist(wordlist)
        charset_sizes = [len(charset) for charset in m.charsets.values()]
        if max(charset_sizes) == 1:
            args.log.warning('Not creating character matrices because of cs_max = 1')
            continue

        func = phy.bin
        kw = dict(
            missing_is_zero=args.missing_is_zero,
            polymorphism_is_zero=args.polymorphism_is_zero)
        d = args.repos.cross_validation_dir / wordlist.stem
        random.seed(0)
        for train_ratio in args.train_ratios:
            sub_d = d / ("cv_" + str(int(train_ratio * 100)))
            train_d = sub_d / "train"
            test_d = sub_d / "test"
            train_d.mkdir(parents=True, exist_ok=True)
            test_d.mkdir(parents=True, exist_ok=True)
            for sample_idx in range(args.num_samples):
                try:
                    (train_matrix, test_matrix) = m.split_train_test(train_ratio, args.min_concepts)
                except ValueError:
                    args.log.warning(
                        'cannot create cv data with train_ratio {} '.format(int(train_ratio * 100)))
                    break
                fname = "bin" + str(sample_idx) + ".phy"
                p_train = train_d / fname
                p_train.write_text(func(train_matrix, **kw))
                p_test = test_d / fname
                p_test.write_text(func(test_matrix, **kw))
            args.log.info(int(train_ratio * 100))
