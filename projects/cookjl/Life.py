import math
import random
import ev3dev.ev3 as ev3
import time
import math

import robot_controller as robo

class player(object):

    def __init__(self):
        self.money=0
        self.kids=0
        self.education=0
        self.house=0
        self.job=0
        self.payrate = 0

    def move(self, robot):
        roll = random.randrange(1,10)
        print("You rolled a ",roll)



    def play(self, robot, color):
        if color == "green":
            self.payday()

    def payday(self):
        self.money += self.payrate
        print("Pay Day! You now have ",self.money," dollars.")

def main():

    robot = robo.Snatch3r

