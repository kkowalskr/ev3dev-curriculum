import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()
    root.title("Colorful Fetch")

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    top_label = ttk.Label(main_frame, text="Color to Fetch?")
    top_label.grid(row=0, column=1)

    # left_side_label = ttk.Label(main_frame, text="Red")
    # left_side_label.grid(row=0, column=0)

    red_button = ttk.Button(main_frame, text="Red")
    red_button.grid(row=2, column=0)
    #left_green_button['command'] = lambda: send_led_command(mqtt_client,
    # "left", "green")

    white_button = ttk.Button(main_frame, text="White")
    white_button.grid(row=3, column=0)
    #left_red_button['command'] = lambda: send_led_command(mqtt_client,
    # "left", "red")

    black_button = ttk.Button(main_frame, text="Blue")
    black_button.grid(row=4, column=0)
    #left_black_button['command'] = lambda: send_led_command(mqtt_client,
    # "left", "black")

    # button_label = ttk.Label(main_frame, text="  Buttom messages from EV3  ")
    # button_label.grid(row=1, column=1)

    # button_message = ttk.Label(main_frame, text="--")
    # button_message.grid(row=2, column=1)

    # right_side_label = ttk.Label(main_frame, text="Right LED")
    # right_side_label.grid(row=0, column=2)

    green_button = ttk.Button(main_frame, text="Green")
    green_button.grid(row=2, column=2)
    #right_green_button['command'] = lambda: send_led_command(mqtt_client,
                                                            #  "right",
    # "green")

    yellow_button = ttk.Button(main_frame, text="Yellow")
    yellow_button.grid(row=3, column=2)
    #right_red_button['command'] = lambda: send_led_command(mqtt_client,
    # "right", "red")

    black_button = ttk.Button(main_frame, text="Black")
    black_button.grid(row=4, column=2)
    #right_black_button['command'] = lambda: send_led_command(mqtt_client,
    # "right", "black")

    new_menu_button = ttk.Button(main_frame)

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    root.mainloop()


main()
