import random as rd
def main():
    key = "FCP EVQKZGMTRAYONUJDLWHBXSI"

    text = "I love Pizza"
    code = "ZITYWEIOZSSF"
    mode = 0
    
    result = cipherSubstitution(code, alphabet, key, mode)
    print(result)

def cipherSubstitution(text, key, mode):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    result = ""
    if mode == 1:
        for letter in text:
            if letter == " ":
                result += key[alphabet.find(letter)]
            elif letter.upper() in alphabet:
                result += key[alphabet.find(letter.upper())]
            else:
                result += letter
        return result
    elif mode == 0:
        for letter in text:
            if letter == " ":
                result += alphabet[key.find(letter)]
            elif letter.upper() in key:
                result += alphabet[key.find(letter.upper())]
            else:
                result += letter
        return result
            
# Executes the main function
if __name__ == '__main__':
    main()