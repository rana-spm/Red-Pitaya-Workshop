import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya

#### Creating arbitrary signal ##### 
N = 8192                                       # Signal length in Samples (16384 = buffer) 
t = np.linspace(0, 1, int(N))*2*np.pi           # Sample vector
x = np.sin(t)    # One period of custom signal

waveform_ch_10 = [] 

for n in x:                                           # Transforming custom signal into a string (appropriate shape for SCPI commands) 
    waveform_ch_10.append(f"{n:.5f}") 
waveform = ", ".join(map(str, waveform_ch_10))

freq = 100000
ampl = 1

rp_s.tx_txt('GEN:RST')                                # Reset generator
rp_s.tx_txt('SOUR1:FUNC ARBITRARY')                   # Signal shape
rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + waveform)       # Sending custom signal data

rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))            # Frequency
rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))                # Amplitude

rp_s.tx_txt('SOUR1:TRIG:SOUR INT')                    # Trigger Source internal
rp_s.tx_txt('OUTPUT1:STATE ON')                       # Output 1 turned ON
rp_s.tx_txt('SOUR1:TRIG:INT')

time.sleep(10)

rp_s.close()
