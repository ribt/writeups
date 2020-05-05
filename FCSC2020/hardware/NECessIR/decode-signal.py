import scipy.io.wavfile

_, data = scipy.io.wavfile.read('ir-signal.wav')
rate = 192 # f/ms

offset = 0

for _ in range(4) :
    delta = 0
    moy = 1000
    while moy > 100:
        moy = 0
        for i in range(5) : moy += abs(data[offset+delta+i])
        moy /= 5
        delta += 5

    print ("burst de", round(delta/rate, 2), "ms (", offset, offset+delta, ")")

    offset += delta
    delta = 0
    moy = 0
    while moy < 100:
        moy = 0
        for i in range(5) : moy += abs(data[offset+delta+i])
        moy /= 5
        delta += 5

    #print ("pause de", round(delta/rate, 2), "ms (", offset, offset+delta, ")")

    offset += delta
    bits = "0"
    while True :
        delta = 0
        moy = 1000
        while moy > 100:
            moy = 0
            for i in range(5) : moy += abs(data[offset+delta+i])
            moy /= 5
            delta += 5

        t1 = round(delta/rate, 2)
        #print (" pic de ", t1, "ms (", offset, offset+delta, ")")

        offset += delta

        delta = 0
        moy = 0
        while moy < 100:
            if offset+delta+5 > len(data):
                break
            moy = 0
            for i in range(5) : moy += abs(data[offset+delta+i])
            moy /= 5
            delta += 5

        t2 = round(delta/rate, 2)
        #print ("pause de", t2, "ms (", offset, offset+delta, ")")

        if 0.4 <= t1 <= 0.6:
            if 0.4 <= t2 <= 0.6 :
                bits += "0"
            elif 1.5 <= t2 <= 1.7 :
                bits += "1"

        elif 1.1 <= t1 <= 1.2 :
            print (int(bits, base=2).to_bytes(len(bits)//8, byteorder='big').decode())
            bits = ""
            offset += delta
            break     

        offset += delta
