import numpy as np
import math
import time
from matplotlib import pyplot as plt
import sys
sys.path.append('../examples_py')

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya

##### Acquisition ######
BUFF_SIZE = 16384
TRIG_DLY = 8000 #BUFF_SIZE/2
DEC = pow(2, 7)

n = 8
buff = np.zeros((n, BUFF_SIZE))
buff_strings = ['']*n #np.empty([n], dtype=str)

rp_s.tx_txt('ACQ:RST')                      # Reset acquisition parameters
rp_s.tx_txt('ACQ:SOUR2:GAIN HV')
rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')        # Format of the data (ASCII or BIN)
rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')         # VOLTS or RAW
rp_s.tx_txt('ACQ:DEC ' + str(DEC))                    # Decimation factor
rp_s.tx_txt('ACQ:TRIG:LEV 2.5')             # Trigger level in volts
rp_s.tx_txt('ACQ:TRIG:DLY ' + str(TRIG_DLY))  # Set the trigger delay

curr_perf_time = 0

for i in range(0,n):
    rp_s.tx_txt('ACQ:START')                    # Start acquiring data
    #print(time.perf_counter() - curr_perf_time)
    time.sleep(0.0034)
    rp_s.tx_txt('ACQ:TRIG CH2_NE')              # Set the trigger

    while 1:                              # Wait until the trigger condition is met
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break
    
    rp_s.tx_txt('ACQ:SOUR2:DATA?')              # Request data
    buff_strings[i] = rp_s.rx_txt()                 # Save data
    #curr_perf_time = time.perf_counter()
    
for i in range(0,n):
    # Transform data from a string to a list of floats
    buff_string = buff_strings[i].strip('{}\n\r').replace("  ", "").split(',')
    buff[i, :] = list(map(float, buff_string))

print(len(buff))
print(buff)


# Convert signal to bits
output = []
COUNTER_THRESH = 155 # Number of samples per Morse unit
for i in range(0, n):
    high_val = max(buff[i])
    low_val = min(buff[i])
    print(f"{i}: {high_val=}")
    print(f"{i}: {low_val=}")
    state = 1 # Start in state 1
    counter = 0 # Reset counter
    output.append(1) # Add first one
    for j in range(0, BUFF_SIZE):
        val = buff[i][j] # Get sample value
        # Parse value
        if val > high_val * 0.8: # if above 0 threshhold
            if state == 0: # Same state
                if counter > COUNTER_THRESH: # Has been in same state for long enough
                    output.append(0) # Append bit
                    counter = 0 # Reset counter
            elif state == 1: # State changed
                output.append(0) # Append bit
                state = 0 # Update state
        elif val < low_val + high_val * 0.2: # if below 1 threshhold
            if state == 1: # Same state
                if counter > COUNTER_THRESH: # Has been in same state for long enough
                    output.append(1) # Append bit
                    counter = 0 # Reset counter
            elif state == 0: # State changed
                output.append(1) # Append bit
                state = 1 # Update state
        # Increment number of samples since last bit
        counter += 1
print(output)
print(len(output))


# Decode Morse from bits
receiveDict = {
    ".-" : "A",
    "-..." :"B" ,
    "-.-." : "C" ,
    "-.." : "D",
    "." : "E",
    "..-." : "F",
    "--." : "G",
    "...." : "H",
    ".." : "I",
    ".---" : "J",
    "-.-" : "K",
    ".-.." : "L",
    "--" : "M",
    "-." : "N",
    "---" : "O",
    ".--." : "P",
    "--.-" : "Q",
    ".-." : "R",
    "..." : "S",
    "-" : "T",
    "..-" : "U",
    "...-" : "V",
    ".--" : "W",
    "-..-" : "X",
    "-.--" : "Y",
    "--.." : "Z",
    ".----" : "1",
    "..---" : "2",
    "...--" : "3",
    "....-" : "4",
    "....." : "5",
    "-...." : "6",
    "--..." : "7",
    "---.." : "8",
    "----." : "9",
    "-----" : "0"
}

decoded_morse = []

o_string = "".join(map(str, output))
words = o_string.split('0000000')
for word in words:
    letters = word.split('000')
    for letter in letters:
        morse_string = ''
        
        dots_and_dashes = letter.split('0')
        for dot_or_dash in dots_and_dashes:
            if dot_or_dash == '1':
                morse_string += '.'
            elif dot_or_dash == '111':
                morse_string += '-'
            else:
                morse_string += 'X'
                
        # Decode Morse letter from morse_string
        decoded_morse.append(receiveDict.get(morse_string, '_'))
    decoded_morse.append(" ")
final_string = ''.join(map(str, decoded_morse))



######## PLOTTING THE DATA #########
fig, axs = plt.subplots(n, sharex = True)   # plot the data (n subplots)
fig.suptitle("Measurements")

for i in range(0,n,1):                      # plotting the acquired buffers
    axs[i].plot(buff[i])

# Plotting the received data
plt.plot(buff)
plt.ylabel('Voltage')
plt.show()

time.sleep(10)

rp_s.close()
