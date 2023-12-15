class Client():
    def init(self, addr, step = 10):
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
        if self.stats == {}:
            raise Exception("Can`t send on empty control node")
        else:
            dn_addr = min(self.stats.items(), key = lambda pair : int(pair[1]))[0]
            with open("info.txt", "r") as file:
                text = file.readlines()
                for i in range(len(text)):
                    if text[i] == f"ID: {dn_addr}\n":
                        text.insert(i + 2, f"{message}, active\n")
                        break
            with open("info.txt", "w") as file:
                for i in text:
                    file.write(i)       
            requests.post(f"http://{dn_addr}/send", data = message)    
    def receive(self):
        self.update_stats()
        if self.stats == {}:
            raise Exception("Can`t take from empty control node")
        else:
            dn_addr = max(self.stats.items(), key = lambda p : int(p[1]))[0]
            with open("info.txt", "r") as file:
                text = file.readlines()
                i = 0
                while i != len(text):
                    if text[i] == f"ID: {dn_addr}\n":
                        i += 2
                        break
                    else:
                        i += 1
                if i < len(text):
                    while "ID:" in text[i]:
                        if "non-active" in text[i]:
                            i += 1
                        elif "active" in text[i]:
                            parts = text[i].split(", ")
                            parts[1] = "non-active"
                            text[i] = ", ".join(parts)
            with open("info.txt", "w") as file:
                for i in text:
                    file.write(i) 
            return requests.get(f"http://{dn_addr}/receive").text