"""
  Library of EV3 robot functions that are useful in many different applications
  . For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For
  organizational purposes try to only write methods into this library that
  are NOT specific to one tasks, but rather methods that would be useful
  regardless of the activity.  For example, don't make a connection to the
  remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task
  would want to use the IR remote up button for something different.
  Instead just make a method called arm_up that could be called.  That way
  it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many
    different programs."""

    def __init__(self):
        self.running = True
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=4)
        self.color_sensor = ev3.ColorSensor()
        self.pixy = ev3.Sensor(driver_name='pixy-lego')

        assert self.ir_sensor.connected
        assert self.color_sensor.connected
        assert self.pixy.connected
        assert self.touch_sensor
        assert self.arm_motor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.MAX_SPEED = 900

    def loop_forever(self):
        while self.running:
            time.sleep(0.1)

    def drive_inches(self, distance, sp):
        """Drives the robot forward set amount of distance at a speed and
        backwards at a negative position"""
        pos = distance * 90

        self.left_motor.run_to_rel_pos(position_sp=pos, speed_sp=sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=pos, speed_sp=sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive(self, left_speed_entry, right_speed_entry):
        """Drives the robot forward forever whenever the up button is
        pressed on the keypad or on the tkinter window"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def stop(self):
        """Stops the motors that are running on the robot when the spacebar
        button is pressed on the keypad or on the tkinter window"""
        self.right_motor.stop()
        self.left_motor.stop()

    def backward(self, left_speed_entry, right_speed_entry):
        """Drives the robot backwards when the down is pressed on the keypad
        or on the tkinter window"""
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def turn_degrees(self, degrees, sp):
        """Turns the robot a given amount of degrees at a speed and positive
        position and turns the  opposite way with negative position"""
        pos = int(degrees * 4.6)

        self.left_motor.run_to_rel_pos(position_sp=pos, speed_sp=sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=-pos, speed_sp=sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """Calibrates the robot arm and sets the self.arm_position to 0 when
        the arm is all the way down"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 5112
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_up(self):
        """Lifts the robot arm up until it hits the touch sensor"""
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Lowers the robot arm to position 0"""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def seek_beacon(self):
        """Finds the remote controller and drives to it and returns true
        when the beacon is reached."""
        forward_speed = 300
        turn_speed = 100
        print("running")
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.drive(-100, 100)
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance <= 1:
                        print("You have found the beacon!")
                        self.stop()
                        self.drive_inches(4, 300)
                        ev3.Sound.speak("You have found the beacon!")
                        return True
                    elif current_distance > 1:
                        self.drive(forward_speed, forward_speed)
                elif math.fabs(current_heading) > 2 and math.fabs(
                        current_heading) \
                        < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                    elif current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                elif math.fabs(current_heading) > 10:
                    self.drive(-200, 200)
                    print("Heading too far off to fix: ", current_heading)

            time.sleep(0.2)

        print("Abandon ship!")
        self.stop()
        return False

    def shutdown(self):
        """Shuts down the robot and sets the LEDs to Green"""
        self.running = False

        self.left_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.speak('Goodbye').wait()



