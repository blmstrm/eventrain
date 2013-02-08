import SocketServer
import signal
import sys
import redis
import json
import multiprocessing
import gcm

#Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
LISTENING_PORT = 1234
GCM_SECRET = ""

#Print error method
def printError(ErrorType):
  sys.stderr.write("\nEXCEPTION: Caught "+ErrorType+" error.\n")

#Signal handler method
#TODO Nice handling of signals
def sigHandler(signal, frame):
  try:
    dispatch_process.terminate()
    dispatch_process.join() 

    server_process.terminate()
    server_process.join()
  except:
    printError("PROCESS SHUTDOWN")

  print "Shutting down..."
  sys.exit(0)

#Method for dispatching events to GCM
def event_dispatcher():

  ps = redisServ.pubsub()
  ps.subscribe('alertchannel')

  while True:
     for msgDict in ps.listen():
        keyValueData = redisServ.get(msgDict['data'])
        if keyValueData is not None:
          try:
            eventData = json.loads(keyValueData)
          except:
            printError("MALFORMED JSON")
          #TODO deal with eventData['someKey']

#Class to write to redis server
class RedisWriter(SocketServer.BaseRequestHandler):

  def handle(self):
    try:
      self.data = self.request.recv(1024).strip()
    except:
      printError("NO CONNECTION TO CLIENT")
      #TODO Deal with key for event
    if self.data is not None:
      redisServ.set('alert1',self.data)
      redisServ.publish('alertchannel','alert1')
  

if __name__ == "__main__":

  #Initiate signal handler
  signal.signal(signal.SIGINT,sigHandler)    

  #Init connection to Redis Server
  redisServ = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT, db=0)
   

  #Init TCP listening socket and launch process
  try:
    server = SocketServer.TCPServer(("localhost", LISTENING_PORT), RedisWriter)
  except:
    printError("BUSY SOCKET")
    print "Socket is busy. Maybe you already have an instance of er_server.py running?"
    sys.exit(1)

  #Init and launch server process
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
