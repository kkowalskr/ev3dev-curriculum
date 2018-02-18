import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class Colors(object):
    """Creates a class with all the colors and their values calibrated on the
    robot pixy camera for use throughout the program"""
    def __init__(self):

        self.blue = 1
        self.pink = 2
        self.green = 3
        self.orange = 4


class MyDelegateOnPC(object):
    """Is the delegate for commands from the EV3"""

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def weight_change_display(self, weight):
        """Displays the weight of the dog"""
        message_to_display = "Dog's weight is {}".format(weight)
        self.display_label.configure(text=message_to_display)

    def death_message(self, weight):
        """Displays when the dog died and depending on its weight if it was
        starved or overfed."""
        if weight >= 10:
            message_to_display = "Your dog has died. He was {} " \
                                 "overweight".format(int(weight) - 10)
            self.display_label.configure(text=message_to_display)
        if weight == 0:
            message_to_display = "Your dog has died. He was not fed enough."
            self.display_label.configure(text=message_to_display)


def main():
    """Creates a tkinter window with buttons that communicate with the robot to
    eat, chase its tail, or fetch a certain color. It also connects to the
     broker for communication with the EV3"""
    colors = Colors()
    root = tkinter.Tk()
    root.title("Colorful Fetch")

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    top_label = ttk.Label(main_frame, text="Color to Fetch?")
    top_label.grid(row=0, column=1)

    red_button = ttk.Button(main_frame, text="Blue")
    red_button.grid(row=2, column=0)
    red_button['command'] = lambda: send_color_command(mqtt_client,
                                                       colors.blue)

    white_button = ttk.Button(main_frame, text="Red")
    white_button.grid(row=3, column=0)
    white_button['command'] = lambda: send_color_command(mqtt_client,
                                                         colors.pink)

    blue_button = ttk.Button(main_frame, text="Green")
    blue_button.grid(row=2, column=2)
    blue_button['command'] = lambda: send_color_command(mqtt_client,
                                                        colors.green)

    green_button = ttk.Button(main_frame, text="Orange")
    green_button.grid(row=3, column=2)
    green_button['command'] = lambda: send_color_command(mqtt_client,
                                                         colors.orange)

    chase_tail_button = ttk.Button(main_frame, text="Chase Your Tail")
    chase_tail_button.grid(row=5, column=1)
    chase_tail_button['command'] = lambda: send_chase_tail_command(mqtt_client)

    eat_button = ttk.Button(main_frame, text="Eat (Enter number of times "
                                             "below)")
    eat_button.grid(row=7, column=1)
    eat_button['command'] = lambda: eat_command(mqtt_client, amount_of_food)

    amount_of_food = ttk.Entry(main_frame)
    amount_of_food.grid(row=8, column=1)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=9, column=2)
    quit_button['command'] = lambda: quit_command(mqtt_client)

    message_from_ev3 = ttk.Label(main_frame, text="_________")
    message_from_ev3.grid(row=3, column=1)

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    spacer2 = ttk.Label(main_frame, text="")
    spacer2.grid(row=6, column=2)

    pc_delegate = MyDelegateOnPC(message_from_ev3)
    mqtt_client = com.MqttClient(pc_delegate)
    pc_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_ev3("broker.mqttdashboard.com")

    root.mainloop()


def send_color_command(mqtt_client, color):
    """Sends the fetch command to the EV3 with the chosen color"""
    print("Sending color to fetch = {}".format(color))
    mqtt_client.send_message("color_seek", [color])


def send_chase_tail_command(mqtt_client):
    """Sends the chase tail command to the EV3"""
    print("Sending Chase Your Tail command")
    mqtt_client.send_message("chase_tail")


def eat_command(mqtt_client, entry_box):
    """Sends the eat command to the EV3"""
    print("Sending eat command")
    number_of_meals = entry_box.get()
    mqtt_client.send_message("eat", [int(number_of_meals)])


def quit_command(mqtt_client):
    """Sends the shutdown command to the EV3"""
    print("Sending quit command")
    mqtt_client.send_message("shutdown")


main()
