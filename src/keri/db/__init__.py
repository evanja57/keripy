# -*- encoding: utf-8 -*-
"""
KERI
keri.db Package
"""
import sys

from . import koming, subing, webdbing
from .basebasing import BaserBase, statedict, onKey, snKey, dgKey, fetchTsgs
from .webdbing import WebDBer
from .koming import KomerBase, Komer, IoSetKomer, DupKomer
from .subing import (SuberBase, Suber, OnSuberBase, OnSuber,
                     B64SuberBase, B64Suber, CesrSuberBase, CesrSuber,
                     CesrOnSuber, CatCesrSuberBase, CatCesrSuber,
                     IoSetSuber, B64IoSetSuber, CesrIoSetSuber,
                     CatCesrIoSetSuber, SignerSuber, CryptSignerSuber,
                     SerderSuberBase, SerderSuber, SerderIoSetSuber,
                     SchemerSuber, DupSuber, CesrDupSuber,
                     CatCesrDupSuber, IoDupSuber, B64IoDupSuber,
                     OnIoDupSuber, B64OnIoDupSuber, OnIoSetSuber,
                     B64OnIoSetSuber)

IS_PYODIDE = "emscripten" in sys.platform

if not IS_PYODIDE:
    from . import basing, dbing, escrowing
    from .basing import Baser, BaserDoer, openDB, reopenDB
    from .dbing import (LMDBer, clearDatabaserDir, openLMDB,
                        fnKey, dtKey, splitKey, splitOnKey,
                        splitKeyDT, suffix, unsuffix,
                        splitKeyFN, SuffixSize, splitSnKey, MaxSuffix)
    from .escrowing import Broker
