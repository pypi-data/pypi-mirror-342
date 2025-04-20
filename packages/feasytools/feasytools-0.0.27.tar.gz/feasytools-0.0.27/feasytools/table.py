import struct, gzip
from typing import (
    IO,
    BinaryIO,
    Dict,
    Generic,
    List,
    Optional,
    TextIO,
    Type,
    TypeVar,
    Union,
    Iterable,
    overload,
)
import numpy as np
from abc import abstractmethod, ABCMeta

Table_DType = Type[Union[np.int32, np.float32]]
_Table_DType = TypeVar("_Table_DType", np.int32, np.float32)


def _Lchk(L):
    assert L == "i" or L == "f"


def _dtypechk(dtype):
    assert dtype == np.int32 or dtype == np.float32


def _L2dtype(L) -> Type:
    return np.int32 if L == "i" else np.float32


def _dtype2L(dtype) -> str:
    return "i" if dtype == np.int32 else "f"


class TableWriter(metaclass=ABCMeta):
    """Abstract class for table writer"""

    @abstractmethod
    def __init__(self, col_names: "List[str]", dtype: Type) -> None:
        _dtypechk(dtype)
        self._col_names: "List[str]" = col_names
        self._dtype: Table_DType = dtype

    @property
    def col_num(self) -> int:
        """Column number"""
        return len(self._col_names)

    @property
    def dtype(self) -> Type:
        """Data type"""
        return self._dtype

    @abstractmethod
    def write(self, data: list) -> None:
        """Write one row, the length of data must be equal to the column number of this table"""

    @abstractmethod
    def write_all(self, data: np.ndarray) -> None:
        """Write multiple rows, the length of data (the number of columns in the ndarray) must be equal to the number of columns in this table"""

    @abstractmethod
    def close(self) -> None:
        """Close the writer"""


class FileTableWriter(TableWriter):
    """Abstract class for file table writer"""

    @abstractmethod
    def __init__(self, fh: IO, col_names: "List[str]", dtype: Type) -> None:
        super().__init__(col_names, dtype)
        self._fh = fh


class MemoryTableWriter(TableWriter):
    """Memory table writer"""

    _data: np.ndarray

    def __init__(self, col_names: "List[str]", dtype: Type) -> None:
        """
        Initialization
            col_names: column names
            dtype: data type, can be np.int32 or np.float32
        """
        super().__init__(col_names, dtype)
        self._data = np.zeros((0, len(col_names)), dtype=dtype)

    def write(self, data: list) -> None:
        self._data = np.vstack([self._data, np.array(data, dtype=self._dtype)])

    def write_all(self, data: np.ndarray) -> None:
        self._data = np.vstack([self._data, data])

    def close(self):
        pass

    @property
    def data(self) -> np.ndarray:
        """Get all the data written"""
        return self._data


class CsvTableWriter(FileTableWriter):
    """CSV Table Writer"""

    _fh: TextIO

    def __init__(self, fname: str, col_names: "List[str]", dtype: Type) -> None:
        """
        Initialization
            fname: file name
            col_names: column names
            dtype: data type, can be np.int32 or np.float32
        """
        super().__init__(open(fname, "w"), col_names, dtype)
        self._fh.write(",".join(self._col_names) + "\n")

    def write(self, data: list) -> None:
        self._fh.write(",".join(map(str, data)) + "\n")

    def write_all(self, data: np.ndarray) -> None:
        for ln in data:
            self.write(ln)

    def close(self):
        self._fh.close()


class BinTableWriter(FileTableWriter):
    """Abstract class for binary table writer"""

    _fh: IO

    @abstractmethod
    def __init__(self, fh, col_names: "List[str]", dtype: Type, buf_sz: int = 1024):
        super().__init__(fh, col_names, dtype)
        header = _dtype2L(dtype) + ("|".join(self._col_names))
        header += " " * ((4 - len(header) % 4) % 4)
        header = header.encode()
        self._fh.write(struct.pack("<I", len(header)))
        self._fh.write(header)
        self._buf = []
        self._buf_sz = buf_sz
        self._dcnt = 0

    def __wbuf(self):
        self._fh.write(np.stack(self._buf, dtype=self._dtype).tobytes())
        self._buf = []

    def write(self, data: list):
        self._buf.append(data)
        self._dcnt += 1
        if len(data) >= self._buf_sz:
            self.__wbuf()

    def write_all(self, data: np.ndarray):
        if data.dtype != self._dtype:
            data.astype(self._dtype)
        self._fh.write(data.tobytes())

    def close(self):
        if len(self._buf) > 0:
            self.__wbuf()
        self._fh.close()


class SdtTableWriter(BinTableWriter):
    """SDT Table Writer"""

    def __init__(
        self, fname: str, col_names: "List[str]", dtype: Type, buf_sz: int = 1024
    ):
        """
        Initialization
            fname: file name
            col_names: column names
            dtype: data type, can be np.int32 or np.float32
            buf_sz: buffer size, 1024 by default
        """
        super().__init__(open(fname, "wb"), col_names, dtype, buf_sz)


class SdtGzTableWriter(BinTableWriter):
    """SDT.GZ Table Writer"""

    def __init__(
        self, fname: str, col_names: "List[str]", dtype: Type, buf_sz: int = 1024
    ):
        """
        Initialization
            fname: file name
            col_names: column names
            dtype: data type, can be np.int32 or np.float32
            buf_sz: buffer size, 1024 by default
        """
        super().__init__(gzip.open(fname, "wb"), col_names, dtype, buf_sz)


class TableReader(metaclass=ABCMeta):
    """Abstract class for table reader"""

    @abstractmethod
    def __init__(self, col_names: "List[str]", dtype: Type) -> None:
        _dtypechk(dtype)
        self._col_names: "List[str]" = col_names
        self._col_cnt = len(self._col_names)
        self._cmap = {cn: i for i, cn in enumerate(self._col_names)}
        self._dtype: Type = dtype

    @property
    def head(self) -> "List[str]":
        """Header of the table"""
        return self._col_names

    @property
    def dtype(self) -> Type:
        """Data type of the table, can be np.int32 or np.float32"""
        return self._dtype

    @abstractmethod
    def read(self, cnt: int) -> np.ndarray:
        """Read cnt rows from current position"""

    @abstractmethod
    def read_all(self) -> np.ndarray:
        """Read all the data from the beginning"""

    @abstractmethod
    def close(self) -> None:
        """Close TableReader"""


class FileTableReader(TableReader):
    """Abstract class for file table reader"""

    @abstractmethod
    def __init__(self, f: IO, col_names: "List[str]", dtype: Type) -> None:
        super().__init__(col_names, dtype)
        self._fh: IO = f

    def close(self) -> None:
        self._fh.close()


class MemoryTableReader(TableReader):
    """Memory table reader"""

    _data: np.ndarray

    def __init__(self, col_names: "List[str]", data: np.ndarray):
        """
        Initialization
            col_names: column names
            data: data
        """
        super().__init__(col_names, data.dtype)
        self._data = data
        self.__pos = 0

    def read(self, cnt: int) -> np.ndarray:
        assert cnt > 0, "cnt must be positive"
        ed = cnt + self.__pos
        if ed > self._data.shape[0]:
            ed = self._data.shape[0]
        return self._data[self.__pos : ed]

    def read_all(self) -> np.ndarray:
        return self._data

    def close(self):
        pass


class BinTableReader(FileTableReader):
    """Abstract class for binary table reader"""

    _fh: BinaryIO

    @abstractmethod
    def __init__(self, fname: str, openFunc, allowNegativeSeek: bool = False) -> None:
        self.__fn = fname
        self._openF = openFunc
        fh: BinaryIO = self._openF(self.__fn, "rb")
        hlen = struct.unpack("<I", fh.read(4))[0]
        header = fh.read(hlen).decode()
        super().__init__(fh, header[1:].strip().split("|"), _L2dtype(header[0]))
        self._dstart = hlen + 4
        self._itmsz = self._col_cnt * 4
        self._neg = allowNegativeSeek

    def seek(self, row: int, col: int = 0) -> int:
        """Seek to the data at the row-th row and the col-th column, both row and col are 0-based"""
        dst = self._dstart + self._itmsz * row + 4 * col
        if self._neg or self._fh.tell() <= dst:
            return self._fh.seek(dst)
        else:
            self._fh.close()
            self._fh = self._openF(self.__fn, "rb")
            return self._fh.seek(dst)

    def read(self, cnt: int) -> Optional[np.ndarray]:
        data = self._fh.read(self._itmsz * cnt)
        if data == b"":
            return None
        return np.frombuffer(data, self._dtype).reshape(-1, self._col_cnt)

    def read_all(self) -> np.ndarray:
        self.seek(0, 0)
        return np.frombuffer(self._fh.read(), self._dtype).reshape(-1, self._col_cnt)

    def read_col(self, col_id: Union[int, str]) -> np.ndarray:
        """Read the col_id-th column. col_id can be index or column name"""
        if isinstance(col_id, str):
            col_id = self._cmap[col_id]
        i = 0
        dat = []
        while True:
            self.seek(i, col_id)
            d = self._fh.read(4)
            if d == b"":
                break
            dat.append(d)
            i += 1
        return np.frombuffer(b"".join(dat), dtype=self._dtype)

    def read_at(self, start: int, cnt: int) -> Optional[np.ndarray]:
        """Read range(start,start+cnt) rows"""
        self.seek(start)
        return self.read(cnt)


class SdtTableReader(BinTableReader):
    """SDT Table Reader"""

    def __init__(self, fname: str):
        """
        Initialization
            fname: file name
        """
        super().__init__(fname, open, True)


class SdtGzTableReader(BinTableReader):
    """SDT.GZ Table Reader"""

    def __init__(self, fname: str):
        """
        Initialization
            fname: file name
        """
        super().__init__(fname, gzip.open, False)


class CsvTableReader(FileTableReader):
    """CSV Table Reader"""

    _fh: TextIO

    def __init__(self, fname: str, dtype: Type) -> None:
        """
        Initialization
            fname: file name
            dtype: data type, can be np.int32 or np.float32
        """
        self.__fn = fname
        fh = open(fname, "r")
        super().__init__(fh, fh.readline().strip().split(","), dtype)

    def __parseline(self, ln: str) -> np.ndarray:
        strs = map(lambda x: x.strip(), ln.split(","))
        if self._dtype == np.int32:
            return np.array(list(map(int, strs)), dtype=np.int32)
        else:
            return np.array(list(map(float, strs)), dtype=np.float32)

    def __read1(self) -> Optional[np.ndarray]:
        """Read 1 row from the current position"""
        ln = self._fh.readline().strip()
        if ln == "":
            return None
        return self.__parseline(ln)

    def read(self, cnt: int) -> Optional[np.ndarray]:
        if cnt == 1:
            return self.__read1()
        ret = []
        for _ in range(cnt):
            dat = self.__read1()
            if dat is None:
                break
            ret.append(dat)
        if len(ret) == 0:
            return None
        return np.stack(ret)

    def read_all(self) -> np.ndarray:
        self._fh.close()
        self._fh = open(self.__fn, "r")
        self._fh.readline()
        return np.stack([self.__parseline(x) for x in self._fh.readlines()])


def createTableReader(fname: str, dtype: Optional[Type] = None) -> TableReader:
    """Create TableReader from file name, dtype is required for CSV file"""
    fn = fname.lower()
    if fn.endswith(".csv"):
        assert dtype is not None
        return CsvTableReader(fname, dtype)
    elif fn.endswith(".sdt"):
        return SdtTableReader(fname)
    elif fn.endswith(".sdt.gz"):
        return SdtGzTableReader(fname)
    else:
        raise ValueError("Unsupported file type. Only support csv, sdt and sdt.gz")


def createTableWriter(fname: str, cols: "List[str]", dtype: Type) -> TableWriter:
    """Create TableWriter from file name"""
    fn = fname.lower()
    if fn.endswith(".csv"):
        return CsvTableWriter(fname, cols, dtype)
    elif fn.endswith(".sdt"):
        return SdtTableWriter(fname, cols, dtype)
    elif fn.endswith(".sdt.gz"):
        return SdtGzTableWriter(fname, cols, dtype)
    elif fn.endswith("<mem>"):
        return MemoryTableWriter(cols, dtype)
    else:
        raise ValueError(
            "Unsupported file type. Only support csv, sdt, sdt.gz, and <mem>"
        )


def _convbinfile(
    r: Union[BinaryIO, gzip.GzipFile],
    w: Union[BinaryIO, gzip.GzipFile],
    bufsz: int = 1024 * 1024 * 64,
):
    while True:
        data = r.read(bufsz)
        if data == b"":
            break
        w.write(data)
    r.close()
    w.close()


def convertTableFile(
    rfile: str, wfile: str, dtype: Optional[Type] = None, bufsz: int = 1024
) -> None:
    """Convert a table of one file type to another file type, if the input file is a CSV file, dtype needs to be specified"""
    if rfile.lower().endswith(".sdt.gz") and wfile.lower().endswith(".sdt"):
        _convbinfile(gzip.open(rfile, "rb"), open(wfile, "wb"))
        return
    elif rfile.lower().endswith(".gz") and wfile.lower().endswith(".sdt.gz"):
        _convbinfile(open(rfile, "rb"), gzip.open(wfile, "wb"))
        return
    r = createTableReader(rfile, dtype)
    w = createTableWriter(wfile, r.head, r.dtype)
    while True:
        data = r.read(bufsz)
        if data is None:
            break
        w.write_all(data)
    r.close()
    w.close()


class ReadOnlyTable(Generic[_Table_DType]):
    """
    Read-only data table, all data in the table must be of the same type, either 32-bit int or float.
    The content of a row is directly obtained by subscripting; the content of a column is obtained by the col method.
    Since it is a read-only list, it must be loaded from a file. Supported file types include csv, sdt, and sdt.gz.
    """

    _d: "Optional[np.ndarray[tuple[int,int],np.dtype[_Table_DType]]]"
    _btr: TableReader

    @overload
    def __init__(self, source: MemoryTableReader):
        """Initialize using MemoryTableReader"""

    @overload
    def __init__(self, source: MemoryTableWriter):
        """Initialize using MemoryTableWriter"""

    @overload
    def __init__(
        self, source: str, dtype: Optional[Table_DType] = None, preload: bool = False
    ):
        """
        Initialization
            fname: file name of the table, only support csv, sdt and sdt.gz files.
            dtype: data type, can be np.int32 or np.float32. Only required for csv files.
            preload: whether to preload all data
        Attention:
            Preloading greatly reduces the initialization speed, but greatly improves the runtime performance.
            Csv files force preloading, sdt and sdt.gz files are optional (recommended to turn off sdt.gz and turn on sdt).
            If the data is too large and the memory is insufficient, do not use the preloading function.
        """

    def __init__(
        self,
        source: Union[str, MemoryTableWriter, MemoryTableReader],
        dtype: Optional[Table_DType] = None,
        preload: bool = False,
    ):
        if isinstance(source, str):
            self._btr = createTableReader(source, dtype)
            fn = source.lower()
            if preload or fn.lower().endswith(".csv"):
                self._d = self._btr.read_all()
            else:
                self._d = None
        elif isinstance(source, MemoryTableReader):
            self._btr = source
            self._d = source._data
        elif isinstance(source, MemoryTableWriter):
            self._btr = MemoryTableReader(source._col_names, source._data)
            self._d = source._data

    @property
    def head(self) -> "List[str]":
        """Header of the table"""
        return self._btr._col_names

    @property
    def dtype(self) -> Table_DType:
        """Data type of the table, can be np.int32 or np.float32"""
        return self._btr._dtype

    @property
    def data(self) -> "np.ndarray[(int,int),np.dtype[_Table_DType]]":
        """Data of the table. If all data is not preloaded, this will load all data."""
        if self._d is None:
            self._d = self._btr.read_all()
        return self._d

    def force_load_all(self):
        self._d = self._btr.read_all()

    @overload
    def col(self, c: str) -> "np.ndarray[int,np.dtype[_Table_DType]]":
        """Get the column named c"""

    @overload
    def col(self, c: int) -> "np.ndarray[int,np.dtype[_Table_DType]]":
        """Get the c-th column"""

    @overload
    def col(
        self, c: Iterable[Union[str, int]]
    ) -> "np.ndarray[int,np.dtype[_Table_DType]]":
        """Get multiple columns by name or index"""

    def col(
        self, c: Union[Iterable[Union[str, int]], str, int]
    ) -> "np.ndarray[int,np.dtype[_Table_DType]]":
        if isinstance(c, int) or isinstance(c, str):
            if self._d is None:
                assert isinstance(self._btr, BinTableReader)
                return self._btr.read_col(c)
            else:
                if isinstance(c, str):
                    c = self._btr._cmap[c]
                return self._d[:, c]
        elif isinstance(c, Iterable):
            nc: List[int] = [self._btr._cmap[x] if isinstance(x, str) else x for x in c]
            return self.data[:, nc]
        else:
            raise TypeError(
                "Unsupported type. Only str, int and Iterable[str|int] are supported."
            )

    def row(self, row_id: int) -> "Optional[np.ndarray[int,np.dtype[_Table_DType]]]":
        """Get the row with index row_id"""
        if self._d is not None:
            return self._d[row_id]
        assert isinstance(self._btr, BinTableReader)
        return self._btr.read_at(row_id, 1)

    def at(self, col_name: str, row_id: int) -> _Table_DType:
        """Get the data at the row with index row_id and the column named col_name"""
        return self.data[self._btr._cmap[col_name], row_id]

    def __getitem__(
        self, indices
    ) -> "Union[np.ndarray[tuple[int,...],np.dtype[_Table_DType]],_Table_DType]":
        """Get item by indices, only support numerical indices"""
        return self.data[indices]

    def save(self, path: str):
        """
        Save to .csv or .bin.gz file
            path: file path
        """
        if self._d is None:
            self._d = self._btr.read_all()
        fn = path.lower()
        if fn.endswith(".csv"):
            CsvTableWriter(path, self.head, self.dtype).write_all(self._d)
        elif fn.endswith(".sdt"):
            SdtTableWriter(path, self.head, self.dtype).write_all(self._d)
        elif fn.endswith(".sdt.gz"):
            SdtGzTableWriter(path, self.head, self.dtype).write_all(self._d)
        else:
            raise ValueError("Unsupported file type. Only support csv, sdt and sdt.gz")

    def to_dict_of_list(self) -> "Dict[str,List[_Table_DType]]":
        """Convert the table to a dictionary of lists"""
        if self._d is None:
            self._d = self._btr.read_all()
        ret = {}
        for i, h in enumerate(self.head):
            ret[h] = self._d[:, i].tolist()
        return ret

    def to_list_of_dict(self) -> "List[Dict[str,_Table_DType]]":
        """Convert the table to a list of dictionaries"""
        if self._d is None:
            self._d = self._btr.read_all()
        ret = []
        for r in self._d:
            ret.append({h: r[i] for i, h in enumerate(self.head)})
        return ret

    def __str__(self):
        return ",".join(self.head) + "\n" + super().__str__()
