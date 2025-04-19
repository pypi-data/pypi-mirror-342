# Bibliograpy

Bibliography management to decorate source code.

[![example workflow](https://github.com/SamuelAndresPascal/cosmoloj-py/actions/workflows/bibliograpy.yml/badge.svg)](https://github.com/SamuelAndresPascal/cosmoloj-py/actions)

[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/version.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_relative_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/platforms.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/license.svg)](https://anaconda.org/cosmoloj/bibliograpy)

[![PyPI repository Badge](https://badge.fury.io/py/bibliograpy.svg)](https://badge.fury.io/py/bibliograpy)


* [Preprocessing tool](#preprocessing-tool)
  * [Supported formats and syntaxes](#supported-formats-and-syntaxes)
    * [Bibtex bibliographies](#supported-syntaxes-for-bibtex-bibliographies)
    * [RIS bibliographies](#supported-syntaxes-for-ris-2001--ris-2011-bibliographies)
    * [refer bibliographies](#supported-syntaxes-for-refer-bibliographies)
  * [Processing bibliographies](#processing-bibliographies)
  * [Cross-referencing for Bibtex format](#cross-referencing-support-bibtex-format)
* [API](#api--documentation-library)
* [Documentation](#documentation)




Bibliograpy allows to manage bibliographic centralized references.

1. **Re-use bibliographic standards.** As an *executable tool*, it 
generates python bibliography modules mapping bibliographic files to python constant representations. 

2. **Make bibliographic references easy to use and to maintain.** As an *API*, it allows to decorate functions, classes
and methods in the source code, referencing the centralized python constant bibliographies, defined only once and for 
all.

3. **Transparently inject bibliographic references in docstrings.** As an *underlying documentation library*, it 
supplements the docstring of decorated elements with bibliographical information.


## Preprocessing tool

The `bibliograpy` tool allows generating a source code bibliograpy from a resource bibliography file.

### Supported formats and syntaxes

`bibliograpy` supports bibliography files in `Bibtex`, `RIS (2001)`, `RIS (2011)` or `refer` formats.

Each format can be expressed in its own syntax or using an equivalent representation in `YAML` or `JSON`.

#### Supported syntaxes for Bibtex bibliographies

For instance, let us consider a `Bibtex` bibliography expressed in the `Bibtex` proper syntax:

```bibtex
@misc{nasa
  title = {NASA}
}

@misc{iau,
  title = {International Astronomical Union}
 }
```

But it can also be expressed in `YAML`:

```yml
- entry_type: misc
  cite_key: nasa
  title: NASA
- entry_type: misc
  cite_key: iau
  title: International Astronomical Union
```

Or in `JSON`:

```json
[
  {
    "entry_type": "misc",
    "cite_key": "nasa",
    "title": "NASA"
  },
  {
    "entry_type": "misc",
    "cite_key": "iau",
    "title": "International Astronomical Union"
  }
]
```

Note the `entry_type` and `cite_key` fields used in `YAML`/`JSON` to map the `Bibtex` entry type and cite key values.

####  Supported syntaxes for RIS (2001) / RIS (2011) bibliographies

Let us consider now an equivalent of the previous bibliography, now given in `RIS (2001)` / `RIS (2011)` format:

```ris
TY  - GEN
ID  - nasa
T1  - NASA
ER  -
TY  - GEN
ID  - iau
T1  - International Astronomical Union
ER  -
```

The `bibliograpy` tool supports a `RIS (2001)` / `RIS (2011)` bibliography to be expressed using 
equivalent `YAML` or `JSON` syntaxes, respectively:

```yaml
- TY: GEN
  ID: nasa
  T1: NASA
- TY: GEN
  ID: iau
  T1: International Astronomical Union
```

```json
[
  {
    "TY": "GEN",
    "ID": "nasa",
    "T1": "NASA"
  },
  {
    "TY": "GEN",
    "ID": "iau",
    "T1": "International Astronomical Union"
  }
]
```

**Note that an `ID` field is mandatory for each entry to be processed into a python value.**

####  Supported syntaxes for refer bibliographies

Let us consider now an equivalent of the previous bibliography, now given in `refer` format:

```refer
%X institution
%L nasa
%T NASA

%X institution
%L iau
%T International Astronomical Union

```

The `bibliograpy` tool supports a `refer` bibliography to be expressed using 
equivalent `YAML` or `JSON` syntaxes, respectively:

```yaml
- X: institution
  L: nasa
  T: NASA
- X: institution
  L: iau
  T: International Astronomical Union
```

```json
[
  {
    "X": "institution",
    "L": "nasa",
    "T": "NASA"
  },
  {
    "X": "institution",
    "L": "iau",
    "T": "International Astronomical Union"
  }
]
```

**Note that an `L` (label) field is mandatory for each entry to be processed into a python value.**

### Processing bibliographies

A bibliography file can be preprocessed by the `bibliograpy` tool to produces bibliography python modules.

For instance, there is the python processing result of the previous `Bibtex` bibliography sample:

```py
from bibliograpy.api_bibtex import Misc

NASA = Misc.generic(cite_key='nasa',
                    title='NASA')

IAU = Misc.generic(cite_key='iau',
                   title='International Astronomical Union')
```

There is the processing result of the `RIS (2001)` / `RIS (2011)` one:

```py
from bibliograpy.api_ris2001 import *

NASA = {
    Tags.TY: TypeFieldName.GEN,
    Tags.ID: 'nasa',
    Tags.T1: 'NASA'
}

IAU = {
    Tags.TY: TypeFieldName.GEN,
    Tags.ID: 'iau',
    Tags.T1: 'International Astronomical Union'
}
```

And there is the processing result of the `refer` one:

```py
from bibliograpy.api_refer import *

NASA = {
    Tags.X: 'institution',
    Tags.L: 'nasa',
    Tags.T: 'NASA'
}

IAU = {
    Tags.X: 'institution',
    Tags.L: 'iau',
    Tags.T: 'International Astronomical Union'
}
```

By default, the `bibliograpy` tool searches for a `bibliograpy.yaml` file reproducing the `Bibtex` format.

```shell
bibliograpy bibtex
```

Is equivalent to:

```shell
bibliograpy bibtex bibliograpy.yaml
```

Note the *format* syntax is inferred from the bibliography file extension.

Moreover, *for a given format*, the `bibliograpy` tool allow to convert a bibliography file from one of the 
`JSON`, `YAML` and standard syntaxes to another one. **It does not convert a format to another one.**

### Cross-referencing support (Bibtex format)

The `bibliograpy` tool support the cross-referencing/inheritance mechanism specified by the `Bibtex` format.

Example, from a bibtex bibliography (`bibliograpy.bib`):

```
@misc{ogc,
 institution = {OGC},
 title = {Open Geospatial Consortium}
}

@misc{zeitschrift_fur_vermessungswesen,
 journal = {Zeitschrift für Vermessungswesen},
 title = {Zeitschrift für Vermessungswesen}
}

@techreport{cts_revision_v1_0,
 author = {},
 crossref = {ogc},
 month = {January},
 number = {OGC 01-009},
 title = {Coordinate Transformation Services},
 type = {standard},
 year = {2001}
}

@article{joachim_boljen_2004,
 author = {},
 crossref = {zeitschrift_fur_vermessungswesen},
 pages = {258-260},
 title = {Zur geometrischen Interpretation und direkten Bestimmung von Formfunktionen},
 volume = {129},
 year = {2004}
}
```

```shell
bibliograpy bibtex bibliograpy.bib
```

When processed, the bibliography produces python constants to import in the code which uses the very 
bibliographical references as cross-references from other ones.

```python
from bibliograpy.api_bibtex import *


OGC = Misc.generic(cite_key='ogc',
                   institution='OGC',
                   title='Open Geospatial Consortium')

ZEITSCHRIFT_FUR_VERMESSUNGSWESEN = Misc.generic(cite_key='zeitschrift_fur_vermessungswesen',
                                                journal='Zeitschrift für Vermessungswesen',
                                                title='Zeitschrift für Vermessungswesen',
                                                non_standard=NonStandard(issn='0044-3689'))

CTS_REVISION_V1_0 = TechReport.generic(cite_key='cts_revision_v1_0',
                                       author='',
                                       crossref=OGC,
                                       month='January',
                                       number='OGC 01-009',
                                       title='Coordinate Transformation Services',
                                       type='standard',
                                       year=2001,
                                       non_standard=NonStandard(url='https://portal.ogc.org/files/?artifact_id=999'))

JOACHIM_BOLJEN_2004 = Article.generic(cite_key='joachim_boljen_2004',
                                      author='',
                                      crossref=ZEITSCHRIFT_FUR_VERMESSUNGSWESEN,
                                      pages='258-260',
                                      title='Zur geometrischen Interpretation und direkten Bestimmung von Formfunktionen',
                                      volume='129',
                                      year=2004,
                                      non_standard=NonStandard(url='https://geodaesie.info/system/files/privat/zfv_2004_4_Boljen.pdf'))
```

Nevertheless, to be *actually* cross-resolved by the underlying Bibliograpy library, all the references *must* use a 
scope which have to be named and initialized through respectively `--scope` and `--init-scope` options.

```shell
bibliograpy bibtex --scope=_SCOPE --init-scope="{}" bibliograpy.bib
```

```python
from bibliograpy.api_bibtex import *

_SCOPE = {}


OGC = Misc.generic(cite_key='ogc',
                   institution='OGC',
                   title='Open Geospatial Consortium',
                   scope=_SCOPE)

ZEITSCHRIFT_FUR_VERMESSUNGSWESEN = Misc.generic(cite_key='zeitschrift_fur_vermessungswesen',
                                                journal='Zeitschrift für Vermessungswesen',
                                                title='Zeitschrift für Vermessungswesen',
                                                non_standard=NonStandard(issn='0044-3689'),
                                                scope=_SCOPE)

CTS_REVISION_V1_0 = TechReport.generic(cite_key='cts_revision_v1_0',
                                       author='',
                                       crossref=OGC,
                                       month='January',
                                       number='OGC 01-009',
                                       title='Coordinate Transformation Services',
                                       type='standard',
                                       year=2001,
                                       non_standard=NonStandard(url='https://portal.ogc.org/files/?artifact_id=999'),
                                       scope=_SCOPE)

JOACHIM_BOLJEN_2004 = Article.generic(cite_key='joachim_boljen_2004',
                                      author='',
                                      crossref=ZEITSCHRIFT_FUR_VERMESSUNGSWESEN,
                                      pages='258-260',
                                      title='Zur geometrischen Interpretation und direkten Bestimmung von Formfunktionen',
                                      volume='129',
                                      year=2004,
                                      non_standard=NonStandard(url='https://geodaesie.info/system/files/privat/zfv_2004_4_Boljen.pdf'),
                                      scope=_SCOPE)
```

A default `SHARED_SCOPE` shared scope is provided by the `bibliograpy.api_bibtex` module. If this name is supplied to
the `--scope` option, no initialization is necessary (unless the user wants to shadow the common `SHARED_SCOPE`).

## API / Documentation library

Hence, is it possible to factorize all bibliographic sources contained in a bibliography file as variables in a python 
module. 

Then, the Bibliograpy API allows using them as arguments of decorators.



```py
"""The bibliography module."""

from bibliograpy.api_bibtex import TechReport

IAU_2006_B1 = TechReport.generic(
    cite_key='iau_2006_b1',
    author='',
    institution='iau',
    title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
    year=2006)
```

```py
"""The bibliography_client module using the bibliography module."""

from bibliograpy.api_common import cite

from bibliography import IAU_2006_B1

@cite(IAU_2006_B1)
def my_function():
    """My my_function documentation."""
    return "Hello IAU !"

```

The usage of the decorator has two purposes.

First, to use a bibliographic reference defined once and for all, centralized and reusable, easy to maintain, update,
refactor and search for usage.

Second, to implicitly add to the documentation of the decorated entities a bibliographical section.

```shell
import bibliography_client

>>> help(my_function)
Help on function my_function in module bibliography_client

my_function()
    My my_function documentation.

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
```

## Documentation

[Latest release](https://cosmoloj.com/mkdocs/bibliograpy/latest/)

[Trunk](https://cosmoloj.com/mkdocs/bibliograpy/master/)