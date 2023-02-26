import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya


rp_s.tx_txt('ACQ:RST')                      # Reset acquisition parameters

rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')        # Format of the data (ASCII or BIN)
rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')         # VOLTS or RAW
rp_s.tx_txt('ACQ:DEC 1')                    # Decimation factor
rp_s.tx_txt('ACQ:TRIG:LEV 0.5')             # Trigger level in volts

rp_s.tx_txt('ACQ:START')                    # Start acquiring data
rp_s.tx_txt('ACQ:TRIG CH1_PE')              # Set the trigger

while 1:                              # Wait until the trigger condition is met
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break

rp_s.tx_txt('ACQ:SOUR1:DATA?')              # Request data
buff_string = rp_s.rx_txt()                 # Save data
# Transform data from a string to a list of floats
buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',') 
buff = list(map(float, buff_string))

# Plotting the received data
plt.plot(buff)
plt.ylabel('Voltage')
plt.show()