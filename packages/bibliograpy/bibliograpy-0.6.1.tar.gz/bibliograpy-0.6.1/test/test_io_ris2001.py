"""Test module for RIS 2001 IO"""
from pathlib import Path
from typing import TextIO

import pytest

from bibliograpy.api_core import Formats
from bibliograpy.api_ris2001 import Tags as RIS2001, TypeFieldName
from bibliograpy.io_ris2001 import Ris2001InputFormat


def read_ris_entries(i: TextIO):
    """ris entry parsing shortcut"""
    return Ris2001InputFormat(Formats.RIS2001).from_standard(i)

def test_multiple_records():
    """test sample using the 2011 specification"""

    with open(Path(__file__).parent / 'resources' / 'ris2011' / 'multipleRecords.ris', encoding='utf-8') as s:
        with pytest.raises(ValueError) as e:
            read_ris_entries(s)
        assert e.value.args[0] == 'unknown DA tag'

def test_sample1():
    """test 2001 specification sample"""

    with open(Path(__file__).parent / 'resources' / 'ris2001' / 'sample1.ris', encoding='utf-8') as s:
        result = read_ris_entries(s)
        assert len(result) == 1
        assert result[0] == {
            RIS2001.TY: TypeFieldName.JOUR,
            RIS2001.A1: ['Baldwin,S.A.', 'Fugaccia,I.', 'Brown,D.R.', 'Brown,L.V.', 'Scheff,S.W.'],
            RIS2001.T1: 'Blood-brain barrier breach following cortical contusion in the rat',
            RIS2001.JO: 'J.Neurosurg.',
            RIS2001.Y1: '1996',
            RIS2001.VL: '85',
            RIS2001.SP: '476',
            RIS2001.EP: '481',
            RIS2001.RP: 'Not In File',
            RIS2001.KW: ['cortical contusion', 'blood-brain barrier', 'horseradish peroxidase', 'head trauma',
                         'hippocampus', 'rat'],
            RIS2001.N2: """Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the \
hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe cortical damage and neuronal loss in \
hippocampus subfields CA1, CA3 and hilus. Breakdown of the blood-brain barrier (BBB) was assessed by injecting the \
protein horseradish peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, 6, 12 \
hours, 1, 2, 5, and 10 days). Animals were killed 1 hour after HRP injection and brain sections were reacted with \
diaminobenzidine to visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected \
with HRP 5 minutes prior to or 5 minutes after cortical contusion. Staining at these time points was observed in the \
ipsilateral hippocampus. Some modest staining occurred in the dorsal contralateral cortex near the superior sagittal \
sinus. Cortical HRP stain gradually decreased at increasing time intervals postinjury. By 10 days, no HRP stain was \
observed in any area of the brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and \
remained so at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral \
hippocampus 1 and 2 days following cortical contusion, indicating a biphasic opening of the BBB following head trauma \
and a possible second wave of secondary brain damage days after the contusion injury. These data indicate regions not \
initially destroyed by cortical impact, but evidencing BBB breach, may be accessible to neurotrophic factors \
administered intravenously both immediately and days after brain trauma."""
        }

def test_sample2():
    """test 2001 specification sample"""

    with open(Path(__file__).parent / 'resources' / 'ris2001' / 'sample2.ris', encoding='utf-8') as s:
        result = read_ris_entries(s)
        assert len(result) == 1
        assert result[0] == {
            RIS2001.TY: TypeFieldName.PAT,
            RIS2001.A1: ['Burger,D.R.', 'Goldstein,A.S.'],
            RIS2001.T1: 'Method of detecting AIDS virus infection',
            RIS2001.Y1: '1990/2/27',
            RIS2001.VL: '877609',
            RIS2001.IS: '4,904,581',
            RIS2001.RP: 'Not In File',
            RIS2001.A2: ['Epitope,I.'],
            RIS2001.CY: 'OR',
            RIS2001.PB: '4,629,783',
            RIS2001.KW: ['AIDS', 'virus', 'infection', 'antigens'],
            RIS2001.Y2: '1986/6/23',
            RIS2001.M1: 'G01N 33/569 G01N 33/577',
            RIS2001.M2: """435/5 424/3 424/7.1 435/7 435/29 435/32 435/70.21 435/240.27 435/172.2 530/387 530/808 \
530/809 935/110""",
            RIS2001.N2: """A method is disclosed for detecting the presence of HTLV III infected cells in a medium. \
The method comprises contacting the medium with monoclonal antibodies against an antigen produced as a result of the \
infection and detecting the binding of the antibodies to the antigen. The antigen may be a gene product of the HTLV \
III virus or may be bound to such gene product. On the other hand the antigen may not be a viral gene product but may \
be produced as a result of the infection and may further be bound to a lymphocyte. The medium may be a human body \
fluid or a culture medium. A particular embodiment of the present method involves a method for determining the \
presence of a AIDS virus in a person. The method comprises combining a sample of a body fluid from the person with a \
monoclonal antibody that binds to an antigen produced as a result of the infection and detecting the binding of the \
monoclonal antibody to the antigen. The presence of the binding indicates the presence of a AIDS virus infection. Also \
disclosed are novel monoclonal antibodies, noval compositions of matter, and novel diagnostic kits"""
        }

def test_sample3():
    """test 2001 specification sample"""

    with open(Path(__file__).parent / 'resources' / 'ris2001' / 'sample3.ris', encoding='utf-8') as s:
        result = read_ris_entries(s)
        assert len(result) == 1
        assert result[0] == {
            RIS2001.TY: TypeFieldName.CONF,
            RIS2001.A1: ['Catania,J.', 'Coates,T.', 'Kegeles,S.', 'Peterson,J.', 'Marin,B.', 'Fullilove,M.'],
            RIS2001.T1: """Predicting risk behavior with the AIDS risk reduction model (ARRM) in a random household \
probability sample of San Franciscans: the "AMEN" study""",
            RIS2001.Y1: '1990///6th Annual',
            RIS2001.VL: '6',
            RIS2001.SP: '318',
            RIS2001.EP: '318',
            RIS2001.RP: 'Not In File',
            RIS2001.CY: 'Detroit MI',
            RIS2001.KW: ['risk', 'AIDS', 'models', 'sexual behavior', 'HIV', 'condoms', 'heterosexual', 'bisexual',
                         'ethnicity', 'women'],
            RIS2001.T3: 'International Conference on AIDS 6',
            RIS2001.Y2: '1990/6/20',
            RIS2001.M1: '1',
            RIS2001.N1: """OBJECTIVE: Data from the AIDS In Multi-Ethnic Neighborhoods survey are used to test Stages \
1 & 3 of ARRM (a three stage process model of sexual risk behavior change; Catania, Kegeles, & Coates, 1990). Stage 1 \
analyses examine predictors of labeling one's sexual behavior in terms of HIV risk; Stage 3 concerns predictors of \
sexual behavior (e.g., condom use) (Stage 2 was not assessed in this first wave of the study but will be examined in \
wave 2). METHODS: Data were collected in a random household probability study of 1,781 white (41%), black (26%), and \
Hispanic (25%) (8% Other), unmarried respondents, aged 20-44, residing in selected \"high risk\" census tracts of San \
Francisco (Heterosexual = 83%, Homosexual = 13%, Bisexual = 4%). Labeling defined as making an accurate or inaccurate \
assessment of one's risk for HIV based on prior and current sexual practices. The behavioral outcome is frequency of \
condom use averaged across sexual partners for the past year. RESULTS: Multiple regression (Logistic & LSQ) analyses \
indicate that, 1) Accurate labeling of high risk behavior is related to high susceptibility beliefs (Imp. Chi Sq. \
=,92.46, p less than .0001), but unrelated to knowing someone with AIDS; gay relative to heterosexual men (p less than \
.03), and Hispanics compared to whites (p less than .01) were more likely to accurately label their behavior, 2) \
Greater condom use during vaginal or anal intercourse is significantly related to better sexual communication skills, \
higher perceived benefits and lower costs of condom use, but unrelated to religiosity, self-efficacy, and ethnicity \
(R's range from .50 - .66); these latter results are substantially the same for men and women, and heterosexuals and \
gay men. CONCLUSION: The findings 1) suggest the ARRM model is applicable to most social groups, 2) underscore the \
importance of interventions that enhance communication skills and teach methods of facilitating sexual enjoyment of \
condoms"""
        }

def test_sample456():
    """test 2001 specification sample"""

    with open(Path(__file__).parent / 'resources' / 'ris2001' / 'sample456.ris', encoding='utf-8') as s:
        result = read_ris_entries(s)
        assert len(result) == 3
        assert result[0] == {
            RIS2001.TY: TypeFieldName.RPRT,
            RIS2001.A1: ['Esparza,J.'],
            RIS2001.T1: """Report of a WHO workshop on the measurement and significance of neutralizing antibody to \
HIV and SIV, London, 3-5 October 1988""",
            RIS2001.Y1: '1990',
            RIS2001.VL: '4',
            RIS2001.SP: '269',
            RIS2001.EP: '275',
            RIS2001.RP: 'Not In File',
            RIS2001.CY: 'San Francisco CA',
            RIS2001.PB: 'UC Berkeley',
            RIS2001.KW: ['HIV', 'SIV', 'AIDS'],
            RIS2001.T3: 'World Health Organisation Global Programme on AIDS'
        }
        assert result[1] == {
            RIS2001.TY: TypeFieldName.CHAP,
            RIS2001.A1: ['Franks,L.M.'],
            RIS2001.T1: 'Preface by an AIDS Victim',
            RIS2001.Y1: '1991',
            RIS2001.VL: '10',
            RIS2001.SP: 'vii',
            RIS2001.EP: 'viii',
            RIS2001.RP: 'Not In File',
            RIS2001.T2: 'Cancer, HIV and AIDS.',
            RIS2001.CY: 'Berkeley CA',
            RIS2001.PB: 'Berkeley Press',
            RIS2001.KW: ['HIV', 'AIDS'],
            RIS2001.M1: '1',
            RIS2001.M2: '1',
            RIS2001.SN: '0-679-40110-5'
        }
        assert result[2] == {
            RIS2001.TY: TypeFieldName.CASE,
            RIS2001.A1: ['Cary,A.', 'Friedenrich,W.'],
            RIS2001.T1: 'Redman v. State of California',
            RIS2001.Y1: '1988/10/7',
            RIS2001.VL: '201',
            RIS2001.IS: '32',
            RIS2001.SP: '220',
            RIS2001.EP: '240',
            RIS2001.RP: 'Not In File',
            RIS2001.CY: 'ATLA Law Reporter',
            RIS2001.PB: 'San Diego County 45th Judicial District, California',
            RIS2001.KW: ['AIDS', 'litigation', 'AIDS litigation', 'rape'],
            RIS2001.U1: 'ISSN 0456-8125',
            RIS2001.N1: 'Raped inmate can press case against officials for contracting AIDS'
        }
