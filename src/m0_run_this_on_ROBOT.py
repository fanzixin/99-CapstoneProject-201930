"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.
  Authors:  Your professors (for the framework)
    and Zixin Fan, Yunpu Zhang.
  Spring term, 2018-2019.
"""
# DONE 1:  Put the name of EACH team member in the above.

import time

import mqtt_remote_method_calls as mqtt
import rosebot
import m1_robot_code as m1
import m2_robot_code as m2
import m3_robot_code as m3


class DelegateForRobotCode(m1.MyRobotDelegate,
                           m2.MyRobotDelegate,
                           m3.MyRobotDelegate):
    def __init__(self, robot):
        super().__init__(robot)

    def set_mqtt_sender(self, mqtt_sender):
        super().set_mqtt_sender(mqtt_sender)


def main():
    """
    This code, which must run on the ROBOT:
      1. Constructs a robot, an mqtt_sender, and a delegate to respond
         to messages from the LAPTOP sent via MQTT.
      2. Stays in an infinite loop while a listener (for MQTT messages)
         runs in the background.
    """
    robot = rosebot.RoseBot()

    delegate = DelegateForRobotCode(robot)
    mqtt_sender = mqtt.MqttClient(delegate)
    delegate.set_mqtt_sender(mqtt_sender)

    mqtt_sender.connect_to_pc(lego_robot_number=7)
    # DONE 3: Replace 99 in the above by YOUR team's robot number.

    time.sleep(1)  # To let the connection process complete
    print()
    print("Starting to listen for messages. The delegate responds to them.")
    print()

    # Stay in an infinite loop while the listener (for MQTT messages)
    # runs in the background:
    while True:
        time.sleep(0.01)
        if delegate.is_time_to_quit:
            break


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
