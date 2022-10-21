import socket
from IPy import IP

#Class inspired by Mohamed Ezzat's blog on port scanning

class portscan():
    banners = []
    open_ports = {}
    def __init__(self, target, port_num):
        self.target = target
        self.port_num = port_num

    def check_ip(self):
        try:
            IP(self.target)
            return(self.target)
        except ValueError:
            return socket.gethostbyname(self.target)

    def scan(self):
        for port in range(1, self.port_num):
            self.scan_port(port)
    
    def scan_port(self, port):
        try:
            converted_ip = self.check_ip()
            sock = socket.socket()
            sock.settimeout(0.25)
            sock.connect((converted_ip, port))
            self.open_ports[port] = "Unknown banner"
            try:
                banner = sock.recv(1024).decode().strip('\n').strip('\r')
                self.open_ports[port] = banner
            except:
                self.banners.append(' ')
            sock.close()
        except Exception as e:
            print(e)
            pass