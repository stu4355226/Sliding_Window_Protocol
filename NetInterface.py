#-----------------------------------------------------
# [netsim] edu.fit.icis.netsim
# User: mcarvalho
# Date: 7/24/14 - 3:20 PM
# Copyright (c) 2014 Florida Institute of Technology
# All rights reserved.
#-----------------------------------------------------

import threading
import copy
import math
#import datetime
import time
import traceback
import sys

class NetInterface:
    def __init__(self, channel, bandwidth, x, y):
        self._channel = channel
        self._bandwidth = bandwidth
        if self._bandwidth <= 0:
            self._bandwidth = 8

        self._active = True
        self._xpos = x
        self._ypos = y
        self._rcvBuffer = []
        self.__lock = threading.RLock()
        self.__event = threading.Event()
        #self.__event.clear()

    def getChannelNumber(self):
        return self._channel.getNumber()

    def setNewChannel(self, ch):
        self._channel = ch

    def isChannelBusy(self):
        return self._channel.isBusy()

    #long write (byte[] payload) throws InterruptedException
    def write(self, payloads):
        if self._active == True:
            start = time.time()
            #send each packet with transmission delay
            for payload in payloads:
                nbits = len(payload) * 8

                #if _bandwidth = -1, no delay
                #if _bandwidth = 0, no transmission
                #if _bandwidth > 0, delay = number of bits / _bandwidth
                delay = 0
                if self._bandwidth > 0:
                    #delay = 1000000 * (nbits / self._bandwidth)
                    delay = nbits / self._bandwidth

                if self._bandwidth != 0:
                    self._channel.startWriting(payload, self)
                    #TimeUnit.MICROSECONDS.sleep(delay)
                    #time.sleep(delay)

            #send the packets from current interface to other interface through channel
            #channel can be considered as a calbe with propogation delay
            if self._bandwidth != 0:
                self._channel.finishWriting(self)

            return time.time() - start

        return 0

    def read(self):
        received = []
        while len(self._rcvBuffer) == 0:
            try:
                self.__event.wait()
                break
            except KeyboardInterrupt:
                print traceback.print_stack()
                
        with self.__lock:
            while len(self._rcvBuffer) > 0:
                received.append(copy.deepcopy(self._rcvBuffer.pop(0)))

        self.__event.clear()
        return received

    def getDistanceFrom(self, fromX, fromY):
        distance = 0;
        distance = math.sqrt((self._xpos-fromX)*(self._xpos-fromX) + (self._ypos-fromY)*(self._ypos-fromY))
        return distance

    def getXpos(self):
        return self._xpos

    def getYpos(self):
        return self._ypos

    #######################################################
    def receivePayload(self, payloads, fromX, fromY):
        with self.__lock:
            distance = self.getDistanceFrom(fromX,fromY)
            delay = distance / self._channel.getPropagationSpeed()

            #sleep for the delay
            if type(payloads) is str:
                self._rcvBuffer.append(copy.deepcopy(payloads))
            elif type(payloads) is list:
                self._rcvBuffer.extend(copy.deepcopy(payloads))
            else:
                print "Error: type of payloads is not correct."

            self.__event.set()

    def terminate(self):
        self._channel = None
        self._active = False

if __name__ == '__main__':
    NetInterface(0, 1, 2, 3)

