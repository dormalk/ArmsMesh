from rfbridge import RFBridge 
import threading
import time
import platform
from Message import Message
from redisConnection import RedisTools
from config import Config


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
                                message = Message()
                                message.set_data(sense.collect())
                                message.set_dest(0)
                                msg = message.get_message()
                                #print msg
                                bridge.write(msg)
                                #Here push msg to redis
                                time.sleep(1)

def main():
        print "Running..."
        t = threading.Thread(name = 'rfbridge',target=bridge.begin)
        t.start()
        time.sleep(2)
        bridge.set_nodeid(conf.node_id)
        run()

if __name__ == "__main__":
        main()


