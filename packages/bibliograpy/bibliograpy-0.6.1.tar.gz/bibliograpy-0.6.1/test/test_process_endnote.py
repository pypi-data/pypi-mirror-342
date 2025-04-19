"""Test module for endnote process tool."""

from argparse import Namespace
from pathlib import Path
import pydoc
import sys
import time

import yaml

import pytest

from bibliograpy.api_common import cite

from bibliograpy.process import _process


def _endnote_resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / 'endnote' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def _output(file: str) -> str:
    """Chemin vers les fichiers de sortie."""
    return str(Path(Path(__file__).parent / 'resources' / 'endnote' / 'out' / file))


def test_yml_to_yml():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.yml'),
                       output_file=_output('test_yml_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                '0': 'Journal Article',
                '@': '0066-4189',
                'A': ['Le Bars, Michael', 'Cébron, David', 'Le Gal, Patrice'],
                'D': '2015',
                'I': 'Annual Reviews',
                'J': 'Annual Review of Fluid Mechanics',
                'N': '1',
                'P': '163-193',
                'T': 'Flows driven by libration, precession, and tides',
                'V': '47'
            }
        ]

def test_yml_to_endnote():
    """test process from a yml bibliography to an endnote bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.yml'),
                       output_file=_output('test_yml_to_endnote.enw'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_endnote.enw'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%0 Journal Article
%T Flows driven by libration, precession, and tides
%A Le Bars, Michael
%A Cébron, David
%A Le Gal, Patrice
%J Annual Review of Fluid Mechanics
%V 47
%N 1
%P 163-193
%@ 0066-4189
%D 2015
%I Annual Reviews

"""

def test_yml_to_json():
    """test process from a yml bibliography to a json bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.yml'),
                       output_file=_output('test_yml_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"0": "Journal Article", '
                           '"T": "Flows driven by libration, precession, and tides", '
                           '"A": ["Le Bars, Michael", "C\\u00e9bron, David", "Le Gal, Patrice"], '
                           '"J": "Annual Review of Fluid Mechanics", '
                           '"V": "47", '
                           '"N": "1", '
                           '"P": "163-193", '
                           '"@": "0066-4189", '
                           '"D": "2015", '
                           '"I": "Annual Reviews"}]')

def test_json_to_yml():
    """test process from a json bibliography to a yml bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.json'),
                       output_file=_output('test_json_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                '0': 'Journal Article',
                '@': '0066-4189',
                'A': ['Le Bars, Michael', 'Cébron, David', 'Le Gal, Patrice'],
                'D': '2015',
                'I': 'Annual Reviews',
                'J': 'Annual Review of Fluid Mechanics',
                'N': '1',
                'P': '163-193',
                'T': 'Flows driven by libration, precession, and tides',
                'V': '47'
            }
        ]

def test_json_to_endnote():
    """test process from a json bibliography to an endnote bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.json'),
                       output_file=_output('test_json_to_endnote.enw'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_endnote.enw'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%0 Journal Article
%T Flows driven by libration, precession, and tides
%A Le Bars, Michael
%A Cébron, David
%A Le Gal, Patrice
%J Annual Review of Fluid Mechanics
%V 47
%N 1
%P 163-193
%@ 0066-4189
%D 2015
%I Annual Reviews

"""

def test_json_to_json():
    """test process from a json bibliography to a json bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.json'),
                       output_file=_output('test_json_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"0": "Journal Article", '
                           '"T": "Flows driven by libration, precession, and tides", '
                           '"A": ["Le Bars, Michael", "C\\u00e9bron, David", "Le Gal, Patrice"], '
                           '"J": "Annual Review of Fluid Mechanics", '
                           '"V": "47", '
                           '"N": "1", '
                           '"P": "163-193", '
                           '"@": "0066-4189", '
                           '"D": "2015", '
                           '"I": "Annual Reviews"}]')

def test_endnote_to_yml():
    """test process from an endnote bibliography to a yml bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.enw'),
                       output_file=_output('test_endnote_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_endnote_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                '0': 'Journal Article',
                '@': '0066-4189',
                'A': ['Le Bars, Michael', 'Cébron, David', 'Le Gal, Patrice'],
                'D': '2015',
                'I': 'Annual Reviews',
                'J': 'Annual Review of Fluid Mechanics',
                'N': '1',
                'P': '163-193',
                'T': 'Flows driven by libration, precession, and tides',
                'V': '47'
            }
        ]

def test_endnote_to_endnote():
    """test process from an endnote bibliography to an endnote bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.enw'),
                       output_file=_output('test_endnote_to_endnote.enw'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_endnote_to_endnote.enw'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%0 Journal Article
%T Flows driven by libration, precession, and tides
%A Le Bars, Michael
%A Cébron, David
%A Le Gal, Patrice
%J Annual Review of Fluid Mechanics
%V 47
%N 1
%P 163-193
%@ 0066-4189
%D 2015
%I Annual Reviews

"""

def test_endnote_to_json():
    """test process from an endnote bibliography to a json bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('sample1.enw'),
                       output_file=_output('test_endnote_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_endnote_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"0": "Journal Article", '
                           '"T": "Flows driven by libration, precession, and tides", '
                           '"A": ["Le Bars, Michael", "C\\u00e9bron, David", "Le Gal, Patrice"], '
                           '"J": "Annual Review of Fluid Mechanics", '
                           '"V": "47", '
                           '"N": "1", '
                           '"P": "163-193", '
                           '"@": "0066-4189", '
                           '"D": "2015", '
                           '"I": "Annual Reviews"}]')

def test_yml_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('mini.yml'),
                       output_file=_sibbling_module('test_endnote_yml_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_yml_to_py import INTERNATIONAL_ASTRONOMICAL_UNION, NASA

    @cite(INTERNATIONAL_ASTRONOMICAL_UNION, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union
    * NASA
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union
    * NASA
""")

def test_json_to_py():
    """test process from a json bibliography to a py source bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('mini.json'),
                       output_file=_sibbling_module('test_endnote_json_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_json_to_py import INTERNATIONAL_ASTRONOMICAL_UNION, NASA

    @cite(INTERNATIONAL_ASTRONOMICAL_UNION, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union
    * NASA
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union
    * NASA
""")

def test_endnote_to_py():
    """test process from an endnote bibliography to a py source bibliography"""

    _process(Namespace(CMD='endnote',
                       file=_endnote_resource('mini.enw'),
                       output_file=_sibbling_module('test_endnote_endnote_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_endnote_endnote_to_py import INTERNATIONAL_ASTRONOMICAL_UNION, NASA

    @cite(INTERNATIONAL_ASTRONOMICAL_UNION, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union
    * NASA
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_endnote

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union
    * NASA
""")

def test_input_file_not_found():
    """test process input file not found"""

    with pytest.raises(FileNotFoundError) as e:
        with open(_endnote_resource('not_existing_file.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
