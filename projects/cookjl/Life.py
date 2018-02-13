#import math
import random
# import ev3dev.ev3 as ev3
# import time
# import math
import robot_controller as robo
import tkinter
from tkinter import ttk
############################3
##Jobs
##doctor - 0
##teacher - 1
##accountant - 2
##sales person - 3
##entertainer - 4
##artist - 5
##athlete - 6


class Player(object):

    def __init__(self):
        self.money = 0
        self.kids = 0
        self.education = 0
        self.house = 0
        self.job = 0
        self.salary = 0

    def move(self, robot):
        roll = random.randrange(1, 10)
        print("You rolled a ", roll)
        return roll

    def play(self, robot, color):
        if color == "green":
            self.payday()

    def payday(self):
        self.money += self.salary
        print("Pay Day! You now have ", self.money, " dollars.")


def main():
    player = Player
    robot = robo.Snatch3r
    root = tkinter.Tk()
    root.title("Game Start")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame, text="Would you like to go to college?")
    label.grid(row=0, column=0)
    yes_button = ttk.Button(main_frame, text="Yes")
    yes_button.grid(row=1, column=0)
    yes_button['command'] = lambda: school_choice(player, "Yes")
    no_button = ttk.Button(main_frame, text="No")
    no_button.grid(row=2, column=0)
    no_button['command'] = lambda: school_choice(player, "No")
    root.destroy()
    job_selection(player)

    root = tkinter.Tk()
    root.title("The Game of Life")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    distance = Player.move(robot)
    robot.drive_inches(distance=distance, sp=400)
    player.play()


def school_choice(player, choice):
    if choice == "Yes":
        player.money = player.money - 60000
        player.education += 1


def job_selection(player):
    luck = random.randrange(1, 2)
    job_screen = tkinter.Tk()
    job_screen.title("Job selection")
    frame = ttk.Frame(job_screen, padding=20, relief='raised')
    frame.grid()
    label = ttk.Label(frame, text='Select a job')
    label.grid(row=0, column=0)
    if player.education == 1:
        job_screen = tkinter.Tk()
        job_screen.title("Job selection")
        frame = ttk.Frame(job_screen, padding=20, relief='raised')
        frame.grid()
        label = ttk.Label(frame, text='Select a job')
        label.grid(row=0, column=0)
        if luck == 1:
            doctor_button = ttk.Button(frame, text="Doctor")
            doctor_button.grid(row=1, column=0)
            doctor_button['command'] = lambda: job_choice(player, 0)
        else:
            teacher_button = ttk.Button(frame, text="Teacher")
            teacher_button.grid(row=1, column=0)
            teacher_button['command'] = lambda: job_choice(player, 1)
            accountant_button = ttk.Button(frame, text="Accountant")
            accountant_button.grid(row=2, column=0)
            accountant_button['command'] = lambda: job_choice(player, 2)

    else:
        sales_button = ttk.Button(frame, text="Sales Person")
        sales_button.grid(row=1, column=0)
        sales_button['command'] = lambda: job_choice(player, 3)
        entertainer_button = ttk.Button(frame, text="Entertainer")
        entertainer_button.grid(row=2, column=0)
        entertainer_button['command'] = lambda: job_choice(player, 4)
        if luck == 1:
            athlete_button = ttk.Button(frame, text="Athlete")
            athlete_button.grid(row=3, column=0)
            athlete_button['command'] = lambda: job_choice(player, 6)
        else:
            artist_button = ttk.Button(frame, text="Artist")
            artist_button.grid(row=3, column=0)
            artist_button['command'] = lambda: job_choice(player, 5)
    job_screen.destroy()


def job_choice(player, choice):
    jobs = ["doctor", "teacher", "accountant", "sales person", "entertainer",
            "artist", "athlete"]
    salaries = [120000, 45000, 55000, 60000, random.randrange(20000, 200000),
                 random.randrange(35000, 150000), 250000]
    print("You are now a ", jobs[choice])
    print("You will be paid ", salaries[choice])
    player.job = choice
    player.salary = salaries[choice]
