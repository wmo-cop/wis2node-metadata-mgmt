# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2024 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
from pathlib import Path
import sys

from pygeometa.core import read_mcf
from pygeometa.schemas.wmo_wcmp2 import WMOWCMP2OutputSchema
from pywcmp.wcmp2.ets import WMOCoreMetadataProfileTestSuite2

mcfs = Path.cwd()
mcfs = mcfs.glob('metadata/mcf/*.yml')

for mcf in mcfs:
    print(f'Processing {mcf}')

    print(' Converting MCF to WCMP2')
    mcf_object = read_mcf(mcf)
    record = WMOWCMP2OutputSchema().write(mcf_object, stringify=False)

    print(' Validating WCMP2')
    ts = WMOCoreMetadataProfileTestSuite2(record)
    ets_results = ts.run_tests()

    if ets_results['ets-report']['summary']['FAILED'] > 0:
        print(' WCMP2 ETS validation failure')
        print(json.dumps(ets_results, indent=4))
    else:
        print(' Metadata record passes WCMP2 validation')
