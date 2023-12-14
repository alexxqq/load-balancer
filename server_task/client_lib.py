import requests

class Client():
    def __init__(self, addr, step = 10):
        self.addr = addr
        self.stats = {}
        self.counter = 0
        self.step = step  

    def get_stats(self):
        s = requests.get(f"http://{self.addr}/stats")
        self.stats = s.json()
    
    def update_stats(self):
        self.counter = (self.counter + 1) % self.step
        if self.counter == 0:
            self.get_stats()

    def send(self, message):
        self.update_stats()
        dn_addr = min(self.stats.items(), key = lambda pair : int(pair[1]))[0]
        requests.post(f"http://{dn_addr}/send", data = message)    

    def receive(self):
        self.update_stats()
        dn_addr = max(self.stats.items(), key = lambda p : int(p[1]))[0]
        return requests.get(f"http://{dn_addr}/receive").text     
    


