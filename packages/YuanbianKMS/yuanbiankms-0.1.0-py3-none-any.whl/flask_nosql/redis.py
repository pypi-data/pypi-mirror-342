# coding: utf-8
try:
    import redis
except ImportError:
    import os

    os.system("pip install redis")
finally:
    from redis import Redis as NoSqlDB


class Redis:
    def __init__(self, app=None):
        self._redis_client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        redis_url = app.config.get("REDIS_URL", "redis://localhost:6379/0")
        self._redis_client = NoSqlDB.from_url(redis_url)

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['redis'] = self

    def get(self, key, type="str"):
        value = self._redis_client.get(key)
        if value:
            if type == "int":
                return int(value) if value else 0
            return value.decode()
        return None

    def set(self, key, value, ex=300):
        self._redis_client.set(key, value, ex)

    def delete(self, key):
        self._redis_client.delete(key)

    def incr(self, key, amount=1):
        return self._redis_client.incr(key, amount)

    def exists(self, key):
        return self._redis_client.exists(key)

    def expire(self, key, time):
        return self._redis_client.expire(key, time)

    def ttl(self, key):
        return self._redis_client.ttl(key)

    def sadd(self, key, member):
        return self._redis_client.sadd(key, member)

    def smembers(self, key):
        return self._redis_client.smembers(key)

    def sismember(self, key, val):
        return self._redis_client.sismember(key, val)

    def scard(self, key):
        return self._redis_client.scard(key)

    def hmset(self, key, dicts, ex=None):
        res = self._redis_client.hmset(key, dicts)
        if ex:
            self._redis_client.expire(key, ex)
        return res

    def hgetall(self, key):
        data = self._redis_client.hgetall(key)
        data = {k.decode(): v.decode() for k, v in data.items()}
        return data

    def hget(self, key, field):
        data = self._redis_client.hget(key, field)
        return data

    def hdel(self, keys):
        return self._redis_client.hdel(self, *keys)

    def hdel_key(self, key):
        return self._redis_client.delete(key)

    @property
    def client(self):
        return self._redis_client
