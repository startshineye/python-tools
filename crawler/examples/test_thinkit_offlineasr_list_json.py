#! /usr/bin/env python
# -*- coding=utf-8 -*-
import base64
import json
import threading
import os
import time
import datetime
import signal
import requests
import sys
from datetime import datetime
from Queue import Queue
reload (sys)
sys.setdefaultencoding('utf-8')

SERVER_IP = "127.0.0.1"
SERVER_PORT = 20100
SERVER_URI = 'ability/offlineasr'
#SERVER_URI = '/offlineasr'
#SERVER_URI = '/AuthServer'

kFiledir = './voice'
kWavListFilename = 'test.list'  # 语音文件列表名
kResultTxtFilename = 'result.txt'  # 结果文件名
kCutHead = False  # 是否去头
kSendSilentPacketNum = 5
kSendSilent = False
kchannels = 0
kstereo_on = 3
kThreadNum = 1 # 线程数
kType = '1' # 使用第几个集群
#kpostfix = '.xml' #获取结果类型
kpostfix = 'kh.wav' #获取结果类型
kOnePacketLen = 16000  # 每包大小，最好设置为1600

USER = 'lvxiangyang'
TOKEN = 'b00f837094a84641977a1e923d54bfba'
gIsSelectUser = 'false'
gIsAddUser = 'false'
gIsDelUser = 'false'
expiredTime = 0
passWord = 'abc'
threadNum = 10
trafficNum = 100

gIsSetThread = 'false'
#1:查询线数，2：设置线数
g_Type = '1'
g_SetthreadIp = '127.0.0.1'
g_SetthreadNum = '20'

gFileTpye = 'offline_stream' #发送语音方式：offline_stream,offline_file
gcallBackPath = 'http://127.0.0.1:20100/ability/test1' #回调地址
gserverIp = '127.0.0.1' #文件服务ip地址
gurgent = 1 #任务优先级
gIsHttp = 'false'
gHttpUrl = 'http://127.0.0.1:10001/' #发送文件地址
gGrstimeOut = 3600 #超时时间
gProcTime = 0
gMaxTesponsetime = 0
gFileQueue = Queue()
gThreadLock = threading.Lock()
gSilentBuffer = 0
kPreUrl = "http://%s:%d/%s"
url = kPreUrl % (SERVER_IP, SERVER_PORT, SERVER_URI)
headers = {'content-type': 'application/json','Accept': 'application/json'}

def recog_speech_http_onthread(wavFile):
    
    if (os.path.exists(wavFile) == False) and (gIsHttp != "true"):
       #gThreadLock.acquire()
       resultTxt = "No such file or directory"
       print wavFile + ' ==> ' + resultTxt
       return

    pos_file_type = wavFile.rfind(".")
    if pos_file_type != -1:
        file_type = wavFile[pos_file_type + 1:]
        tmpfile = wavFile[:pos_file_type]
    if kpostfix == ".xml":
        resfilename = tmpfile + kpostfix
    else:
        resfilename = tmpfile + "_" + kpostfix

    session = requests.Session()
    if gFileTpye == 'offline_file':
        if gIsHttp == 'true':
            tmpwavFile = gHttpUrl + wavFile
            print tmpwavFile
            SendFile(session,tmpwavFile,resfilename)
            print "send file end"
            return
        else:
            SendFile(session,wavFile,resfilename)
            print "send file end"
            return
    file = open(wavFile, 'rb')
    file.seek(0, 2)
    audioLen = file.tell()
    file.seek(0, 0)
    if audioLen == 0:
        print wavFile + " audioLen is 0"
        file.close()
        return

    sid = SessionBegin(session)

    if sid != "ssb_request error" and sid != "sid is null":
          idx = 1
          sumAudioLen = 0  
          startTime = 0
          endTime = 0
          if kSendSilent == True:
             for i in range(kSendSilentPacketNum):
                 time.sleep(0.01)
                 audioWriteStatus = AudioWrite(gSilentBuffer,sid,idx,session,file_type)
                 if audioWriteStatus == "audioWrite ok":
                    idx += 1
	         #else:
                    #SessionEnd(sid)	  
                    #return
          isOver = False 
          while isOver == False:
                if (kCutHead == True and kSendSilent == False and idx == 1) or (kCutHead == True and kSendSilent == True and idx == kSendSilentPacketNum + 1):
                  file.seek(44)
                  buffer = file.read(44)
                  sumAudioLen += 44
                buffer = file.read(kOnePacketLen)

                time.sleep(0.1)
                sumAudioLen += len(buffer)

                if idx == 1:
                   audioStatus = "2"
                else:
                   audioStatus = "2"
                if  sumAudioLen >= audioLen:
                    isOver = True
                    audioStatus = "4"
                audioWriteStatus = AudioWrite(buffer,sid,idx,audioStatus,session,file_type)
                #time.sleep(0.05)
                if audioWriteStatus == "audioWrite ok":
                   idx += 1
                else:
                   print audioWriteStatus
                   file.close()
                   return

          file.close()
          procTime = [0]

          result = GetResult(sid,idx,procTime,session)
          #print result
          SessionEnd(sid,session)
          if result is None:       
             resultTxt = "null"             
          elif result:
	     if 'wav' in kpostfix:
                 resultTxt = result
             else:
                 resultTxt = result.encode("utf-8")
          else: 
             resultTxt = result
          #endTime = int(round(time.time() * 1000))
          #gThreadLock.acquire()
          #procTime = endTime - startTime
          global gProcTime, gMaxTesponsetime
          gProcTime += procTime[0]
          if (procTime[0] > gMaxTesponsetime):
              gMaxTesponsetime = procTime[0]
          #print wavFile + ' ==> ' + resultTxt + ' // time: ' + bytes(procTime[0]) + ' sid: ' + sid
		  
          try:				
              resultFile = open(resfilename, 'w')
          except IOError:
              print"Unable to open file"
              return
          #pos_name = wavFile.rfind("/")
          #if pos_name != -1:
             #wavFile = wavFile[pos_name + 1:]

          resultFile.write(resultTxt)
          resultFile.close()
          #gThreadLock.release()

    else:
      print "sid is null"

def SendFile(session,voiceFilePath,sttFilePath):
    sendPayLoad = {
                  "method":gFileTpye,
                  "jsonrpc": "2.0",
                  "params": {
                      "type": kType,
                      "postfix": kpostfix,
                      "user": USER,
                      "token": TOKEN,
                      "voiceFilePath": voiceFilePath,
                      "sttFilePath": sttFilePath,
                      "callBackPath": gcallBackPath,
                      "serverIp": gserverIp,
                      "channels": kchannels,
                      "stereo_on": kstereo_on,
                      "urgent": gurgent
                  },
                  "id": 1
                 }
    sendReponse = session.post(url, json=sendPayLoad, headers=headers)
    if sendReponse.status_code != 200:
       print "send_request error"
       return "send_request error"
    else:
       sendResult = base64.b64decode(sendReponse.text)
       sendData = json.loads(sendResult)
       print sendData

def SessionDeluser(session):
    authPayLoad = {
                  "method":"delete_user",
                  "jsonrpc": "2.0",
                  "params": {
                      "engine_type": 2,
                      "passWord": passWord,
                      "user": USER
                  },
                  "id": 1
                 }
    #ssbReponse = session.post(url, json=ssbPayLoad, headers=headers,verify=False)
    authReponse = session.post(url, json=authPayLoad, headers=headers)
    if authReponse.status_code != 200:
       print "auth_request error"
       return "auth_request error"
    else:
       authResult = base64.b64decode(authReponse.text)
       authData = json.loads(authResult)
       print(authResult)
       if 'result' in authData:
          retcode = authData['result']['code']
          print retcode
          if retcode == 0:
             return authData
          else:
             return "code is not 0"

def SessionSetThread(session):
    SetThreadPayLoad = {
                  "method":"setup_thread",
                  "jsonrpc": "2.0",
                  "params": {
                      "type": g_Type,
                      "threadNum": g_SetthreadNum,
                      "machinfo": g_SetthreadIp
                  },
                  "id": 1
                 }
    #ssbReponse = session.post(url, json=ssbPayLoad, headers=headers,verify=False)
    print SetThreadPayLoad
    SetThreadReponse = session.post(url, json=SetThreadPayLoad, headers=headers)
    if SetThreadReponse.status_code != 200:
       print "SetThread_request error"
       return "SetThread_request error"
    else:
       SetThreadResult = base64.b64decode(SetThreadReponse.text)
       SetThreadData = json.loads(SetThreadResult)
       print(SetThreadResult)
       if 'result' in SetThreadData:
          retcode = SetThreadData['result']['ret']
          #print retcode
          if retcode == 0:
             msg = SetThreadData['result']['msg']
             #print msg
             return msg
          else:
             print SetThreadData
             return "code is not 0"

def SessionAdduser(session):
    authPayLoad = {
                  "method":"add_user",
                  "jsonrpc": "2.0",
                  "params": {
                      "engine_type": 2,
                      "passWord": passWord,
                      "user": USER,
                      "threadNum": threadNum,
                      "trafficNum": trafficNum
                  },
                  "id": 1
                 }
    #ssbReponse = session.post(url, json=ssbPayLoad, headers=headers,verify=False)
    authReponse = session.post(url, json=authPayLoad, headers=headers)
    if authReponse.status_code != 200:
       print "auth_request error"
       return "auth_request error"
    else:
       authResult = base64.b64decode(authReponse.text)
       authData = json.loads(authResult)
       print(authResult)
       if 'result' in authData:
          retcode = authData['result']['code']
          print retcode
          if retcode == 0:
             token = authData['result']['data']['token']
             print token
             return authData
          else:
             print authData
             return "code is not 0"

def SessionAuth(session):
    authPayLoad = {
                  "method":"select_user",
                  "jsonrpc": "2.0",
                  "params": {
                      "engine_type": 2,
                      "user": USER,
                      "requestType": "http" 
                  },
                  "id": 1
                 }
    #ssbReponse = session.post(url, json=ssbPayLoad, headers=headers,verify=False)
    authReponse = session.post(url, json=authPayLoad, headers=headers)
    if authReponse.status_code != 200:
       print "auth_request error"
       return "auth_request error"
    else:
       authResult = base64.b64decode(authReponse.text)
       authData = json.loads(authResult)
       #authData = json.loads(authResult)
       #authData = json.loads(authReponse.text)
       print(authResult)
       #print(authData['result']['sid'])
       if 'result' in authData:
          retcode = authData['result']['code']
          print retcode
          if retcode == 0:
             #token = authData['result']['data']['token']
             #print token
             #return token
             return authData
          else:
             return "code is not 0" 
        
def SessionBegin(session):
    #session = requests.Session() 
    ssbPayLoad = {
                  "method":gFileTpye,
                  "jsonrpc": "2.0",
                  "params": {
                      "cmd": "ssb",
                      "type": kType,
                      "postfix": kpostfix,
                      "user": USER,
                      "token": TOKEN
                  },
                  "id": 1
                 }
    #print ssbPayLoad
    #print url
    ssbReponse = session.post(url, json=ssbPayLoad, headers=headers,verify=False)
    #ssbReponse = session.post(url, json=ssbPayLoad, headers=headers)
    if ssbReponse.status_code != 200:
       print "ssb_request error"
       return "ssb_request error"
    else:
       ssbResult = base64.b64decode(ssbReponse.text)
       ssbData = json.loads(ssbResult)
       #ssbData = json.loads(ssbResult)
       #ssbData = json.loads(ssbReponse.text)
       print(ssbResult)
       #print(ssbData['result']['sid'])
       sid = ""
       if 'result' in ssbData:
          sid = ssbData['result']['sid']
          return sid
       else:
          return "sid is null"

def AudioWrite(voiceBuffer,sid,idx,audioStatus,session,file_type):
    session = requests.Session()
    voice = base64.b64encode(voiceBuffer) 

    audioWritePayLoad = {
                          "jsonrpc": "2.0",
                          "method": gFileTpye,
                          "params": {
                              "cmd": "auw",
                              "type": "1",
                              "sid": sid,
                              "postfix": file_type,
                              "data":voice,
                              "audioStatus":audioStatus,
                              "channels": kchannels,
                              "stereo_on": kstereo_on,
                              "urgent": gurgent
                          },
                          "id": 1
                        }
    audioWriteReponse = session.post(url, json=audioWritePayLoad, headers=headers,verify=False)
    #audioWriteReponse = session.post(url, json=audioWritePayLoad, headers=headers)
    if audioWriteReponse.status_code != 200:
       return "audioWrite_request error"
    else:
       audioWriteResult = base64.b64decode(audioWriteReponse.text)
       audioWriteData = json.loads(audioWriteResult)
       if 'error' in audioWriteData:
           print audioWriteData
           return "audioWrite is error"
       #print(audioWriteReponse.text)
       #print audioWriteData
       #audioWriteData = json.loads(audioWriteReponse.text)
       #print(txtWriteResult)
       #print(audioWriteData["error"])
       return "audioWrite ok"

def GetResult(sid,idx,procTime,session):
    #session = requests.Session()
    grsisOver = False
    timeOut = 1
    while grsisOver == False:
          getResultPayLoad ={
                        "jsonrpc": "2.0",
                        "method": gFileTpye,
                        "params": {
                            "cmd": "grs",
                            "sid": sid,
                            "type": "2"
                        },
                        "id": 1                  
                      }
    
          startTime_ms = 0
          endTime_ms = 0
          startTime_ms = int(round(time.time() * 1000))
          getResultReponse = session.post(url, json=getResultPayLoad, headers=headers,verify=False)
          #getResultReponse = session.post(url, json=getResultPayLoad, headers=headers)
          endTime_ms = int(round(time.time() * 1000))
          procTime[0] = endTime_ms - startTime_ms
          #print '// time: ' + bytes(procTime[0])
          if timeOut == gGrstimeOut:
               print sid + " is timeout!!!"
               return "grs request is timeout"
          if getResultReponse.status_code != 200:
               return "grs request is error"
          else:
              if getResultReponse.text !="":
                  getResult = base64.b64decode(getResultReponse.text)
                  #print getResult
                  getResultData = json.loads(getResult)
                  #getResultData = json.loads(getResultReponse.text)
           
                  if 'result' in getResultData:
                      #getResult = base64.b64decode(getResultData['result']['result'])
                      getrecStatus = getResultData['result']['recStatus']
                      #print getrecStatus
                      if getrecStatus != 2:
                          grsisOver = True
                          if 'wav' in kpostfix:
                              getResult = base64.b64decode(getResultData['result']['result'])
                          else:
                              getResult = getResultData['result']['result']
                          return getResult
                      else:
                          time.sleep(1)
                          timeOut = timeOut + 1

                  else:
	                   return "result is null"
              else:
	               return "grs reponse is null"
       

def SessionEnd(sid,session):
    #session = requests.Session()
    sessionPayLoad ={
                      "jsonrpc": "2.0",
                      "method": gFileTpye,
                      "params": {
                          "cmd": "sse",
                          "type": "2",
                          "sid": sid,
                      },
                      "id": 1   
                  
                    }
    sessionReponse = session.post(url, json=sessionPayLoad, headers=headers,verify=False)
    #sessionReponse = session.post(url, json=sessionPayLoad, headers=headers)
    if sessionReponse.status_code != 200:
       print "session_request error"
    else:
       sessionResult = base64.b64decode(sessionReponse.text)
       sessionData = json.loads(sessionResult)
       #sessionData = json.loads(sessionReponse.text)
   

def RecogSpeechHttpMultithread():
    while gFileQueue.qsize() > 0:
        recog_speech_http_onthread(gFileQueue.get())

def Stop(signum, frame):
    sys.exit(0)

def endWith(*endstring):
    ends = endstring

    def run(s):
        f = map(s.endswith, ends)
        if True in f: return s

    return run

if __name__ == '__main__':
	if gIsSetThread == 'true':
            session = requests.Session()
            retdata = SessionSetThread(session)
            print retdata
            sys.exit()
        if gIsDelUser == 'true':
            session = requests.Session()
            retdata = SessionDeluser(session)
            print retdata
            sys.exit()
        if gIsAddUser == 'true':
            session = requests.Session()
            retdata = SessionAdduser(session)
            if retdata != "code is not 0":
                TOKEN = retdata['result']['data']['token']
                url = retdata['result']['data']['engine_url']
                print TOKEN
                print url
                sys.exit()
            else:                
                print "AddUser is error and exit"
                sys.exit()
        #"""
        if gIsSelectUser == 'true':
            authsession = requests.Session()
            retdata = SessionAuth(authsession)
            if retdata != "code is not 0":
                TOKEN = retdata['result']['data']['token']
                url = retdata['result']['data']['engine_url']
                print TOKEN
                print url
                #sys.exit()
            else:
                print "Get token is error and exit"
                sys.exit()
        #"""
        if gIsHttp != 'true':
            os.system('rm -rf ' + kResultTxtFilename)
            file_object = open(kWavListFilename, 'w')
            for root, dirs, files in os.walk(kFiledir):
                for file in files:
                    file_object.write(kFiledir + '/' + file + '\n')
            file_object.close()
       #while 1:
        if (kSendSilent):
           silentFile = open("TheTruth.wav", "rb")
           gSilentBuffer = silentFile.read(kOnePacketLen)
           silentFile.close()
        signal.signal(signal.SIGINT, Stop)
        signal.signal(signal.SIGTERM, Stop) 

        wavList = open(kWavListFilename, 'r')
        for line in wavList.readlines():
            line = line.strip()
            gFileQueue.put(line)
        wavList.close()
        listSize = gFileQueue.qsize()

        threads = []
        for i in xrange(kThreadNum):
            trd = threading.Thread(target=RecogSpeechHttpMultithread)
            trd.setDaemon(True)
            threads.append(trd)
            trd.start()
        while 1:
            alive = False
            for i in xrange(kThreadNum):
                alive = threads[i].isAlive()
                if alive:
                    break
            if not alive:
                break

        print "number of files processed: " + bytes(listSize)
        #print "max responsetime: " + bytes(gMaxTesponsetime)
        #print "average responsetime: " + bytes(gProcTime/listSize)
