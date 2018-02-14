import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

class MyDelegate(object):
    def __init__(self):
        self.running = True

    def move_by(self,distance):
        pos = 90*distance
        ev3.LargeMotor(ev3.OUTPUT_B).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_C).run_to_rel_pos(position_sp=pos,
                                                    speed_sp=400,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.LargeMotor(ev3.OUTPUT_B).wait_while(ev3.Motor.STATE_RUNNING)
        ev3.LargeMotor(ev3.OUTPUT_C).wait_while(ev3.Motor.STATE_RUNNING)


def main():
    my_delegate = MyDelegate
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()



main()




