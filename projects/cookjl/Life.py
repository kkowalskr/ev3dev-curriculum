import math
import random
import ev3dev.ev3 as ev3
import time
import math
import robot_controller as robo
import tkinter
from tkinter import ttk

class Player(object):

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
        return roll

    def play(self, robot, color):
        if color == "green":
            self.payday()

    def payday(self):
        self.money += self.payrate
        print("Pay Day! You now have ",self.money," dollars.")

def main():
    player = Player
    robot = robo.Snatch3r
    root = tkinter.Tk()
    root.title("Game Start")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,text = "Would you like to go to college?")
    label.grid(row=0, column=0)
    yes_button = ttk.Button(main_frame, text = "Yes")
    yes_button.grid(row = 1, column = 0)
    yes_button['command'] = lambda : school_choice(player,"Yes")
    no_button = ttk.Button(main_frame, text = "No")
    no_button.grid(row = 2, column = 0)
    no_button['command'] = lambda : school_choice(player, "No")
    root.destroy()
    job_selection(player)


    distance =  Player.move(robot)
    robot.drive_inches(distance)

def school_choice(player, choice):
    if choice == "Yes":
        player.money = player.money - 60000
        player.education += 1

def job_selection(player):
    if player.education ==1:
        job_screen = tkinter.Tk()
        job_screen.title("Job selection")
        frame = ttk.Frame(job_screen, padding=20, relief='raised')
        frame.grid()
        label = ttk.Label(frame, text='Select a job')
        label.grid(row=0, column=0)


    else: