"""
This file's purpose is to set up a delegate to receive messages from the PC
and coordinate robot movement from the parameters.  The delegate then sends
back the color found from the color sensor to the PC using the mqtt client

Author: Jack Cook
"""
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):
    """ Delegate class to run processes based on messages received from the
    PC"""
    def __init__(self):
        self.running = True

    def move_by(self, distance):
        """ Takes in a distance from the PC, moves that many inches,
        and then calls the move_by command to communicate back to the PC"""
        pos = 90*distance
        ev3.LargeMotor(ev3.OUTPUT_B).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                                    stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_C).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                                    stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_B).wait_while(ev3.Motor.STATE_RUNNING)
        time.sleep(2)
        send_back(self.mqtt_client)

    def set(self, mqtt_client):
        """ Assigns mqtt_client to an instance of the MyDelegate class so
        that it can be sent through as a parameter for other functions
        within the objects code"""
        self.mqtt_client = mqtt_client


def main():
    """ Sets up a delegate and connects to the PC to receive and later send
    messages"""
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.set(mqtt_client)
    mqtt_client.connect_to_pc()
    while ev3.Button.backspace is not True:
        time.sleep(.1)


def send_back(mqtt_client):
    """ Sends a message back to the PC with the color of the space beneath."""
    color = ''
    assert ev3.ColorSensor
    if ev3.ColorSensor().color == ev3.ColorSensor.COLOR_GREEN:
        color = 'green'
    elif ev3.ColorSensor().color == ev3.ColorSensor.COLOR_RED:
        color = 'red'
    elif ev3.ColorSensor().color == ev3.ColorSensor.COLOR_WHITE:
        color = 'white'
    elif ev3.ColorSensor().color == ev3.ColorSensor.COLOR_BLUE:
        color = 'blue'
    elif ev3.ColorSensor().color == ev3.ColorSensor.COLOR_BLACK:
        color = 'black'

    mqtt_client.send_message('color_seen', [color])


main()
