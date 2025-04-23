"""
Create trees for the families referenced in the lingpy_wordlists, based on the Glottolog
classification and pruned and renamed to the varieties in the wordlist.
"""
import pathlib

from pyglottolog import Glottolog
from cldfcatalog import Catalog
from clldutils.path import git_describe

from pylexibench.tree import get_tree
from pylexibench.util import output, empty_dir


class Tree(type(pathlib.Path())):
    @property
    def markdown(self):
        return '[{}]({})'.format(self.stem, self.name)


def register(parser):
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


def run(args):
    if not args.repos.wordlists_dir.exists():
        args.log.error('Run lingpy_wordlists before glottolog_trees')
        return
    empty_dir(args.repos.trees_dir)
    table, ascii_trees = [], []
    glcat = Catalog(args.glottolog, args.glottolog_version) \
        if args.glottolog else Catalog.from_config('glottolog', tag=args.glottolog_version)
    with glcat:
        gl_version = git_describe(glcat.dir)
        gl = Glottolog(glcat.dir)
        lgs = {lg.id: lg for lg in gl.languoids()}
        for wordlist in args.repos.iter_wordlists(
                lambda wl: not args.wordlist or wl.stem == args.wordlist):
            gc2lid, glottocode_problems = wordlist.glottocode2doculects(lgs, gl)
            for ptype, problems in glottocode_problems.__dict__.items():
                loglevel = args.log.warning if ptype != 'family' else args.log.info
                if problems:
                    loglevel('{}: {} Glottocodes {}'.format(wordlist.stem, ptype, problems))
            tree = get_tree(gc2lid, lgs)
            splits = [len(n.descendants) for n in tree.walk() if n.descendants]
            table.append([
                wordlist,
                Tree(args.repos.trees_dir.joinpath(wordlist.stem + '.tree')),
                len(wordlist.doculects),
                sum(1 for n in tree.walk() if n.is_leaf),
                len(splits),
                len([s for s in splits if s > 2]),
            ])
            if sum(1 for n in tree.walk() if n.is_leaf) <= 50:
                ascii_trees.append('## {}\n\n```\n{}\n```\n'.format(
                    wordlist.stem, tree.ascii_art()))
            args.repos.trees_dir.mkdir(parents=True, exist_ok=True)
            args.repos.trees_dir.joinpath(wordlist.stem + '.tree').write_text(
                "{};".format(tree.newick))
    output(
        args,
        ['Wordlist', 'Tree', 'Doculects', 'Leafs in tree', 'Splits', 'Polytomies'],
        table,
        args.repos.trees_dir,
        """# Glottolog trees

## Tree files

The following tree files in Newick format are available. These use the `DOCULECT` values from the
corresponding wordlists as node labels.

{table}

Trees with at most 50 leafs are shown below.
""" + '\n'.join(ascii_trees),
        settings="""
[Glottolog](https://github.com/glottolog/glottolog) version {}
""".format(gl_version)
    )
