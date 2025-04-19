"""Test module for endnote IO"""
from pathlib import Path
from typing import TextIO

from bibliograpy.api_core import Formats
from bibliograpy.api_endnote import Tags
from bibliograpy.io_endnote import EndnoteInputFormat


def read_entries(i: TextIO):
    """ris entry parsing shortcut"""
    return EndnoteInputFormat(Formats.ENDNOTE).from_standard(i)

def test_sample1():
    """test endnote sample1"""

    with open(Path(__file__).parent / 'resources' / 'endnote' / 'sample1.enw', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.D: '2015',
            Tags.I: 'Annual Reviews',
            Tags.N: '1',
            Tags.P: '163-193',
            Tags.AT: '0066-4189',
            Tags.J: 'Annual Review of Fluid Mechanics',
            Tags.V: '47',
            Tags.ZERO: 'Journal Article',
            Tags.T: 'Flows driven by libration, precession, and tides',
            Tags.A: ['Le Bars, Michael', 'Cébron, David', 'Le Gal, Patrice']
        }

def test_sample2():
    """test endnote sample2"""

    with open(Path(__file__).parent / 'resources' / 'endnote' / 'sample2.enw', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.D: '2003',
            Tags.I: 'IOP Publishing',
            Tags.N: '1',
            Tags.P: '494',
            Tags.AT: '1538-3881',
            Tags.J: 'The Astronomical Journal',
            Tags.V: '126',
            Tags.ZERO: 'Journal Article',
            Tags.T: 'A new precession formula',
            Tags.A: ['Fukushima, Toshio']
        }

def test_sample3():
    """test endnote sample3"""

    with open(Path(__file__).parent / 'resources' / 'endnote' / 'sample3.enw', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 2
        assert result[0] == {
            Tags.D: '2016',
            Tags.I: 'Elsevier',
            Tags.P: '317-323',
            Tags.AT: '0096-3003',
            Tags.J: 'Applied Mathematics and Computation',
            Tags.V: '275',
            Tags.ZERO: 'Journal Article',
            Tags.T: 'A new approach on curves of constant precession',
            Tags.A: ['Uzunoğlu, Beyhan', 'Gök, İsmail', 'Yaylı, Yusuf']
        }
        assert result[1] == {
            Tags.D: '2016',
            Tags.I: 'Elsevier',
            Tags.P: '317-323',
            Tags.AT: '0096-3003',
            Tags.J: 'Applied Mathematics and Computation',
            Tags.V: '275',
            Tags.ZERO: 'Journal Article',
            Tags.T: 'A new approach on curves of constant precession',
            Tags.A: ['Uzunoğlu, Beyhan', 'Gök, İsmail']
        }
