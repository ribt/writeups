import numpy as np
import base64
from math import sqrt

flag = open("flag.txt", "r").read()

SAMP_RATE = 24e3
MAX_LEN = 256000

FREQ_HIGH = 5e3
FREQ_LOW = 1e3

TIMING_DOT = 1/1000
TIMING_DASH = 5/1000
TIMING_SEP_LETTER = 5/1000
TIMING_SPACE = 20/1000

alphabet = { 'A':'.-', 'B':'-...',
            'C':'-.-.', 'D':'-..', 'E':'.',
            'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-',
            'L':'.-..', 'M':'--', 'N':'-.',
            'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-',
            'U':'..-', 'V':'...-', 'W':'.--',
            'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--',
            '4':'....-', '5':'.....', '6':'-....',
            '7':'--...', '8':'---..', '9':'----.',
            '0':'-----', ', ':'--..--', '.':'.-.-.-',
            '?':'..--..', '/':'-..-.', '-':'-....-',
            '(':'-.--.', ')':'-.--.-'}

rev_alphabet = {v:k for k,v in alphabet.items()}

def morse_decode(msg):
    res = ""
    for word in msg.split(" "):
        for letter in word.split("_"):
            if letter in rev_alphabet:
                res += rev_alphabet[letter]
            elif letter == "":
                continue
            else:
                raise ValueError("Not a correct Morse character")
        res += " "
    return res

def decode_sample(sample):
    # Frequency should not be too far from the expected values
    if abs(sample-FREQ_HIGH) < 100:
        return 1
    elif abs(sample-FREQ_LOW) < 100:
        return 0
    else:
        raise ValueError("Frequency of your signal is off, try again")

# Compute the timing difference between the provided timing and the expected one
def diff(nb_samples, expected_timing):
    expected_nb_samples = expected_timing * SAMP_RATE
    d = abs(expected_nb_samples-nb_samples) / expected_nb_samples
    return d

def fm_decode(s):
    # Get instantaneous frequency
    freq = np.diff(np.unwrap(np.angle(s)))
    freq = (SAMP_RATE / (2*np.pi)) * freq

    timings = []

    current = decode_sample(freq[0])
    cnt = 1
    for c in freq[1:]:
        new = decode_sample(c)
        if new == current:
            cnt += 1
            continue
        else:
            timings.append(cnt)
            current = new
            cnt = 1
    timings.append(cnt)

    data = ""
    current_symbol = decode_sample(freq[0])
    for timing in timings:
        # This decoder allows up to 10% imprecision in timings.
        # That is, to receive a dot of 1ms, the decoder allows
        # pulses that last between 0.9 and 1.1ms.
        # To receive a dash of 5ms, the decoder allows pulses
        # that last between 4.5 and 5.5ms.
        if current_symbol == 1:
            current_symbol = 0
            if diff(timing, TIMING_DOT) < 0.10:
                data += "."
            elif diff(timing, TIMING_DASH) < 0.10:
                data += "-"
        else:
            current_symbol = 1
            if diff(timing, TIMING_SEP_LETTER) < 0.10:
                data += "_"
            elif diff(timing, TIMING_SPACE) < 0.10:
                data += " "
            else:
                # A correct decoder should handle this case,
                # not done here to keep the code simple
                continue
    return data


def main():

    try:
        encoded = input("signal > ")
    except:
        print("Please check your inputs.")
        exit(0)

    if len(encoded) > MAX_LEN:
        print("Error: signal too long")
        exit(0)

    try:
        signal = np.frombuffer(base64.b64decode(encoded), dtype = np.complex64)

        data = fm_decode(signal)
        msg = morse_decode(data).strip()

        if msg == "CAN I GET THE FLAG":
            print(f"Well done: {flag}")
        else:
            print(f"You said {msg}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
