"""
RIS 2001 specification model.
"""
from dataclasses import dataclass
from enum import Enum, auto

from bibliograpy.bibliography import RIS_2001
from bibliograpy.api_bibtex import _cite


@dataclass(frozen=True)
class Tag:
    """A field tag."""
    auto: auto
    repeating: bool = False

@_cite(RIS_2001)
class Tags(Tag, Enum):
    """
    RIS fields.
    """

    TY = auto()
    """Type of reference. 
    This must contain one of the following field names as defined in the section, Reference Type field names."""

    ER = auto()
    """End of reference.
    Must be the last tag in a reference."""

    ID = auto()
    """Reference ID.
    The Reference ID can consist of any alphanumeric characters—up to 20 characters in length."""

    T1 = auto()
    """Title Primary.
    Note that the BT tag maps to this field only for Whole Book and Unpublished Work references.
    This field can contain alphanumeric characters; there is no practical length limit to this field."""
    TI = auto()  # synonym of T1
    CT = auto()  # synonym of T1

    BT = auto()

    T2 = auto()
    """Title Secondary.
    Note that the BT tag maps to this field for all reference types except for Whole Book and Unpublished Work 
    references.
    There is no practical limit to the length of this field."""

    T3 = auto()
    """Title Series.
    This field can contain alphanumeric characters; there is no practical length limit to this field."""

    A1 = (auto(), True)
    """Author Primary.
    Each author must be on a separate line, preceded by this tag. Each reference can contain unlimited author fields, 
    and can contain up to 255 characters for each field. The author name must be in the following syntax:

    Lastname, Firstname, Suffix

    For Firstname, you can use full names, initials, or both. The format for the author’s first name is as follows:

    Phillips,A.J

    Phillips,Albert John

    Phillips,Albert

    Lastname = Any string of letters, spaces, and hyphens

    Firstname = Any string of letters, spaces, and hyphens

    Initial = Any single letter followed by a period

    Full Name = Any string of letters, spaces, and hyphens

    Suffix = Jr/Sr/II/III/MD etc. (Phillips,A.J.,Sr.); use of the suffix is optional"""
    AU = (auto(), True)  # synonym of A1

    A2 = (auto(), True)
    """Author Secondary.
    Each author must be on a separate line, preceded by this tag. There is no practical limit to the number of authors
    in this field. The author name must be in the correct syntax (refer to A1 and AU fields).
    This author name can be up to 255 characters long."""
    ED = (auto(), True)  # synonym of A2

    A3 = (auto(), True)
    """Author Series. 
	Each author must be on a separate line, preceded by this tag. There is no practical limit to the number of authors 
	in this field. The author name must be in the correct syntax (refer to A1 and AU fields).
	Each author name can be up to 255 characters long."""

    Y1 = auto()
    """Date Primary.
    This date must be in the following format:

    YYYY/MM/DD/other info

    The year, month and day fields are all numeric. The other info field can be any string of letters, spaces and
    hyphens. Note that each specific date information is optional, however the slashes ("/") are not. For example, if
    you just had the <year> and <other info>, then the output would look like: "1998///Spring."
    """
    PY = auto()  # synonym of Y1

    Y2 = auto()
    """Date Secondary. (Refer to Y1 and PY fields)."""

    N1 = auto()
    """Notes.
    These are free text fields and can contain alphanumeric characters; there is no practical length limit to this
    field."""
    AB = auto()  # synonym of Y1

    N2 = auto()
    """Abstract.
    This is a free text field and can contain alphanumeric characters; there is no practical length limit to this field.
    """

    KW = (auto(), True)
    """Keywords.
    Each keyword or phrase must be on its own line, preceded by this tag. A keyword can consist of multiple words
    (phrases) and can be up to 255 characters long. There is no limit to the amount of keywords in a single reference.
    """

    RP = auto()
    """Reprint status.
    This optional field can contain one of three status notes. Each must be in uppercase,
    and the date after "ON REQUEST" must be in the US date format, in parentheses: (MM/DD/YY). 
    If this field is blank in your downloaded text file, the import function assumes the reprint status is 
    “NOT IN FILE.”
    
    The three options are:

    IN FILE - This is for references that you have a physical copy of in your files.
    NOT IN FILE - This is for references that you do not have physical copies of in your files.
    ON REQUEST (MM/DD/YY) - This means that you have sent for a reprint of the reference; the date is the date on which
    the reprint was requested (in MM/DD/YY format)."""

    JF = auto()
    """Periodical name: full format.
    This is an alphanumeric field of up to 255 characters."""
    JO = auto()  # synonym of JF

    JA = auto()
    """Periodical name: standard abbreviation.
    This is the periodical in which the article was (or is to be, in the case of in-press references) published.
    This is an alphanumeric field of up to 255 characters.

    If possible, periodical names should be abbreviated in the Index Medicus style, with periods after the
    abbreviations. If this is not possible (your large bibliography file in WordPerfect has no periods after
    abbreviations), you can use the "RIS Format (Adds periods)" Import Filter definition. This definition uses the
    Periodical Word Dictionary."""

    J1 = auto()
    """Periodical name: user abbreviation 1.
	This is an alphanumeric field of up to 255 characters."""

    J2 = auto()
    """Periodical name: user abbreviation 2.
    This is an alphanumeric field of up to 255 characters."""

    VL = auto()
    """Volume number.
    There is no practical limit to the length of this field."""

    IS = auto()
    """Issue.
    There is no practical limit to the length of this field."""
    CP = auto()  # synonym of IS

    SP = auto()
    """Start page number; an alphanumeric string.
    There is no practical limit to the length of this field."""

    EP = auto()
    """Ending page number, as above."""

    CY = auto()
    """City of publication; this is an alphanumeric field.
    There is no practical limit to the length of this field."""

    PB = auto()
    """Publisher; this is an alphanumeric field.
    There is no practical limit to the length of this field."""

    SN = auto()
    """ISSN/ISBN. This is an alphanumeric field.
    There is no practical limit to the length of this field."""

    AD = auto()
    """Address.
    This is a free text field and contain alphanumeric characters; there is no practical length limit to this field."""

    AV = auto()
    """Availability.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    M1 = auto()
    """Miscellaneous 1.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    M2 = auto()
    """Miscellaneous 2.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    M3 = auto()
    """Miscellaneous 3.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    U1 = auto()
    """User definable 1.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    U2 = auto()
    """User definable 2.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    U3 = auto()
    """User definable 3.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    U4 = auto()
    """User definable 4.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    U5 = auto()
    """User definable 5.
    This is an alphanumeric field and there is no practical limit to the length of this field."""

    UR = auto()
    """Web/URL.
	There is no practical limit to the length of this field.
	URL addresses can be entered individually, one per tag or multiple addresses can be entered on one line
	using a semi-colon as a separator."""

    L1 = auto()
    """Link to PDF.
    There is no practical limit to the length of this field.
    URL addresses can be entered individually, one per tag or multiple addresses can be entered on one line
    using a semi-colon as a separator."""

    L2 = auto()
    """Link to Full-text.
    There is no practical limit to the length of this field.
    URL addresses can be entered individually, one per tag or multiple addresses can be entered on one line
    using a semi-colon as a separator."""

    L3 = auto()
    """Related Records.
    There is no practical limit to the length of this field."""

    L4 = auto()
    """Image(s).
    There is no practical limit to the length of this field."""

    @staticmethod
    def parse(tag_str: str):
        """Parses a tag name into an enum value."""
        for n in Tags:
            if tag_str == n.name:
                return n
        raise ValueError(f'unknown {tag_str} tag')


@_cite(RIS_2001)
class TypeFieldName(Enum):
    """Reference Type Field Names

    The following describes the valid reference type field names that can be used with for the reference type field when
    importing references into Reference Manager."""

    ABST = auto()
    """Abstract"""

    ADVS = auto()
    """Audiovisual material"""

    ART = auto()
    """Art Work"""

    BILL = auto()
    """Bill/Resolution"""

    BOOK = auto()
    """Book, Whole"""

    CASE = auto()
    """Case"""

    CHAP = auto()
    """Book chapter"""

    COMP = auto()
    """Computer program"""

    CONF = auto()
    """Conference proceeding"""

    CTLG = auto()
    """Catalog"""

    DATA = auto()
    """Data file"""

    ELEC = auto()
    """Electronic Citation"""

    GEN = auto()
    """Generic"""

    HEAR = auto()
    """Hearing"""

    ICOMM = auto()
    """Internet Communication"""

    INPR = auto()
    """In Press"""

    JFULL = auto()
    """Journal (full)"""

    JOUR = auto()
    """Journal"""

    MAP = auto()
    """Map"""

    MGZN = auto()
    """Magazine article"""

    MPCT = auto()
    """Motion picture"""

    MUSIC = auto()
    """Music score"""

    NEWS = auto()
    """Newspaper"""

    PAMP = auto()
    """Pamphlet"""

    PAT = auto()
    """Patent"""

    PCOMM = auto()
    """Personal communication"""

    RPRT = auto()
    """Report"""

    SER = auto()
    """Serial (Book, Monograph)"""

    SLIDE = auto()
    """Slide"""

    SOUND = auto()
    """Sound recording"""

    STAT = auto()
    """Statute"""

    THES = auto()
    """Thesis/Dissertation"""

    UNBILL = auto()
    """Unenacted bill/resolution"""

    UNPB = auto()
    """Unpublished work"""

    VIDEO = auto()
    """Video recording"""

    @staticmethod
    def parse(entry_type: str):
        """Parses an entry type name into an enum value."""
        for n in TypeFieldName:
            if entry_type == n.name:
                return n
        raise ValueError(f'unknown {entry_type} type')


def default_ris2001_formatter(r: dict[Tags, str | list[str] | TypeFieldName]):
    """The default formatter for RIS 2001 references."""
    title = r[Tags.TI] if Tags.TI in r else (r[Tags.T1] if Tags.T1 in r else (r[Tags.CT] if Tags.CT in r else ""))
    return f"{title} [{r[Tags.ID]}]" if Tags.ID in r else title
