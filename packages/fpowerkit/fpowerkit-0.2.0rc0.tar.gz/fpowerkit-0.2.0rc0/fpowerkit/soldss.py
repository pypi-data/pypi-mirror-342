from .solbase import *

class OpenDSSSolver(SolverBase):
    def __init__(self, grid:Grid, source_bus:str, eps:float = 1e-6, default_saveto:str = DEFAULT_SAVETO, max_iter:int = 100, init_t:int = 0):
        super().__init__(grid, eps, default_saveto)
        from py_dss_interface import DSS
        self._g = grid
        t = init_t
        d = DSS()
        d.text("clear")
        cir = f"new circuit.my_circuit basekv={grid.Ub} pu=1 MVASC3=5000000 5000000 bus1={source_bus}"
        self.source_bus = source_bus
        assert source_bus in grid.BusNames, f"Source bus {source_bus} not found in the grid"
        d.text(cir)
        for bus in grid.Buses:
            bid = bus.ID
            if bid != bid.lower():
                raise ValueError(f"Bus ID {bid} must be lower case")
            p = bus.Pd(t) * grid.Sb_kVA
            q = bus.Qd(t) * grid.Sb_kVA
            d.text(f"New Load.{bid} bus1={bid} kv={self.grid.Ub} kW={p} kvar={q} vmin={bus.MinV} vmax={bus.MaxV}")
        for line in self.grid.Lines:
            fid = line.fBus
            tid = line.tBus
            if line.ID != line.ID.lower():
                raise ValueError(f"Line ID {line.ID} must be lower case")
            d.text(f"New line.{line.ID} bus1={fid} bus2={tid} R1={line.R*grid.Zb} units=ohm X1={line.X*grid.Zb} units=ohm")
        for pvw in self.grid.PVWinds:
            if pvw.ID != pvw.ID.lower():
                raise ValueError(f"PVWind ID {pvw.ID} must be lower case")
            if pvw.Pr is None:
                raise ValueError(f"PVWind {pvw.ID} has no Pr value")
            p = pvw.Pr
            if pvw.Qr is None:
                raise ValueError(f"PVWind {pvw.ID} has no Qr value")
            q = pvw.Qr
            bid = pvw.BusID
            
            s = f"New Generator.{pvw.ID} bus1={bid} kv={grid.Ub} kw={p*grid.Sb_kVA} kvar={q*grid.Sb_kVA}"
            d.text(s)
        for ess in self.grid.ESSs:
            if ess.ID != ess.ID.lower():
                raise ValueError(f"ESS ID {ess.ID} must be lower case")
            if ess.P is None:
                raise ValueError(f"ESS {ess.ID} has no P value")
            p = ess.P
            if ess.Q is None:
                raise ValueError(f"ESS {ess.ID} has no Q value")
            q = ess.Q
            bid = ess.BusID
            if p > 0: # charging = load
                bus = self.grid.Bus(bid)
                s = f"New Load.{ess.ID} bus1={bid} kv={grid.Ub} kW={p*grid.Sb_kVA} kvar={q*grid.Sb_kVA} vmin={bus.MinV} vmax={bus.MaxV}"
            else: # discharging = generator
                s = f"New Generator.{ess.ID} bus1={bid} kv={grid.Ub} kw={p*grid.Sb_kVA} kvar={q*grid.Sb_kVA}"
            d.text(s)
        for gen in self.grid.Gens:
            if gen.ID != gen.ID.lower():
                raise ValueError(f"Generator ID {gen.ID} must be lower case")
            if gen.P is None:
                raise ValueError(f"Generator {gen.ID} has no P value")
            p = gen.P(t) if isinstance(gen.P, TimeFunc) else gen.P
            if gen.Q is None:
                raise ValueError(f"Generator {gen.ID} has no Q value")
            q = gen.Q(t) if isinstance(gen.Q, TimeFunc) else gen.Q
            bid = gen.BusID
            
            s = f"New Generator.{gen.ID} bus1={bid} kv={grid.Ub} kw={p*grid.Sb_kVA} kvar={q*grid.Sb_kVA}"
            d.text(s)
        d.text("set mode=snapshot")
        self.dss = d

    def solve(self, _t:int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        self.dss.text(f"set Voltagebases=[{self.grid.Ub}]")
        self.dss.text("calcv")
        self.dss.text("solve maxcontrol=10000")
        bnames = self.dss.circuit.buses_names
        bvolt = np.array(self.dss.circuit.buses_volts).reshape(-1, 3, 2)
        sb_theta = 0
        for i, bn in enumerate(bnames):
            v1 = bvolt[i,0][0] + 1j * bvolt[i,0][1]
            v2 = bvolt[i,1][0] + 1j * bvolt[i,1][1]
            v = v1 - v2
            b = self.grid.Bus(bn)
            b._v = abs(v) / self.grid.Ub / 1000
            b.theta = math.atan2(v.imag, v.real)
            if bn == self.source_bus:
                sb_theta = b.theta
        
        for i, bn in enumerate(bnames):
            self.grid.Bus(bn).theta -= sb_theta
        
        for l in self.grid.Lines:
            vi = self.grid.Bus(l.fBus).V_cpx
            vj = self.grid.Bus(l.tBus).V_cpx
            assert vi is not None and vj is not None
            i = (vi-vj)/l.Z
            l.I = abs(i)
            s = vi*i.conjugate()
            l.P = s.real
            l.Q = s.imag
        return GridSolveResult.OK, 0.0