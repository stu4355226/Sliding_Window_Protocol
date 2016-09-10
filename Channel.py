#-----------------------------------------------------
# [netsim] edu.fit.icis.netsim
# User: mcarvalho
# Date: 7/24/14 - 3:16 PM
# Copyright (c) 2014 Florida Institute of Technology
# All rights reserved.
#-----------------------------------------------------

import collections
import copy
import math
import random
import sys
import time
import threading

# Channel class
class Channel: 
    def __init__(self, number, BER=0, pDelay=0): # init with list of points
        self._pendWrt = {}
        self._interfaces = {}
        #self._interfaces = collections.defaultdict(list)
        self._channelNumber = number

        self._BER = BER

        self._pDelay = pDelay

        #_channelNumber = 0;
        #self._scrambleLevel = 5            
        self._scrambleLevel = 0            

        self._propSpeed = 300000000.0     
        self._rand = random
        self.__lock = threading.RLock()

    def getNumber(self):
        return self._channelNumber

    def addInterface(self, iFace):
        if iFace not in self._interfaces:
            self._interfaces[iFace] = None
            self._pendWrt[iFace] = []

    def removeInterface(self, iFace):
        del(self._pendWrt[iFace])
        del(self._interfaces[iFace])

    def startWriting(self, payload, iFace):
        pendWrite = copy.deepcopy(payload)
        self._pendWrt[iFace].append(pendWrite)
        if len(self._pendWrt[iFace]) > 1:
            self.__scramble(iFace)

    def finishWriting(self, iFace):
        #payload = self._pendWrt.pop(iFace, None)
        time.sleep(self._pDelay)
        payloads = []
        while len(self._pendWrt[iFace]) > 0:
            payloads.append(self._pendWrt[iFace].pop(0))

        for payload in payloads:
            if payload is not None:
                self.__applyBER(payload)

        for netIFace in self._interfaces.iterkeys():
            if netIFace != iFace:
                netIFace.receivePayload(copy.deepcopy(payloads), iFace.getXpos(), iFace.getYpos())

    def getPropagationSpeed(self):
        return self._propSpeed

    def isBusy(self):
        if len(self._pendWrt) > 0:
            return true

        return false

    def setBER(self, BER):
        self._BER = BER

    def getBER():
        return self._BER

    def __scramble(self, iFace):
        for payload in self._pendWrt[iFace]:
            if len(payload) > 0:
                for i in range(0, self._scrambleLevel):
                    payload[self._rand.randrange(len(payload))] = chr(32+self._rand.randrange(64))

    def __applyBER(self, payload):
        self._nber = (1 - self._BER) % 1;
        self._prob = math.pow(self._nber, (8*len(payload)))
        chance = math.fabs(self._rand.randrange(1000))/1000.0
        if chance > self._prob:
            if len(payload) > 0:
                for i in range(0, self._scrambleLevel):
                    #payload[math.abs(self._rand.randrange(len(payload)))] = chr(32+self._rand.randrange(32))
                    payload_list = list(payload)
                    payload_list[self._rand.randrange(len(payload))] = chr((32+self._rand.randrange(32)))
                    payload = ''.join(payload_list)

if __name__ == '__main__':
    ch = Channel(0, 1)
    ch.addInterface(2)

