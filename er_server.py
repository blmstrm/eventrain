import SocketServer
import signal
import sys
import redis
import json
import multiprocessing
import gcm

#Configuration
HOST = "localhost"
PORT = 1234
GCM_SECRET = ""


#Signal handler method
def sigHandler(signal, frame):
  dispatch_process.terminate()

  server_process.terminate()
  server_process.join()

  sys.exit(0)

#Class to write to redis server
class RedisWriter(SocketServer.BaseRequestHandler):

  def handle(self):
    self.data = self.request.recv(1024).strip()
    #TODO Catch exceptions
    #TODO Deal with key for event
    redisServ.set('alert1',self.data)
    redisServ.publish('alertchannel','alert1')

#Method for dispatching events to GCM
def event_dispatcher():

  ps = redisServ.pubsub()
  ps.subscribe('alertchannel')

  while True:
     for msgDict in ps.listen():
        keyValueData = redisServ.get(msgDict['data'])
        if keyValueData is not None:
          print " %s keyValueData" % keyValueData
          eventData = json.loads(keyValueData)
          print eventData['kalle']


if __name__ == "__main__":

  #Initiate signal handler
  signal.signal(signal.SIGINT,sigHandler)    

  #Init connection to Redis Server
  redisServ = redis.StrictRedis(host='localhost',port=6379, db=0)
   

  #Init TCP listening socket and launch process
  HOST,PORT = "localhost", 1234
  server = SocketServer.TCPServer((HOST, PORT), RedisWriter)
  server_process = multiprocessing.Process(target=server.serve_forever)
  server_process.daemon = True
  server_process.start()

  #Init and launch event_dispatcher process
  dispatch_process = multiprocessing.Process(target=event_dispatcher)
  dispatch_process.daemon = True
  dispatch_process.start()

  #Wait for threads or interrupt on Ctrl-C
  server_process.join()
  dispatch_process.join()
