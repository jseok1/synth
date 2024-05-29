import numpy as np
import matplotlib.pyplot as plt

from envelope import Envelope

FREQ_SAMPLE = 44100
SAMPLE_SIZE = 512

env = Envelope(FREQ_SAMPLE, SAMPLE_SIZE)

envs = []
gates = []
triggers = []

env.set_in('attack', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('decay', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('sustain', np.ones((SAMPLE_SIZE)) * 0.85)
env.set_in('release', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
gate = np.zeros((SAMPLE_SIZE,))
gate[100:] = 1
env.set_in('gate', gate)
gates.append(gate)
trigger = np.zeros(SAMPLE_SIZE)
trigger[100] = 1
trigger[150] = 1
env.set_in('trigger', trigger)
triggers.append(trigger)
env.process()
envs.append(env.get_out('env').copy())

env.set_in('attack', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('decay', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('sustain', np.ones((SAMPLE_SIZE)) * 0.85)
env.set_in('release', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
gate = np.zeros((SAMPLE_SIZE,))
gate[:200] = 1
env.set_in('gate', gate)
gates.append(gate)
trigger = np.zeros((SAMPLE_SIZE,))
env.set_in('trigger', trigger)
triggers.append(trigger)
env.process()
envs.append(env.get_out('env').copy())

env.set_in('attack', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('decay', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('sustain', np.ones((SAMPLE_SIZE)) * 0.85)
env.set_in('release', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
gate = np.ones((SAMPLE_SIZE,))
env.set_in('gate', gate)
gates.append(gate)
trigger = np.zeros((SAMPLE_SIZE,))
trigger[0] = 1
env.set_in('trigger', trigger)
triggers.append(trigger)
env.process()
envs.append(env.get_out('env').copy())

env.set_in('attack', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('decay', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('sustain', np.ones((SAMPLE_SIZE)) * 0.85)
env.set_in('release', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
gate = np.zeros((SAMPLE_SIZE,))
gate[100:450] = 1
env.set_in('gate', gate)
gates.append(gate)
trigger = np.zeros((SAMPLE_SIZE,))
trigger[100] = 1
trigger[400] = 1
env.set_in('trigger', trigger)
triggers.append(trigger)
env.process()
envs.append(env.get_out('env').copy())

env.set_in('attack', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('decay', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
env.set_in('sustain', np.ones((SAMPLE_SIZE)) * 0.85)
env.set_in('release', np.ones((SAMPLE_SIZE)) * 0.5 * SAMPLE_SIZE / FREQ_SAMPLE)
gate = np.zeros((SAMPLE_SIZE,))
env.set_in('gate', gate)
gates.append(gate)
trigger = np.zeros((SAMPLE_SIZE,))
env.set_in('trigger', trigger)
triggers.append(trigger)
env.process()
envs.append(env.get_out('env').copy())

plt.figure()
plt.plot(np.arange(SAMPLE_SIZE * len(envs)) / FREQ_SAMPLE, (np.arange(SAMPLE_SIZE * len(envs)) % SAMPLE_SIZE == 0).astype(int))
plt.plot(np.arange(SAMPLE_SIZE * len(envs)) / FREQ_SAMPLE, np.concatenate(envs))
plt.plot(np.arange(SAMPLE_SIZE * len(gates)) / FREQ_SAMPLE, np.concatenate(gates))
plt.plot(np.arange(SAMPLE_SIZE * len(triggers)) / FREQ_SAMPLE, np.concatenate(triggers))
plt.show()
