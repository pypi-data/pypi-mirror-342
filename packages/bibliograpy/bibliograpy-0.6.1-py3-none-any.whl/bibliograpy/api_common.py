""""Common management of citation decorators for references."""

from bibliograpy.api_bibtex import BibtexReference, default_bibtex_formatter
from bibliograpy.api_core import CitationFormatter
from bibliograpy.api_ris2001 import Tags as Ris2001, TypeFieldName as Ris2001Field, default_ris2001_formatter
from bibliograpy.api_ris2011 import Tags as Ris2011, TypeFieldName as Ris2011Field, default_ris2011_formatter
from bibliograpy.api_refer import Tags as Refer, default_refer_formatter
from bibliograpy.api_endnote import Tags as Endnote, default_endnote_formatter


class DefaultCitationFormatter(CitationFormatter):
    """Default citation formatter."""

    def __init__(self, prefix: str, itemize: str):
        self._prefix = prefix
        self._itemize = itemize

    def format(self, refs: list) -> str:

        if len(refs) == 1:
            return f"\n\n{self._prefix} {self._by_type(refs[0])}\n"

        result = f"\n\n{self._prefix}\n\n"
        for r in refs:
            result += f"{self._itemize} {self._by_type(r)}\n"
        return result

    def _by_type(self, r):
        if isinstance(r, BibtexReference):
            return self.bibtex(r)

        if isinstance(r, dict):
            if Ris2001.TY in r:
                return self.ris2001(r)
            if Ris2011.TY in r:
                return self.ris2011(r)
            if Refer.L in r:
                return self.refer(r)
            if Endnote.A in r or Endnote.T in r:
                return self.endnote(r)

        raise ValueError('unexpected reference type')

    def bibtex(self, r: BibtexReference):
        """Bibtex reference formatter."""
        return default_bibtex_formatter(r)

    def ris2001(self, r: dict[Ris2001, str | list[str] | Ris2001Field]):
        """RIS 2001 reference formatter."""
        return default_ris2001_formatter(r)

    def ris2011(self, r: dict[Ris2011, str | list[str] | Ris2011Field]):
        """RIS 2011 reference formatter."""
        return default_ris2011_formatter(r)

    def refer(self, r: dict[Refer, str | list[str]]):
        """refer reference formatter."""
        return default_refer_formatter(r)

    def endnote(self, r: dict[Endnote, str | list[str]]):
        """endnote reference formatter."""
        return default_endnote_formatter(r)

cite = DefaultCitationFormatter(prefix='Bibliography:', itemize='*')
