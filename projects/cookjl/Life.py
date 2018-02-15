import random
import ev3dev.ev3 as ev3
import time
# import math
import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

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

    def move(self):
        roll = random.randrange(1, 10)
        print("You rolled a ", roll)
        return roll

    def play(self, color):
        print(color)
        if color == "white":
            print("play working")
        #elif color == "red":

    def payday(self):
        self.money += self.salary
        print("Pay Day! You now have ", self.money, " dollars.")

class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in
        self.running = True

    def color_seen(self, color):
        print("Space is: " +color)
        message_to_display = "You landed on {}.".format(color)

        self.display_label.configure(text=message_to_display)


def main():
    player = Player()
    root = tkinter.Tk()
    root.title("Game Start")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()


    label = ttk.Label(main_frame, text="Would you like to go to college?")
    label.grid(row=0, column=0)
    yes_button = ttk.Button(main_frame, text="Yes")
    yes_button.grid(row=1, column=0)
    yes_button['command'] = lambda: school_choice(player,root, "Yes")
    no_button = ttk.Button(main_frame, text="No")
    no_button.grid(row=2, column=0)
    no_button['command'] = lambda: school_choice(player,root, "No")
    root.mainloop()
    job_selection(player)
# "Main game window, sets up a move button."
    root = tkinter.Tk()
    root.title("The Game of Life")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    move_button = ttk.Button(main_frame,text = "Move")
    move_button.grid(row=0, column=0)
    color_label = ttk.Label(root, text = "ev3 color detected")
    color_label.grid(row=1, column=0)
    pc_delegate = MyDelegateOnThePc(color_label)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    move_button['command'] = lambda: send_move_command(mqtt_client, distance=player.move())
    root.mainloop()


def school_choice(player,root, choice):
    print("buttons work")
    if choice is "Yes":
        player.money = player.money - 60000
        player.education += 1
    root.destroy()


def job_selection(player):
    luck = random.randrange(1, 2)
    job_screen = tkinter.Tk()
    job_screen.title("Job selection")
    frame = ttk.Frame(job_screen, padding=20, relief='raised')
    frame.grid()
    label = ttk.Label(frame, text='Select a job')
    label.grid(row=0, column=0)
    if player.education == 1:

        if luck == 1:
            doctor_button = ttk.Button(frame, text="Doctor")
            doctor_button.grid(row=1, column=0)
            doctor_button['command'] = lambda: job_choice(player,job_screen, 0)
            teacher_button = ttk.Button(frame, text="Teacher")
            teacher_button.grid(row=2, column=0)
            teacher_button['command'] = lambda: job_choice(player,
                                                           job_screen, 1)
            accountant_button = ttk.Button(frame, text="Accountant")
            accountant_button.grid(row=3, column=0)
            accountant_button['command'] = lambda: job_choice(player,
                                                              job_screen, 2)
        else:
            teacher_button = ttk.Button(frame, text="Teacher")
            teacher_button.grid(row=1, column=0)
            teacher_button['command'] = lambda: job_choice(player,
                                                           job_screen, 1)
            accountant_button = ttk.Button(frame, text="Accountant")
            accountant_button.grid(row=2, column=0)
            accountant_button['command'] = lambda: job_choice(player,
                                                              job_screen, 2)

    else:
        sales_button = ttk.Button(frame, text="Sales Person")
        sales_button.grid(row=1, column=0)
        sales_button['command'] = lambda: job_choice(player,job_screen, 3)
        entertainer_button = ttk.Button(frame, text="Entertainer")
        entertainer_button.grid(row=2, column=0)
        entertainer_button['command'] = lambda: job_choice(player,
                                                           job_screen, 4)
        if luck == 1:
            athlete_button = ttk.Button(frame, text="Athlete")
            athlete_button.grid(row=3, column=0)
            athlete_button['command'] = lambda: job_choice(player,
                                                           job_screen, 6)
        else:
            artist_button = ttk.Button(frame, text="Artist")
            artist_button.grid(row=3, column=0)
            artist_button['command'] = lambda: job_choice(player,job_screen, 5)
    job_screen.mainloop()


def job_choice(player,screen, choice):
    jobs = ["doctor", "teacher", "accountant", "sales person", "entertainer",
            "artist", "athlete"]
    salaries = [120000, 45000, 55000, 60000, random.randrange(20000, 200000),
                 random.randrange(35000, 150000), 250000]
    print("You are now a ", jobs[choice])
    print("You will be paid ", salaries[choice])
    player.job = choice
    player.salary = salaries[choice]
    screen.destroy()

def send_move_command(mqtt_client, distance):
    mqtt_client.send_message("move_by", [distance])

main()