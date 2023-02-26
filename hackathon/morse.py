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

def send():
    word = input("Enter words: ")
    morse = ""
    for letter in word.upper():
        if letter in sendDict:
            morse += sendDict[letter] + " "
        else:
            if letter == " ":
                morse += "/ "
            else:
                morse += letter + " "
    print(morse.strip())
    return morse.strip()

# Convert the message into the signal
def convert_string_to_signal(message):
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
    return words_morse_string

            

def convert_word_to_binarymorse(phrase):
    morse_code = ''
    for char in phrase:
        if char == " ":
            morse_code += "0000000"
        else:
            morse_code += sendDict[char.upper()] + "0"

    binary_morse_code = ""
    for morse_char in morse_code:
        if morse_char == ".":
            binary_morse_code += "1"
        elif morse_char == "-":
            binary_morse_code += "111"
        elif morse_char == " ":
            binary_morse_code += "0"

    return binary_morse_code[:-1]

print(convert_word_to_binarymorse("Hello W"))
# .. / -. . . -.. / -... .- --. . .-.. ...
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

def binary_to_text(output):
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
    return final_string

print(binary_to_text(convert_word_to_binarymorse("I need bagels")))