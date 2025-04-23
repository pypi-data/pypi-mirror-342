"""
Write character matrix_formats for cognate data encoded in the lingpy_wordlists.
"""
import pathlib
import statistics
import collections


from clldutils.color import sequential_colors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors as cm

from pylexibench.matrix import Matrix
from pylexibench.matrix_formats import catg, nexus, phy
from pylexibench.util import output, plot_wordlist_stats, empty_dir
from pyglottolog import Glottolog
from cldfcatalog import Catalog

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
FORMATS = {
    'bin.catg': catg.bin,
    'multi.catg': catg.multi,
    #
    'bin.phy': phy.bin,
    'multi.phy': phy.multi,
    #
    'bin_part_2.phy': phy.bin_part_2,
    'bin_part_3.phy': phy.bin_part_3,
    'bin_part_4.phy': phy.bin_part_4,
    'bin_part_5.phy': phy.bin_part_5,
    'bin_part_6.phy': phy.bin_part_6,
    #
    'bv.phy': phy.bv,
    'bv_part_2.phy': phy.bv_part_2,
    'bv_part_3.phy': phy.bv_part_3,
    'bv_part_4.phy': phy.bv_part_4,
    'bv_part_5.phy': phy.bv_part_5,
    'bv_part_6.phy': phy.bv_part_6,
    #
    'bin.nex': nexus.bin,
    'multi.nex': nexus.multi,
}


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
        '--formats',
        nargs='+',
        help='Character matrix formats which are to be constructed',
        choices=list(FORMATS.keys()),
        default=["bin.catg", "multi.catg", "bin.phy", "multi.phy", "bin.nex", "multi.nex"])
    parser.add_argument(
        '--wordlist',
        help='Name of a specific wordlist to process',
        default=None)
    parser.add_argument(
        '--glottolog',
        metavar='GLOTTOLOG',
        help='Path to repository clone of Glottolog data',
        default=None)
    parser.add_argument(
        '--glottolog-version',
        help='Version of Glottolog data to checkout',
        default=None)
    parser.add_argument(
        '--plotstyle',
        type=int,
        choices=range(1, 3),
        help='Style of stats plot',
        default=1)


def polymorphism_analysis(m):
    polymorphic_cells = 0
    polymorphic_concepts = {}
    concepts_per_language = collections.defaultdict(int)
    for concept, values in m.matrix.items():
        for doculect, cell in values.items():
            if len(cell) > 0:
                concepts_per_language[doculect] += 1
                if len(cell) > 1:
                    polymorphic_cells += 1
                    polymorphic_concepts[concept] = 1
    polymorphic_cell_ratio = polymorphic_cells / (len(m.doculects) * len(m.concepts))
    polymorphic_concept_ratio = len(polymorphic_concepts) / len(m.concepts)
    avg_concepts_per_language = statistics.mean(
        [concepts_per_language[doculect] / len(m.concepts) for doculect in m.doculects])
    return [polymorphic_cell_ratio, polymorphic_concept_ratio, avg_concepts_per_language]


def process(args, wordlist, compatible, gl, lgs):
    row = [wordlist.stem]
    row.append(wordlist)
    m = Matrix.from_wordlist(wordlist)
    if compatible:
        args.log.info("Glottolog compatible")
        doculects, glottocode_problems = wordlist.doculects_with_glottocodes(lgs, gl)
        for ptype, problems in glottocode_problems.__dict__.items():
            loglevel = args.log.warning if ptype != 'family' else args.log.info
            if problems:
                loglevel('{}: {} Glottocodes {}'.format(wordlist.stem, ptype, problems))
        m = m.restrict_matrix(doculects)
    else:
        args.log.info(wordlist.stem)
    charset_sizes = [len(charset) for charset in m.charsets.values()]
    if max(charset_sizes) == 1:
        args.log.warning('Not creating character matrices because of cs_max = 1')
        return [], 0, {}
    row.extend([
        min(charset_sizes),
        max(charset_sizes),
        statistics.mean(charset_sizes),
        statistics.median(charset_sizes),
        statistics.stdev(charset_sizes)])

    row += polymorphism_analysis(m)

    for fname in args.formats:
        func = FORMATS[fname]
        kw = dict(
            missing_is_zero=args.missing_is_zero,
            polymorphism_is_zero=args.polymorphism_is_zero)
        if compatible:
            d = args.repos.compatible_matrices_dir
        else:
            d = args.repos.matrices_dir
        d.joinpath(wordlist.stem).mkdir(parents=True, exist_ok=True)
        p = d.joinpath(wordlist.stem, fname)
        try:
            p.write_text(func(m, **kw))
            args.log.info(fname)
            row.append(MatrixFile(p))
        except ValueError:
            row.append('')
            args.log.warning('cannot create {}'.format(fname))
    maxsize = max(len(v) for _, _, v in m.itervalues())
    d = collections.Counter(len(val) for _, _, val in m.itervalues())
    return row, maxsize, d


def finish(args, table, maxsizes, data, compatible):
    header = [
        'Name',
        'wordlist',
        ('cs_min', False),
        'cs_max',
        ('cs_mean', False),
        ('cs_median', False),
        ('cs_stdev', False),
        'polymorphic_cell_ratio',
        'polymorphic_concept_ratio',
        'concepts_per_language',
    ] + list(args.formats)
    settings = []
    for attr in ['missing_is_zero', 'polymorphism_is_zero']:
        if getattr(args, attr):
            settings.append('- `--{}`'.format(attr.replace('_', '-')))
    if compatible:
        outdir = args.repos.compatible_matrices_dir
    else:
        outdir = args.repos.matrices_dir
    output(
        args,
        header,
        table,
        outdir,
        README_TEMPLATE,
        settings='\n'.join(settings),
    )
    if compatible:
        plot_path = args.repos.compatible_matrices_dir / 'stats.svg'
    else:
        plot_path = args.repos.matrices_dir / 'stats.svg'
    if args.plotstyle == 1:
        plot_wordlist_stats(
            data,
            plot_path,
            (12, 8),
            plot,
            args.test,
            max(maxsizes),
        )
    if args.plotstyle == 2:
        plot_wordlist_stats(
            data,
            plot_path,
            (12, 8),
            plot_style2,
            args.test,
            max(maxsizes),
        )


def run(args):
    if not args.repos.wordlists_dir.exists():
        args.log.error('Run lingpy_wordlists before character_matrices')
        return
    empty_dir(args.repos.matrices_dir)

    glcat = Catalog(args.glottolog, args.glottolog_version) \
        if args.glottolog else Catalog.from_config('glottolog', tag=args.glottolog_version)
    with glcat:
        gl = Glottolog(glcat.dir)
        lgs = {lg.id: lg for lg in gl.languoids()}

    table = []
    table_compatible = []
    data, maxsizes = collections.OrderedDict(), []
    data_compatible, maxsizes_compatible = collections.OrderedDict(), []

    for wordlist in args.repos.iter_wordlists(
            lambda wl: not args.wordlist or wl.stem == args.wordlist):

        row, maxsize, d = process(args, wordlist, False, None, None)
        if len(row) == 0:
            continue
        table.append(row)
        maxsizes.append(maxsize)
        data[wordlist.stem] = d
        row, maxsize, d = process(args, wordlist, True, gl, lgs)
        if len(row) == 0:
            continue
        table_compatible.append(row)
        maxsizes_compatible.append(maxsize)
        data_compatible[wordlist.stem] = d

    finish(args, table, maxsizes, data, False)
    finish(args, table_compatible, maxsizes_compatible, data_compatible, True)


def plot(ax, data, maxsize):
    colors = {1: '#fff'}
    for i, color in zip(range(2, maxsize + 1), sequential_colors(maxsize + 2)[3:]):
        colors[i] = color

    ax.set_xlabel('number of concept-language pairs')
    ax.legend(
        handles=[
            mpatches.Patch(color=colors[i], label='polymorphic' if i > 1 else 'non-polymorphic')
            for i in range(1, maxsize + 1)
        ],
        fontsize=6,
    )

    bottom = [0 for _ in data.keys()]
    for size in range(1, maxsize + 1):
        ax.barh(
            data.keys(),
            [data[k].get(size, 0) for k in data.keys()],
            height=[0.7 for _ in data.keys()],
            left=bottom,
            edgecolor='black',
            linewidth=1,
            color=colors[size],)
        for i, k in enumerate(data.keys()):
            bottom[i] = bottom[i] + data[k].get(size, 0)

    ax.tick_params(axis='y', labelsize=6)


def plot_style2(ax, data, maxsize):
    colors = []
    for size in range(0, maxsize + 1):
        if size < 10:
            colors.append(cm.to_hex(plt.cm.tab10(size)))
        else:
            colors.append("black")

    bottom = [0 for _ in data.keys()]
    for size in range(0, maxsize + 1):
        ax.barh(
            data.keys(),
            [data[k].get(size, 0) for k in data.keys()],
            left=bottom,
            color=colors[size],
            label=r'$\nu=' + str(size) + '$')
        for i, k in enumerate(data.keys()):
            bottom[i] = bottom[i] + data[k].get(size, 0)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), fancybox=True, shadow=True, ncol=11)
    ax.tick_params(axis='y', labelsize=6)
    ax.set_xlabel("#language-concept-pairs")
