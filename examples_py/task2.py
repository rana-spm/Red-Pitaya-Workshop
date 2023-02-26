import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya

wave_form1 = 'TRIANGLE'
freq = 5 * 1000     # 5 kHz
ampl = 0.5          # 0.5 V

ncyc = 3
nor = 65536
period = 1/5000 * 15 * 1000000

rp_s.tx_txt('GEN:RST')                                # Reset generator
rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form1).upper())  # Signal shape
rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))            # Frequency
rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))                # Amplitude
rp_s.tx_txt('SOUR1:BURS:STAT BURST')                  # Enable burst mode
rp_s.tx_txt('SOUR1:BURS:NCYC ' + str(ncyc))           # Number of periods in a burst
rp_s.tx_txt('SOUR1:BURS:NOR ' + str(nor))             # Number of repeated bursts
rp_s.tx_txt('SOUR1:BURS:INT:PER ' + str(period))      # Duration of a single burst (includes signal and delay)
rp_s.tx_txt('SOUR1:TRIG:SOUR INT')                    # Trigger Source internal
rp_s.tx_txt('OUTPUT1:STATE ON')                       # Output 1 turned ON
rp_s.tx_txt('SOUR1:TRIG:INT')

time.sleep(10)

rp_s.close()
