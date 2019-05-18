"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Zixin Fan.
  Spring term, 2018-2019.
"""
# DONE 1:  Put your name in the above.

import mqtt_remote_method_calls as mqtt
import rosebot
import m2_robot_code as m2
import m3_robot_code as m3
import math


class MyRobotDelegate(object):
    """
    Defines methods that are called by the MQTT listener when that listener
    gets a message (name of the method, plus its arguments)
    from a LAPTOP via MQTT.
    """
    def __init__(self, robot):
        self.robot = robot  # type: rosebot.RoseBot
        self.mqtt_sender = None  # type: mqtt.MqttClient
        self.is_time_to_quit = False  # Set this to True to exit the robot code

    def set_mqtt_sender(self, mqtt_sender):
        self.mqtt_sender = mqtt_sender

    def go(self, left_motor_speed, right_motor_speed):
        """ Tells the robot to go (i.e. move) using the given motor speeds. """
        print_message_received("go", [left_motor_speed, right_motor_speed])
        self.robot.drive_system.go(left_motor_speed, right_motor_speed)

    # TODO: Add methods here as needed.
    def Forward_or_Backward(self, distance, speed, delta):
        self.robot.drive_system.go(speed, speed)
        self.robot.drive_system.right_motor.reset_position()

        while True:
            if abs(self.robot.drive_system.right_motor.get_position() * math.pi / 180 - distance) < delta:
                break

        self.robot.drive_system.right_motor.turn_off()
        self.robot.drive_system.left_motor.turn_off()

    def Go_until_distance(self, until_distance, speed, delta):
        while True:
            current_until_distance = self.Get_distance()
            print(current_until_distance)
            if current_until_distance - until_distance > delta + 30:
                self.robot.drive_system.go(speed, speed)
            elif current_until_distance - until_distance > delta:
                self.robot.drive_system.go(15, 15)
            elif current_until_distance - until_distance < -delta - 30:
                self.robot.drive_system.go(-speed, -speed)
            elif current_until_distance - until_distance < -delta:
                self.robot.drive_system.go(-15, -15)
            else:
                break

        self.robot.drive_system.right_motor.turn_off()
        self.robot.drive_system.left_motor.turn_off()

    def Get_distance(self):
        list = []

        for k in range(5):
            list = list + [self.robot.sensor_system.ir_proximity_sensor.get_distance()]

        current_until_distance = (sum(list) - max(list) - min(list)) / 3
        return current_until_distance


def print_message_received(method_name, arguments):
    print()
    print("The robot's delegate has received a message")
    print("for the  ", method_name, "  method, with arguments", arguments)


# TODO: Add functions here as needed.

