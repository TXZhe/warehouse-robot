#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import globalvariable
import time
from threading import Thread
from TCPData import TCPData

lmLeft = ev3.LargeMotor('outA')
lmRight = ev3.LargeMotor('outB')
mm = ev3.MediumMotor('outC')

us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()
cs.mode = "COL-COLOR"
gs = ev3.GyroSensor()
ts = ev3.TouchSensor()

data = TCPData()

#avoid collision, when ultrasonic senor detects
#there is an obstical in collision distance car
#will turn 90 degrees. Will stop at terminal

COLLISION_DISTANCE = 180

RSPEED = 100

RSPEED_DELTA = 0

find_obstacle = False

#Control robot move as given command:
#1. Go straight
#2. Turn clock wise
#If there is an obstacle: turn 90 degrees. and then go straight for 1s.
#If find the terminal: Stop.
def go_robot(command):
    global find_obstacle
    global RSPEED
    global RSPEED_DELTA
    global data
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

    if (find_obstacle):
        RSPEED_DELTA = 0
        lmRight.run_forever(speed_sp = RSPEED )
        lmLeft.run_forever(speed_sp = -RSPEED )
        while (gs.value() > -90 and not globalvariable.find_terminal
                and not globalvariable.stop_now):
            pass
        #put wheel speed, turnning angle to TCPData when find obstacle
        data.leftWheelSpeed(-RSPEED)
        data.rightWheelSpeed(RSPEED)
        data.gyro(gs.value())
        data.option("find_obstacle_turn_90")
        globalvariable.bt_move_message.put(data)

        lmLeft.run_forever(speed_sp = RSPEED )
        time.sleep(1)

        data.leftWheelSpeed(RSPEED)
        data.option("find_obstacle_go_1")
        globalvariable.bt_move_message.put(data)

    else:
        if command == 1:
            lmLeft.run_forever(speed_sp = RSPEED)
            lmRight.run_forever(speed_sp = RSPEED)
            time.sleep(1)

            data.leftWheelSpeed(RSPEED)
            data.rightWheelSpeed(RSPEED)
            data.gyro(gs.value())
            data.option("go_straight")
            globalvariable.bt_move_message.put(data)

        #Turn clock wise until: 1. Find blak; 2. Have turned 360 degrees.
        #If it has turned 360 degrees but still not find black. Rotation radius increas.
        elif command == 2:
            lmLeft.run_forever(speed_sp = RSPEED + RSPEED_DELTA)
            lmRight.run_forever(speed_sp = - RSPEED + RSPEED_DELTA)

            while (cs.value() != 1 and gs.value() < 360
                    and not globalvariable.find_terminal and not find_obstacle
                    and not globalvariable.stop_now):
                pass

            data.leftWheelSpeed(RSPEED + RSPEED_DELTA)
            data.rightWheelSpeed(- RSPEED + RSPEED_DELTA)
            data.gyro(gs.value())
            data.option("turn_around_find_black")
            globalvariable.bt_move_message.put(data)

            if(cs.value() != 1):
                RSPEED_DELTA = RSPEED_DELTA + 100
            else:
                RSPEED_DELTA = 0


    lmLeft.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)
    lmRight.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)


#Ultrasonic sensor:
#If there is an obstacle: Stop immediatelly.
def UltrasonicSensor_work():
    global find_obstacle
    #Check ultrasonic sensor
    while (1):
        #print(us.value())
        if ((us.value()) <= COLLISION_DISTANCE):
            if (not find_obstacle):
                find_obstacle = True
        else:
            find_obstacle = False
        time.sleep(0.5)


def go_robot_a():
    #Thread of Ultrasonic Sensor
    tus = Thread(target=UltrasonicSensor_work)
    tus.setDaemon(True)
    tus.start()

    while (not globalvariable.find_terminal
            and not globalvariable.stop_now
            and globalvariable.model != "M"):
        #Check color sensor
        #1 is black
        #if ts.value() == True:
            #break
        data.mode("A")
        if cs.value() == 1:
            #go straight for a while
            go_robot(1)
        else:
            #rotate for some angle
            go_robot(2)
        #TODO: send record to server

    #Unload  Medium motor
    if(globalvariable.find_terminal):
        mm.run_forever(speed_sp = RSPEED)
        time.sleep(1)
        mm.run_forever(speed_sp = -RSPEED)
        time.sleep(1)
        mm.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)


if __name__ == '__main__':
    globalvariable.model == "A"
    tmp = Thread(target=go_robot_a)
    tmp.setDaemon(True)
    tmp.start()
    globalvariable.find_terminal = ts.value()
