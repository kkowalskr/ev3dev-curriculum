import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White",
               "Brown"]


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    robot = robo.Snatch3r()
    # robot.pixy.mode = "SIG1"

    root = tkinter.Tk()
    root.title("MQTT Remote")

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
    if not ev3.ColorSensor.COLOR_GREEN or ev3.ColorSensor.COLOR_BROWN:
        mqtt_client.send_message("drive", [int(left_speed_entry.get()),
                                           int(right_speed_entry.get())])
    else:
        ev3.Sound.speak('Mario as died')
        robot.stop()


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    if not ev3.ColorSensor.COLOR_GREEN or ev3.ColorSensor.COLOR_BROWN:
        mqtt_client.send_message("drive", [-int(left_speed_entry.get()),
                                           int(right_speed_entry.get())])
    else:
        ev3.Sound.speak('Mario has died')


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    if not ev3.ColorSensor.COLOR_GREEN or ev3.ColorSensor.COLOR_BROWN:
        mqtt_client.send_message("drive", [int(left_speed_entry.get()),
                                           -int(right_speed_entry.get())])
    else:
        ev3.Sound.speak('Mario has died')


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    print("backward")
    if not ev3.ColorSensor.COLOR_GREEN or ev3.ColorSensor.COLOR_BROWN:
        mqtt_client.send_message("backward", [int(left_speed_entry.get()),
                                              int(right_speed_entry.get())])
    else:

        ev3.Sound.speak('Mario has died')


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
