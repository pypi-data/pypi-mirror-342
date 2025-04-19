"""Bibtex I/O module."""

import json

from typing import Any, TextIO

import bibtexparser
import yaml
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

from bibliograpy.api_bibtex import TYPES, BibtexReference, ENTRYTYPE_FIELD_IN_MODEL_DICT, ID_FIELD_IN_MODEL_DICT
from bibliograpy.api_core import InputFormat, OutputFormat, Formats, Format

_ENTRY_TYPE_FIELD_IN_DICT = 'entry_type'


class BibtexInputFormat(InputFormat):
    """Bibtex input format implementation."""

    def __init__(self, source: Format):
        super().__init__(source=source, standard=Formats.BIBTEX)

    def from_yml(self, i: TextIO):
        """Reads from yml representation."""
        return yaml.safe_load(i)

    def from_json(self, i: TextIO):
        """Reads from json representation."""
        return json.load(i)

    def from_standard(self, i: TextIO):
        """Reads from standard format."""
        meta = {}
        content = []
        for e in bibtexparser.load(i).entries:
            meta[_ENTRY_TYPE_FIELD_IN_DICT] = e[ENTRYTYPE_FIELD_IN_MODEL_DICT]
            meta[BibtexReference.CITE_KEY_FIELD] = e[ID_FIELD_IN_MODEL_DICT]
            del e[ENTRYTYPE_FIELD_IN_MODEL_DICT]
            del e[ID_FIELD_IN_MODEL_DICT]
            content.append({**meta, **e})
        return content

class BibtexOutputFormat(OutputFormat):
    """Bibtex format implementation."""

    def __init__(self,
                 content: list[dict],
                 target: Format,
                 scope_symbol: str | None,
                 init_scope: str | None):
        super().__init__(target=target, standard=Formats.BIBTEX)
        self._content = content
        self._scope_symbol = scope_symbol
        self._init_scope = init_scope

    def _to_standard_ext(self) -> list[str]:
        """Extensions to be serialized to standard format."""
        return ['bib', 'bibtex']

    def to_yml(self, o: TextIO):
        """Writes to yml representation."""
        yaml.dump(self._content, o, sort_keys=False)

    def to_json(self, o: TextIO):
        """Writes to json representation."""
        json.dump(self._content, fp=o, sort_keys=False)

    def to_standard(self, o: TextIO):
        """Writes to standard format."""

        scope: dict[str, Any] = {}
        entries = []

        for ref in self._content:
            entry_type = ref[_ENTRY_TYPE_FIELD_IN_DICT]
            if entry_type in TYPES:
                entries.append(TYPES[entry_type].from_dict(ref, scope).to_bib())

        db = BibDatabase()
        db.entries = entries
        writer = BibTexWriter()
        writer.order_entries_by = None

        bibtexparser.dump(bib_database=db, bibtex_file=o, writer=writer)

    def to_py(self, o: TextIO):
        """Writes to python representation."""
        scope: dict[str, Any] = {}

        o.write('from bibliograpy.api_bibtex import *\n')
        o.write('\n')

        if self._init_scope is not None:
            o.write(f'{self._scope_symbol} = {self._init_scope}\n')
            o.write('\n')

        for ref in self._content:
            entry_type = ref[_ENTRY_TYPE_FIELD_IN_DICT]
            if entry_type in TYPES:
                o.write(f"{TYPES[entry_type].from_dict(ref, scope).to_py(scope_symbol=self._scope_symbol)}\n")
