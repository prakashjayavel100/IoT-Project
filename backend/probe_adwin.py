from river.drift import ADWIN

print('ok')
print('ADWIN class', ADWIN)
print('ADWIN init signature:', ADWIN.__init__.__code__.co_varnames)

for name in ['drift_detected', 'change', 'change_detected']:
    print(name, hasattr(ADWIN, name), getattr(ADWIN, name, None))

d = ADWIN(grace_period=1, min_window_length=5, delta=0.01)
for v in [100.0, 102.0, 99.0, 101.0, 100.5]:
    d.update(v)
print('stable attrs', [a for a in dir(d) if 'drift' in a or 'change' in a])
print('stable drift_detected', getattr(d, 'drift_detected', None), 'change', getattr(d, 'change', None), 'change_detected', getattr(d, 'change_detected', None))

print('-- shift sequence --')
d2 = ADWIN(grace_period=1, min_window_length=5, delta=0.01)
for v in [100.0, 102.0, 99.0, 101.0, 100.5, 500.0, 10.0]:
    d2.update(v)
    print('updated', v, 'drift_detected', getattr(d2, 'drift_detected', None), 'change', getattr(d2, 'change', None), 'change_detected', getattr(d2, 'change_detected', None))
