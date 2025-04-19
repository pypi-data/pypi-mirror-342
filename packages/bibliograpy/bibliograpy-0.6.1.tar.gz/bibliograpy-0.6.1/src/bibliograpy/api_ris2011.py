"""
RIS 2011 specification model.
"""
from dataclasses import dataclass
from enum import Enum, auto

from bibliograpy.bibliography import RIS_2011
from bibliograpy.api_bibtex import _cite


@dataclass(frozen=True)
class Tag:
    """A field tag."""
    auto: auto
    repeating: bool = False

@_cite(RIS_2011)
class Tags(Tag, Enum):
    """
    RIS fields.
    """

    TY = auto()
    """Type of reference. 
    This must contain the abbreviation for the reference type as found in the next section. This will determine how all 
    other fields are interpreted."""

    ER = auto()
    """End of reference.
    Must be the last tag in a reference."""

    AU = (auto(), True)
    """Authors, Editors, Translators. 
    Each author must be on a separate line, preceded by the tag that corresponds to the author role (see individual ref 
    type matrix for role definitions). Each reference can contain unlimited author fields, and can contain up to 255 
    characters for each field. The author name must be in the following syntax:
    
    Lastname, Firstname, Suffix
    
    For Firstname, you can use full names, initials, or both. The format for the author’s first name is as follows:
    
    Phillips, A.J
    
    Phillips, Albert John
    
    Phillips, Albert
    
    Lastname = Any string of letters, spaces, and hyphens
    
    Firstname = Any string of letters, spaces, and hyphens
    
    Initial = Any single letter followed by a period
    
    Full Name = Any string of letters, spaces, and hyphens
    
    Suffix = Jr/Sr/II/III/MD etc. (Phillips,A.J.,Sr.); use of the suffix is optional"""

    A2 = (auto(), True)
    """Secondary Author"""

    A3 = (auto(), True)
    """Tertiary Author"""

    A4 = (auto(), True)
    """Subsidiary Author"""

    AB = auto()
    """Abstract"""

    AD = auto()
    """Author address"""

    AN = auto()
    """Accession Number"""

    C1 = auto()
    """Custom 1"""

    C2 = auto()
    """Custom 2"""

    C3 = auto()
    """Custom 3"""

    C4 = auto()
    """Custom 4"""

    C5 = auto()
    """Custom 5"""

    C6 = auto()
    """Custom 6"""

    C7 = auto()
    """Custom 7"""

    C8 = auto()
    """Custom 8"""

    CA = auto()
    """Caption"""

    CN = auto()
    """Call Number"""

    CY = auto()
    """Place Published"""

    DB = auto()
    """Name of Database"""

    DO = auto()
    """DOI"""

    DP = auto()
    """Database provider"""

    ET = auto()
    """Edition"""

    ID = auto()
    """The characters allowed in the reference ID fields can be in the set "0" through "9," or "A" through "Z.\""""

    PY = auto()
    """This is the publication year. 
    It must be four numeric characters. Dates prior to 1000 should use “0” in the positions before the intended date. 
    For example, the year 765 would be represented as 0765."""

    DA = auto()
    """Dates must be in the following format:
    
    YYYY/MM/DD/other info
    
    The year, month and day fields are all numeric. The other info field can be any string of letters, spaces and 
    hyphens.
    
    Note that each specific date information is optional, however the slashes (“/”) are not. For example, if you just 
    had the <year> and <other info>, then the output would look like: “1993///Spring.”
    
    Date information should be set forth in the following format:
    
    YYYY or
    YYYY/MM or
    YYYY/MM/DD or
    YYYY/MM/DD/other info"""

    KW = (auto(), True)
    """Keywords.
    Each keyword or phrase must be on its own line, preceded by this tag. A keyword can consist of multiple words 
    (phrases) and can be up to 255 characters long. There can be unlimited keywords in a reference."""

    RP = auto()
    """Reprint status.
    This optional field can contain one of three status notes. Each must be in uppercase, and the date after 
    “ON REQUEST” must be in USA format, in parentheses (MM/DD/YY). If this field is blank the Import function assumes 
    the reprint status is “NOT IN FILE.”
    
    The three options are:

    IN FILE – The data provider has a corresponding physical copy for the reference.
    NOT IN FILE – The data provider does not have a corresponding physical copy.
    ON REQUEST (mm/dd/yy) - This means that the data provider has requested a reprint of the reference; the date is the 
    date on which the reprint was requested (in mm/dd/yy format)."""

    J2 = auto()
    """Periodical name: standard abbreviation. 
    This is the abbreviation of the periodical in which the article is published. If possible, periodical names should 
    be abbreviated in the Index Medicus® style, with periods after the abbreviations. This field is mapped to the full 
    journal name in T2 and is used as the journal abbreviation in output styles."""

    L1 = auto()
    """File attachment"""

    L4 = auto()
    """Figure"""

    LA = auto()
    """Language"""

    LB = auto()
    """Label"""

    IS = auto()
    """Number"""

    M3 = auto()
    """Type of Work"""

    N1 = auto()
    """Notes"""

    NV = auto()
    """Number of Volumes"""

    OP = auto()
    """Original Publication"""

    PB = auto()
    """Publisher"""

    UR = auto()
    """Web/URL.
    There is no practical length limit to this field. URL addresses can be entered individually, one per tag, or
    multiple addresses can be entered on one line using a semi-colon as a separator."""

    # following fields are for implicit RIS 2001 retrocompatibility in RIS 2011 samples
    T3 = auto()
    CT = auto()
    U3 = auto()
    L3 = auto()
    T1 = auto()
    CP = auto()
    AV = auto()
    EP = auto()
    JO = auto()
    U1 = auto()
    U5 = auto()
    VL = auto()
    L2 = auto()
    JF = auto()
    U4 = auto()
    ED = (auto(), True)
    J1 = auto()
    SN = auto()
    Y1 = auto()
    T2 = auto()
    N2 = auto()
    TI = auto()
    BT = auto()
    A1 = (auto(), True)
    JA = auto()
    M2 = auto()
    U2 = auto()
    M1 = auto()
    Y2 = auto()
    SP = auto()

    @staticmethod
    def parse(tag_str: str):
        """Parses a tag name into an enum value."""
        for n in Tags:
            if tag_str == n.name:
                return n
        raise ValueError(f'unknown {tag_str} tag')


@_cite(RIS_2011)
class TypeFieldName(Enum):
    """Reference Type Field Names

    The following describes the valid reference type field names that can be used with for the reference type field when
    importing references into Reference Manager."""

    ABST = auto()
    """Abstract"""

    AGGR = auto()
    """Aggregated Database"""

    ANCIENT = auto()
    """Ancient Text"""

    ADVS = auto()
    """Audiovisual material"""

    ART = auto()
    """Art Work"""

    BILL = auto()
    """Bill"""

    BLOG = auto()
    """Blog"""

    BOOK = auto()
    """Book, Whole"""

    CASE = auto()
    """Case"""

    CHAP = auto()
    """Book Section"""

    CHART = auto()
    """Chart"""

    CLSWK = auto()
    """Classical Work"""

    COMP = auto()
    """Computer program"""

    CONF = auto()
    """Conference proceeding"""

    CPAPER = auto()
    """Conference Paper"""

    CTLG = auto()
    """Catalog"""

    DATA = auto()
    """Dataset"""

    DICT = auto()
    """Dictionary"""

    EDBOOK = auto()
    """Edited book"""

    EBOOK = auto()
    """Electronic book"""

    ECHAP = auto()
    """Electronic Book Section"""

    EJOUR = auto()
    """Electronic Article"""

    ENCYC = auto()
    """Encyclopedia"""

    EQUA = auto()
    """Equation"""

    FIGURE = auto()
    """Figure"""

    GEN = auto()
    """Generic"""

    GOVDOC = auto()
    """Government Document"""

    GRNT = auto()
    """Grant"""

    HEAR = auto()
    """Hearing"""

    ICOMM = auto()
    """Internet Communication"""

    INPR = auto()
    """In Press Article"""

    JFULL = auto()
    """Full Journal"""

    JOUR = auto()
    """Journal"""

    LEGAL = auto()
    """Legal Rule"""

    MAP = auto()
    """Map"""

    MGZN = auto()
    """Magazine article"""

    MANSCPT = auto()
    """Manuscript"""

    MUSIC = auto()
    """Music"""

    NEWS = auto()
    """Newspaper"""

    DBASE = auto()
    """Online Database"""

    MULTI = auto()
    """Online Multimedia"""

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

    STAND = auto()
    """Standard"""

    STAT = auto()
    """Statute"""

    THES = auto()
    """Thesis/Dissertation"""

    UNBILL = auto()
    """Unenacted bill/resolution"""

    UNPD = auto()
    """Unpublished work"""

    VIDEO = auto()
    """Video recording"""

    ELEC = auto()
    """Web Page"""

    @staticmethod
    def parse(entry_type: str):
        """Parses an entry type name into an enum value."""
        for n in TypeFieldName:
            if entry_type == n.name:
                return n
        raise ValueError(f'unknown {entry_type} type')

def default_ris2011_formatter(r: dict[Tags, str | list[str] | TypeFieldName]):
    """The default formatter for RIS 2011 references."""
    title = r[Tags.TI] if Tags.TI in r else (r[Tags.T1] if Tags.T1 in r else (r[Tags.CT] if Tags.CT in r else ""))
    return f"{title} [{r[Tags.ID]}]" if Tags.ID in r else title
