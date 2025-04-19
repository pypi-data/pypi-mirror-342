"""
refer specification model.
"""
from dataclasses import dataclass
from enum import Enum, auto

from bibliograpy.bibliography import REFER_MAN
from bibliograpy.api_bibtex import _cite


@dataclass(frozen=True)
class Tag:
    """A field tag."""
    auto: auto
    repeating: bool = False

@_cite(REFER_MAN)
class Tags(Tag, Enum):
    """
    REFER fields.
    """

    A = (auto(), True)
    """The name of an author.  If the name contains a title such as Jr.
    at the end, it should be separated  from  the  last  name  by  a
    comma.   There can be multiple occurrences of the %A field.  The
    order is significant.  It is a good idea always to supply an  %A
    field or a %Q field."""

    B = auto()
    """For an article that is part of a book, the title of the book."""

    C = auto()
    """The place (city) of publication."""

    D = auto()
    """The  date of publication.  The year should be specified in full.
    If the month is specified, the name rather than  the  number  of
    the  month  should be used, but only the first three letters are
    required.  It is a good idea always to supply a %D field; if the
    date  is  unknown,  a  value  such as in press or unknown can be
    used."""

    E = (auto(), True)
    """For an article that is part of a book, the name of an editor  of
    the  book.  Where the work has editors and no authors, the names
    of the editors should be  given  as  %A  fields  and  , (ed)  or
    , (eds) should be appended to the last author."""

    G = auto()
    """US Government ordering number."""

    I = auto()
    """The publisher (issuer)."""

    J = auto()
    """For an article in a journal, the name of the journal."""

    K = auto()
    """Keywords to be used for searching."""

    L = auto()
    """Label."""

    N = auto()
    """Journal issue number."""

    O = auto()
    """Other  information.   This  is usually printed at the end of the
    reference."""

    P = auto()
    """Page number.  A range of pages can be specified as m-n."""

    Q = (auto(), False)
    """The name of the author, if the author is  not  a  person.   This
    will  only be used if there are no %A fields.  There can only be
    one %Q field."""

    R = auto()
    """Technical report number."""

    S = auto()
    """Series name."""

    T = auto()
    """Title.  For an article in a book or journal, this should be  the
    title of the article."""

    V = auto()
    """Volume number of the journal or book."""

    X = auto()
    """Annotation."""

    @staticmethod
    def parse(tag_str: str):
        """Parses a tag name into an enum value."""
        for n in Tags:
            if tag_str in (n.name, "%" + n.name):
                return n
        raise ValueError(f'unknown {tag_str} tag')

def default_refer_formatter(r: dict[Tags, str | list[str]]):
    """The default formatter for refer references."""
    title = r[Tags.T] if Tags.T in r else ""
    return f"{title} [{r[Tags.L]}]" if Tags.L in r else title
