"""Test module for refer process tool."""

from argparse import Namespace
from pathlib import Path
import pydoc
import sys
import time

import yaml

import pytest

from bibliograpy.api_common import cite

from bibliograpy.process import _process


def _refer_resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / 'refer' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def _output(file: str) -> str:
    """Chemin vers les fichiers de sortie."""
    return str(Path(Path(__file__).parent / 'resources' / 'refer' / 'out' / file))


def test_yml_to_yml():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.yml'),
                       output_file=_output('test_yml_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                'A': ['Brian W. Kernighan', 'Lorinda L. Cherry'],
                'T': 'A System for Typesetting Mathematics',
                'J': 'J. Comm. ACM',
                'V': '18',
                'N': '3',
                'D': 'March 1978',
                'P': '151-157',
                'K': 'eqn'
            }]

def test_yml_to_refer():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.yml'),
                       output_file=_output('test_yml_to_refer.refer'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_refer.refer'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%A Brian W. Kernighan
%A Lorinda L. Cherry
%T A System for Typesetting Mathematics
%J J. Comm. ACM
%V 18
%N 3
%D March 1978
%P 151-157
%K eqn

"""

def test_yml_to_json():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.yml'),
                       output_file=_output('test_yml_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_yml_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"A": ["Brian W. Kernighan", "Lorinda L. Cherry"], '
                           '"T": "A System for Typesetting Mathematics", '
                           '"J": "J. Comm. ACM", '
                           '"V": "18", '
                           '"N": "3", '
                           '"D": "March 1978", '
                           '"P": "151-157", '
                           '"K": "eqn"}]')

def test_json_to_yml():
    """test process from a json bibliography to a yml bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.json'),
                       output_file=_output('test_json_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                'A': ['Brian W. Kernighan', 'Lorinda L. Cherry'],
                'T': 'A System for Typesetting Mathematics',
                'J': 'J. Comm. ACM',
                'V': '18',
                'N': '3',
                'D': 'March 1978',
                'P': '151-157',
                'K': 'eqn'
            }]

def test_json_to_refer():
    """test process from a json bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.json'),
                       output_file=_output('test_json_to_refer.refer'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_refer.refer'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%A Brian W. Kernighan
%A Lorinda L. Cherry
%T A System for Typesetting Mathematics
%J J. Comm. ACM
%V 18
%N 3
%D March 1978
%P 151-157
%K eqn

"""

def test_json_to_json():
    """test process from a json bibliography to a json bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.json'),
                       output_file=_output('test_json_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_json_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"A": ["Brian W. Kernighan", "Lorinda L. Cherry"], '
                           '"T": "A System for Typesetting Mathematics", '
                           '"J": "J. Comm. ACM", '
                           '"V": "18", '
                           '"N": "3", '
                           '"D": "March 1978", '
                           '"P": "151-157", '
                           '"K": "eqn"}]')

def test_refer_to_yml():
    """test process from a bib bibliography to a yml bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.refer'),
                       output_file=_output('test_refer_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_refer_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {
                'A': ['Brian W. Kernighan', 'Lorinda L. Cherry'],
                'T': 'A System for Typesetting Mathematics',
                'J': 'J. Comm. ACM',
                'V': '18',
                'N': '3',
                'D': 'March 1978',
                'P': '151-157',
                'K': 'eqn'
            }]

def test_refer_to_refer():
    """test process from a RIS 2001 bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.refer'),
                       output_file=_output('test_refer_to_refer.refer'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_refer_to_refer.refer'), encoding='utf-8') as s:
        content = s.read()
        assert content == """%A Brian W. Kernighan
%A Lorinda L. Cherry
%T A System for Typesetting Mathematics
%J J. Comm. ACM
%V 18
%N 3
%D March 1978
%P 151-157
%K eqn

"""

def test_refer_to_json():
    """test process from a RIS 2001 bibliography to a json bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('sample1.refer'),
                       output_file=_output('test_refer_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_refer_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"A": ["Brian W. Kernighan", "Lorinda L. Cherry"], '
                           '"T": "A System for Typesetting Mathematics", '
                           '"J": "J. Comm. ACM", '
                           '"V": "18", '
                           '"N": "3", '
                           '"D": "March 1978", '
                           '"P": "151-157", '
                           '"K": "eqn"}]')

def test_yml_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('mini.yml'),
                       output_file=_sibbling_module('test_refer_yml_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_refer_yml_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_json_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('mini.json'),
                       output_file=_sibbling_module('test_refer_json_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_refer_json_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_refer_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='refer',
                       file=_refer_resource('mini.refer'),
                       output_file=_sibbling_module('test_refer_refer_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_refer_refer_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_refer

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_input_file_not_found():
    """test process input file not found"""

    with pytest.raises(FileNotFoundError) as e:
        with open(_refer_resource('not_existing_file.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
