from .grid import Grid
from .solbase import DEFAULT_SAVETO, GridSolveResult, SolverBase
from warnings import warn

ESTIMATORS = ['distflow']
CALCULATORS = ['opendss', 'newton', 'gridcal', 'none']
CALCULATORS_NEED_SOURCE_BUS = ['opendss', 'gridcal']

class CombinedSolver(SolverBase):
    """
    A class that use DistFlowSolver to estimate the power flow and then use OpenDSSSolver or NewtonSolver to solve the power flow problem.
    """
    def __init__(self, grid:Grid, eps:float = 1e-6, max_iter:int = 1000, *, 
            default_saveto:str = DEFAULT_SAVETO, estimator:str = 'distflow', 
            calculator:str = 'newton', mlrp:float = 0.5 ,source_bus:str = ""):
        super().__init__(grid, eps, max_iter, default_saveto = default_saveto)
        assert estimator in ESTIMATORS, f"Invalid estimator '{estimator}'. Choose from: " + ','.join(ESTIMATORS) + "."
        assert calculator in CALCULATORS, f"Invalid solver type '{calculator}'. Choose from: " + ','.join(CALCULATORS) + "."

        from .soldist import DistFlowSolver
        self.est = DistFlowSolver(grid, mlrp = mlrp)
        self.cal_str = calculator
        if calculator in CALCULATORS_NEED_SOURCE_BUS:
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
            from .soldss import OpenDSSSolver
            solver = OpenDSSSolver(self.est.grid, source_bus = self.source_bus)
        elif self.cal_str == 'gridcal':
            from .solgcal import GridCalSolver
            solver = GridCalSolver(self.est.grid, slack_bus = self.source_bus)
        else:
            from .solnt import NewtonSolver
            solver = NewtonSolver(self.est.grid)
        res, obj = solver.solve(_t, timeout_s = timeout_s)
        return res, obj