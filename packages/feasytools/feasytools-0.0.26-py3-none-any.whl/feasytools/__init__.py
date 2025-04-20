from .tfunc import FloatLike, quicksum, quickmul, calcFunc, makeFunc
from .tfunc import TimeFunc, OverrideFunc, ConstFunc, TimeImplictFunc, ComFunc, ManualFunc, SegFunc
from .tfunc import PlusFunc, QuickSumFunc, MinusFunc, MulFunc, QuickMulFunc, TrueDivFunc, FloorDivFunc
from .argchk import ArgChecker, KeyNotSpecifiedError, ArgumentWithoutKeyError
from .table import Table_DType, TableWriter, TableReader, createTableReader, createTableWriter, convertTableFile
from .table import FileTableWriter, FileTableReader, MemoryTableWriter, MemoryTableReader, SdtTableWriter, SdtTableReader
from .table import CsvTableWriter, CsvTableReader, BinTableWriter, BinTableReader, SdtGzTableWriter, SdtGzTableReader
from .table import ReadOnlyTable
from .pq import Heap, PQueue, BufferedPQ
from .rangelist import RangeList, RangeListAlwaysTrue, CreateRangeList
from .geo import Point, Seg, KDTree, EdgeFinder
from .pdf import *
from .perf import FEasyTimer

def time2str(tspan:float):
    tspan=round(tspan)
    s=tspan%60
    m=tspan//60%60
    h=tspan//3600
    return f"{h:02}:{m:02}:{s:02}"