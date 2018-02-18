import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class PictureToComputer(object):
    def mario_is_dead(self):
        root1 = tkinter.Toplevel()

        photo = tkinter.PhotoImage(file='mario.gif')

        button1 = ttk.Button(root1, image=photo)

        button1.image = photo
        button1.grid()
        button1['command'] = lambda: print('Game over')

    def mushroom_obtained(self):
        root2 = tkinter.Toplevel()

        photo = tkinter.PhotoImage(file='mushroom.gif')

        button2 = ttk.Button(root2, image=photo)

        button2.image = photo
        button2.grid()
        button2['command'] = lambda: print('Mario grew')

    def won_game(self):
        root3 = tkinter.Toplevel()

        photo = tkinter.PhotoImage(file='peach.gif')

        button3 = ttk.Button(root3, image=photo)

        button3.image = photo
        button3.grid()
        button3['command'] = lambda: print('Congrats! You have won the game! ')

    def crush_turtle(self):
        root4 = tkinter.Toplevel()

        photo = tkinter.PhotoImage(file='koopa.gif')

        button4 = ttk.Button(root4, image=photo)

        button4.image = photo
        button4.grid()
        button4['command'] = lambda: print('You have crushed Koopa Troopa ')


def main():
    robot_to_computer = PictureToComputer()
    mqtt_client = com.MqttClient(robot_to_computer)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Let's Play Mario")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client,
                                                     left_speed_entry,
                                                     right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client,
                                                 left_speed_entry,
                                                 right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client,
                                               left_speed_entry,
                                               right_speed_entry)
    root.bind('<Left>', lambda event: send_left(mqtt_client, left_speed_entry,
                                                right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client,
                                                 left_speed_entry,
                                                 right_speed_entry)
    root.bind('<Right>', lambda event: send_right(mqtt_client,
                                                  left_speed_entry,
                                                  right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_back(mqtt_client,
                                               left_speed_entry,
                                               right_speed_entry)
    root.bind('<Down>', lambda event: send_back(mqtt_client,
                                                left_speed_entry,
                                                right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("forward")
    mqtt_client.send_message("mario", [int(left_speed_entry.get()),
                                       int(right_speed_entry.get())])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    mqtt_client.send_message("mario", [-int(left_speed_entry.get()),
                                       int(right_speed_entry.get())])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    mqtt_client.send_message("mario", [int(left_speed_entry.get()),
                                       -int(right_speed_entry.get())])


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    print("backward")
    mqtt_client.send_message("backward", [int(left_speed_entry.get()),
                                          int(right_speed_entry.get())])


def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
