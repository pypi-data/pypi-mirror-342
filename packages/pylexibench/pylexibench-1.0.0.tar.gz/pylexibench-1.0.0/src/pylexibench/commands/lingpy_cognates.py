"""
Compute cognate sets.
"""
import statistics

from lingpy import Wordlist, LexStat
from lingpy.evaluate.acd import bcubes
from pylexibench.util import output, empty_dir


def register(parser):
    parser.add_argument("algorithm", choices=["lexstat", "sca"])
    parser.add_argument("--cognate-threshold", type=int, default=50)
    parser.add_argument("--sca-threshold", type=float, default=0.45)
    parser.add_argument("--lexstat-threshold", type=float, default=0.55)


def run(args):
    if not args.repos.wordlists_dir.exists():
        args.log.error('Run lingpy_wordlists before lingpy_cognates')
        return
    empty_dir(args.repos.cognates_dir)
    table = []
    for wordlist in args.repos.iter_wordlists():
        args.log.info(f"Analyzing wordlist {wordlist.name[:-4]}...")
        res = (sca if args.algorithm == "sca" else lexstat)(
            wordlist,
            args.sca_threshold,
            args.lexstat_threshold,
            args.cognate_threshold,
            test=args.test)
        if res:
            table.append([wordlist.name[:-4]] + list(res))
        args.log.info("...done")

    table.append(
        ["TOTAL"] + [statistics.mean([row[i] for row in table]) for i in range(len(table[0])) if i])
    header = ["Dataset", "SCA Precision", "SCA Recall", "SCA F-Score"]
    if args.algorithm == "lexstat":
        header.extend(["LexStat Precision", "LexStat Recall", "LexStat F-Score"])

    output(
        args,
        header,
        table,
        args.repos.cognates_dir,
        """# Computed cognacy

{table}
""",
        settings="""
- Algorithm: {args.algorithm} with thresholds
- `--sca-threshold`: {args.sca_threshold}
- `--lexstat-threshold`: {args.lexstat_threshold}
""".format(args=args)
    )


def sca(wordlist, sca_threshold, lexstat_threshold, cognate_threshold, test=False):
    lex = LexStat(str(wordlist))
    lex.cluster(method="sca", ref="scaid", threshold=sca_threshold)
    return bcubes(lex, "cogid", "scaid", pprint=False)


def lexstat(wordlist, sca_threshold, lexstat_threshold, cognate_threshold, test=False):
    wl = Wordlist(str(wordlist))
    if wl.width <= cognate_threshold:
        lex = LexStat(str(wordlist))
        lex.cluster(method="sca", ref="scaid", threshold=sca_threshold)
        p, r, f = bcubes(lex, "cogid", "scaid", pprint=False)
        lex.get_scorer(runs=10 if test else 10000)
        lex.cluster(
            method="lexstat",
            ref="lexstatid",
            threshold=lexstat_threshold,
            cluster_method="infomap")
        p2, r2, f2 = bcubes(lex, "cogid", "lexstatid", pprint=False)
        return [p, r, f, p2, r2, f2]
