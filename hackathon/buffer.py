import numpy as np
import math
import time
from matplotlib import pyplot as plt
import sys
sys.path.append('../examples_py')

import redpitaya_scpi as scpi

IP = '169.254.55.175'
rp_s = scpi.scpi(IP)         # Establishing socket communication with Red Pitaya

state = ''

##### Acquisition ######
BUFF_SIZE = 16384
TRIG_DLY = BUFF_SIZE/2
DEC = pow(2, 7)

def receive(n):
    # Update state
    global state
    state = 'rx'
    
    buff = np.zeros((n, BUFF_SIZE))
    buff_strings = ['']*n #np.empty([n], dtype=str)

    time.sleep(0.2)
    
    rp_s.tx_txt('ACQ:RST')                      # Reset acquisition parameters
    rp_s.tx_txt('ACQ:SOUR2:GAIN HV')
    rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')        # Format of the data (ASCII or BIN)
    rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')         # VOLTS or RAW
    rp_s.tx_txt('ACQ:DEC ' + str(DEC))                    # Decimation factor
    rp_s.tx_txt('ACQ:TRIG:LEV 2.5')             # Trigger level in volts
    rp_s.tx_txt('ACQ:TRIG:DLY ' + str(TRIG_DLY))  # Set the trigger delay

    for i in range(0,n):
        rp_s.tx_txt('ACQ:START')                    # Start acquiring data
        time.sleep(0.134)
        rp_s.tx_txt('ACQ:TRIG CH2_NE')              # Set the trigger

        while 1:                              # Wait until the trigger condition is met
            rp_s.tx_txt('ACQ:TRIG:STAT?')
            if rp_s.rx_txt() == 'TD':
                break
            if state == 'tx':
                return None
        
        rp_s.tx_txt('ACQ:SOUR2:DATA?')              # Request data
        buff_strings[i] = rp_s.rx_txt()                 # Save data
    
    for i in range(0,n):
        # Transform data from a string to a list of floats
        buff_string = buff_strings[i].strip('{}\n\r').replace("  ", "").split(',')
        buff[i, :] = list(map(float, buff_string))
    # Print buffers
    if False:
        cmt = 0
        for sample in buff[0]:
            if cmt < 700:
                print(sample)
            else:
                break
            cmt += 1
        print(buff)
    if False:
        ######## PLOTTING THE DATA #########
        fig, axs = plt.subplots(n, sharex = True)   # plot the data (n subplots)
        fig.suptitle("Measurements")

        for i in range(0,n,1):                      # plotting the acquired buffers
            axs[i].plot(buff[i])

        # Plotting the received data
        plt.plot(buff)
        plt.ylabel('Voltage')
        plt.show()

    # Convert signal to bits
    output = []
    COUNTER_THRESH = round((2170 / 7) / 2) # Number of samples per Morse unit
    for i in range(0, n):
        high_val = max(buff[i])
        low_val = min(buff[i])
        #print(f"{i}: {high_val=}")
        #print(f"{i}: {low_val=}")
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
                    counter = 0 # Reset counter
            elif val < low_val + high_val * 0.2: # if below 1 threshhold
                if state == 1: # Same state
                    if counter > COUNTER_THRESH: # Has been in same state for long enough
                        output.append(1) # Append bit
                        counter = 0 # Reset counter
                elif state == 0: # State changed
                    output.append(1) # Append bit
                    state = 1 # Update state
                    counter = 0 # Reset counter
            # Increment number of samples since last bit
            counter += 1
    # Print bits
    #print(output)
    #print(f"Length: {len(output)}")

    # Dict from morse string to letter
    receiveDict = {
        "" : "",
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
        "-----" : "0",
        ".-.-.-" : '.',
        "--..--" : ',',
        '..--..' : '?',
        '.----.' : "'",
        '-.-.--' : '!',
        '---...' : ':'
        
    }
    # Decode bits into message
    decoded_morse = []
    o_string = "".join(map(str, output))
    words = o_string.split('00000')
    for word in words:
        if word == '':
            continue
        letters = word.split('000')
        for letter in letters:
            if letter == '':
                continue
            # Convert letter to morse string
            morse_string = ''
            dots_and_dashes = letter.split('0')
            for dot_or_dash in dots_and_dashes:
                if dot_or_dash == '1':
                    morse_string += '.'
                elif dot_or_dash == '111' or dot_or_dash == '11':
                    morse_string += '-'
                elif dot_or_dash == '':
                    morse_string += ''
                else:
                    morse_string += 'X'
            # Decode letter from morse_string
            decoded_morse.append(receiveDict.get(morse_string, '_'))
        decoded_morse.append(' ')
    final_string = ''.join(map(str, decoded_morse))
    return final_string


##### Generation ######
sendDict = {
    "A" : ".-",
    "B" : "-...",
    "C" : "-.-.",
    "D" : "-..",
    "E" : ".",
    "F" : "..-.",
    "G" : "--.",
    "H" : "....",
    "I" : "..",
    "J" : ".---",
    "K" : "-.-",
    "L" : ".-..",
    "M" : "--",
    "N" : "-.",
    "O" : "---",
    "P" : ".--.",
    "Q" : "--.-",
    "R" : ".-.",
    "S" : "...",
    "T" : "-",
    "U" : "..-",
    "V" : "...-",
    "W" : ".--",
    "X" : "-..-",
    "Y" : "-.--",
    "Z" : "--..",
    "1" : ".----",
    "2" : "..---",
    "3" : "...--",
    "4" : "....-",
    "5" : ".....",
    "6" : "-....",
    "7" : "--...",
    "8" : "---..",
    "9" : "----.",
    "0" : "-----",
}

def transmit(message):
    # Update state
    global state
    state = 'tx'
    
    # Convert the message into bits
    words = message.split(' ')
    words_morse = []
    for word in words:
        letters = [letter for letter in word]
        letters_morse = []
        for letter in letters:
            dots_and_dashes = sendDict.get(letter.upper(), '')
            bits = []
            for dot_or_dash in dots_and_dashes:
                if dot_or_dash == '.':
                    bits.append('1')
                elif dot_or_dash == '-':
                    bits.append('111')
            bits_string = '0'.join(bits)
            letters_morse.append(bits_string)
        letters_morse_string = '000'.join(letters_morse)
        words_morse.append(letters_morse_string)
    words_morse_string = '0000000'.join(words_morse)
    print(words_morse_string)
    
    # Convert bits into full signal
    signal = []
    high_val = 1
    low_val = 0
    for word_morse_string in words_morse:
        word_signal = []
        bits = [bit for bit in word_morse_string]
        print(''.join(bits))
        for bit in bits:
            if bit == '1':
                word_signal.append(high_val)
            elif bit == '0':
                word_signal.append(low_val)
        signal.append(word_signal)
    
    # Generate waveform
    FREQ = 57600
    AMPL = 1
    for word_signal in signal:
        # Repeat each bit 7 times
        repeated_signal = np.repeat(word_signal, 7)[:16384]
        # Pad with 0 to BUFF_SIZE
        full_signal = np.zeros(BUFF_SIZE)
        full_signal[:len(repeated_signal)] = repeated_signal
        waveform = []
        for bit in repeated_signal:
            waveform.append(f'{bit:.5f}')
        waveform_str = ', '.join(map(str, waveform))
        
        time.sleep(0.2)
        
        rp_s.tx_txt('GEN:RST')                                # Reset generator
        rp_s.tx_txt('SOUR1:FUNC ARBITRARY')                   # Signal shape
        rp_s.tx_txt('SOUR1:TRAC:DATA:DATA ' + waveform_str)       # Sending custom signal data

        rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(FREQ))            # Frequency
        rp_s.tx_txt('SOUR1:VOLT ' + str(AMPL))                # Amplitude

        rp_s.tx_txt('SOUR1:TRIG:SOUR INT')                    # Trigger Source internal
        rp_s.tx_txt('OUTPUT1:STATE ON')                       # Output 1 turned ON
        rp_s.tx_txt('SOUR1:TRIG:INT')

# If running buffer.py from command line:
if __name__ == "__main__":
    # Test transmit
    print(transmit("SOS"))
    # Print output from n buffers
    #n = 8
    #output = receive(n)
    #print(f"Final Output: {output}")
