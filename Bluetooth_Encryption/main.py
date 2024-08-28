import sys
import random

c0_init, c1_init = 0, 0

class LFSR:
    def __init__(self, size, feedback, iv, offset):
        self.size=size
        self.feedback=feedback
        self.iv=iv
        self.registers=iv
        self.offset=offset
    def clock(self):
        output=(self.registers>>self.offset)%2
        temp=self.registers & self.feedback
        i=self.registers%2
        self.registers=self.registers>>1
        while temp>0:
            i= i^(temp%2)
            temp=temp>>1
        self.registers+=(i*(2**(self.size-1)))
        return output
    def getState(self):
        return self.registers

class E0:
    def __init__(self, c0, c1):
        self.c0=c0
        self.c1=c1
        self.c2=0
        self.t1=[0,1,2,3]
        self.t2=[0,3,1,2] 

    def stream(self, l1, l2, l3, l4):

        x1=l1.clock()
        x2=l2.clock()
        x3=l3.clock()
        x4=l4.clock()
        
        y=x1+x2+x3+x4

        s=(y+self.c1)//2

        self.c2 = s ^ self.t1[self.c1] ^ self.t2[self.c0]

        self.c0,self.c1=self.c1,self.c2

        return x1^x2^x3^x4^(self.c0%2)

def key_initialisation(i1,i2,i3,i4):
    l1=LFSR(25,139296,0, 1)
    l2=LFSR(31,557184,0, 1)
    l3=LFSR(33,536871456,0, 6)
    l4=LFSR(39,34359740424,0, 6)
    l1.registers=int("0b"+i1[-25::],2)
    i1=i1[:-25:]
    l2.registers=int("0b"+i2[-31::],2)
    i2=i2[:-25:]
    l3.registers=int("0b"+i3[-33::],2)
    i3=i3[:-25:]
    l4.registers=int("0b"+i4[-39::],2)
    i4=i4[:-25:]
    for _ in range(14):
        temp = l1.feedback & l1.registers
        i = (l1.registers % 2) ^ int(i1[-1])
        l1.registers=l1.registers>>1
        i1=i1[:-1:]
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l1.registers+=(i*(2**24))
    for _ in range(8):
        temp = l2.feedback & l2.registers
        i = (l2.registers % 2) ^ int(i2[-1])
        l2.registers=l2.registers>>1
        i2=i2[:-1:]
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l2.registers+=(i*(2**30))
    for _ in range(6):
        temp = l3.feedback & l3.registers
        i = (l3.registers % 2) ^ int(i3[-1])
        l3.registers=l3.registers>>1
        i3=i3[:-1:]
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l3.registers+=(i*(2**32))
    c0,c1,c2=0,0,0
    t1=[0,1,2,3]
    t2=[0,3,1,2]
    key=""
    for counter in range(200):
        x1=(l1.registers>>1)%2
        x3=(l3.registers>>1)%2
        x2=(l2.registers>>6)%2
        x4=(l4.registers>>6)%2

        temp = l1.feedback & l1.registers
        if len(i1)>0:
            i = (l1.registers % 2) ^ int(i1[-1])
            i1=i1[:-1:]
        else:
            i = (l1.registers % 2)
        l1.registers=l1.registers>>1
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l1.registers+=(i*(2**24))

        temp = l2.feedback & l2.registers
        if len(i2)>0:
            i = (l2.registers % 2) ^ int(i2[-1])
            i2=i2[:-1:]
        else:
            i = (l2.registers % 2)
        l2.registers=l2.registers>>1
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l2.registers+=(i*(2**30))

        temp = l3.feedback & l3.registers
        if len(i3)>0:
            i = (l3.registers % 2) ^ int(i3[-1])
            i3=i3[:-1:]
        else:
            i = (l3.registers % 2)
        l3.registers=l3.registers>>1
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l3.registers+=(i*(2**32))

        temp = l4.feedback & l4.registers
        if len(i4)>0:
            i = (l4.registers % 2) ^ int(i4[-1])
            i4=i4[:-1:]
        else:
            i = (l4.registers % 2)
        l4.registers=l4.registers>>1
        while temp>0:
            i^=(temp%2)
            temp=temp>>1
        l4.registers+=(i*(2**38))

        y=x1+x2+x3+x4

        s=(y+c1)//2

        c2 = s ^ t1[c1] ^ t2[c0]

        if counter>71:
            key = key + str(x1^x2^x3^x4^(c1%2))
        
        c0, c1 = c1, c2
    c0_init,c1_init = c0, c1
    return key

if __name__ == "__main__":
    kc = int(sys.argv[1])
    adr = int(sys.argv[2])
    cl = int(sys.argv[3])
    L = int(sys.argv[4])
    message = sys.argv[5]
    mode = int(sys.argv[6])

    g1=[285, 65599, 16777435, 4294967471, 1099511627833, 281474976711313, 72057594037928085, 18446744073709551643, 4722366482869645215241, 1208925819614629174706709, 309485009821345068724781371, 79228162514264337593543950557, 20282409603651670423947251287197, 5192296858534827628530496329220431, 1329227995784915872903807060280344807, 340282366920938463463374607431768211456]
    g2=[1175844861634428935813091155870789775, 9815912988204713400838090403540975, 35412024868864710189726331142283, 112256740381119350757443988185, 429197933009095916768023111, 210501753318130147820305, 3319837469090077974643, 11649547092320092197, 784501845831757, 6108063835323, 54347703511, 479995577, 2546147, 17271, 137, 1]

    KC = g2[(L-1)] * (kc%g1[L-1])
    KC=bin(KC)
    if len(KC)>130:
        KC=KC[len(KC)-128::]
    else:
        KC=KC[2::]
        while len(KC)<128:
            KC="0"+KC

    cl=bin(cl)[2::]

    adr=bin(adr)[2::]

    i1 = adr[-24:-16:]+cl[-16:-8:]+KC[-104:-96:]+KC[-72:-64:]+KC[-40:-32:]+KC[-8::]+cl[1]
    i2 = adr[-32:-24:]+adr[-8::]+KC[-112:-104:]+KC[-80:-72:]+KC[-48:-40:]+KC[-16:-8:]+cl[-4::]+"001"
    i3 = adr[-40:-32:]+cl[-24:-16:]+KC[-120:-112:]+KC[-88:-80:]+KC[-56:-48:]+KC[-24:-16:]+cl[0]
    i4 = adr[-48:-40:]+adr[-16:-8:]+KC[-128:-120:]+KC[-96:-88:]+KC[-64:-56:]+KC[-32:-24:]+cl[-8:-4:]+"111"

    

    initialization_vector = key_initialisation(i1,i2,i3,i4)

    initialization_vector_1=int("0b" + initialization_vector[0:8:] + initialization_vector[32:40:] + initialization_vector[64:72:] + initialization_vector[96], 2)
    initialization_vector_2=int("0b" + initialization_vector[8:16:] + initialization_vector[40:48:] + initialization_vector[72:80:] + initialization_vector[97:104:], 2)
    initialization_vector_3=int("0b" + initialization_vector[16:24:] + initialization_vector[48:56:] + initialization_vector[80:88:] + initialization_vector[104:112:] + initialization_vector[120] , 2)
    initialization_vector_4=int("0b" + initialization_vector[24:32:] + initialization_vector[56:64:] + initialization_vector[88:96:] + initialization_vector[112:120:] + initialization_vector[121::] , 2)

    lfsr1 = LFSR(25, 139296, initialization_vector_1, 1)
    lfsr2 = LFSR(31, 557184, initialization_vector_2, 6)
    lfsr3 = LFSR(33, 536871456, initialization_vector_3, 1)
    lfsr4 = LFSR(39, 34359740424, initialization_vector_4, 6)

    if mode==1:
        plain_text = ""
        for i in message:
            temp = bin(ord(i))
            temp=temp[2::]
            while len(temp)<8:
                temp="0"+temp
            plain_text += temp

        sender = E0(c0_init, c1_init)
        cipher_text=""
        for i in plain_text:
            cipher_text += str(int(i) ^ sender.stream(lfsr1, lfsr2, lfsr3, lfsr4))

        with open("static/output.txt","w") as file:
            file.write("Kc used: " + str(kc) + "\n")
            file.write("Bluetooth Address used: " + str(adr) + "\n")
            file.write("Clock used: " + str(cl) + "\n")
            file.write("L used: " + str(L) + "\n")
            file.write("Given message : " + message + "\n")
            file.write("Cipher text: "+ cipher_text + "\n")
        
    if mode==2:
        sender = E0(c0_init, c1_init)
        cipher_text=""
        for i in message:
            cipher_text += str(int(i) ^ sender.stream(lfsr1, lfsr2, lfsr3, lfsr4))

        decrypted_message=""

        counter = 0
        while counter<len(cipher_text):
            counter_2 = 0
            temp = ""
            while counter_2<8:
                temp += cipher_text[counter]
                counter += 1
                counter_2 += 1
            decrypted_message += chr(int("0b"+temp, 2))

        with open("static/output.txt","w") as file:
            file.write("Kc used: " + str(kc) + "\n")
            file.write("Bluetooth Address used: " + str(adr) + "\n")
            file.write("Clock used: " + str(cl) + "\n")
            file.write("L used: " + str(L) + "\n")
            file.write("Given message : " + message + "\n")
            file.write("Decrypted text: " + decrypted_message)
