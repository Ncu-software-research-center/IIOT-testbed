class MockRedis:
    def __init__(self, host, port, password, encoding, decode_responses):
        self.data = {}
    def get(self, name):
        return self.data.get(name, '')
    def hget(self, name, key):
        return self.data.get(name, '').get(key, '')
    def set(self, name, value):
        self.data[name] = value
    def hset(self, name, key, value):
        if name in self.data:
            self.data[name][key] = value
        else:
            self.data[name] = {}
            self.data[name][key] = value