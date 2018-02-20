import robot_controller as robo


def main():
    """Runs robot snatcher on the ev3 robot"""
    robot = robo.Snatch3r()
    robot.loop_forever()


main()
