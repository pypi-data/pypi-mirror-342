from .grid import Grid
from .solbase import GridSolveResult, SolverBase
from .soldist import DistFlowSolver
from .soldss import OpenDSSSolver
from .solnt import NewtonSolver
from warnings import warn

class CombinedSolver(SolverBase):
    """
    A class that use DistFlowSolver to estimate the power flow and then use OpenDSSSolver or NewtonSolver to solve the power flow problem.
    """
    def __init__(self, g: Grid, estimator:str = 'distflow', calculator:str = 'opendss', mlrp:float = 0.5 ,source_bus:str = ""):
        assert estimator in ['distflow',], "Invalid estimator. Currently only 'distflow' is available."
        assert calculator in ['opendss', 'newton', 'none'], "Invalid solver type. Choose from 'opendss', 'newton' of 'none'."
        self.est = DistFlowSolver(g, mlrp = mlrp)
        self.cal_str = calculator
        if calculator == 'opendss':
            assert source_bus != "", "source_bus cannot be empty when using OpenDSSSolver."
            self.source_bus = source_bus
        else:
            if source_bus != "":
                warn(Warning("source_bus is ignored when not using OpenDSSSolver."))

    def solve(self, _t:int, /, *, timeout_s: float = 1):
        res, obj = self.est.solve(_t, timeout_s=timeout_s)
        if res == GridSolveResult.Failed:
            return res, obj
        if self.cal_str == 'none':
            return res, obj
        elif self.cal_str == 'opendss':
            solver = OpenDSSSolver(self.est.grid, self.source_bus)
        else:
            solver = NewtonSolver(self.est.grid)
        res, obj = solver.solve(_t, timeout_s=timeout_s)
        return res, obj