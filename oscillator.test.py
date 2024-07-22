import numpy as np
import matplotlib.pyplot as plt
import time

from modules.oscillator import Oscillator

FREQ_SAMPLE = 44100
SAMPLE_SIZE = 256

# 

out = []
sync = []

leader = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)
follower = Oscillator(FREQ_SAMPLE, SAMPLE_SIZE)

total = 0

n = 1
for i in range(n):
  start = time.time()
  leader._params['pul_width'] = 0.5
  leader._params['pul_width_mod_amt'] = 0.5
  leader.set_in_channel('in_volt_per_oct', np.ones((SAMPLE_SIZE,)) * 5)
  leader.set_in_channel('in_pul_width_mod', np.ones((SAMPLE_SIZE,)) * 0)
  leader.process()
  sync.append(leader.get_out_channel('out_saw'))

  follower.set_in_channel('in_volt_per_oct', np.ones((SAMPLE_SIZE,)) * 1)
  follower.set_in_channel('in_sync', sync[-1])
  follower.process()
  out.append(follower.get_out_channel('out_saw'))
  end = time.time()

  total += end - start

print(total)

plt.figure()
plt.plot(
  np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
  (np.arange(SAMPLE_SIZE * n) % SAMPLE_SIZE == 0).astype(int),
  color='lightgrey',
)
plt.plot(
  np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
  np.concatenate(sync),
)
# plt.plot(
#   np.arange(SAMPLE_SIZE * n) / FREQ_SAMPLE,
#   np.concatenate(out),
# )
plt.show()
