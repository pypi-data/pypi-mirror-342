"""Test module for RIS 2001 api"""

from bibliograpy.api_ris2001 import Tags as RIS2001
from bibliograpy.api_ris2011 import Tags as RIS2011

def test_ris2001_retrocompatibility_support():
    """Test all RIS 2001 tags are defined in RIS 2011"""
    assert len({e for e in RIS2001 if e.name not in [t.name for t in RIS2011]}) == 0
    assert len({e for e in RIS2001 if e.name not in [t.name for t in RIS2011]}) == 0
