import getopt, sys
import http.server
from typing import Counter
from prometheus_client import start_http_server
from prometheus_client import Gauge
from prometheus_client import Counter
from threading import Thread
import random

from time import sleep, perf_counter

# Remove first element of args 
argumentList = sys.argv[1:]
# Options
options = "c:h:e:"
 
# Long options
long_options = ["Cameras=", "HDs=", "Error="]

amountOfCameras = 4
amountOfHDs = 1
errorProbability = 0.05

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-c", "--Cameras"):
            amountOfCameras = int(currentValue)
        elif currentArgument in ("-h", "--HDs"):
            amountOfHDs = int(currentValue)
        elif currentArgument in ("-e", "--Error"):
            errorProbability = float(currentValue)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

print("This code is running with", amountOfCameras, 'cameras and', amountOfHDs, 'HDs')

camGauges = [] 
camCounters = []
hdGauges = [] 
hdCounters = []

def funcThreadCamera(id):
    print('Starting a camera... ', id)
    secondsOffline = 0
    isOffline = False
    while(1):
        caosNumber = random.random()
        if(isOffline):
            if(caosNumber < errorProbability):
                isOffline = False
                secondsOffline = 0
                camGauges[id].set(0)
                print("Camera "+str(id)+" is ONLINE" )
            else:
                camGauges[id].inc()
                secondsOffline+=1
                print("Camera "+str(id)+" is offline for "+ str(secondsOffline) + " seconds") 
        else:
            if(caosNumber < errorProbability):
                camCounters[id].inc() 
                camGauges[id].inc()
                secondsOffline+=1
                isOffline = True
                print("Camera "+str(id)+" is offline for "+ str(secondsOffline) + " seconds") 
        sleep(1)    

def funcThreadHd(id):
    print('Starting a HD... ', id)
    secondsOffline = 0
    isOffline = False
    while(1):
        caosNumber = random.random()
        if(isOffline):
            if(caosNumber < errorProbability):
                isOffline = False
                secondsOffline = 0
                camGauges[id].set(0)
                print("HD "+str(id)+" is ONLINE" )
            else:
                camGauges[id].inc()
                secondsOffline+=1
                print("HD "+str(id)+" is offline for "+ str(secondsOffline) + " seconds") 
        else:
            if(caosNumber < errorProbability):
                camCounters[id].inc() 
                camGauges[id].inc()
                secondsOffline+=1
                isOffline = True
                print("HD "+str(id)+" is offline for "+ str(secondsOffline) + " seconds") 
        sleep(1) 



def createThreads(amtCam, amtHds):
    camThreads = []
    hdThreads = []
    for camera in range(amtCam):
        camThreads.append(Thread(target=funcThreadCamera, args=(camera,)))
        camGauges.append(Gauge('camera_time_stopped_in_seconds_'+str(camera), 'Informs the time that camera '+ str(camera) +' is offline in seconds')) 
        camCounters.append(Counter('camera_numbers_of_times_offline_'+str(camera), 'Informs the numbers of times that camera '+ str(camera) +' was offline')) 
    
    for hd in range(amtHds):
        hdThreads.append(Thread(target=funcThreadHd, args=(hd,)))
        hdGauges.append(Gauge('hd_time_stopped_in_seconds_'+str(hd), 'Informs the time that camera '+ str(hd) +' is offline in seconds')) 
        hdCounters.append(Counter('hd_numbers_of_times_offline_'+str(hd), 'Informs the numbers of times that camera '+ str(hd) +' was offline')) 

    return camThreads, hdThreads

def startThreads(camThreads, hdThreads):
    for camera in camThreads:
        camera.start()
    for hds in hdThreads:
        hds.start()


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World!")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('', 8001), ServerHandler)
    print("Prometheus metrics available on port 8000 /metrics")
    print("HTTP server available on port 8001")
    camThreads, hdThreads = createThreads(amountOfCameras, amountOfHDs)
    startThreads(camThreads, hdThreads)
    server.serve_forever()

