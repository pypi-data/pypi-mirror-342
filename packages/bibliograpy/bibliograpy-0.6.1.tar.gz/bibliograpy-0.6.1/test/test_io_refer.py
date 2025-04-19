"""Test module for refer IO"""
from pathlib import Path
from typing import TextIO

from bibliograpy.api_core import Formats
from bibliograpy.api_refer import Tags
from bibliograpy.io_refer import ReferInputFormat


def read_entries(i: TextIO):
    """ris entry parsing shortcut"""
    return ReferInputFormat(Formats.REFER).from_standard(i)

def test_sample1():
    """test refer sample"""

    with open(Path(__file__).parent / 'resources' / 'refer' / 'sample1.refer', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.A: ['Brian W. Kernighan', 'Lorinda L. Cherry'],
            Tags.T: 'A System for Typesetting Mathematics',
            Tags.J: 'J. Comm. ACM',
            Tags.V: '18',
            Tags.N: '3',
            Tags.D: 'March 1978',
            Tags.P: '151-157',
            Tags.K: 'eqn'
        }

def test_sample2():
    """test refer sample"""

    with open(Path(__file__).parent / 'resources' / 'refer' / 'sample2.refer', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 1
        assert result[0] == {
            Tags.A: ['Brian W. Kernighan', 'Lorinda L. Cherry'],
            Tags.T: 'A System for Typesetting Mathematics',
            Tags.J: 'J. Comm. ACM',
            Tags.V: '18',
            Tags.N: '3',
            Tags.D: 'March 1978',
            Tags.P: '151-157',
            Tags.K: 'eqn'
        }

def test_sample3():
    """test refer sample"""

    with open(Path(__file__).parent / 'resources' / 'refer' / 'sample3.refer', encoding='utf-8') as s:
        result = read_entries(s)
        assert len(result) == 2
        assert result[0] == {
            Tags.A: ['Brian W. Kernighan'],
            Tags.T: 'A System for Typesetting Mathematics',
            Tags.J: 'J. Comm. ACM',
            Tags.V: '18',
            Tags.N: '3',
            Tags.D: 'March 1978',
            Tags.P: '151-157',
            Tags.K: 'eqn'
        }
        assert result[1] == {
            Tags.A: ['Lorinda L. Cherry'],
            Tags.T: 'A System for Typesetting Mathematics',
            Tags.J: 'J. Comm. ACM',
            Tags.V: '18',
            Tags.N: '3',
            Tags.D: 'March 1978',
            Tags.P: '151-157',
            Tags.K: 'eqn'
        }
