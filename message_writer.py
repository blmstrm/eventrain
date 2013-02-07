#!/usr/bin/python
import SocketServer
import signal
import sys
import redis
import json

def sigHandler(signal, frame):
  sys.exit(0)

class RedisWriter(SocketServer.BaseRequestHandler):

  def handle(self):
    self.data = self.request.recv(1024).strip()
    #TODO Catch exceptions
    #TODO Deal with key for event
    print  redisServ.set('alert1',self.data)
    print redisServ.publish('alertchannel','alert1')

if __name__ == "__main__":
  signal.signal(signal.SIGINT,sigHandler)    
  redisServ = redis.StrictRedis(host='localhost',port=6379, db=0)
  HOST,PORT = "localhost",1234
  server = SocketServer.TCPServer((HOST, PORT), RedisWriter)
  print "Waiting for client"
  server.serve_forever()



