#!/usr/bin/env python3
import carauto
import carmanually
import carauto
import globalvariable
import bluetoothmodule
import time
from threading import Thread
import ev3dev.ev3 as ev3
import queue
from TCPData import TCPData

command = queue.Queue()

auto_on = False

btn = ev3.Button()

def car_go():
    global command
    global auto_on
    while(True):
        if(globalvariable.model == "A"):
            if(not auto_on):
                carauto.go_robot_a()
                auto_on = True
        while(globalvariable.model == "M"):
            auto_on = False
            if(not command.empty()):
                carmanually.go_robot_m(command.get())
                #time.sleep(1)

if __name__ == '__main__':
    bt = Thread(target=bluetoothmodule.start_bluetooth)
    bt.setDaemon(True)
    bt.start()

    cg = Thread(target=car_go)
    cg.setDaemon(True)
    cg.start()


    while(btn.any()==False):
        if(not globalvariable.bt_server_message.empty()):
            tmp_sm = globalvariable.bt_server_message.get()
            if (tmp_sm == "A"):
                globalvariable.model = "A"
            elif (tmp_sm == "M"):
                globalvariable.model = "M"
            elif (tmp_sm == "S"):
                globalvariable.stop_now = True
            elif (tmp_sm == "1"):
                command.put("1")
            elif (tmp_sm == "2"):
                command.put("2")
            elif (tmp_sm == "3"):
                command.put("3")
            elif (tmp_sm == "4"):
                command.put("4")
            elif (tmp_sm == "5"):
                command.put("5")

        if(not globalvariable.bt_arduino_message.empty()):
            tmp_am = globalvariable.bt_arduino_message.get()
            if (tmp_am == "Something"):
                globalvariable.find_terminal = True
