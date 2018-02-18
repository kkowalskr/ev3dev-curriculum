import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


class MyDelegate(object):
    def __init__(self):
        self.running = True

    def move_by(self, distance):
        pos = 90*distance
        ev3.LargeMotor(ev3.OUTPUT_B).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                                    stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_C).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                                    stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_B).wait_while(ev3.Motor.STATE_RUNNING)
        time.sleep(2)
        print("move_by")
        send_back(self.mqtt_client)


    def set(self, mqtt_client):
        self.mqtt_client = mqtt_client


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.set(mqtt_client)
    mqtt_client.connect_to_pc()
    print("Connected")
    print("Running....")
    while ev3.Button.backspace is not True:
        time.sleep(.1)


def send_back(mqtt_client):
    color = 'green'
    assert ev3.ColorSensor
    print("send back")
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
