"""Test module for core api"""
import sys
import pydoc

from bibliograpy.api_bibtex import Misc, TechReport, BibtexReference
from bibliograpy.api_core import CitationFormatter

SCOPE: dict[str, BibtexReference] = {}


IAU = Misc.generic(cite_key='iau',
                   title='International Astronomical Union',
                   institution='IAU',
                   scope=SCOPE)


IAU_2006_B1 = TechReport.generic(
    cite_key='iau_2006_b1',
    author='',
    crossref='iau',
    title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
    year=2006,
    scope=SCOPE)


def test_custom_citation_formatter():
    """test custom citation formatter"""

    class _CitationFormatter(CitationFormatter):
        def format(self, refs: list) -> str:
            if len(refs) == 1:
                return f"\n\nBibliographie : {self.ref_formatter(refs[0])}\n"

            result = "\n\nBibliographie :\n\n"
            for r in refs:
                result += f"* {self.ref_formatter(r)}\n"
            return result

        def ref_formatter(self, r: BibtexReference) -> str:
            """The single reference formatter."""
            return f"{r.title} [{r.cite_key}]"

    ref = _CitationFormatter()

    @ref(IAU_2006_B1, IAU)
    def tatafr():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api_core

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs

    Bibliographie :

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api_core

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs
    
    Bibliographie :
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
