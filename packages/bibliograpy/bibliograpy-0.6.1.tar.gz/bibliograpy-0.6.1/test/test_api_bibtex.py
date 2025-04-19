"""Test module for bibtex api"""
import sys
import pydoc

import pytest

from bibliograpy.api_bibtex import Misc, TechReport, BibtexReference, inbook
from bibliograpy.api_common import cite

SCOPE: dict[str, BibtexReference] = {}


IAU = Misc.generic(cite_key='iau',
                   title='International Astronomical Union',
                   institution='IAU',
                   scope=SCOPE)


IAU_2006_B1 = TechReport.generic(
    cite_key='iau_2006_b1',
    author='',
    crossref=IAU,
    title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
    year=2006,
    scope=SCOPE)


def test_to_source_bib():
    """test to python source bib serialization"""
    assert (IAU_2006_B1.to_py(scope_symbol=None) ==
"""
IAU_2006_B1 = TechReport.generic(cite_key='iau_2006_b1',
                                 author='',
                                 crossref=IAU,
                                 title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
                                 year=2006)""")


def test_to_source_bib_with_scope():
    """test to python source bib serialization"""
    assert (IAU_2006_B1.to_py(scope_symbol='SCOPE') ==
"""
IAU_2006_B1 = TechReport.generic(cite_key='iau_2006_b1',
                                 author='',
                                 crossref=IAU,
                                 title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
                                 year=2006,
                                 scope=SCOPE)""")


def test_builtin_reference_decorator():
    """test build-in reference decorator with a single reference, an array of references and references in varargs"""

    @cite(IAU_2006_B1)
    def bib_ref():
        """ma doc"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")
    else:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc
    
    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")

    @cite([IAU_2006_B1, IAU])
    def bib_ref_foo():
        """ma doc avec plusieurs références"""


    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")

    @cite(IAU_2006_B1, IAU)
    def bib_ref_bar():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_bar) ==
"""Python Library Documentation: function bib_ref_bar in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_b\bba\bar\br()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(bib_ref_bar) ==
"""Python Library Documentation: function bib_ref_bar in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_b\bba\bar\br()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")


def test_mandatory_field():
    """test mandatory field management"""
    with pytest.raises(ValueError) as e:
        TechReport.generic(
            cite_key='iau_2006_b1',
            author='',
            title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
            year=2006)
    assert e.value.args[0] == 'missing mandatory field for TechReport iau_2006_b1'


def test_cross_reference():
    """test cross reference hierarchy management"""
    scope = {}
    assert len(scope) == 0

    iau_org = Misc.generic(cite_key='iau',
                           institution='Internation Astronomical Union',
                           author='iau',
                           crossref='no_ref',
                           scope=scope)
    assert len(scope) == 1
    assert 'iau' in scope
    assert scope['iau'] is iau_org
    assert iau_org.institution == 'Internation Astronomical Union'
    assert iau_org.author == 'iau'

    iau_author = Misc.generic(cite_key='iau_author', author='IAU', crossref='iau', scope=scope)
    assert len(scope) == 2
    assert 'iau_author' in scope
    assert scope['iau_author'] is iau_author
    assert iau_author.institution is None
    assert iau_author.author == 'IAU'
    assert iau_author.cross_resolved().institution == 'Internation Astronomical Union'

    iau_2006 = TechReport.generic(
        cite_key='iau_2006_b1',
        crossref='iau_author',
        title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
        year=2006,
        scope=scope)
    assert len(scope) == 3
    assert 'iau_2006_b1' in scope
    assert scope['iau_2006_b1'] is iau_2006
    assert iau_2006.institution is None
    assert iau_2006.cross_resolved().institution == 'Internation Astronomical Union'
    assert iau_2006.author is None
    assert iau_2006.cross_resolved().author == 'IAU'


def test_specific_entry_type_decorator():
    """test build-in reference decorator with a single reference, an array of references and references in varargs"""

    @inbook(crossref=IAU_2006_B1, title="mon inbook", pages=235, publisher='', author='auteur')
    def bib_ref():
        """ma doc"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc

    Bibliography: mon inbook
""")
    else:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api_bibtex

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc
    
    Bibliography: mon inbook
""")


def test_builtin_reference_decorator_class_usage():
    """test build-in reference decorator with a single reference, an array of references and references in varargs"""

    @cite(IAU_2006_B1)
    class BibRef:
        """ma doc"""

        def bib(self):
            """ma doc bib"""
            return "foo"

        def ref(self):
            """ma doc ref"""
            return "bar"

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(BibRef) ==
                """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |
 |  Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |
 |  Methods defined here:
 |
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    elif sys.version_info.minor >= 11:
        assert (pydoc.render_doc(BibRef) ==
                """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    else:
        assert (pydoc.render_doc(BibRef) ==
                """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables (if defined)
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object (if defined)
""")

    @cite([IAU_2006_B1, IAU])
    class BibRefFoo:
        """ma doc"""

        def bib(self):
            """ma doc bib"""
            return "foo"

        def ref(self):
            """ma doc ref"""
            return "bar"

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(BibRefFoo) ==
                """Python Library Documentation: class BibRefFoo in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfF\bFo\boo\bo(builtins.object)
 |  ma doc
 |
 |  Bibliography:
 |
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |
 |  Methods defined here:
 |
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    elif sys.version_info.minor >= 11:
        assert (pydoc.render_doc(BibRefFoo) ==
                """Python Library Documentation: class BibRefFoo in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfF\bFo\boo\bo(builtins.object)
 |  ma doc
 |  
 |  Bibliography:
 |  
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    else:
        assert (pydoc.render_doc(BibRefFoo) ==
                """Python Library Documentation: class BibRefFoo in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfF\bFo\boo\bo(builtins.object)
 |  ma doc
 |  
 |  Bibliography:
 |  
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables (if defined)
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object (if defined)
""")

    @cite(IAU_2006_B1, IAU)
    class BibRefBar:
        """ma doc"""

        def bib(self):
            """ma doc bib"""
            return "foo"

        def ref(self):
            """ma doc ref"""
            return "bar"

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(BibRefBar) ==
                """Python Library Documentation: class BibRefBar in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfB\bBa\bar\br(builtins.object)
 |  ma doc
 |
 |  Bibliography:
 |
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |
 |  Methods defined here:
 |
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    elif sys.version_info.minor >= 11:
        assert (pydoc.render_doc(BibRefBar) ==
                """Python Library Documentation: class BibRefBar in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfB\bBa\bar\br(builtins.object)
 |  ma doc
 |  
 |  Bibliography:
 |  
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    else:
        assert (pydoc.render_doc(BibRefBar) ==
                """Python Library Documentation: class BibRefBar in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bfB\bBa\bar\br(builtins.object)
 |  ma doc
 |  
 |  Bibliography:
 |  
 |  * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
 |  * International Astronomical Union [iau]
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables (if defined)
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object (if defined)
""")


def test_specific_entry_type_decorator_class_usage():
    """test build-in reference decorator with a single reference, an array of references and references in varargs"""

    @inbook(crossref=IAU_2006_B1, title="mon inbook", pages=235, publisher='', author='auteur')
    class BibRef:
        """ma doc"""

        def bib(self):
            """ma doc bib"""
            return "foo"

        def ref(self):
            """ma doc ref"""
            return "bar"

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(BibRef) ==
                """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |
 |  Bibliography: mon inbook
 |
 |  Methods defined here:
 |
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    elif sys.version_info.minor >= 11:
        assert (pydoc.render_doc(BibRef) ==
                    """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: mon inbook
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    else:
        assert (pydoc.render_doc(BibRef) ==
                    """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: mon inbook
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables (if defined)
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object (if defined)
""")


def test_method_and_class_usage():
    """test build-in reference decorator with a single reference, an array of references and references in varargs"""

    @inbook(crossref=IAU_2006_B1, title="mon inbook", pages=235, publisher='', author='auteur')
    class BibRef:
        """ma doc"""

        @cite(IAU)
        def bib(self):
            """ma doc bib"""
            return "foo"

        def ref(self):
            """ma doc ref"""
            return "bar"

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(BibRef) ==
                """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |
 |  Bibliography: mon inbook
 |
 |  Methods defined here:
 |
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |
 |      Bibliography: International Astronomical Union [iau]
 |
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    elif sys.version_info.minor >= 11:
        assert (pydoc.render_doc(BibRef) ==
                    """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: mon inbook
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |      
 |      Bibliography: International Astronomical Union [iau]
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object
""")
    else:
        assert (pydoc.render_doc(BibRef) ==
                    """Python Library Documentation: class BibRef in module test_api_bibtex

class B\bBi\bib\bbR\bRe\bef\bf(builtins.object)
 |  ma doc
 |  
 |  Bibliography: mon inbook
 |  
 |  Methods defined here:
 |  
 |  b\bbi\bib\bb(self)
 |      ma doc bib
 |      
 |      Bibliography: International Astronomical Union [iau]
 |  
 |  r\bre\bef\bf(self)
 |      ma doc ref
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  _\b__\b_d\bdi\bic\bct\bt_\b__\b_
 |      dictionary for instance variables (if defined)
 |  
 |  _\b__\b_w\bwe\bea\bak\bkr\bre\bef\bf_\b__\b_
 |      list of weak references to the object (if defined)
""")
