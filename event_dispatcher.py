#!/usr/bin/python

import redis
import signal
import sys
import json

def sigHandler(signal, frame):
  sys.exit(0)


if __name__ == "__main__":

  redisServ = redis.StrictRedis(host='localhost',port=6379, db=0)
  ps = redisServ.pubsub()
  ps.subscribe('alertchannel')
  signal.signal(signal.SIGINT,sigHandler)    

  while True:
     for msgDict in ps.listen():
        keyValueData = redisServ.get(msgDict['data'])
        if keyValueData is not None:
          print " %s keyValueData" % keyValueData
          eventData = json.loads(keyValueData)
          print eventData['kalle']



