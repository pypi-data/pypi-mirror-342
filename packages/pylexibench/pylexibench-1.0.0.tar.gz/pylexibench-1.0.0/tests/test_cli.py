import shutil

import pytest
from clldutils.clilib import ParserError

from pylexibench.__main__ import main, RepoType
from pylexibench.repository import Repository


def test_RepoType(tmp_path, tests_dir):
    with pytest.raises(ParserError):
        RepoType(tmp_path)

    assert isinstance(RepoType(tests_dir / 'repos'), Repository)


def test_download(tests_dir, tmp_repos, mocker):
    class Record:
        def __init__(self, doi):
            self.doi = doi
            self.concept_doi = 'cdoi'
            self.creators = ['one author', 'another author']
            self.title = 'the title'
            self.year = '1998'

        @classmethod
        def from_concept_doi(cls, concept_doi):
            return cls('other_doi')

        def download(self, dir):
            shutil.copytree(tests_dir / 'repos' / 'download' / dir.name, dir)

    class API:
        def get_record(self, *args):
            return Record('doi')
    mocker.patch('pylexibench.dataset.cldfzenodo.API', API())
    main(['--repos', str(tmp_repos), 'download', '--force'])
    main(['--repos', str(tmp_repos), 'download', '-u'])
    assert '@book' in tmp_repos.joinpath('download', 'sources.bib').read_text()


def test_workflow(tmp_repos, glottolog_path):
    def run(*args):
        main(['--repos', str(tmp_repos), '--test'] + list(args))

    run('lingpy_wordlists')
    assert tmp_repos.joinpath('lingpy_wordlists', 'README.md').exists()

    run('lingpy_cognates', 'sca')
    assert tmp_repos.joinpath('lingpy_cognates', 'stats.tsv').exists()

    run('lingpy_cognates', 'lexstat')
    assert tmp_repos.joinpath('lingpy_cognates', 'stats.tsv').exists()

    run('glottolog_trees', '--glottolog', str(glottolog_path))
    res = tmp_repos.joinpath('glottolog_trees', 'galuciotupi-tupian.tree').read_text()
    assert res == '(((Ma,((Ak,Me),(Tu,Wa))),Kt),((Xi,Ju),((Aw,(Pg,Ta,Pt,Uk)),Mw),(Ku,Mu)),(((Ar,Gv),Sa),Su),(Pu,Ka));'

    run('character_matrices', '--missing-is-zero')
    res = tmp_repos.joinpath('character_matrices', 'galuciotupi-tupian', 'bin.catg').read_text()
    assert '712' in res
