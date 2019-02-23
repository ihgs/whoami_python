import sqlite3
import random
import string
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Session(metaclass=Singleton):

    _sessions = {}

    def _now(self):
        return datetime.now().timestamp() + 60*30

    def _is_not_expire(self, expire_time):
        return expire_time < self._now()
    
    def new(self, value):
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        self._sessions[key] = {
            'value': value,
            'expire_time': self._now()
        }
        return key

    def get(self, key):
        sess = self._sessions[key]
        if sess is None:
            return None

        if (self._is_not_expire(sess['expire_time'])):
            sess['expire_time'] = self._now()
            return sess['value']

