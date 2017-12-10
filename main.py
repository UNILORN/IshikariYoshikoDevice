#-*- coding:utf-8 -*-
#
# Copyright (c) OPTiM Corporation 2017. All rights reserved.
# Permission to use, copy, modify and redistribute are strongly controlled
# under the rights of OPTiM Corporation.
#

import CiosRaspberryHat
#import SensorPutLed
import sys
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv

if __name__ == '__main__':
    url = "wss://api.optim.cloud/v1/messaging"
    channel = ""

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    token = os.environ.get("ACCESS_TOKEN")

    cios = CiosRaspberryHat.CiosRaspberryHat(url,channel,token)
    #gyro = GyroscopeLed.GyroscopeLed()

    message = cios.getSensorData()
    #sp = SensorPutLed.SensorPutLed(message)
    
    cios.connection()
 
    LedTime = 0.01

    while True:
        time.sleep(LedTime)
        message = cios.getSensorData()
        
        if message != "error":
            sp.setSensorData(message)

        cios.sendMessage(message)