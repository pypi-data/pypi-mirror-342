from warnings import warn
from .solbase import *

class GridCalSolver(SolverBase):
    def __init__(self, grid:Grid, eps:float = 1e-6, max_iter:int = 1000, *, default_saveto:str = DEFAULT_SAVETO, 
            slack_bus:str, slack_gen:str = "", init_t:int = 0):
        try:
            import GridCalEngine as gce
        except ImportError:
            raise ImportError("GridCalEngine is not installed. Please install it using 'pip install GridCalEngine'")
        super().__init__(grid, eps, max_iter, default_saveto = default_saveto)
        self.max_iter = max_iter
        self._g = grid
        assert slack_bus in grid.BusNames
        self.slack_bus = slack_bus
        if slack_gen == "":
            slack_gens = grid.GensAtBus(slack_bus)
            if len(slack_gens) == 0:
                raise RuntimeError("Slack generator not identified, and no generator connects with the slack bus.")
            slack_gen = slack_gens[0].ID
            #print(f"FPowerKit Info: Use {slack_gen} as the slack generator.")
        assert slack_gen in grid.GenNames
        self.slack_gen = slack_gen
        gcg = gce.MultiCircuit(Sbase=grid.Sb_MVA)
        t = init_t
        buses:dict[str, gce.Bus] = {}
        for bus in grid.Buses:
            bid = bus.ID
            p = bus.Pd(t)
            q = bus.Qd(t)
            b_inst = gce.Bus(bid, 
                Vnom=grid.Ub, # type:ignore
                vmin=bus.MinV, vmax=bus.MaxV, is_slack=bid==slack_bus)
            buses[bid] = b_inst
            gcg.add_bus(b_inst)
            gcg.add_load(b_inst, gce.Load(bid+"_load", P = p*grid.Sb_MVA, Q = q*grid.Sb_MVA))
        
        for line in self.grid.Lines:
            fid = line.fBus
            tid = line.tBus
            gcg.add_line(gce.Line(buses[fid], buses[tid], name=line.ID, r=line.R, x=line.X))

        for pvw in self.grid.PVWinds:
            if pvw.Pr is None:
                raise ValueError(f"PVWind {pvw.ID} has no Pr value")
            p = pvw.Pr
            if pvw.Qr is None:
                raise ValueError(f"PVWind {pvw.ID} has no Qr value")
            q = pvw.Qr
            bid = pvw.BusID
            g_inst = gce.Generator(pvw.ID, P=p*grid.Sb_MVA, power_factor=pvw.PF, Sbase = grid.Sb_MVA)
            gcg.add_generator(buses[bid], g_inst)
        
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
                gcg.add_load(buses[bid], gce.Load(ess.ID, P=p*grid.Sb_MVA, Q=q*grid.Sb_MVA))
            else: # discharging = generator
                g_inst = gce.Generator(ess.ID, P=p*grid.Sb_MVA, power_factor=ess.PF, Sbase = grid.Sb_MVA)
                gcg.add_generator(buses[bid], g_inst)

        for gen in self.grid.Gens:
            bid = gen.BusID
            if gen.ID == slack_gen:
                g_inst = gce.Generator(gen.ID, vset=1.0)
                if gen.P is not None or gen.Q is not None:
                    warn(f"Given value of P and Q of the slack generator {gen.ID} is ignored.")
            else:
                if gen.P is None:
                    p = 0
                else:
                    p = gen.P(t) if isinstance(gen.P, TimeFunc) else gen.P
                if gen.Q is None:
                    pf = 0.8
                else:
                    q = gen.Q(t) if isinstance(gen.Q, TimeFunc) else gen.Q
                    pf = p / (p**2 + q**2) ** 0.5
                g_inst = gce.Generator(gen.ID, P=p*grid.Sb_MVA, power_factor=pf, Sbase = grid.Sb_MVA, vset=1.0)
            gcg.add_generator(buses[bid], g_inst)

        self.grid_cal = gcg

    def solve(self, _t:int, /, *, timeout_s:float = 1) -> 'tuple[GridSolveResult, float]':
        import GridCalEngine as gce
        options = gce.PowerFlowOptions(gce.SolverType.NR,
                            max_iter=self.max_iter,
                            retry_with_other_methods=False,
                            tolerance=self.eps,
                            control_q=False,
                            control_taps_phase=False,
                            control_taps_modules=False,
                            apply_temperature_correction=False,
                            use_stored_guess=False,
                            initialize_angles=True,
                            verbose=False)

        power_flow = gce.PowerFlowDriver(self.grid_cal, options)
        power_flow.run()
        assert isinstance(power_flow.results, gce.PowerFlowResults)
        if not power_flow.results.converged:
            return GridSolveResult.Failed, 0.0
        bus_res = power_flow.results.get_bus_df()

        for i, bn in enumerate(self._g.BusNames):
            b = self.grid.Bus(bn)
            v = bus_res.loc[bn, 'Vm']
            assert isinstance(v, (float, np.floating)), f"Bus {bn} voltage is not a float: {type(v)}"
            b._v = float(v)
            angle = bus_res.loc[bn, 'Va']
            assert isinstance(angle, (float, np.floating)), f"Bus {bn} angle is not a float: {type(angle)}"
            b.theta = float(angle) / 180 * math.pi
        
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
