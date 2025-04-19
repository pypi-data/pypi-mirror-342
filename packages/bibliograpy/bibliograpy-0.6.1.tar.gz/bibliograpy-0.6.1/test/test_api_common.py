"""Test module for bibtex api"""
import sys
import pydoc


from bibliograpy.api_bibtex import Misc, TechReport, BibtexReference
from bibliograpy.api_common import DefaultCitationFormatter
from bibliograpy.api_ris2001 import Tags as Ris2001, TypeFieldName as Ris2001Type

NASA = {Ris2001.TY: Ris2001Type.GEN, Ris2001.TI: 'NASA', Ris2001.ID: 'nasa'}

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


def test_parameterized_default_citation_formatter():
    """test parameterized default citation formatter"""

    class _DefaultCitationFormatter(DefaultCitationFormatter):
        def bibtex(self, r: BibtexReference) -> str:
            base = f'{r.title} [{r.cite_key}]'
            if r.crossref:
                return base + f' -> [{r.crossref}]'
            return base

    ref = _DefaultCitationFormatter(prefix='Références bibliographiques :',
                                    itemize='++')

    @ref(IAU_2006_B1, IAU, NASA)
    def tatafr():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api_common

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs

    Références bibliographiques :

    ++ Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1] -> [iau]
    ++ International Astronomical Union [iau]
    ++ NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api_common

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs
    
    Références bibliographiques :
    
    ++ Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1] -> [iau]
    ++ International Astronomical Union [iau]
    ++ NASA [nasa]
""")
