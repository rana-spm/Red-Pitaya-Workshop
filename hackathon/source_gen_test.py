import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya


##### Signal Gen ######

#### Creating arbitrary signal ##### 
N = 16384                                       # Signal length in Samples (16384 = buffer) 
# Input list of bits
bits = [1, 0, 0, 1, 0]

# Number of times each bit should be repeated
reps = int(np.ceil(16384 / len(bits)))
new_bits = np.repeat(bits, reps)[:16384]

# Convert bits to string format
waveform_ch_10 = []
for n in new_bits:
    waveform_ch_10.append(f"{n:.5f}")
waveform = ", ".join(map(str, waveform_ch_10))

freq = 57600  # Set frequency to 57.6kHz
ampl = 1

rp_s.tx_txt('GEN:RST')                                # Reset generator
rp_s.tx_txt('SOUR1:FUNC ARBITRARY')                   # Signal shape
rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + waveform)       # Sending custom signal data

rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))            # Frequency
rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))                # Amplitude

rp_s.tx_txt('SOUR1:TRIG:SOUR INT')                    # Trigger Source internal
rp_s.tx_txt('OUTPUT1:STATE ON')                       # Output 1 turned ON
rp_s.tx_txt('SOUR1:TRIG:INT')

