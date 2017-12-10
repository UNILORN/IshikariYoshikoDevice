#-*- coding:utf-8 -*-
#
# Copyright (c) OPTiM Corporation 2017. All rights reserved.
# Permission to use, copy, modify and redistribute are strongly controlled
# under the rights of OPTiM Corporation.
#

from websocket import create_connection
import sys
import json
import time
import os
from sense_hat import SenseHat

#
# CiosRaspberryHat
# 
# CiosとRaspberryPI3+SenseHatを接続するクラス
# websocket, SenseHatModuleを使用
#
class CiosRaspberryHat:
    
    #
    # Constructor 
    # 
    # url string WebsocketのURL
    # channel_id string CiosのチャネルID
    # access_token string Ciosのアクセストークン
    #
    def __init__(self,url,channel_id,access_token):
        self.url = url
        self.channel = channel_id
        self.token = access_token
        self.ws = 0

        self.sense = SenseHat() # SenseHat　インスタンス作成
        self.sense.set_imu_config(True, True, True) # 加速度センサーの有効化

        self.connectCount = 0
        self.screen = "top"
    #
    # connection
    #
    # WebSocketへのコネクションを貼る 
    #
    def connection(self):
        try:
            ws_url = self.url + "?" + "channel_id=" + self.channel + "&access_token=" + self.token
            print("--------------- WebSocket Connection ---------------")
            print("ConnectionURL: "+ ws_url)
            print("--------------- WebSocket Connection ---------------")
            self.sense.show_letter("C",text_colour=[0,255,255])
            self.ws = create_connection(ws_url)
        except:
            print("Websocket Connection Error...")
            self.sense.show_letter("E",text_colour=[255,0,0])
            self.errorReConnect()
            return "error"

    #
    # getSensorData
    #
    # SenseHatからのデータを取得、JSON整形を行う
    # return: Json String 
    #
    def getSensorData(self):
        try:
            humidity      = self.sense.get_humidity()
            temp          = self.sense.get_temperature()
            pressure      = self.sense.get_pressure()
            orientation   = self.sense.get_orientation_degrees()
            compass       = self.sense.get_compass_raw()
            gyroscope     = self.sense.get_gyroscope_raw()
            accelerometer = self.sense.get_accelerometer_raw()
            message = {
                "humidity":   humidity,
                "temperature":temp,
                "pressure":   pressure,
                "degrees_p":  orientation["pitch"],
                "degrees_r":  orientation["roll"],
                "degrees_y":  orientation["yaw"],
                "compass_x":  compass["x"],
                "compass_y":  compass["y"],
                "compass_z":  compass["z"],
                "gyroscope_x":   gyroscope["x"],
                "gyroscope_y":   gyroscope["y"],
                "gyroscope_z":   gyroscope["z"],
                "accelerometer_x":accelerometer["x"],
                "accelerometer_y":accelerometer["y"],
                "accelerometer_z":accelerometer["z"]
            }
            send_message = json.dumps(message)
            return send_message

        except:
            print("getSensorData Error...")
            self.ws.close()
            self.sense.show_letter("E",text_colour=[255,0,0])
            self.errorReConnect()
            return "error"

    #
    # sendMessage
    #
    # message string 送信するメッセージ（Json形式）
    #
    def sendMessage(self,message):
        try:
            print("--------------- WebSocket Send Message ---------------")
            print(message)
            print("--------------- WebSocket Send Message ---------------")
            self.ws.send(message)
        except:
            print("Websocket Send Error...")
            self.ws.close()
            self.sense.show_letter("E",text_colour=[255,0,0])
            self.errorReConnect()
            return "error"

    #
    # Error ReConnect WebSocket
    #
    # message string 送信するメッセージ（Json形式）
    #
    def errorReConnect(self):
        try:
            if self.connectCount > 0:   # ErrorCount カウント数以上のエラーで停止
                raise
            self.connectCount += 1
            for v in range(self.connectCount):  # Error数に応じて、待機時間を追加
                print("Wait ::: "+str(self.connectCount-v)+" sec")
                time.sleep(1)
            self.connection()
        
        except:
            print("Websocket connection Error count : "+str(self.connectCount)+" Over")
            self.sense.show_letter("E",text_colour=[255,0,0])
            time.sleep(0.5)
            self.sense.show_letter("E",text_colour=[0,255,0])
            time.sleep(0.5)
            self.sense.show_letter("E",text_colour=[0,0,255])
            time.sleep(0.5)
            self.sense.show_letter("E",text_colour=[255,0,0])
            time.sleep(2)
            self.sense.clear()
            exit()