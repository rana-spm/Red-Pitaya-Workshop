import numpy as np
import math
import time
from matplotlib import pyplot as plt

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya

for i in range(0,10,1):
	rp_s.tx_txt('DIG:PIN LED0,1')  # Turn LED0 on
	time.sleep(1)
	rp_s.tx_txt('DIG:PIN LED0,0')  # Turn LED0 off
	time.sleep(1)

rp_s.close()                 # Close socket communication
