import random
import numpy as np  
class Network:
    def __init__(self,inp,hid,out):
        self.x = 0
        self.hid = hid
        self.inp = inp
        self.out = out
        self.itoh = np.array([0 for x in range(self.inp*self.hid)])
        self.itoh[random.randrange(0,self.inp*self.hid)] = 1
        self.itoh[random.randrange(0,self.inp*self.hid)] = 1
        self.itoh = self.itoh.reshape(-1,self.hid)

        self.htoo = np.array([0 for x in range(self.hid*self.out)])
        self.htoo[random.randrange(0,self.hid*self.out)] = 1
        self.htoo[random.randrange(0,self.hid*self.out)] = 1
        self.htoo = self.htoo.reshape(-1,self.out)
        

        self.itoo = np.array([0 for x in range(self.inp*self.out)])
        self.itoo[random.randrange(0,self.inp*self.out)] = 1
        self.itoo[random.randrange(0,self.inp*self.out)] = 1
        self.itoo = self.itoo.reshape(-1,self.out)

    def move(self,parameters): 
        input = np.array(parameters)
        hidden = input @ self.itoh
        output1 = hidden @ self.htoo
        output2 = input @ self.itoo
        print(output1+output2)
        return output1+output2

