
import math

class AdaptiveOptimizer:
    def __init__(self):
        self.lr = 0.01
        self.momentum = 0.9
        self.params = {
            'trigger_threshold': 0.02,
            'resonance_freq': 30.0,
            'coupling': 0.95,
        }
        self.history = []

    def step(self, measured):
        target = 0.8
        error = target - measured
        self.params['trigger_threshold'] *= (1 + self.lr * error)
        self.params['resonance_freq'] += self.lr * error * 10
        self.params['coupling'] += self.lr * error * 0.1
        self.params['trigger_threshold'] = max(0.001, min(0.1, self.params['trigger_threshold']))
        self.params['resonance_freq'] = max(10, min(60, self.params['resonance_freq']))
        self.params['coupling'] = max(0.5, min(1.0, self.params['coupling']))
        self.history.append({'measured': measured, 'params': dict(self.params), 'error': error})
        return dict(self.params)

def subcritical_soc(gamma_max=2.1, rate=0.05, steps=50):
    return [gamma_max * (1 - math.exp(-rate * t)) for t in range(steps)]

def layered_fractal(file_sizes, labels):
    layers = {}
    for label in set(labels):
        sizes = [s for s, l in zip(file_sizes, labels) if l == label]
        if len(sizes) >= 10:
            min_s, max_s = min(sizes), max(sizes)
            if min_s == 0: continue
            scales = [max_s / (2**i) for i in range(1, 8)]
            counts = []
            for scale in scales:
                boxes = set()
                for s in sizes:
                    boxes.add(int(s / max(scale, 0.001)))
                counts.append(len(boxes))
            if len(scales) >= 2:
                log_s = [math.log10(1/s) if s > 0 else 0 for s in scales]
                log_n = [math.log10(c) if c > 0 else 0 for c in counts]
                n = len(log_s)
                sx, sy = sum(log_s), sum(log_n)
                sxy = sum(x*y for x,y in zip(log_s, log_n))
                sxx = sum(x*x for x in log_s)
                if n*sxx - sx**2 != 0:
                    layers[label] = (n*sxy - sx*sy) / (n*sxx - sx**2)
    return layers

def seismic_transfer(f_wind, f_ground, cavity_f=35, q=50):
    w_w, w_g, w_c = 2*math.pi*f_wind, 2*math.pi*f_ground, 2*math.pi*cavity_f
    cavity = 1 / math.sqrt(1 + (q*(w_w/w_c - w_c/w_w))**2)
    coupling = math.exp(-abs(f_wind - f_ground) / 5)
    return cavity * coupling
