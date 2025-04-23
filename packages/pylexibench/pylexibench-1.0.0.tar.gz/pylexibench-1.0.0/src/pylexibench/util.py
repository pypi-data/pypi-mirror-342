import shutil
import typing
import pathlib
import argparse
import collections

import matplotlib.pyplot as plt
from clldutils.clilib import Table as CLITable
from clldutils.markup import Table, add_markdown_text, iter_markdown_sections
from csvw.dsv import UnicodeWriter
from lingpy import tokens2class, Wordlist

__all__ = ['clean_wordlist', 'clean_cognacy', 'output', 'empty_dir']


def plot_wordlist_stats(data, figpath, figsize, func, test, *args, **kwargs):
    data = collections.OrderedDict(
        # Sort data by family first.
        sorted(data.items(), key=lambda i: (i[0].split('-')[-1], i[0].split('-')[0]), reverse=True))
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0.3)

    func(ax, data, *args, **kwargs)

    fig.tight_layout()
    plt.savefig(str(figpath))
    if not test:
        plt.show()  # pragma: no cover
    return fig, ax


def empty_dir(d):
    if not d.exists():
        d.mkdir()
    for p in d.iterdir():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
    return d


def output(args: argparse.Namespace,
           header: typing.List[str],
           table: typing.Iterable[typing.Iterable],
           outdir: pathlib.Path,
           readme_template: str,
           settings: typing.Optional[str] = None,
           with_cli_table=True,
           **fmt_kw):
    """
    Write tabular output to the terminal, to a markdown formatted file and to a TSV file.
    """
    drop = []
    for i, col in enumerate(header):
        if isinstance(col, tuple) and not col[1]:
            drop.append(i)
    header = [col[0] if isinstance(col, tuple) else col for col in header]

    if with_cli_table:
        with CLITable(
                args,
                *[col for i, col in enumerate(header) if i not in drop], **fmt_kw) as t:
            for row in table:
                t.append([str(cell) for i, cell in enumerate(row) if i not in drop])
    fmt_kw['rows'] = [
        [getattr(cell, 'markdown', str(cell)) for i, cell in enumerate(row) if i not in drop]
        for row in table]
    tsv_path = outdir / 'stats.tsv'
    tsv_path.parent.mkdir(parents=True, exist_ok=True)
    with UnicodeWriter(tsv_path, delimiter="\t") as writer:
        writer.writerows([header] + table)
    tbl = Table(*[col for i, col in enumerate(header) if i not in drop], **fmt_kw).render()
    readme = readme_template.format(table=tbl)
    title = next(iter_markdown_sections(readme))[1]
    desc = """
The data in this directory has been created running the `lexibench {}` command""".format(
        outdir.name)
    if settings:
        desc += " with the following settings:\n{}\n".format(settings)
    else:
        desc += '.'
    desc += '\nSummary statistics about the data is available in [stats.tsv](stats.tsv).\n\n'
    outdir.joinpath('README.md').write_text(add_markdown_text(readme, desc, title))


def clean_cognacy(cognacy, col='cognacy'):
    if cognacy:
        # We ignore the ?, marking some sort of doubt in a cognacy assignment.
        cognacy = cognacy.replace('?', '')

    if not cognacy or not cognacy.strip() or cognacy.strip() == "0":
        return None

    if col == 'partial_cognacy':  # pragma: no cover
        cogids = cognacy.split()
        if len(cogids) == 1:
            return cogids[0]
        # Reducing partial cognacy to "full" cognacy requires indovidual decisions.
        # See Wu and List 2023.
        return None

    for cogid in cognacy.split(','):
        assert cogid.strip()
        return cogid.strip()


def clean_wordlist(wln):
    edited = 0
    for items, idx in enumerate(wln, start=1):
        for h in wln.columns:
            entry = wln[idx, h]
            if isinstance(entry, str):
                pentry = (entry
                          .replace("\t", "")
                          .replace("\n", "")
                          .replace("\r", ''))
                # Fix unclosed quotes which will create problems when written to TSV.
                if pentry.startswith('"') and not pentry.endswith('"'):
                    pentry = pentry[1:]
                if entry != pentry:
                    edited += 1
                    wln[idx, h] = pentry

    exclude = {}
    for idx in wln:
        if wln[idx, 'cogid'] is None:
            exclude[idx] = 'not-coded'
        else:
            try:
                tokens2class(wln[idx, "tokens"], "sca")
            except ValueError:
                exclude[idx] = 'not-segmentable'
    if exclude:
        new_wl = {0: wln.columns}
        for idx in wln:
            if idx not in exclude:
                new_wl[idx] = wln[idx]
        wln = Wordlist(new_wl)
    return (
        wln,
        items,
        edited,
        len([v for v in exclude.values() if v == 'not-segmentatble']),
        len([v for v in exclude.values() if v == 'not-coded']))
