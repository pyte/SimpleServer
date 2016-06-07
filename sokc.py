try:
    import socket
    import os
    import time
except ImportError:
    print """ Missing socket or os or time library. """
os.system('title Anurodh HTML server')
def __Server_Configurations():

    with open('server.conf') as fd:
        config = fd.read()
    configx = config.split('\n')
    conflist = []
    for conf in configx:
        try:
            if conf[0] == '#':
                pass
            else:
                conflist.append(conf)
        except :
            pass
    return conflist[0].split('=')[1], conflist[1].split('=')[1],conflist[2].split('=')[1] , conflist[3].split('=')[1] , conflist[4].split('=')[1]

def write_log(lfile , rf , ip):
    with open(lfile,'a') as fd:
        fd.write('File : '+rf+'\n')
        fd.write('IP : '+ip+'\n')
        fd.write('----------------\n')
        fd.close()
def show(fil , ip):
    print ip + ' : ---- : ' + fil    

class Server:

    def __init__(self, port , file_root, dip , noc, log_file):
        self.host = ''
        self.port = port
        self.root_dir = file_root
        self.dip = dip
        self.noc = noc
        self.log = log_file

    def _gen_headers(self, code):
        h = 'HTTP/1.1 200 OK\n'
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) 
        h += 'Date: ' + current_date +'\n'
        h += 'Server: Anurodh-Server\n'
        h += 'Connection: Keep-Alive\n\n'
        return h

    def activate(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

        while True:
            self.sock.listen(self.noc)
            client , addr = self.sock.accept()
            if addr[0] == self.dip:
                un = '<h1><font color="red">Unauthorize access. IP : '+addr[0]+' has been blocked by server.</font></h1>'
                res_hd = self._gen_headers(200)
                res_hd = res_hd.encode()
                dd = res_hd+un
                client.send(dd)
                client.close()
                rf = '' 
                write_log(self.log ,rf , addr[0])
                show(addr[0], 'Blocked IP')
            else:
                data = client.recv(1024)
                string = bytes.decode(data)
                req = string.split(' ')[0]
                req_file = string.split(' ')[1]
                fix = req_file
                write_log(self.log ,req_file , addr[0])
                show(addr[0], fix)
                if req_file == '/':
                    req_file = '/index.html'
                    
                else:
                    req_file = req_file

                req_file = self.root_dir+req_file
                res_hd = self._gen_headers(200)
                res_hd = res_hd.encode()

                try:
                    fd = open(req_file,'rb')
                    d = fd.read()
                    fd.close()
                    dd = res_hd+d
                    client.send(dd)
                    client.close()
                except IOError:
                    pass
 
                    #client.send(res_hd+'Error 404. Document not found on the server.')


        self.sock.close()


file_root, server_port, dip, noc , log_file = __Server_Configurations()            
s = Server(int(server_port),file_root,dip , int(noc) , log_file)
s.activate()
        
        

