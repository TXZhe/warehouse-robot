#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
import bluetoothmodule
import globalvariable

from TCPData import TCPData

lmLeft = ev3.LargeMotor('outA')
lmRight = ev3.LargeMotor('outB')
mm = ev3.MediumMotor('outC')

us = ev3.UltrasonicSensor()
cs = ev3.ColorSensor()
cs.mode = "COL-COLOR"
gs = ev3.GyroSensor()
ts = ev3.TouchSensor()

RSPEED = 100

#Get command from controller
#command:
#0: nop
#1: go straight
#2: go black
#3: turn right
#4: turn left
#5: unload
def go_robot_m(command):
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

    data = TCPData()
    data.mode("M")

    if command == "1":
        data.leftWheelSpeed(RSPEED)
        data.rightWheelSpeed(RSPEED)

        lmLeft.run_forever(speed_sp = RSPEED)
        lmRight.run_forever(speed_sp = RSPEED)
        time.sleep(1)
    elif command == "2":
        data.leftWheelSpeed(-RSPEED)
        data.rightWheelSpeed(-RSPEED)

        lmLeft.run_forever(speed_sp = -(RSPEED))
        lmRight.run_forever(speed_sp = -(RSPEED))
        time.sleep(1)
    elif command == "3":
        data.leftWheelSpeed(RSPEED)
        data.rightWheelSpeed(-RSPEED)

        lmLeft.run_forever(speed_sp = RSPEED)
        lmRight.run_forever(speed_sp = -(RSPEED))
        while (gs.value() < 90 and (not globalvariable.stop_now)):
            print(gs.value())
            pass
    elif command == "4":
        data.leftWheelSpeed(-RSPEED)
        data.rightWheelSpeed(RSPEED)

        lmLeft.run_forever(speed_sp = -(RSPEED))
        lmRight.run_forever(speed_sp = RSPEED)
        while (gs.value() > -90 and (not globalvariable.stop_now)):
            print(gs.value())
            pass
    elif command == "5":
        data.leftWheelSpeed(0)
        data.rightWheelSpeed(0)

        mm.run_forever(speed_sp = RSPEED)
        time.sleep(1)
        mm.run_forever(speed_sp = -(RSPEED))
        time.sleep(1)
        mm.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)

    lmLeft.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)
    lmRight.stop(stop_action = ev3.Motor.STOP_ACTION_HOLD)

    data.option(command)
    data.gyro(gs.value())
    data.ultrasonic(us.value())

if __name__ == '__main__':
    #for i in range(5):
        #go_robot_m(str(i))
    go_robot_m("5")
