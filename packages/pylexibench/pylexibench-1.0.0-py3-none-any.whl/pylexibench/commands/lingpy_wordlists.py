"""
Extract LingPy lingpy_wordlists from lexibank datasets.
"""
import math
import collections

from matplotlib import colormaps, ticker
import matplotlib.patches as mpatches
import matplotlib.colors as cm
import matplotlib.pyplot as plt
from pylexibench.util import output, plot_wordlist_stats, empty_dir
from pylexibench.wordlist import Wordlist
from pylexibench.matrix import Matrix

README_TEMPLATE = """\
# LingPy Wordlists


## Wordlist statistics

The following table lists single-family lingpy_wordlists extracted from the Lexibank datasets
listed in [download](../download).

{table}

![](stats.svg)
"""


def format_settings(args):
    res = [
        "`--language-threshold`: {args.language_threshold}",
        "`--concept-threshold`: {args.concept_threshold}",
        "[`--coverage-threshold`](https://github.com/lingpy/lingpy/blob/"
        "7c3bb88fb4417aba058cbc3e41f6277bbe8b37c5/src/lingpy/compare/"
        "sanity.py#L26): {args.coverage_threshold}"
    ]
    return '\n'.join('- ' + line for line in res).format(args=args)


def register(parser):
    parser.add_argument(
        "--language-threshold",
        help="Number of different varieties a wordlist must contain to be considered",
        type=int,
        default=4)
    parser.add_argument(
        "--concept-threshold",
        help="Number of different concepts a wordlist must contain to be considered",
        type=int,
        default=85)
    parser.add_argument(
        "--coverage-threshold",
        help="Minimum coverage (computed as `lingpy.sanity.average_coverage`) a wordlist must "
             "have to be considered",
        type=float,
        default=0.45)
    parser.add_argument(
        '--plotstyle',
        type=int,
        choices=range(1, 3),
        help='Style of stats plot',
        default=1)


def run(args):
    if not args.repos.download_dir.exists():
        args.log.error('Run download before lingpy_wordlists')
        return
    empty_dir(args.repos.wordlists_dir)
    stats = []
    data, maxsizes, widths = collections.OrderedDict(), [], []
    for dataset in args.repos.datasets:
        for p, stat in dataset.iter_wordlists(
            args.language_threshold,
            args.concept_threshold,
            args.coverage_threshold,
            args.repos.wordlists_dir,
            args.log,
        ):
            wln = Wordlist(p)
            stats.append([dataset, wln] + list(stat))
            m = Matrix.from_wordlist(wln)
            maxsizes.append(m.max_charset_size)
            widths.append(len(m.doculects))
            data[wln.stem] = collections.Counter(len(charset) for charset in m.charsets.values())

    stats = [[i] + list(r) for i, r in enumerate(stats, start=1)]
    if args.plotstyle == 1:
        plot_wordlist_stats(
            data,
            args.repos.wordlists_dir / 'stats.svg',
            (6, 8),
            plot,
            args.test,
            max(maxsizes),
            widths,
        )
    if args.plotstyle == 2:
        plot_wordlist_stats(
            data,
            args.repos.wordlists_dir / 'stats.svg',
            (8, 12),
            plot_style2,
            args.test,
            max(maxsizes),
            widths,
        )
    output(
        args,
        [
            ("Number", False),  # drop
            "Dataset",
            "Filename",
            "Name",
            "Family",
            "Concepts",
            "Languages",
            "Words",
            "Coverage",
            "Diversity",
            "Cognatesets",  # Cognatesets
            ("orig_items", False),  # drop
            ("edited", False),  # drop
            ("unsegmentable", False),  # drop
            ("uncoded", False),  # drop
        ],
        stats,
        args.repos.wordlists_dir,
        README_TEMPLATE,
        settings=format_settings(args),
        with_cli_table=False)


def plot(ax, data, maxsize, widths):
    mw = max(widths)
    # log-scale the heights of the horizontal bars.
    widths = [abs(math.log(w / mw) - math.log(1 / mw)) / math.log(1 / mw) for w in widths]

    ax.set_xlabel('number of concepts')
    bottom = [0 for _ in data.keys()]
    cmx = colormaps['viridis'].resampled(maxsize)

    def co(size):
        return cmx(abs((math.log(size / maxsize) - math.log(1 / maxsize)) / math.log(1 / maxsize)))

    ax.legend(
        handles=[
            mpatches.Patch(color=co(1), label='1 cognate set'),
            mpatches.Patch(color=co(2), label='2 cognate sets'),
            mpatches.Patch(color=co(3), label='3 cognate sets'),
            mpatches.Patch(color=co(maxsize), label='{} cognate sets'.format(maxsize)),
        ],
        fontsize=6,
    )

    for size in range(1, maxsize + 1):
        ax.barh(
            data.keys(),
            [data[k].get(size, 0) for k in data.keys()],
            height=[widths[i] for i, _ in enumerate(data.keys())],
            left=bottom,
            color=co(size))
        for i, k in enumerate(data.keys()):
            bottom[i] = bottom[i] + data[k].get(size, 0)

    ax.set_xscale('log')
    ax.set_xticks([100, 200, 500])
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    ax.tick_params(axis='y', labelsize=6)


def plot_style2(ax, data, maxsize, widths):
    colors = [None]
    for size in range(1, maxsize + 1):
        if size < 10:
            colors.append(cm.to_hex(plt.cm.tab10(size)))
        else:
            colors.append("black")

    ax.set_xlabel('number of concepts')
    bottom = [0 for _ in data.keys()]

    for size in range(1, min(maxsize + 1, 8)):
        if size == 7:
            ax.barh(
                data.keys(),
                [sum([data[k].get(s, 0) for s in range(7, maxsize + 1)]) for k in data.keys()],
                left=bottom,
                color="lightgray",
                label=r'$\kappa \geq 7$')
            break
        if size == 1:
            color = "dimgray"
        else:
            color = cm.to_hex(plt.cm.Set1(size - 2))
        ax.barh(
            data.keys(),
            [data[k].get(size, 0) for k in data.keys()],
            # height=[widths[i] for i, _ in enumerate(data.keys())],
            left=bottom,
            color=color,
            label=r'$\kappa=' + str(size) + '$')
        for i, k in enumerate(data.keys()):
            bottom[i] = bottom[i] + data[k].get(size, 0)

    ax.set_xscale('log')
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    ax.tick_params(axis='y', labelsize=6)
    ax.legend(
        loc='upper center', bbox_to_anchor=(0.5, 1), fancybox=True, shadow=True, ncol=7)
