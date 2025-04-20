from abc import ABCMeta, abstractmethod
from functools import reduce
from operator import add, sub, mul, truediv, floordiv
from typing import Callable, Iterable, Optional, Union, overload
import bisect
import xml.etree.ElementTree as ET
from feasytools.pq import PQueue

class TimeFunc(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self,time:int)->float: ...
    @abstractmethod
    def __str__(self)->str: ...
    def __add__(self,other:'FloatLike')->'TimeFunc':
        return calcFunc(self,other,'+')
    def __sub__(self,other:'TimeFunc')->'TimeFunc':
        return calcFunc(self,other,'-')
    def __mul__(self,other)->'TimeFunc':
        return calcFunc(self,other,'*')
    def __truediv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'/')
    def __floordiv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'//')

_oper_trans = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '//': floordiv
}
_Oper = Callable[[float,float],float]
FloatLike = Union[TimeFunc,float,int]

class OverrideFunc(TimeFunc):
    '''A function returning predefined values normally, and returning an alternative value if set.'''
    def __init__(self,default:TimeFunc,override_val:Optional[float] = None):
        self._val:TimeFunc=default
        self._override:Optional[float] = override_val
    
    def __call__(self,t:int)->float:
        if self._override is not None: return self._override
        return self._val(t)
    
    def setOverride(self,overval:float):
        '''Set the alternative value'''
        self._override=overval
    
    def clearOverride(self):
        '''Clear the alternative value'''
        self._override=None
    
    def __repr__(self):
        if self._override is None: return f"OverrideF<{self._val}>"
        return f"OverrideF<O={self._override}>"

    def __str__(self):
        if self._override is None: return str(self._val)
        return str(self._override)+"(Override)"

class PlusFunc(TimeFunc):
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)+self._f2(_t)
    def __repr__(self)->str: return f"PlusFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class QuickSumFunc(TimeFunc):
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return sum(f(_t) for f in self._fs)
    def __repr__(self)->str: return f"QuickSumFunc({self._fs})"
    def __str__(self)->str: return repr(self)

class MinusFunc(TimeFunc):
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)-self._f2(_t)
    def __repr__(self)->str: return f"MinusFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class MulFunc(TimeFunc):
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)*self._f2(_t)
    def __repr__(self)->str: return f"MulFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class QuickMulFunc(TimeFunc):
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return reduce(mul, (f(_t) for f in self._fs))
    def __repr__(self)->str: return f"QuickMulFunc({self._fs})"
    def __str__(self)->str: return repr(self)

class TrueDivFunc(TimeFunc):
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)/self._f2(_t)
    def __repr__(self)->str: return f"TrueDivFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class FloorDivFunc(TimeFunc):
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)//self._f2(_t)
    def __repr__(self)->str: return f"FloorDivFunc({self._f1},{self._f2})"
    def __str__(self)->str: return repr(self)

class ConstFunc(TimeFunc):
    def __init__(self,const:float): self._val:float=const
    def __call__(self,time:int)->float: return self._val
    def __repr__(self)->str: return f"ConstFunc({self._val})"
    def __str__(self)->str: return str(self._val)

class SegFunc(TimeFunc):
    '''Segmented const function'''
    _tl:'list[int]'
    _d:'list[float]'
    
    @overload
    def __init__(self,time_line:'list[int]', data:'list[float]'): ...
    @overload
    def __init__(self,time_line:'list[tuple[int,float]]'): ...
    @overload
    def __init__(self): ...

    def __init__(self,time_line:'Union[list[int],tuple[int,float]]'=[], data:'list[float]' = []):
        if len(data) == 0:
            self.__init1(time_line)
        else:
            self.__init0(time_line,data)
        self._rep = 1
        self._per = 0

    def __init0(self, time_line:'list[int]', data:'list[float]'):
        if len(time_line) != len(data):
            raise ValueError(f"Time line length {len(time_line)} is not equal to data length {len(data)}.")
        for i in range(1,len(time_line)):
            if time_line[i]<=time_line[i-1]:
                raise ValueError(f"Time must be strictly increasing: [{i}]={time_line[i]}<=[{i-1}]={time_line[i-1]}")
        self._tl = time_line
        self._d = data
    
    def __init1(self,time_line:'list[tuple[int,float]]'):
        self._tl = [t for t,_ in time_line]
        self._d = [d for _,d in time_line]
        for i in range(1,len(self._tl)):
            if self._tl[i]<=self._tl[i-1]:
                raise ValueError(f"Time must be strictly increasing: [{i}]={self._tl[i]}<=[{i-1}]={self._tl[i-1]}")
    
    def __len__(self)->int: return len(self._d)

    def __iter__(self): return zip(self._tl,self._d)

    def __call__(self,time:int)->float:
        if len(self._tl) == 0: return 0
        if time < self._tl[0]:
            raise ValueError(f"Time {time} must be later than the start time {self._tl[0]}.")
        return self._d[bisect.bisect_right(self._tl, time) - 1]
    
    def __repr__(self)->str:
        return f"SegFunc({[(t,d) for t,d in self]})"

    def __str__(self)->str:
        return str([(t,d) for t,d in self])
    
    def toXML(self, tag_name:str="seg", tag_item:str="item", 
               attr_time:str="time", attr_value:str="val",
               value_trans:Optional[Callable[[int, float],str]]=None) -> str:
        return ET.tostring(self.toXMLNode(tag_name,tag_item,attr_time,attr_value,value_trans), "unicode")
        
    def toXMLNode(self, tag_name:str="seg", tag_item:str="item", 
                    attr_time:str="time", attr_value:str="val",
                    value_trans:Optional[Callable[[int, float],str]]=None) -> ET.Element:
        e = ET.Element(tag_name)
        if self._per > 0:
            e.attrib["repeat"] = str(self._rep)
            e.attrib["period"] = str(self._per)
        for t, d in self:
            if t >= self._per: break
            if value_trans is not None:
                vs = value_trans(t, d)
            else:
                vs = str(d)
            e.append(ET.Element(tag_item,{attr_time:str(t),attr_value:vs}))
        return e
    
    def add(self, time:int, val:float):
        assert len(self._tl) == 0 or time > self._tl[-1]
        self._tl.append(time)
        self._d.append(val)
        self._rep = 1
        self._per = 0

    def repeat(self, times:int, period:int)->'SegFunc':
        if len(self._tl) == 0: return SegFunc()
        if times == 1: return SegFunc(self._tl,self._d)
        if times < 1: raise ValueError(f"times must be greater than 0, but got {times}.")
        if period <= self._tl[-1]: raise ValueError(f"period {period} must be greater than the last time {self._tl[-1]}.")
        ret = SegFunc()
        for i in range(times):
            for t,d in self:
                ret.add(t+i*period,d)
        ret._rep = times
        ret._per = period
        return ret
    
    @staticmethod
    def qs(v:'list[SegFunc]') -> 'SegFunc':
        ret = SegFunc()
        pq:'PQueue[tuple[int, int]]' = PQueue()
        sum = 0
        n = len(v)
        for i in range(n):
            if len(v[i]) > 0: pq.push(v[i]._tl[0], (i, 0))
        ctime = -1
        while not pq.empty():
            htime, (idx, prog) = pq.top
            pq.pop()
            if ctime != htime:
                if ctime >= 0:
                    ret.add(ctime, sum)
                ctime = htime
            if prog > 0:
                sum = sum - v[idx]._d[prog - 1] + v[idx]._d[prog]
            else:
                sum += v[idx]._d[prog]
            if prog < len(v[idx]) - 1:
                pq.push(v[idx]._tl[prog + 1], (idx, prog + 1))
        if len(ret._tl) == 0:
            ret.add(0, sum)
        elif ctime >= 0 and ctime != ret._tl[-1]:
            ret.add(ctime, sum)
        return ret
    
    def value_trans(self,func:Callable[[int, float],float])->'SegFunc':
        return SegFunc(self._tl,[func(t, d) for t, d in zip(self._tl,self._d)])

    def __neg__(self)->'SegFunc':
        return SegFunc(self._tl,[-d for d in self._d])
    
    def __add__(self,other:'FloatLike')->'SegFunc':
        if isinstance(other,(float,int)):
            return SegFunc(self._tl,[d + other for d in self._d])
        elif isinstance(other,ConstFunc):
            return SegFunc(self._tl,[d + other._val for d in self._d])
        elif isinstance(other,SegFunc):
            return SegFunc.qs([self, other])
        else:
            return PlusFunc(self, other)
    
    def __sub__(self,other:'FloatLike')->'SegFunc':
        if isinstance(other,(float,int)):
            return SegFunc(self._tl,[d - other for d in self._d])
        elif isinstance(other,ConstFunc):
            return SegFunc(self._tl,[d - other._val for d in self._d])
        elif isinstance(other,SegFunc):
            return SegFunc.qs([self, -other])
        else:
            return MinusFunc(self, other)


class TimeImplictFunc(TimeFunc):
    '''A special TimeFunc, whose value is only determined by when it is called. Parameter `time` in __call__ is ignored.'''
    def __init__(self,func:'Callable[[],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f()
    def __repr__(self)->str:return f"TimeImplictFunc({self._f})"
    def __str__(self)->str: return repr(self)


class ComFunc(TimeFunc):
    '''Wrap a Python function as a TimeFunc'''
    def __init__(self,func:'Callable[[int],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f(time)
    def __repr__(self)->str:return f"ComFunc({self._f})"
    def __str__(self)->str: return repr(self)


class ManualFunc(TimeFunc):
    '''A const function with a manually changeable value'''
    def __init__(self,init_val:float):self._v=init_val
    def setManual(self,val:float):self._v=val
    def __call__(self,time:int)->float:return self._v
    def __repr__(self)->str:return f"ManualFunc({self._v})"
    def __str__(self)->str: return str(self._v)+"(Manual)"

def __calc_c0(f1:Union[ConstFunc,float],f2:float,op:_Oper)->float:
    if isinstance(f1,float): return op(f1,f2)
    elif isinstance(f1,ConstFunc): return op(f1._val,f2)
    else: raise TypeError(f1)

def __calc_c1(f1:SegFunc,f2:float,op:_Oper)->SegFunc:
    return SegFunc(f1._tl,[op(d,f2) for d in f1._d])

def __calc_c2(f1:TimeImplictFunc,f2:float,op:_Oper)->TimeImplictFunc:
    return TimeImplictFunc(lambda: op(f1._f(),f2))

def quicksum(funcs:Iterable[TimeFunc])->TimeFunc:
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(0)
    consts = []
    segs = []
    others = []
    for f in ret:
        if isinstance(f,ConstFunc): consts.append(f._val)
        elif isinstance(f,SegFunc): segs.append(f)
        else: others.append(f)
    if len(others)==0:
        if len(segs)==0: return ConstFunc(sum(consts))
        else: return SegFunc.qs(segs) + sum(consts)
    if len(segs)==0 and len(consts)==0:
        return QuickSumFunc(others)
    elif len(segs)==0:
        others.append(ConstFunc(sum(consts)))
        return QuickSumFunc(others)
    elif len(consts)==0:
        others.append(SegFunc.qs(segs))
        return QuickSumFunc(others)
    else:
        s = SegFunc.qs(segs) + sum(consts)
        others.append(s)
        return QuickSumFunc(others)

def quickmul(funcs:Iterable[TimeFunc])->TimeFunc:
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(1)
    if len(ret)==1: return ret[0]
    if len(ret)==2: return MulFunc(ret[0],ret[1])
    return QuickMulFunc(ret)

def calcFunc(f1:FloatLike,f2:FloatLike,op:str)->TimeFunc:
    _op = _oper_trans[op]
    if isinstance(f2,ConstFunc): f2=f2._val
    if isinstance(f2,(float,int)):
        if isinstance(f1,(ConstFunc,float,int)): return ConstFunc(__calc_c0(f1,f2,_op))
        elif isinstance(f1,SegFunc): return __calc_c1(f1,f2,_op)
        elif isinstance(f1,TimeImplictFunc): return __calc_c2(f1,f2,_op)
        else: f2 = ConstFunc(f2)
    if isinstance(f1,(float,int)): f1 = ConstFunc(f1)
    if isinstance(f1,ConstFunc) and op in ['+','*']:
        if isinstance(f2,SegFunc): return __calc_c1(f2,f1._val,_op)
        elif isinstance(f2,TimeImplictFunc): return __calc_c2(f2,f1._val,_op)
    assert isinstance(f1,TimeFunc) and isinstance(f2,TimeFunc)
    if op=='+': return PlusFunc(f1,f2)
    elif op=='-': return MinusFunc(f1,f2)
    elif op=='*': return MulFunc(f1,f2)
    elif op=='/': return TrueDivFunc(f1,f2)
    elif op=='//': return FloorDivFunc(f1,f2)
    else: raise ValueError(op)

def makeFunc(time_line:'list[int]',data:list)->TimeFunc:
    '''Make SegFunc or ConstFunc from time_line and data'''
    if len(time_line)!=len(data):
        raise ValueError(f"Time line length {len(time_line)} is not equal to data length {len(data)}.")
    if len(data)==1: return ConstFunc(data[0])
    else: return SegFunc(time_line,data)
