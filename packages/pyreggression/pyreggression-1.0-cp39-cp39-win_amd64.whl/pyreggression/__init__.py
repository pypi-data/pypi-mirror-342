"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyreggression.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyreggression-1.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pyreggression-1.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

import atexit
from contextlib import contextmanager
from threading import Lock
from typing import Iterator, List
from io import StringIO
import tempfile
import csv
import os

import numpy as np
import pandas as pd

from ._binding import (
    unsafe_hs_pyreggression_version,
    unsafe_hs_pyreggression_main,
    unsafe_hs_pyreggression_run,
    unsafe_hs_pyreggression_init,
    unsafe_hs_pyreggression_exit,
)

VERSION: str = "1.0.0"


_hs_rts_init: bool = False
_hs_rts_lock: Lock = Lock()


def hs_rts_exit() -> None:
    global _hs_rts_lock
    with _hs_rts_lock:
        unsafe_hs_pyreggression_exit()


@contextmanager
def hs_rts_init(args: List[str] = []) -> Iterator[None]:
    global _hs_rts_init
    global _hs_rts_lock
    with _hs_rts_lock:
        if not _hs_rts_init:
            _hs_rts_init = True
            unsafe_hs_pyreggression_init(args)
            atexit.register(hs_rts_exit)
    yield None


def version() -> str:
    with hs_rts_init():
        return unsafe_hs_pyreggression_version()


def main(args: List[str] = []) -> int:
    with hs_rts_init(args):
        return unsafe_hs_pyreggression_main()

def pyreggression_run(myCmd : str, dataset : str, testData : str, loss : str, loadFrom : str, dumpTo : str, parseCSV : str, parseParams : int, calcDL : int) -> str:
    with hs_rts_init():
        return unsafe_hs_pyreggression_run(myCmd, dataset, testData, loss, loadFrom, dumpTo, parseCSV, parseParams, calcDL)

class PyReggression():
    def __init__(self, dataset, testData, loss, loadFrom, parseCSV, parseParams):
        self.dataset = dataset
        self.testData = testData
        self.loss = loss
        self.loadFrom = loadFrom
        self.parseCSV = parseCSV
        self.parseParams = int(parseParams)

        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, delete_on_close=False, suffix='.egraph')
        self.tempname = self.temp_file.name
        self.temp_file.close()
        print("Calculating DL...")
        pyreggression_run("top 10", self.dataset, self.testData, self.loss, self.loadFrom, self.tempname, self.parseCSV, self.parseParams, 1)
    def __del__(self):
        os.remove(self.tempname)
    def runQuery(self, query, df=True):
        csv_data = pyreggression_run(query, self.dataset, self.testData, self.loss, self.tempname, self.tempname, self.parseCSV, self.parseParams, 0)
        if df and len(csv_data) > 0:
            csv_io = StringIO(csv_data.strip())
            self.results = pd.read_csv(csv_io, header=0)
        else:
            self.results = pd.DataFrame() if df else csv_data
        return self.results

    def top(self, n, filters=[], criteria="by fitness", pattern="", isRoot=False, negate=False):
        filters_str = " ".join([f"with {f}" for f in filters])
        patmatch = f"{'not ' if negate else ''} matching {'root' if isRoot else ''} {pattern}" if len(pattern)>0 else ""
        query = f"top {n} {filters_str} {criteria} {patmatch}"
        return self.runQuery(query)

    def distribution(self, filters=[], limitedAt=25, dsc=True, byFitness=True, atLeast=1000, fromTop=5000):
        filters_str = " ".join([f"with {f}" for f in filters])
        query = f"distribution {filters_str} limited at {limitedAt} {'dsc' if dsc else 'asc'} {'by fitness' if byFitness else ''} with at least {atLeast} from top {fromTop}"
        return self.runQuery(query)
    def countPattern(self, pattern):
        query = f"count-pattern {pattern}"
        return self.runQuery(query, df=False)
    def report(self, n):
        return self.runQuery(f"report {n}")
    def optimize(self, n):
        return self.runQuery(f"optimize {n}")
    def subtrees(self, n):
        return self.runQuery(f"subtrees {n}")
    def insert(self, expr):
        return self.runQuery(f"insert {expr}")
    def pareto(self, byFitness=True):
        return self.runQuery(f"pareto {'by fitness' if byFitness else 'by dl'}")
    def save(self, fname):
        return self.runQuery(f"save {fname}", df=False)
    def load(self, fname):
        return self.runQuery(f"load {fname}", df=False)
