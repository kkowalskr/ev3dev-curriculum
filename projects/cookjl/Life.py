import random
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


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


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in, money_label, money,
                                                             education, job,
                 salary):
        self.display_label = label_to_display_messages_in
        self.running = True
        self.money = money
        self.education = education
        self.job = job
        self.salary = salary
        self.money_label = money_label
        self.house = 0
        self.spouse = 0
        self.kids = 0

    def color_seen(self, color):
        print("Space is: " + color)
        message_to_display = "You landed on {}.".format(color)

        self.display_label.configure(text=message_to_display)
        if color == "green":
            message_to_display = "Payday! +${}".format(self.salary)
            self.money += self.salary
            self.display_label.configure(text=message_to_display)
        if color == "red":
            if self.house > 0:
                loss = self.house*10000
                message_to_display = "Mortgage payment -${}".format(loss)
                self.money -= loss
                self.display_label.configure(text=message_to_display)
            elif self.education == 1:
                loss = self.salary/2
                message_to_display = "Student loan payment -${}".format(loss)
                self.money -= loss
                self.display_label.configure(text=message_to_display)
            else:
                loss = self.money/5
                message_to_display = "Medical bills -${}".format(loss)
                self.money -= loss
                self.display_label.configure(text=message_to_display)

        if color == "white":
            if self.spouse == 0:
                root = tkinter.Tk()
                root.title("Marriage")
                main_frame = ttk.Frame(root, padding=20, relief='raised')
                main_frame.grid()

                label = ttk.Label(main_frame,
                                  text="Would you like to get married?")
                label.grid(row=0, column=0)
                yes_button = ttk.Button(main_frame, text="Yes")
                yes_button.grid(row=1, column=0)
                yes_button['command'] = lambda: marriage_choice(self, root,
                                                                "Yes")
                no_button = ttk.Button(main_frame, text="No")
                no_button.grid(row=2, column=0)
                no_button['command'] = lambda: marriage_choice(self, root,
                                                               "No")
                root.mainloop()
            else:
                loss = 10000
                message_to_display = "You've had a child! -${}".format(loss)
                self.money_label -= loss
                self.kids += 1
                self.display_label.configure(text=message_to_display)

        if color == "blue":
            print("House selection or raise")
            if self.house == 0:
                root = tkinter.Tk()
                root.title("House selection")
                main_frame = ttk.Frame(root, padding=20, relief='raised')
                main_frame.grid()

                label = ttk.Label(main_frame,
                                  text="What house would you like to buy?")
                label.grid(row=0, column=0)
                shack_button = ttk.Button(main_frame, text="Cozy Shack")
                shack_button.grid(row=1, column=0)
                shack_button['command'] = lambda: house_choice(self, root, 1)
                houseboat_button = ttk.Button(main_frame, text="Houseboat")
                houseboat_button.grid(row=2, column=0)
                houseboat_button['command'] = lambda: house_choice(self, root, 2)
                smallcape_button = ttk.Button(main_frame, text="Small Cape")
                smallcape_button.grid(row=3, column=0)
                smallcape_button['command'] = lambda: house_choice(self, root, 3)
                penthouse_button = ttk.Button(main_frame, text="Exec. Penthouse")
                penthouse_button.grid(row=4, column=0)
                penthouse_button['command'] = lambda: house_choice(self, root, 4)
                root.mainloop()
            else:
                add = self.salary/3
                message_to_display = "You got a raise of ${}".format(add)
                self.salary += add
                self.display_label.configure(text=message_to_display)

        if color == "black":
            message_to_display = "Game Over"
            self.display_label.configure(text=message_to_display)
            print("Game over")
            print("Money: $", self.money)
            if self.spouse == 1:
                print("Married with", self.kids, "kids")
            houses = ["Shack", "Houseboat", "Small Cape", "Executive "
                                                          "Penthouse"]
            print("You lived in a", houses[self.house])
            quit()

        new_money = "You have ${}.".format(self.money)

        self.money_label.configure(text=new_money)


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
    yes_button['command'] = lambda: school_choice(player, root, "Yes")
    no_button = ttk.Button(main_frame, text="No")
    no_button.grid(row=2, column=0)
    no_button['command'] = lambda: school_choice(player, root, "No")
    root.mainloop()
    job_selection(player)
# "Main game window, sets up a move button."
    root = tkinter.Tk()
    root.title("The Game of Life")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    move_button = ttk.Button(main_frame, text="Move")
    move_button.grid(row=0, column=0)
    color_label = ttk.Label(root, text="ev3 color detected")
    color_label.grid(row=1, column=0)
    money_label = ttk.Label(root, text="Money: ")
    money_label.grid(row=2, column=0)
    pc_delegate = MyDelegateOnThePc(color_label, money_label, player.money,
                                    player.education, player.job,
                                    player.salary)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    move_button['command'] = lambda: send_move_command(mqtt_client, distance=player.move())
    root.mainloop()


def school_choice(player, root, choice):
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
            doctor_button['command'] = lambda: job_choice(player,
                                                          job_screen, 0)
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
        sales_button['command'] = lambda: job_choice(player, job_screen, 3)
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
            artist_button['command'] = lambda: job_choice(player,
                                                          job_screen, 5)
    job_screen.mainloop()


def job_choice(player, screen, choice):
    jobs = ["doctor", "teacher", "accountant", "sales person", "entertainer",
            "artist", "athlete"]
    salaries = [120000, 45000, 55000, 60000, random.randrange(20000, 200000),
                 random.randrange(35000, 150000), 250000]
    print("You are now a ", jobs[choice])
    print("You will be paid ", salaries[choice])
    player.job = choice
    player.salary = salaries[choice]
    screen.destroy()


def marriage_choice(player, screen, choice):
    if choice == "Yes":
        player.spouse = 1
        player.salary = player.salary*1.5
    screen.destroy()


def house_choice(player, screen, choice):
    player.house = choice
    screen.destroy()


def send_move_command(mqtt_client, distance):
    mqtt_client.send_message("move_by", [distance])


main()
