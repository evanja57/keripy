# -*- encoding: utf-8 -*-
"""
KERI
keri.end package

ReST endpoints

"""

from ..kering import (OOBI_RE as OOBI_RE, DOOBI_RE as DOOBI_RE,
                      WOOBI_RE as WOOBI_RE,
                      OOBI_AID_HEADER as OOBI_AID_HEADER)
from .ending import (Signage, Inputage, signature,
                     designature, normalize, siginput,
                     desiginput, PointEnd, LocationEnd,
                     AdminEnd, OOBIEnd, loadEnds, setup,
                     Mimes, KeriMimes)
from .priming import parseArgs
