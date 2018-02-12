# Tells the robot what color to seek and then the robot goes and picks up#
# that color #

import ev3dev.ev3 as ev3

import time
import robot_controller as robo


def main():

    print('Fetch')

    robot = robo.Snatch3r()
    robot.arm_calibration()
    color_seek(robot)
    go_to(robot)
    come_back(robot)


def color_seek(robot):

    robot.pixy.mode = 'SIG1'

    while True:

        if robot.pixy.value(1) == 0:
            robot.drive(-100, 100)
        elif robot.pixy.value(1) < 150:
            robot.drive(-100, 100)
        elif robot.pixy.value(1) > 170:
            robot.drive(100, - 100)
        elif 170 > robot.pixy.value(1) > 150:
            robot.stop()
            print('Color Found!')
            break

        time.sleep(0.25)


def go_to(robot):

#    while robot.ir_sensor.proximity > 10:
#        print(robot.ir_sensor.proximity)
 #       robot.drive(400, 400)

    while robot.color_sensor.reflected_light_intensity < 85:
        robot.drive(400, 400)

    robot.stop()

#    robot.drive_inches(5, 400)

    time.sleep(1)

    print('Arrived at color!')

    robot.arm_up()

    time.sleep(1)


def come_back(robot):

    robot.pixy.mode = 'SIG2'

    while True:
        if robot.pixy.value(1) == 0:
            robot.drive(-100, 100)
        elif robot.pixy.value(1) < 150:
            robot.drive(-100, 100)
        elif robot.pixy.value(1) > 170:
            robot.drive(100, - 100)
        elif 170 > robot.pixy.value(1) > 150:
            robot.stop()
            print('Home Found!')
            break

    while robot.color_sensor.reflected_light_intensity < 85:
        robot.drive(400, 400)

    robot.stop()
    robot.arm_down()

    print('Color Returned!')
    ev3.Sound.speak('Woof, Woof')


main()
