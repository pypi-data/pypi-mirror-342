# pylexibench

## Installing

Install `pylexibench` via pip, preferably in a new virtual environment:
```shell
pip install pylexibench
```
This will also install the cli command `lexibench`.


## Usage

`pylexibench` provides a set of cli commands to curate a data repository suitable as benchmark for
computational methods for cognate detection and phylogenetic reconstruction. At the core of such a
repository is a list of suitable lexical datasets from the Lexibank collection. Each command
computes artefacts derived from these datasets which are suitable as input for various computational
methods. The output of each command is put in a sub-directory of the repository, named after the
command, so `lexibench download` will populate the `download` directory and so on. In addition,
summary statistics about the computed artefacts are written to a TSV file `stats.tsv` as well as to
a table in a Markdown formatted file `README.md` in this directory. The `README.md` also contains
information about the options passed when running the command.

The commands are implemented as *sub-commands* of the main `lexibench` command, which is installed
when installing the `pylexibench` package.

Before running any pylexibench command, create a direcotry `[my_lexibench_repos]`) where you want to store the lexibench data.
Set up a dataset list `lexibank.tsv` providing the datasets you aim to examine
(for a list with all datasets contained in lexibench see [here](https://codeberg.org/lexibank/lexibench/src/branch/main/etc/lexibank.tsv)).
Place in in `[my_lexibench_repos]/etc/`.

Note that `download` needs to be executed first, followed by `lingpy_wordlists`. The remaining commands can be executed afterwards.
 
```shell
$ lexibench -h
usage: lexibench [-h] [--log-level LOG_LEVEL] [--repos REPOS]
                 COMMAND ...

options:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        log level [ERROR|WARN|INFO|DEBUG] (default: 20)
  --repos REPOS         Directory where dataset list can be found and results stored. (default: None)

available commands:
  Run "COMAMND -h" to get help for a specific command.

  COMMAND
    character_matrices  Write character matrix_formats for cognate data encoded in the lingpy_wordlists.
    download            Download lexibank datasets as specified in the repository's dataset list and write a corresponding
    glottolog_trees     Create trees for the families referenced in the lingpy_wordlists, based on the Glottolog classification
    lingpy_cognates     Compute cognate sets.
    lingpy_wordlists    Extract LingPy lingpy_wordlists from lexibank datasets.
```


## `lexibench download`

The `lexibench download` command downloads the CLDF datasets listed in `etc/lexibank.tsv` from
Zenodo into `download/`.
```shell
$ lexibench download -h
usage: lexibench download [-h] [-f] [-u]

Download lexibank datasets as specified in the repository's dataset list and write a corresponding
BibTeX file for reference.

options:
  -h, --help     show this help message and exit
  -f, --force    Force download of a dataset even if it already exists. (default: False)
  -u, --upgrade  Download newest release of a dataset. (default: False)
```
Exemplary usage  with upgrade option:
```shell
lexibench --repos [my_lexibench_repos] download --upgrade
```


## `lexibench lingpy_wordlists`

The `lexibench lingpy_wordlists` command extracts single-family wordlists from the datasets and
writes these in LingPy's `Wordlist` format to `lingpy_wordlists/`.
```shell
$ lexibench lingpy_wordlists -h
usage: lexibench lingpy_wordlists [-h] [--language-threshold LANGUAGE_THRESHOLD] [--concept-threshold CONCEPT_THRESHOLD] [--coverage-threshold COVERAGE_THRESHOLD]

Extract LingPy lingpy_wordlists from lexibank datasets.

options:
  -h, --help            show this help message and exit
  --language-threshold LANGUAGE_THRESHOLD
                        Number of different varieties a wordlist must contain to be considered (default: 4)
  --concept-threshold CONCEPT_THRESHOLD
                        Number of different concepts a wordlist must contain to be considered (default: 85)
  --coverage-threshold COVERAGE_THRESHOLD
                        Minimum coverage (computed as `lingpy.sanity.average_coverage`) a wordlist must have to be considered (default: 0.45)
```
Exemplary usage:
```shell
lexibench --repos [my_lexibench_repos] lingpy_wordlists
```


## `lexibench glottolog_trees`

The `lexibench glottolog_trees` command computes topological trees based on the Glottolog
classification, i.e. the doculects in a wordlist are matched to Glottolog languoids and the
associated Glottolog family tree is then pruned only contain these doculects as leaf nodes.
```shell
$ lexibench glottolog_trees -h
usage: lexibench glottolog_trees [-h] [--wordlist WORDLIST] [--glottolog GLOTTOLOG] [--glottolog-version GLOTTOLOG_VERSION]

Create trees for the families referenced in the lingpy_wordlists, based on the Glottolog classification
and pruned and renamed to the varieties in the wordlist.

options:
  -h, --help            show this help message and exit
  --wordlist WORDLIST   Name of a specific wordlist to process (default: None)
  --glottolog GLOTTOLOG
                        Path to repository clone of Glottolog data (default: None)
  --glottolog-version GLOTTOLOG_VERSION
                        Version of Glottolog data to checkout (default: None)
```
Exemplary usage:
```shell
lexibench --repos [my_lexibench_repos] glottolog_trees --glottolog [my_glottolog]
```


## `lexibench character_matrices`
The `lexibench character_matrices` creates character matrices in the specified formats for the wordlist in `lingpy_wordlists/` and saves them to `character_matrices/`. Additionally, there are character matrices created, which contain only those languages, for which there is a glottocode available. They are save to `character_matrices_compatible/`. Trees inferred on these character matrices can be compared to the glottolog tree.

```shell
$ lexibench character_matrices -h
usage: lexibench character_matrices [-h] [--missing-is-zero] [--polymorphism-is-zero] --formats FORMATS [FORMATS ...] [--wordlist WORDLIST]

Write character matrices in specified formats for cognate data encoded in the lingpy_wordlists.

options:
  -h, --help            show this help message and exit
  --missing-is-zero     Code a missing counterpart for a concept in a doculect as 0 rather than as missing data (default: False)
  --polymorphism-is-zero
                        Code the case of multiple counterparts (in different cognate sets) for a concept in a doculect as 0 (default: False)
  --formats FORMATS [FORMATS ...]
                        Character matrix formats which are to be constructed (default: ['bin.catg', 'multi.catg', 'bin.phy', 'multi.phy', 'bin.nex', 'multi.nex'])

  --wordlist WORDLIST   Name of a specific wordlist to process (default: None)
  --glottolog GLOTTOLOG
                        Path to repository clone of Glottolog data (default: None)
  --glottolog-version GLOTTOLOG_VERSION
                        Version of Glottolog data to checkout (default: None)
```
Exemplary usage (for creating character matrices in bin.nex and multi.nex format):
```shell
lexibench --repos [my_lexibench_repos] character_matrices --format bin.nex multi.nex --glottolog [my_glottolog]
```


## `lexibench lingpy_cognates`

```shell
$ lexibench lingpy_cognates -h
usage: lexibench lingpy_cognates [-h] [--cognate-threshold COGNATE_THRESHOLD] [--sca-threshold SCA_THRESHOLD] [--lexstat-threshold LEXSTAT_THRESHOLD] {lexstat,sca}

Compute cognate sets.

positional arguments:
  {lexstat,sca}

options:
  -h, --help            show this help message and exit
  --cognate-threshold COGNATE_THRESHOLD
  --sca-threshold SCA_THRESHOLD
  --lexstat-threshold LEXSTAT_THRESHOLD
```
Exemplary usage for cognate clustering with lexstat:
```shell
lexibench --repos [my_lexibench_repos] lingpy_cognates lexstat
```

