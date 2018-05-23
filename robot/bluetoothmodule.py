import bluetooth
import threading
import json
import time
import globalvariable
import pickle


hostMACAddress = '24:71:89:4E:2B:F6'
clientMACAddress = '5C:F3:70:8B:17:90'
arduinoMACAddress = '40:2C:F4:6F:FC:C5'

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 6

server_socket.bind((hostMACAddress, port))
server_socket.listen(1)
client_client = None
arduino_client = None

def start_bluetooth():
 class ConnectedClient(threading.Thread):
    def __init__(self, socket, client_info):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client_info = client_info
        self.message = None
        self.message_to_send = None

    def run(self):
        try:
            while True:
                data = self.socket.recv(1024)
                if len(data) != 0:
                    str_data = data.decode('utf-8')
                    self.message = str_data
                    print(self.message)
                    if client_info[0] == clientMACAddress:
                        globalvariable.bt_server_message.put(self.message)
                print("q:",globalvariable.bt_move_message.qsize())
                if not globalvariable.bt_move_message.empty():
                    print("sending")
                    self.socket.send(pickle.dumps(globalvariable.bt_move_message.get()))
                    self.message_to_send = None
        except IOError:
            pass
        self.socket.close()
        print(self.client_info, ": disconnected")


 while True:
        print("Waiting for client")
        global arduino_client
        if arduino_client is None or client_client is None:
            client_socket, client_info = server_socket.accept()
            print(client_info, ": connection accepted")
            print(client_info[0])
            if client_info[0] == clientMACAddress:
                print("client_client")
                client_client = ConnectedClient(client_socket, client_info)
                client_client.setDaemon(True)
                client_client.start()

            elif client_info[0] == arduinoMACAddress:
                print("arduino_client")
                arduino_client = ConnectedClient(client_socket, client_info)
                arduino_client.setDaemon(True)
                arduino_client.start()

        print(client_client.message)
        globalvariable.bt_arduino_message.put("lalal") #waiting ardiuno

        #print("receive:"+globalvariable.bt_arduino_message)
        time.sleep(1)
 server_socket.close()

if __name__ == '__main__':
    start_bluetooth()
