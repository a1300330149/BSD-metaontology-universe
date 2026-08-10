import math

class GeneResonanceEngine:
    def __init__(self):
        self.pillar_mass = 300.0
        self.stability_coeff = 1.0000
        self.displacement_threshold = 0.05
        self.num_channels = 8
        self.channel_medium = 'magnetic'
        self.angles = [i * 45 for i in range(self.num_channels)]
        self.resonant_freqs = [35.0] * self.num_channels
        self.attenuation = 0.005
        self.trigger_threshold = 0.02
        self.trigger_delay = 0.005
        self.false_alarm_rate = 0.0005
        self.pearl_mass = 0.3
        self.catch_rate = 1.0
        self.resonance_freq = 30.0

    def gene_hub(self, levels):
        mean = sum(levels) / len(levels)
        var = sum((x-mean)**2 for x in levels) / len(levels)
        stab = 1.0 / (1.0 + math.sqrt(var))
        max_dev = max(abs(x-mean) for x in levels) / max(mean, 0.001)
        bal = 1.0 / (1.0 + max_dev)
        load = sum(levels) * 0.01
        return {"hub_load": load, "stability": stab, "balance": bal,
                "status": "CENTERED" if stab > 0.99 else "DRIFTING"}

    def gene_channel(self, src, tgt, angle):
        shared = set(src) & set(tgt)
        total = set(src) | set(tgt)
        q = len(shared) / max(len(total), 1)
        diff = abs(angle - self.angles[0]) % 360
        dm = math.cos(math.radians(diff))
        rm = abs(1.0 - self.resonant_freqs[0] / max(len(src), 1))
        return {"quality": q, "direction": dm, "resonance": rm,
                "status": "FLOWING" if q > 0.8 else "BLOCKED"}

    def gene_trigger(self, sig, noise):
        snr = sig / max(noise, 0.001)
        tf = sig * self.stability_coeff
        trig = snr > 10 and tf > self.trigger_threshold and self.stability_coeff > 0.999
        fa = math.exp(-snr / 50) * self.false_alarm_rate
        return {"snr": snr, "force": tf, "triggered": trig,
                "false_alarm": fa, "status": "TRIGGERED" if trig else "ARMED"}

    def gene_resonance(self, a, b):
        if not a or not b:
            return {"score": 0, "status": "NO_SIGNAL"}
        ov = len(set(a) & set(b))
        tot = len(set(a) | set(b))
        sc = ov / max(tot, 1)
        cp = self.catch_rate * sc
        met = sc > 0.7 and cp > 0.95
        return {"score": sc, "catch": cp, "freq": self.resonance_freq,
                "status": "PEARL_DISPATCHED" if met else "WAITING"}

    def full_cycle(self, data):
        r = {}
        r["hub"] = self.gene_hub(data.get("expression_levels", []))
        r["channels"] = [self.gene_channel(data.get("source_genes", []),
                        data.get("target_genes", []), a) for a in self.angles]
        r["trigger"] = self.gene_trigger(data.get("signal_strength", 0),
                        data.get("noise_level", 1))
        r["resonance"] = self.gene_resonance(data.get("geneset_a", []),
                        data.get("geneset_b", []))
        r["cycle"] = "COMPLETE" if (r["hub"]["status"] == "CENTERED" and
                    r["trigger"]["triggered"] and
                    r["resonance"]["status"] == "PEARL_DISPATCHED") else "INCOMPLETE"
        return r
