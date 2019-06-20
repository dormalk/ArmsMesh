from rfbridge import RFBridge 
import threading
import time
import platform
from Message import Message
from redisConnection import RedisTools
from config import Config
from demo import commander

if platform.system() == 'Windows':
        from sensorTest import GPS,ACC,PULSE,EMARG
else:
        from sensor import GPS,ACC,PULSE,EMARG


conf = Config()
redisTool = RedisTools()
bridge = RFBridge(conf.node_id,redisTool)

sensors = []
sensors.append(GPS())
sensors.append(ACC())
sensors.append(PULSE())
sensors.append(EMARG())

def run():
        timer = int(round(time.time() * 1000))
        while(1):
                delta = int(round(time.time() * 1000))-timer
                if delta > 3000:
                        timer = int(round(time.time() * 1000))
                        for sense in sensors:
                                try:
                                        message = Message()
                                        message.set_data(sense.collect())
                                        message.set_dest(0)
                                        msg = message.get_message()
                                        #print msg
                                        bridge.write(msg)
                                        #Here push msg to redis
                                        time.sleep(0.5)
                                except (ValueError) as e:
                                        #print e
                                        time.sleep(0.5)
                                
def main():
        print "Running..."
                                        
        t = threading.Thread(name = 'rfbridge',target=bridge.begin)
        t.start()
        bridge.set_nodeid(conf.node_id)

        time.sleep(10)
        bridge.set_nodeid(conf.node_id)
        time.sleep(10)
        if conf.node_id %10 == 0 :
                comand = commander()
                s= threading.Thread(name = 'run',target=run)
                s.start()
                comand.start(conf.node_id)
        else:
                run()

if __name__ == "__main__":
        main()


