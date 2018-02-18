# Tells the robot what color to seek and then the robot goes and picks up#
# that color #

import ev3dev.ev3 as ev3

import time
import robot_controller as robo
import mqtt_remote_method_calls as com


class MyRobotClass(object):
    """A class that has the commands from robot controller as well as other
    commands. It also starts the class with a weight of 2, connects to the
    broker, and sends that weight to the PC"""
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.weight = 2
        self.mqtt_client = com.MqttClient(self)
        self.mqtt_client.connect_to_pc("broker.mqttdashboard.com")
        self.robot.mqtt_client = self.mqtt_client

        self.mqtt_client.send_message("weight_change_display", [self.weight])

    def color_seek(self, color):
        """Seeks a certain color received from the PC. Goes to that color
        until it is over the color Red, picks the color up, finds the 'home'
        color, drives until it is over white, puts down the color and 'woofs'."""
        self.robot.pixy.mode = 'SIG{}'.format(color)
        print(self.robot.pixy.value(1))

        while self.robot.color_sensor.color != ev3.ColorSensor.COLOR_RED:
            if self.robot.pixy.value(1) == 0:
                self.robot.drive(-100, 100)
            elif self.robot.pixy.value(1) < 175:
                self.robot.drive(100, -100)
            elif self.robot.pixy.value(1) > 195:
                self.robot.drive(-100, 100)
            elif 195 > self.robot.pixy.value(1) > 175:
                self.robot.drive(500, 500)
        self.robot.stop()
        print('Arrived at color!')
        time.sleep(0.25)

        self.robot.arm_up()

        time.sleep(1)

        self.robot.pixy.mode = 'SIG7'

        while self.robot.color_sensor.color != ev3.ColorSensor.COLOR_WHITE:

            if self.robot.pixy.value(1) == 0:
                self.robot.drive(-100, 100)
            elif self.robot.pixy.value(1) < 175:
                self.robot.drive(100, -100)
            elif self.robot.pixy.value(1) > 195:
                self.robot.drive(-100, 100)
            elif 195 > self.robot.pixy.value(1) > 175:
                self.robot.drive(400, 400)

        self.robot.stop()
        self.robot.arm_down()

        print('Color Returned!')
        ev3.Sound.speak('Woof, Woof').wait()

    def chase_tail(self):
        """The robot will turn 360 degrees at full speed for as many times
        as 10 minus its weight. The weight will also be halved. If the weight
        reaches 0 it will call the death command."""
        number_of_turns = 10 - self.weight
        for _ in range(number_of_turns):
            self.robot.turn_degrees(360, self.robot.MAX_SPEED)
        self.weight = self.weight // 2
        self.mqtt_client.send_message("weight_change_display", [self.weight])

        if self.weight == 0:
            self.death()

    def eat(self, number_of_meals):
        """The weight will increase by an amount received from the PC. If
        the weight of the object is over 10 then it will call the death
        command"""
        self.weight = self.weight + number_of_meals
        print(self.weight)
        self.mqtt_client.send_message("weight_change_display", [self.weight])

        if self.weight > 10:
            self.death()

    def shutdown(self):
        """The ev3 speaks 'Ruff Ruff' and then calls the shutdown in
        robot controller"""
        ev3.Sound.speak('Ruff Ruff').wait()
        self.robot.shutdown()

    def death(self):
        """Sends the death message command to the PC with the current object
        weight. Plays a little song and then calls shutdown in the
        robot controller"""
        self.mqtt_client.send_message("death_message", [self.weight])
        time.sleep(3)
        ev3.Sound.play("/home/robot/csse120/assets/sounds/tf_nemesis.wav"
                       "").wait()
        self.robot.shutdown()


def main():
    """Prints fetch, creates a MyRobotClass object, calls an arm calibration
    loop forever from robot controller"""
    print('Fetch')

    my_robot = MyRobotClass()

    my_robot.robot.arm_calibration()
    my_robot.robot.loop_forever()


main()
