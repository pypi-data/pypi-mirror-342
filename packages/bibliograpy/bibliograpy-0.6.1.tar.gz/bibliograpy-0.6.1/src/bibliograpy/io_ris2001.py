"""RIS I/O module."""

import json

from typing import TextIO

import yaml

from bibliograpy.api_core import InputFormat, OutputFormat, Format, Formats
from bibliograpy.api_ris2001 import Tags, TypeFieldName

class Ris2001InputFormat(InputFormat):
    """Ris 2001 input format implementation."""

    def __init__(self, source: Format):
        super().__init__(source=source, standard=Formats.RIS2001)

    def from_yml(self, i: TextIO):
        """Reads from yml representation."""
        return [{Tags.parse(k): TypeFieldName.parse(e[k]) if Tags.parse(k) is Tags.TY else e[k] for k in e}
                for e in yaml.safe_load(i)]

    def from_json(self, i: TextIO):
        """Reads from json representation."""
        return [{Tags.parse(k): TypeFieldName.parse(e[k]) if Tags.parse(k) is Tags.TY else e[k] for k in e}
                for e in json.load(i)]

    def from_standard(self, i: TextIO) -> list[dict[Tags, str | list[str] | TypeFieldName]]:
        """Reads from standard format."""

        results: list[dict[Tags, str | list[str] | TypeFieldName]] = []

        while line := i.readline():
            if line.rstrip() == '':
                continue
            entry: dict[Tags, str | list[str] | TypeFieldName] = {Tags.TY: _parse_ris_entry_type(line)}
            entry.update(_read_ris_entry(i))
            results.append(entry)
        return results

def _parse_ris_entry_type(line: str) -> TypeFieldName:
    # first field must contain entry type
    tag = Tags.parse(line[:2])
    if tag is not Tags.TY:
        raise ValueError(f'expected type field but found {tag}')

    if line[2:6] != '  - ':
        raise ValueError(f'type line "{line}" is not correctly formatted')

    return TypeFieldName.parse(line[6:].rstrip())

def _read_ris_entry(tio: TextIO) -> dict[Tags, str | list[str]]:
    """Reads a single RIS entry from the input stream."""

    result = {}

    last_tag: Tags | None = None

    while line := tio.readline():

        try:
            tag = Tags.parse(line[:2])
            last_tag = tag

            if tag is Tags.ER:
                return result

            if tag is Tags.TY:
                raise ValueError('only one type field is expected, a ')

            if tag.repeating:
                if tag in result:
                    result[tag].append(line[6:].rstrip('\n\r'))
                else:
                    result[tag] = [line[6:].rstrip('\n\r')]
            else:
                result[tag] = line[6:].rstrip('\n\r')
        except ValueError as e:
            if line[2:6] == '  - ' or last_tag is None:
                raise e

            # long field support
            if last_tag.repeating:
                result[last_tag][-1] += line.rstrip('\n\r')
            else:
                result[last_tag] += line.rstrip('\n\r')
    raise ValueError(f'the last RIS entry tag is expected to be {Tags.ER.name} but found {last_tag}')


class Ris2001OutputFormat(OutputFormat):
    """Bibtex format implementation."""

    def __init__(self,
                 content: list[dict[Tags, str | list[str] | TypeFieldName]],
                 target: Format):
        super().__init__(target=target, standard=Formats.RIS2001)
        self._content = content

    def to_yml(self, o: TextIO):
        """Writes to yml representation."""
        yaml.dump([{k.name: (e[k].name if isinstance(e[k], TypeFieldName) else e[k]) for k in e}
                   for e in self._content],
                  o,
                  sort_keys=False)

    def to_json(self, o: TextIO):
        """Writes to json representation."""
        json.dump([{k.name: (e[k].name if isinstance(e[k], TypeFieldName) else e[k]) for k in e}
                   for e in self._content],
                  fp=o,
                  sort_keys=False)

    def to_standard(self, o: TextIO):
        """Writes to standard format."""

        for bib_entry in self._content:
            o.write(f'{Tags.TY.name}  - {bib_entry[Tags.TY].name}')
            o.write('\n')

            for tag in bib_entry:

                if tag is Tags.TY:
                    continue

                if tag.repeating:
                    for l in bib_entry[tag]:
                        o.write(f'{tag.name}  - {l}\n')
                else:
                    o.write(f'{tag.name}  - {bib_entry[tag]}\n')

            o.write(f'{Tags.ER.name}  - \n')

    def to_py(self, o: TextIO):
        """Writes to python representation."""

        o.write('from bibliograpy.api_ris2001 import *\n\n')
        o.write('\n')

        for bib_entry in self._content:
            o.write(f'{bib_entry[Tags.ID].upper()} = ')
            o.write('{\n')
            for e in bib_entry:
                if e is Tags.TY:
                    o.write(f"  Tags.{e.name}: {bib_entry[e]},\n")
                else:
                    o.write(f"  Tags.{e.name}: '{bib_entry[e]}',\n")
            o.write('}\n')
