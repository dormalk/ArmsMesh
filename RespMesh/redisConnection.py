import redis 
import json
TimeOut =   100
HOST    =   '127.0.0.1'
PORT    =   6379
DB      =   0
GPS =   "GPS"
ACC =   "ACC"
PULS    =   "PULS"
EMERG   =   "Emerg"

class RedisTools():
    def __init__ (self):
        self.con    =   redis.Redis(host    =   HOST,   port    =   PORT,   db  =   DB)
        self.pipe   =   self.con.pipeline()
        self.timeOut    =   TimeOut   
    
    def pipeLpush(self,key,value):
        self.con.lpush(key,value)
    	self.con.expire(key, 100)
    def pipeRpop(self,key):
        self.pipe.rpop(key)
    
    def pipeRpush(self,key,value):
        self.pipe.rpush(key,value).expire(key,self.timeOut)
    
    def pipeLpop(self,key):
        self.pipe.lpop(key)
    
    def pipeExecute(self):
        self.pipe.execute()
    
    def lpop(self,key):
        return self.con.lpop(key)
    
    def rpop(self,key):
        return self.con.rpop(key)
    
    def llen(self,key):
        return self.con.llen(key)
    
    def lrange(self,key,s,e):
        return self.con.lrange(key,s,e)
    
    def ttl(self,key):
        return self.con.ttl(key)
    
    def emptyGPS(self):
        times   =   int(self.llen(GPS))
        for i   in  range(times):
            print   i,  self.lpop(GPS)
    
    def emptyACC(self):
        times   =   int(self.llen(ACC))
        for i   in  range (times):
            print   i,   self.lpop(ACC)
    
    def emptyPuls(self):
        times = int(self.llen(PULS))
        for i   in  range (times):
            print   i,   self.lpop(PULS)



r = RedisTools()

r.pipeLpush("G","0.0.0")
print r.lpop("G")
    
