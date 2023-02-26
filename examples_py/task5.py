import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya


##### Signal Gen ######


wave_form1 = 'sine'
freq = 20 * 1000    # 20 kHz
ampl = 1            # 1 V

rp_s.tx_txt('GEN:RST')                                # Reset generator
rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form1).upper())  # Signal shape
rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))            # Frequency
rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))                # Amplitude
rp_s.tx_txt('SOUR1:TRIG:SOUR INT')                    # Trigger Source internal
rp_s.tx_txt('OUTPUT1:STATE ON')                       # Output 1 turned ON
rp_s.tx_txt('SOUR1:TRIG:INT')



##### Acquisition ######

rp_s.tx_txt('ACQ:RST')                      # Reset acquisition parameters

rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')        # Format of the data (ASCII or BIN)
rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')         # VOLTS or RAW
rp_s.tx_txt('ACQ:DEC 1')                    # Decimation factor
rp_s.tx_txt('ACQ:TRIG:LEV 0.5')             # Trigger level in volts

rp_s.tx_txt('ACQ:START')                    # Start acquiring data
time.sleep(0.5)

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

time.sleep(10)

rp_s.close()
