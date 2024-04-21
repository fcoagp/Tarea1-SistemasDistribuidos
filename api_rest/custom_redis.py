import random
import redis

class CustomRedisCacheType:    
    def get(self,redis_hosts,id):
        pass
    
    def set(self,redis_hosts,id,data):
        pass


class CentralCache(CustomRedisCacheType):
    def __init__(self):
        super()
    
    def get(self,redis_hosts,id):
        redis_host = list(redis_hosts.keys())[0]
        return redis_host,redis_hosts[redis_host].get(id)
    
    def set(self,redis_hosts,id,data):
        redis_host = list(redis_hosts.keys())[0]
        redis_hosts[redis_host].set(id,data)
    

class DuplicateCache(CustomRedisCacheType):
    def __init__(self):
        super()
        
    def get(self,redis_hosts,id):
        redis_host = list(redis_hosts.keys())[random.randrange(0,len(redis_hosts))]
        return redis_host,redis_hosts[redis_host].get(id)
    
    def set(self,redis_hosts,id,data):
        for redis_host in redis_hosts.values():
            redis_host.set(id,data)

class PartitionCache(CustomRedisCacheType):
    def __init__(self):
        super()
        
    def getRedisHost(self,redis_hosts,id):
        return list(redis_hosts.keys())[id % len(redis_hosts)]
    
    def get(self,redis_hosts,id):
        redis_host = self.getRedisHost(redis_hosts,id)
        return redis_host,redis_hosts[redis_host].get(id)
    
    def set(self,redis_hosts,id,data):
        redis_host = self.getRedisHost(redis_hosts,id)
        redis_hosts[redis_host].set(id,data)


class CustomRedis:
    redis_hosts = {}
    cache_type: CustomRedisCacheType = None
    
    def __init__(self, hosts,cache_type):
        for host in hosts:
            self.redis_hosts[host] = redis.Redis(host=host, port=6379, db=0)
            
        if cache_type == 'CENTRAL':
            self.cache_type = CentralCache()
        elif cache_type == 'DUPLICATE':
            self.cache_type = DuplicateCache()
        elif cache_type == 'PARTITION':
            self.cache_type = PartitionCache()
    
    def get(self,id:str):
        return self.cache_type.get(self.redis_hosts,id)
    
    def set(self,id:str,data:str):
        return self.cache_type.set(self.redis_hosts,id,data)
    
    def deleteAllKeys(self):
        for client in self.redis_hosts.values():
            for key in client.keys('*'):
                client.delete(key)
    
    def close(self):
        for client in self.redis_hosts.values():
            for key in client.keys('*'):
                client.close(key)
