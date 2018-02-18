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
        ev3.LargeMotor(ev3.OUTPUT_C).wait_while(ev3.Motor.STATE_RUNNING)
        print("move_by")
        send_back()
        # mqtt_client = com.MqttClient()
        # print("error check 1")
        # mqtt_client.connect_to_pc()
        # print("error check 2")
        # mqtt_client.send_message('color_seen',[ev3.ColorSensor.color])


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    print("Connected")
    print("Running....")
    while my_delegate.running:
        time.sleep(.1)


def send_back():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    if ev3.ColorSensor.color == ev3.ColorSensor.COLOR_GREEN:
        color = 'green'
    elif ev3.ColorSensor.color == ev3.ColorSensor.COLOR_RED:
        color = 'red'
    elif ev3.ColorSensor.color == ev3.ColorSensor.COLOR_WHITE:
        color = 'white'
    elif ev3.ColorSensor.color == ev3.ColorSensor.COLOR_BLUE:
        color = 'blue'
    elif ev3.ColorSensor.color == ev3.ColorSensor.COLOR_BLACK:
        color = 'black'
        my_delegate.running = False
    mqtt_client.send_message('color_seen', [color])


main()
