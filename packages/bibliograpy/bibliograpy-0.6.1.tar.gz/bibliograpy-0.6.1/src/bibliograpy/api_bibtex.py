"""Bibtex API module."""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Any
import logging

from bibliograpy.api_core import SimpleCitationFormatter

LOG = logging.getLogger(__name__)

_ANONYM_CITE_KEY = ""
ENTRYTYPE_FIELD_IN_MODEL_DICT = "ENTRYTYPE"
ID_FIELD_IN_MODEL_DICT = "ID"

@dataclass(frozen=True)
class NonStandard:
    """Non-standard bibtex bibliography reference fields."""

    doi: str | None = None
    """DOI number"""

    issn: str | None = None
    """ISSN number"""

    eissn: str | None = None
    """ISSN number"""

    isbn: str | None = None
    """ISBN number"""

    url: str | None = None
    """URL of a web page"""

    @staticmethod
    def from_dict(source: dict) -> NonStandard | None:
        """Builds a non-standard reference field set from a dict."""
        if any(f in source for f in ['doi', 'issn', 'eisssn', 'isbn', 'url']):
            return NonStandard(
                doi=source['doi'] if 'doi' in source else None,
                issn=source['issn'] if 'issn' in source else None,
                eissn=source['eissn'] if 'eissn' in source else None,
                isbn=source['isbn'] if 'isbn' in source else None,
                url=source['url'] if 'url' in source else None)
        return None


    def to_py(self) -> str:
        """Serialization of the non-standard reference field set in processed python code."""

        base = f"{type(self).__name__}("

        fields = []
        for f in dataclasses.fields(type(self)):
            value = getattr(self, f.name)

            if value is not None:
                fields.append(f"{f.name}='{value}'")

        return f"{base}{', '.join(fields)})"


@dataclass(frozen=True, repr=False)
class BibtexReference:
    """A bibliography reference."""

    CITE_KEY_FIELD = 'cite_key'
    NON_STANDARD_FIELD = 'non_standard'
    SCOPE_FIELD = 'scope'
    CROSSREF_FIELD = 'crossref'

    cite_key: str

    address: str | None
    """address of the publisher or the institution
    
    not used in article, misc and unpublished
    optional everywhere else
    https://www.bibtex.com/f/address-field/"""

    annote: str | None
    """an annotation
    
    https://www.bibtex.com/f/annote-field/"""

    author: str | None
    """ist of authors of the work
    
    optional for booklet, manual and misc
    required everywhere else
    https://www.bibtex.com/f/author-field/"""

    booktitle: str | None
    """title of the book
    
    required for incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/booktitle-field/"""

    chapter: str | None
    """number of a chapter in a book
    
    required for inbook and incollection
    not used everywhere else
    https://www.bibtex.com/f/chapter-field/"""

    crossref: str | None
    """The database key of the entry being cross referenced."""

    edition: str | None
    """edition number of a book
    
    optional for book, inbook, incollection and manual
    not used everywhere else
    https://www.bibtex.com/f/edition-field/"""

    editor: str | None
    """list of editors of a book
    
    required for book and inbook
    optional for incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/editor-field/"""

    howpublished: str | None
    """a publication notice for unusual publications
    
    optional for booklet and misc
    not used everywhere else
    https://www.bibtex.com/f/howpublished-field/"""

    institution: str | None
    """name of the institution that published and/or sponsored the report
    
    required for techreport
    not used everywhere else
    https://www.bibtex.com/f/institution-field/
    """

    journal: str | None
    """name of the journal or magazine the article was published in
    
    required for article
    not used everywhere else
    https://www.bibtex.com/f/journal-field/
    """

    month: str | None
    """the month during the work was published
    
    optional
    https://www.bibtex.com/f/month-field/"""

    note: str | None
    """
    notes about the reference
    
    required for unpublished
    optional everywhere else
    https://www.bibtex.com/f/note-field/"""

    number: str | int | None
    """number of the report or the issue number for a journal article
    
    optional for article, book, inbook, incollection, inproceedings and techreport
    not used everywhere else
    https://www.bibtex.com/f/number-field/"""

    organization: str | None
    """name of the institution that organized or sponsored the conference or that published the manual
    
    optional for inproceedings and manual
    not used everywhere else
    https://www.bibtex.com/f/organization-field/"""

    pages: str | int | None
    """page numbers or a page range
    
    required for inbook
    optional for article, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/pages-field/"""

    publisher: str | None
    """name of the publisher
    
    required for book, inbook and incollection
    optional for inproceedings
    not used everywhere else
    https://www.bibtex.com/f/publisher-field/"""

    school: str | None
    """name of the university or degree awarding institution
    
    required for masterthesis and phdthesis
    not used everywhere else
    https://www.bibtex.com/f/school-field/"""

    series: str | None
    """name of the series or set of books
    
    optional for book, inbook, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/series-field/"""

    title: str | None
    """title of the work
    
    optional for misc
    required everywhere else
    https://www.bibtex.com/f/title-field/"""

    type: str | None
    """type of the technical report or thesis
    
    optional for inbook, incollection, masterthesis and techreport
    not used everywhere else
    https://www.bibtex.com/f/type-field/"""

    volume: str | int | None
    """volume number
    
    optional for article, book, inbook, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/volume-field/"""

    year: str | int | None
    """year the book was published
    
    required for article, book, inbook, incollection, inproceedings, masterthesis, phdthesis, techreport
    optional for booklet, misc and unpublished
    not used for manual
    https://www.bibtex.com/f/year-field/"""

    non_standard: NonStandard | None
    """Non standard fields."""

    scope: dict[str, BibtexReference] | None
    """Environnement de résolution des références croisées."""

    def _hierarchy(self) -> list[BibtexReference]:
        """Calcul de la hiérarchie par références croisées."""
        current: BibtexReference | None = self

        hierarchy: list[BibtexReference] = [current]
        while current is not None:
            if current.crossref is not None and current.scope is not None and current.crossref in current.scope:
                parent: BibtexReference = current.scope[current.crossref]
                hierarchy.append(parent)
                current = parent
            else:
                current = None
        return hierarchy

    def cross_resolved(self) -> BibtexReference:
        """Calcul de la référence héritant des champs des références croisées parentes."""
        hierarchy = self._hierarchy()

        if len(hierarchy) == 1:
            return self

        resolved_standard_dict: dict[str, Any] = {}
        for f in dataclasses.fields(type(self)):

            if f.name in [BibtexReference.NON_STANDARD_FIELD, BibtexReference.SCOPE_FIELD]:
                continue

            for i in hierarchy:
                v = getattr(i, f.name)
                if v is not None:
                    resolved_standard_dict[f.name] = v
                    break

        resolved_non_standard_dict: dict[str, Any] = {}
        for f in dataclasses.fields(NonStandard):

            for i in hierarchy:
                if i.non_standard is not None:
                    v = getattr(i.non_standard, f.name)
                    if v is not None:
                        resolved_non_standard_dict[f.name] = v
                        break

        resolved_standard_dict[BibtexReference.NON_STANDARD_FIELD] = NonStandard.from_dict(resolved_non_standard_dict)

        # il ne faut pas ajouter dans le scope cette instance résolue par références croisées car sa clef étant la même
        # que celle de la référence explicite, les deux entreraient en conflit dans le scope
        # seule la référence explicite doit être ajoutée au scope
        # si on souhaite disposer des champs hérités par références croisées, il faut utiliser l'instance résolue
        return type(self).from_dict(source=resolved_standard_dict,
                                    scope=None)
    @staticmethod
    def to_source_symbol(cite_key: str) -> str:
        """Produces a Python symbol for the reference."""
        return cite_key.upper()

    def to_py(self, scope_symbol: str | None) -> str:
        """Serialization of the reference in processed python code."""

        base = f"{BibtexReference.to_source_symbol(self.cite_key)} = {type(self).__name__}.generic("

        fields = []
        for f in dataclasses.fields(type(self)):

            if BibtexReference.SCOPE_FIELD == f.name:
                continue

            value = getattr(self, f.name)

            if f.name == BibtexReference.CROSSREF_FIELD and value is not None:
                fields.append(f"{f.name}={BibtexReference.to_source_symbol(value)}")
            elif isinstance(value, str):
                if "'" in value:
                    fields.append(f'{f.name}="{value}"')
                else:
                    fields.append(f"{f.name}='{value}'")
            elif isinstance(value, NonStandard):
                fields.append(f'{f.name}={value.to_py()}')
            elif value is not None:
                fields.append(f'{f.name}={value}')

        if scope_symbol is not None:
            fields.append(f'{BibtexReference.SCOPE_FIELD}={scope_symbol}')

        # argument indentation management
        sep = ',\n'
        for _ in range(len(base)):
            sep += ' '

        return f"\n{base}{sep.join(fields)})"

    def to_bib(self) -> dict:
        """converts to a bibtex parser dict"""
        result = {}
        for f in dataclasses.fields(type(self)):

            if BibtexReference.SCOPE_FIELD == f.name:
                continue

            if BibtexReference.CITE_KEY_FIELD == f.name:
                field_name = ID_FIELD_IN_MODEL_DICT
            else:
                field_name = f.name

            value = getattr(self, f.name)

            if isinstance(value, str):
                result[field_name] = value
            elif isinstance(value, NonStandard):
                ns = {}
                for f in dataclasses.fields(NonStandard):
                    v = getattr(value, f.name)
                    if v is not None:
                        ns[f.name] = str(v)

                result = result | ns

            elif value is not None:
                result[field_name] = str(value)

        result[ENTRYTYPE_FIELD_IN_MODEL_DICT] = type(self).bibtex_entry_type()
        return result

    def _mandatory_values(self) -> dict[str, Any]:
        """Checks if standard mandatory fields are not None."""
        raise NotImplementedError

    @classmethod
    def bibtex_entry_type(cls):
        """Gets the bibtex entrytype name"""
        for bibtex, internal_type in TYPES.items():
            if internal_type == cls:
                return bibtex
        raise ValueError

    @classmethod
    def generic(cls,
                cite_key: str,
                address: str | None = None,
                annote: str | None = None,
                booktitle: str | None = None,
                author: str | None = None,
                chapter: str | None = None,
                crossref: str | BibtexReference | None = None,
                edition: str | None = None,
                editor: str | None = None,
                howpublished: str | None = None,
                institution: str | None = None,
                journal: str | None = None,
                month: str | None = None,
                note: str | None = None,
                number: str | None = None,
                organization: str | None = None,
                pages: str | int | None = None,
                publisher: str | None = None,
                school: str | None = None,
                series: str | None = None,
                title: str | None = None,
                type: str | None = None,
                volume: str | int | None = None,
                year: str | int | None = None,
                non_standard: NonStandard | None = None,
                scope: dict[str, BibtexReference] | None = None) -> BibtexReference:
        """builds a generic reference, allowing to init each field"""
        instance = cls(cite_key=cite_key,
                       address=address,
                       annote=annote,
                       booktitle=booktitle,
                       author=author,
                       chapter=chapter,
                       crossref=crossref.cite_key if isinstance(crossref, BibtexReference) else crossref,
                       edition=edition,
                       editor=editor,
                       howpublished=howpublished,
                       institution=institution,
                       journal=journal,
                       month=month,
                       note=note,
                       number=number,
                       organization=organization,
                       pages=pages,
                       publisher=publisher,
                       school=school,
                       series=series,
                       title=title,
                       type=type,
                       volume=volume,
                       year=year,
                       non_standard=non_standard,
                       scope=scope)

        if any(v is None for k, v in instance._mandatory_values().items()):
            if all(v is not None for k, v in instance.cross_resolved()._mandatory_values().items()):
                LOG.info('all mandatory values resolved in scope cross references')
            else:
                raise ValueError(f'missing mandatory field for {cls.__name__} {instance.cite_key}')

        # scope management for crossref
        if scope is not None:
            # les chaines vides doivent être ignorées car elles représentent l'unique clef des citations anonymes
            if cite_key != '' and cite_key in scope:
                raise ValueError(f'{cite_key} is already present in bibliograpy scope for {scope[cite_key]}')

            scope[cite_key] = instance

        return instance

    @classmethod
    def from_dict(cls, source: dict[str, Any], scope: dict[str, BibtexReference] | None) -> BibtexReference:
        """Builds a reference from a dict."""
        return cls.generic(
            cite_key=source[BibtexReference.CITE_KEY_FIELD],
            address=source['address'] if 'address' in source else None,
            annote=source['annote'] if 'annote' in source else None,
            author=source['author'] if 'author' in source else None,
            booktitle=source['booktitle'] if 'booktitle' in source else None,
            chapter=source['chapter'] if 'chapter' in source else None,
            crossref=source['crossref'] if 'crossref' in source else None,
            edition=source['edition'] if 'edition' in source else None,
            editor=source['editor'] if 'editor' in source else None,
            howpublished=source['howpublished'] if 'howpublished' in source else None,
            institution=source['institution'] if 'institution' in source else None,
            journal=source['journal'] if 'journal' in source else None,
            month=source['month'] if 'month' in source else None,
            note=source['note'] if 'note' in source else None,
            number=source['number'] if 'number' in source else None,
            organization=source['organization'] if 'organization' in source else None,
            pages=source['pages'] if 'pages' in source else None,
            publisher=source['publisher'] if 'publisher' in source else None,
            school=source['school'] if 'school' in source else None,
            series=source['series'] if 'series' in source else None,
            title=source['title'] if 'title' in source else None,
            type=source['type'] if 'type' in source else None,
            volume=source['volume'] if 'volume' in source else None,
            year=source['year'] if 'year' in source else None,
            non_standard=NonStandard.from_dict(source),
            scope=scope)


def default_bibtex_formatter(r: BibtexReference):
    """The default formatter for bibtex references."""
    r = r.cross_resolved()
    return f"{r.title} [{r.cite_key}]" if r.cite_key != _ANONYM_CITE_KEY else r.title


_cite = SimpleCitationFormatter(prefix='Bibliography:', itemize='*', reference_formatter=default_bibtex_formatter)


class _InternalReference(BibtexReference):
    """Internal bibliographic usage before defining standard types."""

    def _mandatory_values(self):
        """Checks if standard mandatory fields are not None."""
        return {}

_bibtex_com = _cite(_InternalReference.generic(cite_key='bibtex_com',
                                               title='www.bibtex.com'))

_bibtex_package = _cite(
    _InternalReference.generic(cite_key='bibtex_package',
                               title='CTAN Bibtex package documentation',
                               non_standard=NonStandard(
                           url='https://distrib-coffee.ipsl.jussieu.fr/pub/mirrors/ctan/biblio/bibtex/base/btxdoc.pdf')
                               ))

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Article(BibtexReference):
    """any article published in a periodical like a journal article or magazine article

    An article from a journal or magazine.
    Required fields: author, title, journal, year.
    Optional fields: volume, number, pages, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values"""
        return {
            'author': self.author,
            'title': self.title,
            'journal': self.journal,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Book(BibtexReference):
    """a book

    A book with an explicit publisher.
    Required fields: author or editor, title, publisher, year.
    Optional fields: volume or number, series, address, edition, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author or editor': self.author or self.editor,
            'title': self.title,
            'publisher': self.publisher,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Booklet(BibtexReference):
    """like a book but without a designated publisher

    A work that is printed and bound, but without a named publisher or sponsoring institution.
    Required field: title.
    Optional fields: author, howpublished, address, month, year, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {'title': self.title}

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inbook(BibtexReference):
    """a section or chapter in a book

    A part of a book, which may be a chapter (or section or whatever)and/or a range of pages.
    Required fields: author or editor, title, chapter and/or pages, publisher, year.
    Optional fields: volume or number, series, type, address, edition, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author or editor': self.author or self.editor,
            'title': self.title,
            'chapter or pages': self.chapter or self.pages,
            'publisher': self.publisher,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Incollection(BibtexReference):
    """an article in a collection

    A part of a book having its own title.
    Required fields: author, title, booktitle, publisher, year.
    Optional fields: editor, volume or number, series, type, chapter, pages, address, edition, month, note"""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'booktitle': self.booktitle,
            'publisher': self.publisher,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inproceedings(BibtexReference):
    """a conference paper (same as the conference entry type)

    An article in a conference proceedings.
    Required fields: author, title, booktitle, year.
    Optional fields: editor, volume or number, series, pages, address, month, organization, publisher, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'booktitle': self.booktitle,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Conference(Inproceedings):
    """The same as INPROCEEDINGS, included for Scribe compatibility."""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Manual(BibtexReference):
    """a technical manual

    manual Technical documentation.
    Required field: title.
    Optional fields: author, organization, address, edition, month, year, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {'title': self.title}

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Mastersthesis(BibtexReference):
    """a Masters thesis

    mastersthesis A Master’s thesis.
    Required fields: author, title, school, year.
    Optional fields: type, address, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'school': self.school,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Misc(BibtexReference):
    """used if nothing else fits

    misc Use this type when nothing else fits.
    Required fields: none.
    Optional fields: author, title, howpublished, month, year, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {}

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Phdthesis(BibtexReference):
    """a PhD thesis

    phdthesis A PhD thesis.
    Required fields: author, title, school, year.
    Optional fields: type, address, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'school': self.school,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Proceedings(BibtexReference):
    """the whole conference proceedings

    proceedings The proceedings of a conference.
    Required fields: title, year.
    Optional fields: editor, volume or number, series, address, month, organization, publisher, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'title': self.title,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class TechReport(BibtexReference):
    """a technical report, government report or white paper

    techreport A report published by a school or other institution, usually numbered within a series.
    Required fields: author, title, institution, year.
    Optional fields: type, number, address, month, note."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'institution': self.institution,
            'year': self.year
        }

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Unpublished(BibtexReference):
    """a work that has not yet been officially published

    unpublished A document having an author and title, but not formally published.
    Required fields: author, title, note.
    Optional fields: month, year."""

    def _mandatory_values(self):
        """Returns all the mandatory values."""
        return {
            'author': self.author,
            'title': self.title,
            'note': self.note
        }

# Déclarations de références anonymes
# les références anonymes n'ont pas de cite_key
# elles ne sont pas réutilisables et sont simplement déclarées une seule fois

def _anonym(constructor: type[BibtexReference]):
    def internal(
            address: str | None = None,
            annote: str | None = None,
            booktitle: str | None = None,
            author: str | None = None,
            chapter: str | None = None,
            crossref: str | BibtexReference | None = None,
            edition: str | None = None,
            editor: str | None = None,
            howpublished: str | None = None,
            institution: str | None = None,
            journal: str | None = None,
            month: str | None = None,
            note: str | None = None,
            number: str | None = None,
            organization: str | None = None,
            pages: str | int | None = None,
            publisher: str | None = None,
            school: str | None = None,
            series: str | None = None,
            title: str | None = None,
            type: str | None = None,
            volume: str | int | None = None,
            year: str | int | None = None,
            non_standard: NonStandard | None = None,
            ref_supplier = _cite):
        return ref_supplier(constructor.generic(
                    cite_key=_ANONYM_CITE_KEY,
                    address=address,
                    annote=annote,
                    booktitle=booktitle,
                    author=author,
                    chapter=chapter,
                    crossref=crossref,
                    edition=edition,
                    editor=editor,
                    howpublished=howpublished,
                    institution=institution,
                    journal=journal,
                    month=month,
                    note=note,
                    number=number,
                    organization=organization,
                    pages=pages,
                    publisher=publisher,
                    school=school,
                    series=series,
                    title=title,
                    type=type,
                    volume=volume,
                    year=year,
                    non_standard=non_standard,
                    scope=None if crossref is None else crossref.scope))
    return internal

article = _anonym(Article)
book = _anonym(Book)
booklet = _anonym(Booklet)
inbook = _anonym(Inbook)
incollection = _anonym(Incollection)
inproceedings = _anonym(Inproceedings)
conference = _anonym(Conference)
manual = _anonym(Manual)
mastersthesis = _anonym(Mastersthesis)
misc = _anonym(Misc)
phdthesis = _anonym(Phdthesis)
proceedings = _anonym(Proceedings)
techreport = _anonym(TechReport)
unpublished = _anonym(Unpublished)

TYPES: dict[str, type[BibtexReference]] = {
    'article': Article,
    'book': Book,
    'booklet': Booklet,
    'inbook': Inbook,
    'incollection': Incollection,
    'inproceedings': Inproceedings,
    'conference': Conference,
    'manual': Manual,
    'mastersthesis': Mastersthesis,
    'misc': Misc,
    'phdthesis': Phdthesis,
    'proceedings': Proceedings,
    'techreport': TechReport,
    'unpublished': Unpublished
}



SHARED_SCOPE: dict[str, BibtexReference] = {}
