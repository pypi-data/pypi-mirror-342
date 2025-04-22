from itertools import chain
import cvxpy as cp
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass
from collections import deque
import math
from .solbase import *

Var = cp.Variable
VF = Union[Var, float]

@dataclass
class LoadReduceModule:
    '''Load Reduce module'''
    Bus: BusID
    Limit: TimeFunc
    Reduction: FloatVar = None

class _Island:
    def __init__(self, g: Grid, buses: Iterable[BusID], cutlines: set[LineID]):
        self.grid = g
        self.Buses: set[str] = set()
        self.Gens: set[str] = set()
        self.Lines: set[str] = set()
        self.PVWs: set[str] = set()
        self.ESSs: set[str] = set()
        for b in buses:
            self.Buses.add(b)
            self.Gens.update(gen.ID for gen in g._gatb[b])
            self.Lines.update(ln.ID for ln in g._ladjfb[b] if ln.ID not in cutlines)
            self.Lines.update(ln.ID for ln in g._ladjtb[b] if ln.ID not in cutlines)
            self.PVWs.update(p.ID for p in g._patb[b])
            self.ESSs.update(e.ID for e in g._eatb[b])
    
    def __repr__(self):
        return f"Island: {self.Buses}\nGens: {self.Gens}\nLines: {self.Lines}\nPVWs: {self.PVWs}\nESSs: {self.ESSs}"
    
    def __str__(self):
        return self.__repr__()
    
    def BusItems(self):
        for b in self.Buses:
            yield b, self.grid.Bus(b)
    
    def GenItems(self):
        for g in self.Gens:
            yield g, self.grid.Gen(g)
    
    def LineItems(self):
        for l in self.Lines:
            yield l, self.grid.Line(l)
    
    def PVWItems(self):
        for p in self.PVWs:
            yield p, self.grid.PVWind(p)
    
    def ESSItems(self):
        for e in self.ESSs:
            yield e, self.grid.ESS(e)

class IslandResult(IntEnum):
    Undefined = -1
    OK = 0          # The island is solved without overflow
    OverFlow = 1    # The island is solved but overflow
    Failed = 2      # No island is solved

class DistFlowSolver(SolverBase):
    '''DistFlow solver'''
    def __init__(self, grid: Grid, eps: float = 1e-6, default_saveto: str = DEFAULT_SAVETO, /,
             *, mlrp: float = 0.5, secondary_cost: bool = True):
        '''
        Initialize
            grid: Grid object
            default_saveto: Default path to save the results
            mlrp: Maximum proportion of load reduction
            secondary_cost: Whether to include the secondary cost. 
                If False, the cost is calculated as CostB * Pg + CostC;
                If True, the cost is calculated as CostA * Pg^2 + CostB * Pg + CostC,
                    which is likely to induce numerical instability.
        '''
        super().__init__(grid, eps, default_saveto)
        self._decb: dict[BusID, LoadReduceModule] = {}
        self.C = 1e9
        self._mlrp = mlrp
        self._oflines: set[LineID] = set()
        self._ofbuses: set[BusID] = set()
        self._sec_cost = secondary_cost
        self.UpdateGrid()        
    
    @property
    def OverflowLines(self):
        return self._oflines
    
    @property
    def OverflowBuses(self):
        return self._ofbuses
    
    def UpdateGrid(self, cut_overflow_lines: bool = False):
        self._islands = tuple(
            _Island(self.grid, il, self._oflines) for il in self.__detect_islands(cut_overflow_lines)
        )
        self._island_res = [(IslandResult.Undefined, -1.0) for _ in range(len(self._islands))]
        self.__il_relax = [False] * len(self._islands)
    
    def __detect_islands(self, cutofl: bool):
        '''Detect islands'''
        q: deque[BusID] = deque()
        visited: set[BusID] = set()
        islands: list[set[BusID]] = []
        for bus in self.grid.BusNames:
            if bus in visited: continue
            q.append(bus)
            island: set[BusID] = set()
            while len(q) > 0:
                b = q.popleft()
                if b in visited: continue
                visited.add(b)
                island.add(b)
                for line in self.grid._ladjfb[b]:
                    if cutofl and line.ID in self._oflines: continue
                    if line._tBus in visited: continue
                    q.append(line._tBus)
                for line in self.grid._ladjtb[b]:
                    if cutofl and line.ID in self._oflines: continue
                    if line._fBus in visited: continue
                    q.append(line._fBus)
            islands.append(island)
        return islands
    
    @property
    def Islands(self):
        return self._islands
    
    @property
    def IslandResults(self):
        return self._island_res
    
    @property
    def MLRP(self):
        '''Get the maximum load reduction proportion'''
        return self._mlrp
    @MLRP.setter
    def MLRP(self, v: float):
        '''Set the maximum load reduction proportion'''
        if v < 0 or v > 1:
            raise ValueError("Invalid maximum load reduction proportion")
        self._mlrp = v
    
    def AddReduce(self, bus: BusID, limit: TimeFunc, reduction: Optional[FloatVar] = None):
        '''Add a load reduction module'''
        self._decb[bus] = LoadReduceModule(bus, limit, reduction)
    
    def RemoveReduce(self, bus: BusID):
        '''Remove a load reduction module'''
        if bus in self._decb:
            del self._decb[bus]
        
    def GetReduce(self, bus: BusID) -> LoadReduceModule:
        '''Get the load reduction module'''
        return self._decb[bus]
    
    @property
    def DecBuses(self):
        return self._decb
    
    def solve(self, _t: int, /, *, timeout_s: float = 1) -> 'tuple[GridSolveResult, float]':
        '''Get the best result at time _t, return a tuple: (result status, optimal objective value)'''
        allOK = True
        allFail = True
        val = 0
        for i, il in enumerate(self._islands):
            relax = self.__il_relax[i]
            self._island_res[i] = self.__solve(_t, il, timeout_s, relax, relax)
            if self._island_res[i][0] == IslandResult.Failed:
                self.__il_relax[i] = True
                self._island_res[i] = self.__solve(_t, il, timeout_s, True, True)
            if self._island_res[i][0] != IslandResult.Failed:
                allFail = False
                val += self._island_res[i][1]
            if self._island_res[i][0] != IslandResult.OK: allOK = False
            if self._island_res[i][0] == IslandResult.OverFlow: self.__il_relax[i] = False
        if allOK:
            return GridSolveResult.OK, val
        elif allFail:
            print(f"Failed to solve at time {_t}")
            if self.saveto != "":
                p = Path(self.saveto)
                p.mkdir(parents=True, exist_ok=True)
                self.grid.savePQofBus(str(p/f"{_t}_load.csv"), _t)
            return GridSolveResult.Failed, val
        else:
            return GridSolveResult.PartialOK, val
    
    def __chkv(self, d: Union[None, np.ndarray]) -> float:
        assert d is not None, "Value is None"
        assert isinstance(d, (np.ndarray, np.float64, float)), f"Value is {type(d)}"
        ret = d.item()
        assert isinstance(ret, float), f"Value is not a float: {type(ret)}"
        assert ret != float('inf'), "Value is inf"
        assert ret != float('-inf'), "Value is -inf"
        return ret

    def __solve(self, _t: int, island: _Island, timeout_s: float, relaxV: bool, relaxI: bool, clear_results: bool = False) -> 'tuple[IslandResult, float]':
        
        ''' ---------Variables----------
        pg0[k]: Generator active power
        qg0[k]: Generator reactive power
        pvwp[k]: PVWind active power
        --> pg[j]: Active power of all generators at the bus
        --> qg[j]: Reactive power of all generators at the bus
        v[j]: Bus voltage ** 2
        l[i,j]: Line current ** 2
        P[i,j]: Line active power
        Q[i,j]: Line reactive power
        '''
        cons:list[cp.Constraint] = []
        # Create GEN vars
        pg0: dict[str, VF] = {}
        qg0: dict[str, VF] = {}
        for gID, g in island.GenItems():
            if g.FixedP:
                assert g.P is not None
                pg0[gID] = g.P(_t) if isinstance(g.P, TimeFunc) else g.P
            elif g.Pmin is not None and g.Pmax is not None:
                v = Var(name=f"pg_{gID}")
                cons.append(v >= g.Pmin(_t))
                cons.append(v <= g.Pmax(_t))
                pg0[gID] = v
            else:
                raise ValueError(f"Generator {gID} provides neither P or (pmin, pmax)")
            if g.FixedQ:
                assert g.Q is not None
                qg0[gID] = g.Q(_t) if isinstance(g.Q, TimeFunc) else g.Q
            elif g.Qmin is not None and g.Qmax is not None:
                v = Var(name=f"qg_{gID}")
                cons.append(v >= g.Qmin(_t))
                cons.append(v <= g.Qmax(_t))
                qg0[gID] = v
            else:
                raise ValueError(f"Generator {g.ID} provides neither Q or (qmin, qmax)")
        
        pvwp: dict[str, Var] = {
            pID: Var(name=f"pvw_{pID}", nonneg=True) 
            for pID, p in island.PVWItems()
        }
        pvwq: dict[str, Var] = {
            pID: Var(name=f"pvwq_{pID}")
            for pID in island.PVWs
        }
        
        # Add PVW constraints
        for pID, p in island.PVWItems():
            cons.append(pvwp[pID] <= p.P(_t))
            cons.append(pvwp[pID] * math.sqrt(1 - p.PF**2) == pvwq[pID])

        # Bind GEN vars to Bus
        pg: dict[str, list[VF]] = {b: [] for b in island.Buses}
        qg: dict[str, list[VF]] = {b: [] for b in island.Buses}
        pd: dict[str, float] = {bID: b.Pd(_t) for bID, b in island.BusItems()}
        qd: dict[str, float] = {bID: b.Qd(_t) for bID, b in island.BusItems()}
        for gID, g in island.GenItems():
            pg[g.BusID].append(pg0[gID])
            qg[g.BusID].append(qg0[gID])
        for pID, p in island.PVWItems():
            pg[p.BusID].append(pvwp[pID])
            qg[p.BusID].append(pvwq[pID])
        for eID, e in island.ESSItems():
            p, q = e.GetLoad(_t, island.grid.ChargePrice(_t), island.grid.DischargePrice(_t))
            e.P = p
            if p > 0:
                pd[e.BusID] += p
                qd[e.BusID] += q
            elif p < 0:
                pg[e.BusID].append(-p)
                qg[e.BusID].append(-q)
        
        # Create BUS vars
        v = {bID: Var(name=f"v_{bID}") for bID in island.Buses}
        dvmin: dict[str, Var] = {}
        dvmax: dict[str, Var] = {}
        for bid, b in island.BusItems():
            if b.FixedV:
                assert b.V is not None, f"Bus {bid} has fixed voltage but not set"
                cons.append(v[bid] == b.V ** 2)
            elif relaxV:
                dvmin[bid] = Var(name=f"dvmin_{bid}", nonneg=True)
                dvmax[bid] = Var(name=f"dvmax_{bid}", nonneg=True)
                cons.append(v[bid] >= b.MinV ** 2 - dvmin[bid])
                cons.append(v[bid] <= b.MaxV ** 2 + dvmax[bid])
            else:
                cons.append(v[bid] >= b.MinV ** 2)
                cons.append(v[bid] <= b.MaxV ** 2)
        
        # Create Line vars
        dlmax: dict[str, Var] = {}
        l = {lID: Var(name=f"l_{lID}", nonneg=True) for lID in island.Lines}
        
        for lID, ln in island.LineItems():
            if ln.max_I == math.inf:
                continue
            if relaxI:
                dlmax[lID] = Var(name=f"dlmax_{lID}", nonneg=True)
                cons.append(l[lID] <= (ln.max_I/island.grid.Ib) ** 2 + dlmax[lID])
            else:
                cons.append(l[lID] <= (ln.max_I/island.grid.Ib) ** 2)
        
        P = {lID: Var(name=f"P_{lID}") for lID in island.Lines}
        Q = {lID: Var(name=f"Q_{lID}") for lID in island.Lines}

        Pdec: dict[BusID, Var] = {
            bus: Var(name=f"Pdec_{bus}", nonneg=True)
            for bus, lim in self._decb.items()
        }
        for bus, lim in self._decb.items():
            cons.append(Pdec[bus] <= lim.Limit(_t) * self._mlrp)
        
        # ----------Constraints-----------
        for j, bus in island.BusItems():
            flow_in = island.grid.LinesOfTBus(j)
            flow_out = island.grid.LinesOfFBus(j)
            dec = Pdec[j] if j in Pdec else 0
            
            # P constraint
            inflow = cp.sum([P[ln.ID] - ln.R * l[ln.ID] for ln in flow_in if ln.ID in island.Lines])
            outflow = cp.sum([P[ln.ID] for ln in flow_out if ln.ID in island.Lines])
            cons.append(
                inflow + cp.sum(pg[j]) == outflow + pd[j] - dec # type: ignore
            )
            
            # Q constraint
            q_inflow = cp.sum([Q[ln.ID] - ln.X * l[ln.ID] for ln in flow_in if ln.ID in island.Lines])
            q_outflow = cp.sum([Q[ln.ID] for ln in flow_out if ln.ID in island.Lines])
            cons.append(
                q_inflow + cp.sum(qg[j]) == q_outflow + qd[j] # type: ignore
            )

        for lid, line in island.LineItems():
            i, j = line.pair
            lid = line.ID
            cons.append(
                v[j] == v[i] - 2 * (line.R * P[lid] + line.X * Q[lid]) + (line.R ** 2 + line.X ** 2) * l[lid]
            )
            cons.append(
                cp.quad_over_lin(cp.hstack([P[lid], Q[lid]]), v[i]) <= l[lid]
            )
        
        for pID, p in island.PVWItems():
            cons.append(pvwp[pID] + cp.sqrt(1 - p.PF**2) == pvwq[pID])

        # Objective components
        decs = self.C * (cp.sum(list(Pdec.values())) + 
                        (cp.sum(list(dvmin.values())) if relaxV else 0) + 
                        (cp.sum(list(dvmax.values())) if relaxV else 0) + 
                        (cp.sum(list(dlmax.values())) if relaxI else 0))
        
        crpe = cp.sum([p.CC*(p.P(_t)-pvwp[pID]) for pID, p in island.PVWItems()])
        
        if self._sec_cost:
            goal = cp.sum([g.CostA(_t) * cp.square(pg0[gID]) + g.CostB(_t) * pg0[gID] + g.CostC(_t) 
                         for gID, g in island.GenItems()])
        else:
            goal = cp.sum([g.CostB(_t) * pg0[gID] + g.CostC(_t) 
                         for gID, g in island.GenItems()])

        problem = cp.Problem(cp.Minimize(decs + goal + crpe), cons)
        
        try:
            problem.solve(solver=cp.ECOS, verbose=False)
        except cp.SolverError as e:
            if "installed" in e.args[0]:
                raise e
            return IslandResult.Failed, -1

        if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
            for _, bus in island.BusItems():
                if not bus.FixedV: bus._v = 0
                bus.ShadowPrice = 0
            for _, p in island.PVWItems():
                p._pr = p._qr = p._cr = 0
            for _, line in island.LineItems():
                line.I = line.P = line.Q = 0
            for j, gen in island.GenItems():
                if not gen.FixedP: gen._p = 0
                if not gen.FixedQ: gen._q = 0
            for _, e in island.ESSItems():
                e.P = 0
            return IslandResult.Failed, -1

        for j, bus in island.BusItems():
            bus._v = self.__chkv(v[j].value) ** 0.5

        for lid, line in island.LineItems():
            line.I = self.__chkv(l[lid].value) ** 0.5
            line.P = self.__chkv(P[lid].value)
            line.Q = self.__chkv(Q[lid].value)

        for j, gen in island.GenItems():
            p = pg0[j]
            if isinstance(p, Var) and p.value is not None: gen._p = self.__chkv(p.value)
            q = qg0[j]
            if isinstance(q, Var): gen._q = self.__chkv(q.value)
        
        for pID, p in island.PVWItems():
            p._pr = self.__chkv(pvwp[pID].value)
            p._qr = self.__chkv(pvwq[pID].value)
            pgen = p.P(_t)
            p._cr = 1 - p._pr / pgen if pgen > 0 else 0
        
        overflow = False
        self._ofbuses.clear()
        if relaxV:
            for bID, bv in chain(dvmax.items(), dvmin.items()):
                if self.__chkv(bv.value) > 1e-8:
                    overflow = True
                    self._ofbuses.add(bID)
        
        self._oflines.clear()
        if relaxI:
            for lID, lv in dlmax.items():
                if self.__chkv(lv.value) > 1e-8:
                    overflow = True
                    self._oflines.add(lID)
        
        for bus, lim in self._decb.items():
            lim.Reduction = self.__chkv(Pdec[bus].value)
            if lim.Reduction < 1e-8: lim.Reduction = 0

        if not isinstance(goal, (int, float)):
            goal = self.__chkv(goal.value)
        return IslandResult.OverFlow if overflow else IslandResult.OK, goal