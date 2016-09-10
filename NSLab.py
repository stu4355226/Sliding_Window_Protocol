#-----------------------------------------------------
# [netsim] edu.fit.icis.netsim
# User: mcarvalho
# Date: 7/24/14 - 3:14 PM
# Copyright (c) 2014 Florida Institute of Technology
# All rights reserved.
#-----------------------------------------------------

from Channel import *
from NetInterface import *

class NSLab:
    NSLab = None
    _NSLab = None

    def __init__(self):
        self._channels = {}

    @staticmethod
    def getNetSim():
        if NSLab._NSLab is None:
            NSLab._NSLab = NSLab()

        return NSLab._NSLab;

    #def setChannel(self, channelNumber):
    def setChannel(self, *args):
        args_len = len(args)
        if(args_len == 1):
            BER = 0.0
            pDelay = 0
        elif(args_len == 2):
            BER = args[1]
            pDelay = 0
        elif(args_len == 3):
            BER = args[1]
            pDelay = args[2]
        else:
            print "Unknown condition"

        channelNumber = args[0]

        ch = self._channels.get(channelNumber)
        if ch is None:
            ch = Channel(channelNumber, BER, pDelay)
            self._channels[channelNumber] = ch
        else:
            ch.setBER(BER)

    #def getInterface(int channelNumber, double bandwidth) throws Exception
    def getInterface(self, *args):
        args_len = len(args)
        if(args_len == 2):
            xpos = 0 
            ypos = 0
        elif(args_len == 4):
            xpos = args[2] 
            ypos = args[3]
        else:
            print "Unknown condition"

        channelNumber = args[0] 
        bandwidth = args[1]

        ch = self._channels[channelNumber]
        if ch is None:
            raise Exception("Unknown Channel Number (" + str(channelNumber) + "). You must first create the channel!")

        nIface = NetInterface(ch,bandwidth,0,0)
        ch.addInterface(nIface)
        return nIface

    #def setInterfaceChannel(nIface, channelNumber) throws Exception
    def setInterfaceChannel(nIface, channelNumber):
        ch = self._channels[channelNumber]
        if ch is None:
            raise Exception("Unknown Channel Number (" + str(channelNumber) + "). You must first create the channel!")

        nIface.setNewChannel(ch)

