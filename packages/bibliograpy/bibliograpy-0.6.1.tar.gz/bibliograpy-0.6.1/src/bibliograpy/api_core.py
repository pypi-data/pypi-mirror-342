"""Core management of reference decorators."""
from dataclasses import dataclass
from enum import Enum
from typing import TextIO

@dataclass(frozen=True)
class Format:
    """A format representation."""
    title: str | None
    command: str | None
    io_extension: list[str]

class Formats(Format, Enum):
    """Supported bibliography formats."""
    BIBTEX = ('Bibtex', 'bibtex', ['bib', 'bibtex'])
    RIS2001 = ('RIS (2001)', 'ris2001', ['ris'])
    RIS2011 = ('RIS (2011)', 'ris2011', ['ris'])
    REFER = ('refer', 'refer', ['refer'])
    ENDNOTE = ('Endnote', 'endnote', ['enw'])
    YML = (None, None, ['yml', 'yaml'])
    JSON = (None, None, ['json'])
    PYTHON = (None, None, ['py'])

    @staticmethod
    def as_command(format_id: str):
        """Gets a supported format enum instance from a supported process argument string."""
        for f in Formats:
            if format_id == f.command:
                return f
        raise ValueError(f'unexpected format {format_id}')

    @staticmethod
    def as_io_extension(format_id: str):
        """Gets a supported format enum instance from a supported process argument string."""
        for f in Formats:
            if format_id in f.io_extension:
                return f
        raise ValueError(f'unexpected format {format_id}')


class InputFormat:
    """InputFormat interface to deserialize a bibliography."""

    def __init__(self, source: Format, standard: Format):
        self._source = source
        self._standard = standard

    def from_yml(self, i: TextIO):
        """Reads from yml representation."""

    def from_json(self, i: TextIO):
        """Reads from json representation."""

    def from_standard(self, i: TextIO):
        """Reads from standard format."""

    def source(self) -> Format:
        """The source format."""
        return self._source

    def standard(self) -> Format:
        """The standard format."""
        return self._standard

    def read(self, i: TextIO):
        """Deserialization method."""
        if self.source() is Formats.YML:
            return self.from_yml(i)
        if self.source() is Formats.JSON:
            return self.from_json(i)
        if self.source() is self.standard():
            return self.from_standard(i)

        raise ValueError(f'unsupported configuration format {self.source()}')

class OutputFormat:
    """Output format to serialize a bibliography."""

    def __init__(self, target: Format, standard: Format):
        self._target = target
        self._standard = standard

    def to_yml(self, o: TextIO):
        """Writes to yml representation."""

    def to_json(self, o: TextIO):
        """Writes to json representation."""

    def to_standard(self, o: TextIO):
        """Writes to standard format."""

    def to_py(self, o: TextIO):
        """Writes to python representation."""

    def target(self):
        """The file extension."""
        return self._target

    def standard(self) -> Format:
        """The standard format."""
        return self._standard

    def write(self, o: TextIO):
        """Serialization method."""
        if self.target() is Formats.YML:
            return self.to_yml(o)
        if self.target() is Formats.JSON:
            return self.to_json(o)
        if self.target() is Formats.PYTHON:
            return self.to_py(o)
        if self.target() is self.standard():
            return self.to_standard(o)

        raise ValueError(f'unsupported configuration format {self.target()}')


class CitationFormatter:
    """A builder of reference decorators."""

    def format(self, refs: list) -> str:
        """Formats a citation list."""

    def __call__(self, *refs):
        """The reference decorator."""

        def internal(obj):
            if obj.__doc__ is None:
                obj.__doc__ = ''
            if len(refs) == 1:
                ref0 = refs[0]
                if isinstance(ref0, list):
                    obj.__doc__ += self.format(ref0)
                else:
                    obj.__doc__ += self.format([ref0])
            else:
                obj.__doc__ += self.format([*refs])
            return obj

        return internal


class SimpleCitationFormatter(CitationFormatter):
    """A simple citation formatter for """

    def __init__(self, prefix, itemize, reference_formatter):
        self._prefix = prefix
        self._itemize = itemize
        self._reference_formatter = reference_formatter

    def format(self, refs: list) -> str:

        if len(refs) == 1:
            return f"\n\n{self._prefix} {self._reference_formatter(refs[0])}\n"

        result = f"\n\n{self._prefix}\n\n"
        for r in refs:
            result += f"{self._itemize} {self._reference_formatter(r)}\n"
        return result
