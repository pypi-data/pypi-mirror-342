"""Test module for bibtex process tool."""
from argparse import Namespace
from pathlib import Path
import pydoc
import sys
import time

import yaml

import pytest

from bibliograpy.process import _process
from bibliograpy.api_common import cite

def _bibtex_resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / 'bibtex' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def _output(file: str) -> str:
    """Chemin vers les fichiers de sortie."""
    return str(Path(Path(__file__).parent / 'resources' / 'bibtex' / 'out' / file))


def test_bibtex_yml_to_yml():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.yml'),
                       output_file=_output('test_bibtex_yml_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_yml_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [{
            'entry_type': 'misc',
            'cite_key': 'nasa',
            'title': 'NASA'
        },{
            'entry_type': 'misc',
            'cite_key': 'iau',
            'title': 'International Astronomical Union'
        }]

def test_bibtex_yml_to_bib():
    """test process from a yml bibliography to a bibtex bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.yml'),
                       output_file=_output('test_bibtex_yml_to_bib.bib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_yml_to_bib.bib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """@misc{nasa,
 title = {NASA}
}

@misc{iau,
 title = {International Astronomical Union}
}
"""

def test_bibtex_yml_to_json():
    """test process from a yml bibliography to a bibtex bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.yml'),
                       output_file=_output('test_bibtex_yml_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_yml_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"entry_type": "misc", "cite_key": "nasa", "title": "NASA"}, '
                           '{"entry_type": "misc", "cite_key": "iau", "title": "International Astronomical Union"}]')

def test_bibtex_json_to_yml():
    """test process from a json bibliography to a yml bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.json'),
                       output_file=_output('test_bibtex_json_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_json_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [{
            'entry_type': 'misc',
            'cite_key': 'nasa',
            'title': 'NASA'
        },{
            'entry_type': 'misc',
            'cite_key': 'iau',
            'title': 'International Astronomical Union'
        }]

def test_bibtex_json_to_bib():
    """test process from a json bibliography to a bibtex bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.json'),
                       output_file=_output('test_bibtex_json_to_bib.bib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_json_to_bib.bib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """@misc{nasa,
 title = {NASA}
}

@misc{iau,
 title = {International Astronomical Union}
}
"""

def test_bibtex_json_to_json():
    """test process from a json bibliography to a json bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.json'),
                       output_file=_output('test_bibtex_json_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_json_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"entry_type": "misc", "cite_key": "nasa", "title": "NASA"}, '
                           '{"entry_type": "misc", "cite_key": "iau", "title": "International Astronomical Union"}]')

def test_bibtex_bib_to_yml():
    """test process from a bib bibliography to a yml bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.json'),
                       output_file=_output('test_bibtex_bib_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_bib_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [{
            'entry_type': 'misc',
            'cite_key': 'nasa',
            'title': 'NASA'
        },{
            'entry_type': 'misc',
            'cite_key': 'iau',
            'title': 'International Astronomical Union'
        }]

def test_bibtex_bib_to_bib():
    """test process from a bibtex bibliography to a bibtex bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.bib'),
                       output_file=_output('test_bibtex_bib_to_bib.bib'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_bib_to_bib.bib'), encoding='utf-8') as s:
        content = s.read()
        assert content == """@misc{nasa,
 title = {NASA}
}

@misc{iau,
 title = {International Astronomical Union}
}
"""

def test_bibtex_bib_to_json():
    """test process from a bibtex bibliography to a json bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.bib'),
                       output_file=_output('test_bibtex_bib_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_bibtex_bib_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"entry_type": "misc", "cite_key": "nasa", "title": "NASA"}, '
                           '{"entry_type": "misc", "cite_key": "iau", "title": "International Astronomical Union"}]')

def test_bibtex_yml_to_yml_astroloj():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('astroloj.json'),
                       output_file=_bibtex_resource('astroloj.py'),
                       encoding='utf-8',
                       output_dir='.'))

def test_bibtex_yml_to_yml_cosmoloj():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('cosmoloj.json'),
                       output_file=_bibtex_resource('cosmoloj.py'),
                       encoding='utf-8',
                       output_dir='.'))

def test_bibtex_yml_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.yml'),
                       output_file=_sibbling_module('test_bibtex_yml_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_bibtex_yml_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_bibtex_json_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.json'),
                       output_file=_sibbling_module('test_bibtex_json_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_bibtex_json_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_bibtex_bib_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='bibtex',
                       file=_bibtex_resource('mini.bib'),
                       output_file=_sibbling_module('test_bibtex_bib_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_bibtex_bib_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_input_file_not_found():
    """test process input file not found"""

    with pytest.raises(FileNotFoundError) as e:
        with open(_bibtex_resource('not_existing_file.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
