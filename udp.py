class Udp_communication:
    def __init__(self, socket, pickle, server_ip, port):
        self.myId = 9999
        self.my_port = port + 1
        
        self.my_ip = None
        socket_list = socket.getaddrinfo(socket.gethostname(), self.my_port)
        for item in socket_list:
            if item[0] == 2:
                self.my_ip = item[4][0]
                print(self.my_ip)

        
        
        
        self.socket = socket
        self.pickle = pickle
        self.server_ip = server_ip
        self.server_port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(0.03)
        try:
            self.udp_socket.bind((self.my_ip, self.my_port))
            print("client started on:", self.my_ip, ", port:", self.my_port, "connecting to server on:", self.server_ip,
                  ", port:", self.server_port)
        except:
            print("didnt bind")



    def send(self, category,  msg):
        data = [category, self.myId, msg]
        data = self.pickle.dumps(data)
        self.udp_socket.sendto(data, (self.server_ip, self.server_port))

    def receive(self):
        try:
            data = self.udp_socket.recv(1024)
            data = self.pickle.loads(data)
            return data
        except:
            pass
        
    def close(self):
        self.udp_socket.close()