from bibliograpy.api_bibtex import *

_SCOPE = dict()


BIBLIOGRAPI = Misc.generic(cite_key='bibliograpi',
                           author='Samuel Andrés',
                           title='BibliogrAPI Specification',
                           year='2024',
                           non_standard=NonStandard(url='https://cosmoloj.com/bibapi/'),
                           scope=_SCOPE)

RIS_2001 = Misc.generic(cite_key='ris_2001',
                        month='february',
                        title='RIS Format Specifications',
                        year='2001',
                        non_standard=NonStandard(url='https://web.archive.org/web/20110925024348/http://www.refman.com/support/risformat_intro.asp'),
                        scope=_SCOPE)

RIS_2011 = Misc.generic(cite_key='ris_2011',
                        month='october',
                        title='RIS Format Specifications',
                        year='2011',
                        non_standard=NonStandard(url='https://web.archive.org/web/20120616231500/http://www.refman.com/support/risformat_intro.asp'),
                        scope=_SCOPE)

REFER_MAN = Misc.generic(cite_key='refer_man',
                         title='refer(1) — Linux manual page',
                         non_standard=NonStandard(url='https://man7.org/linux/man-pages/man1/refer.1.html'),
                         scope=_SCOPE)
