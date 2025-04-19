"""Test module for ris2011 process tool."""

from argparse import Namespace
from pathlib import Path
import pydoc
import sys
import time

import yaml

import pytest

from bibliograpy.api_common import cite

from bibliograpy.process import _process


def _ris2001_resource(file: str) -> str:
    """Chemin vers les fichiers d'entrée."""
    return str(Path(Path(__file__).parent / 'resources' / 'ris2001' / file))


def _sibbling_module(file: str) -> str:
    """Chemin vers les fichiers de modules voisins."""
    return str(Path(Path(__file__).parent / file))


def _output(file: str) -> str:
    """Chemin vers les fichiers de sortie."""
    return str(Path(Path(__file__).parent / 'resources' / 'ris2011' / 'out' / file))


def test_ris2011_yml_to_yml():
    """test process from a yml bibliography to a yml bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_ris2011_yml_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_yml_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {"TY": "JOUR",
             "A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."],
             "T1": "Blood-brain barrier breach following cortical contusion in the rat",
             "JO": "J.Neurosurg.",
             "Y1": "1996",
             "VL": "85",
             "SP": "476",
             "EP": "481",
             "RP": "Not In File",
             "KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", "head trauma",
                    "hippocampus", "rat"],
             "N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the "
                   "hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe cortical damage and "
                   "neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown of the blood-brain barrier "
                   "(BBB) was assessed by injecting the protein horseradish peroxidase (HRP) 5 minutes prior to or at "
                   "various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and 10 days). Animals were "
                   "killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to "
                   "visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected "
                   "with HRP 5 minutes prior to or 5 minutes after cortical contusion. Staining at these time points "
                   "was observed in the ipsilateral hippocampus. Some modest staining occurred in the dorsal "
                   "contralateral cortex near the superior sagittal sinus. Cortical HRP stain gradually decreased at "
                   "increasing time intervals postinjury. By 10 days, no HRP stain was observed in any area of the "
                   "brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so "
                   "at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral "
                   "hippocampus 1 and 2 days following cortical contusion, indicating a biphasic opening of the BBB "
                   "following head trauma and a possible second wave of secondary brain damage days after the "
                   "contusion injury. These data indicate regions not initially destroyed by cortical impact, but "
                   "evidencing BBB breach, may be accessible to neurotrophic factors administered intravenously both "
                   "immediately and days after brain trauma."}]

def test_ris2011_yml_to_ris():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_ris2011_yml_to_ris.ris'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_yml_to_ris.ris'), encoding='utf-8') as s:
        content = s.read()
        assert content == """TY  - JOUR
A1  - Baldwin,S.A.
A1  - Fugaccia,I.
A1  - Brown,D.R.
A1  - Brown,L.V.
A1  - Scheff,S.W.
T1  - Blood-brain barrier breach following cortical contusion in the rat
JO  - J.Neurosurg.
Y1  - 1996
VL  - 85
SP  - 476
EP  - 481
RP  - Not In File
KW  - cortical contusion
KW  - blood-brain barrier
KW  - horseradish peroxidase
KW  - head trauma
KW  - hippocampus
KW  - rat
N2  - Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the hippocampus at 3.5 \
m/sec with a 2 mm cortical depression. This caused severe cortical damage and neuronal loss in hippocampus subfields \
CA1, CA3 and hilus. Breakdown of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish \
peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and \
10 days). Animals were killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to \
visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected with HRP 5 minutes \
prior to or 5 minutes after cortical contusion. Staining at these time points was observed in the ipsilateral \
hippocampus. Some modest staining occurred in the dorsal contralateral cortex near the superior sagittal sinus. \
Cortical HRP stain gradually decreased at increasing time intervals postinjury. By 10 days, no HRP stain was observed \
in any area of the brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so \
at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral hippocampus 1 and 2 \
days following cortical contusion, indicating a biphasic opening of the BBB following head trauma and a possible \
second wave of secondary brain damage days after the contusion injury. These data indicate regions not initially \
destroyed by cortical impact, but evidencing BBB breach, may be accessible to neurotrophic factors administered \
intravenously both immediately and days after brain trauma.
ER  - 
"""

def test_ris2011_yml_to_json():
    """test process from a yml bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.yml'),
                       output_file=_output('test_ris2011_yml_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_yml_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"TY": "JOUR", '
                           '"A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."], '
                           '"T1": "Blood-brain barrier breach following cortical contusion in the rat", '
                           '"JO": "J.Neurosurg.", '
                           '"Y1": "1996", '
                           '"VL": "85", '
                           '"SP": "476", '
                           '"EP": "481", '
                           '"RP": "Not In File", '
                           '"KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", '
                           '"head trauma", "hippocampus", "rat"], '
                           '"N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex '
                           'above the hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe '
                           'cortical damage and neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown '
                           'of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish '
                           'peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, '
                           '6, 12 hours, 1, 2, 5, and 10 days). Animals were killed 1 hour after HRP injection and '
                           'brain sections were reacted with diaminobenzidine to visualize extravascular accumulation '
                           'of the protein. Maximum staining occurred in animals injected with HRP 5 minutes prior to '
                           'or 5 minutes after cortical contusion. Staining at these time points was observed in the '
                           'ipsilateral hippocampus. Some modest staining occurred in the dorsal contralateral cortex '
                           'near the superior sagittal sinus. Cortical HRP stain gradually decreased at increasing '
                           'time intervals postinjury. By 10 days, no HRP stain was observed in any area of the brain. '
                           'In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so '
                           'at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the '
                           'ipsilateral hippocampus 1 and 2 days following cortical contusion, indicating a biphasic '
                           'opening of the BBB following head trauma and a possible second wave of secondary brain '
                           'damage days after the contusion injury. These data indicate regions not initially '
                           'destroyed by cortical impact, but evidencing BBB breach, may be accessible to '
                           'neurotrophic factors administered intravenously both immediately and days after brain '
                           'trauma."}]')

def test_ris2011_json_to_yml():
    """test process from a json bibliography to a yml bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_ris2011_json_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_json_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {"TY": "JOUR",
             "A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."],
             "T1": "Blood-brain barrier breach following cortical contusion in the rat",
             "JO": "J.Neurosurg.",
             "Y1": "1996",
             "VL": "85",
             "SP": "476",
             "EP": "481",
             "RP": "Not In File",
             "KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", "head trauma",
                    "hippocampus", "rat"],
             "N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the "
                   "hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe cortical damage and "
                   "neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown of the blood-brain barrier "
                   "(BBB) was assessed by injecting the protein horseradish peroxidase (HRP) 5 minutes prior to or at "
                   "various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and 10 days). Animals were "
                   "killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to "
                   "visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected "
                   "with HRP 5 minutes prior to or 5 minutes after cortical contusion. Staining at these time points "
                   "was observed in the ipsilateral hippocampus. Some modest staining occurred in the dorsal "
                   "contralateral cortex near the superior sagittal sinus. Cortical HRP stain gradually decreased at "
                   "increasing time intervals postinjury. By 10 days, no HRP stain was observed in any area of the "
                   "brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so "
                   "at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral "
                   "hippocampus 1 and 2 days following cortical contusion, indicating a biphasic opening of the BBB "
                   "following head trauma and a possible second wave of secondary brain damage days after the "
                   "contusion injury. These data indicate regions not initially destroyed by cortical impact, but "
                   "evidencing BBB breach, may be accessible to neurotrophic factors administered intravenously both "
                   "immediately and days after brain trauma."}]

def test_ris2011_json_to_ris():
    """test process from a json bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_ris2011_json_to_ris.ris'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_json_to_ris.ris'), encoding='utf-8') as s:
        content = s.read()
        assert content == """TY  - JOUR
A1  - Baldwin,S.A.
A1  - Fugaccia,I.
A1  - Brown,D.R.
A1  - Brown,L.V.
A1  - Scheff,S.W.
T1  - Blood-brain barrier breach following cortical contusion in the rat
JO  - J.Neurosurg.
Y1  - 1996
VL  - 85
SP  - 476
EP  - 481
RP  - Not In File
KW  - cortical contusion
KW  - blood-brain barrier
KW  - horseradish peroxidase
KW  - head trauma
KW  - hippocampus
KW  - rat
N2  - Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the hippocampus at 3.5 \
m/sec with a 2 mm cortical depression. This caused severe cortical damage and neuronal loss in hippocampus subfields \
CA1, CA3 and hilus. Breakdown of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish \
peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and \
10 days). Animals were killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to \
visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected with HRP 5 minutes \
prior to or 5 minutes after cortical contusion. Staining at these time points was observed in the ipsilateral \
hippocampus. Some modest staining occurred in the dorsal contralateral cortex near the superior sagittal sinus. \
Cortical HRP stain gradually decreased at increasing time intervals postinjury. By 10 days, no HRP stain was observed \
in any area of the brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so \
at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral hippocampus 1 and 2 \
days following cortical contusion, indicating a biphasic opening of the BBB following head trauma and a possible \
second wave of secondary brain damage days after the contusion injury. These data indicate regions not initially \
destroyed by cortical impact, but evidencing BBB breach, may be accessible to neurotrophic factors administered \
intravenously both immediately and days after brain trauma.
ER  - 
"""

def test_ris2011_json_to_json():
    """test process from a json bibliography to a json bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.json'),
                       output_file=_output('test_ris2011_json_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_json_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"TY": "JOUR", '
                           '"A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."], '
                           '"T1": "Blood-brain barrier breach following cortical contusion in the rat", '
                           '"JO": "J.Neurosurg.", '
                           '"Y1": "1996", '
                           '"VL": "85", '
                           '"SP": "476", '
                           '"EP": "481", '
                           '"RP": "Not In File", '
                           '"KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", '
                           '"head trauma", "hippocampus", "rat"], '
                           '"N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex '
                           'above the hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe '
                           'cortical damage and neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown '
                           'of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish '
                           'peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, '
                           '6, 12 hours, 1, 2, 5, and 10 days). Animals were killed 1 hour after HRP injection and '
                           'brain sections were reacted with diaminobenzidine to visualize extravascular accumulation '
                           'of the protein. Maximum staining occurred in animals injected with HRP 5 minutes prior to '
                           'or 5 minutes after cortical contusion. Staining at these time points was observed in the '
                           'ipsilateral hippocampus. Some modest staining occurred in the dorsal contralateral cortex '
                           'near the superior sagittal sinus. Cortical HRP stain gradually decreased at increasing '
                           'time intervals postinjury. By 10 days, no HRP stain was observed in any area of the brain. '
                           'In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so '
                           'at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the '
                           'ipsilateral hippocampus 1 and 2 days following cortical contusion, indicating a biphasic '
                           'opening of the BBB following head trauma and a possible second wave of secondary brain '
                           'damage days after the contusion injury. These data indicate regions not initially '
                           'destroyed by cortical impact, but evidencing BBB breach, may be accessible to '
                           'neurotrophic factors administered intravenously both immediately and days after brain '
                           'trauma."}]')

def test_ris2011_ris_to_yml():
    """test process from a bib bibliography to a yml bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.ris'),
                       output_file=_output('test_ris2011_ris_to_yml.yml'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_ris_to_yml.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == [
            {"TY": "JOUR",
             "A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."],
             "T1": "Blood-brain barrier breach following cortical contusion in the rat",
             "JO": "J.Neurosurg.",
             "Y1": "1996",
             "VL": "85",
             "SP": "476",
             "EP": "481",
             "RP": "Not In File",
             "KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", "head trauma",
                    "hippocampus", "rat"],
             "N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the "
                   "hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe cortical damage and "
                   "neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown of the blood-brain barrier "
                   "(BBB) was assessed by injecting the protein horseradish peroxidase (HRP) 5 minutes prior to or at "
                   "various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and 10 days). Animals were "
                   "killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to "
                   "visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected "
                   "with HRP 5 minutes prior to or 5 minutes after cortical contusion. Staining at these time points "
                   "was observed in the ipsilateral hippocampus. Some modest staining occurred in the dorsal "
                   "contralateral cortex near the superior sagittal sinus. Cortical HRP stain gradually decreased at "
                   "increasing time intervals postinjury. By 10 days, no HRP stain was observed in any area of the "
                   "brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so "
                   "at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral "
                   "hippocampus 1 and 2 days following cortical contusion, indicating a biphasic opening of the BBB "
                   "following head trauma and a possible second wave of secondary brain damage days after the "
                   "contusion injury. These data indicate regions not initially destroyed by cortical impact, but "
                   "evidencing BBB breach, may be accessible to neurotrophic factors administered intravenously both "
                   "immediately and days after brain trauma."}]

def test_ris2011_ris_to_ris():
    """test process from a RIS 2001 bibliography to a RIS 2001 bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.ris'),
                       output_file=_output('test_ris2011_ris_to_ris.ris'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_ris_to_ris.ris'), encoding='utf-8') as s:
        content = s.read()
        assert content == """TY  - JOUR
A1  - Baldwin,S.A.
A1  - Fugaccia,I.
A1  - Brown,D.R.
A1  - Brown,L.V.
A1  - Scheff,S.W.
T1  - Blood-brain barrier breach following cortical contusion in the rat
JO  - J.Neurosurg.
Y1  - 1996
VL  - 85
SP  - 476
EP  - 481
RP  - Not In File
KW  - cortical contusion
KW  - blood-brain barrier
KW  - horseradish peroxidase
KW  - head trauma
KW  - hippocampus
KW  - rat
N2  - Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex above the hippocampus at 3.5 \
m/sec with a 2 mm cortical depression. This caused severe cortical damage and neuronal loss in hippocampus subfields \
CA1, CA3 and hilus. Breakdown of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish \
peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, 6, 12 hours, 1, 2, 5, and \
10 days). Animals were killed 1 hour after HRP injection and brain sections were reacted with diaminobenzidine to \
visualize extravascular accumulation of the protein. Maximum staining occurred in animals injected with HRP 5 minutes \
prior to or 5 minutes after cortical contusion. Staining at these time points was observed in the ipsilateral \
hippocampus. Some modest staining occurred in the dorsal contralateral cortex near the superior sagittal sinus. \
Cortical HRP stain gradually decreased at increasing time intervals postinjury. By 10 days, no HRP stain was observed \
in any area of the brain. In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so \
at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the ipsilateral hippocampus 1 and 2 \
days following cortical contusion, indicating a biphasic opening of the BBB following head trauma and a possible \
second wave of secondary brain damage days after the contusion injury. These data indicate regions not initially \
destroyed by cortical impact, but evidencing BBB breach, may be accessible to neurotrophic factors administered \
intravenously both immediately and days after brain trauma.
ER  - 
"""

def test_ris2011_ris_to_json():
    """test process from a RIS 2001 bibliography to a json bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('sample1.ris'),
                       output_file=_output('test_ris2011_ris_to_json.json'),
                       encoding='utf-8',
                       output_dir='.'))

    with open(_output('test_ris2011_ris_to_json.json'), encoding='utf-8') as s:
        content = s.read()
        assert content == ('[{"TY": "JOUR", '
                           '"A1": ["Baldwin,S.A.", "Fugaccia,I.", "Brown,D.R.", "Brown,L.V.", "Scheff,S.W."], '
                           '"T1": "Blood-brain barrier breach following cortical contusion in the rat", '
                           '"JO": "J.Neurosurg.", '
                           '"Y1": "1996", '
                           '"VL": "85", '
                           '"SP": "476", '
                           '"EP": "481", '
                           '"RP": "Not In File", '
                           '"KW": ["cortical contusion", "blood-brain barrier", "horseradish peroxidase", '
                           '"head trauma", "hippocampus", "rat"], '
                           '"N2": "Adult Fisher 344 rats were subjected to a unilateral impact to the dorsal cortex '
                           'above the hippocampus at 3.5 m/sec with a 2 mm cortical depression. This caused severe '
                           'cortical damage and neuronal loss in hippocampus subfields CA1, CA3 and hilus. Breakdown '
                           'of the blood-brain barrier (BBB) was assessed by injecting the protein horseradish '
                           'peroxidase (HRP) 5 minutes prior to or at various times following injury (5 minutes, 1, 2, '
                           '6, 12 hours, 1, 2, 5, and 10 days). Animals were killed 1 hour after HRP injection and '
                           'brain sections were reacted with diaminobenzidine to visualize extravascular accumulation '
                           'of the protein. Maximum staining occurred in animals injected with HRP 5 minutes prior to '
                           'or 5 minutes after cortical contusion. Staining at these time points was observed in the '
                           'ipsilateral hippocampus. Some modest staining occurred in the dorsal contralateral cortex '
                           'near the superior sagittal sinus. Cortical HRP stain gradually decreased at increasing '
                           'time intervals postinjury. By 10 days, no HRP stain was observed in any area of the brain. '
                           'In the ipsilateral hippocampus, HRP stain was absent by 3 hours postinjury and remained so '
                           'at the 6- and 12- hour time points. Surprisingly, HRP stain was again observed in the '
                           'ipsilateral hippocampus 1 and 2 days following cortical contusion, indicating a biphasic '
                           'opening of the BBB following head trauma and a possible second wave of secondary brain '
                           'damage days after the contusion injury. These data indicate regions not initially '
                           'destroyed by cortical impact, but evidencing BBB breach, may be accessible to '
                           'neurotrophic factors administered intravenously both immediately and days after brain '
                           'trauma."}]')

def test_ris2011_yml_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('mini.yml'),
                       output_file=_sibbling_module('test_ris2011_yml_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_ris2011_yml_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_ris2011_json_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('mini.json'),
                       output_file=_sibbling_module('test_ris2011_json_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_ris2011_json_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_ris2011_ris_to_py():
    """test process from a yml bibliography to a py source bibliography"""

    _process(Namespace(CMD='ris2011',
                       file=_ris2001_resource('mini.ris'),
                       output_file=_sibbling_module('test_ris2011_ris_to_py.py'),
                       encoding='utf-8',
                       output_dir='.'))

    time.sleep(1) # wait for the bibliography source file to be generated

    from test_ris2011_ris_to_py import IAU, NASA

    @cite(IAU, NASA)
    def bib_ref_foo():
        """ma doc avec plusieurs références en varargs"""

    if sys.version_info.minor >= 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * International Astronomical Union [iau]
    * NASA [nasa]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_process_ris2011

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * International Astronomical Union [iau]
    * NASA [nasa]
""")

def test_input_file_not_found():
    """test process input file not found"""

    with pytest.raises(FileNotFoundError) as e:
        with open(_ris2001_resource('not_existing_file.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
