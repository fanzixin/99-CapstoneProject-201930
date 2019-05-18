"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Zixin Fan.
  Spring term, 2018-2019.
"""
# DONE 1:  Put your name in the above.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as mqtt
import m2_laptop_code as m2
import m3_laptop_code as m3


def get_my_frame(root, window, mqtt_sender):
    # Construct your frame:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame_label = ttk.Label(frame, text="Zixin")
    frame_label.grid()
    # DONE 2: Put your name in the above.

    # Add the rest of your GUI to your frame:
    # TODO: Put your GUI onto your frame (using sub-frames if you wish).
    entry_distance = ttk.Entry(frame, width = 8)
    entry_distance.grid()
    entry_distance.insert(0, '12')

    entry_speed = ttk.Entry(frame, width = 8)
    entry_speed.grid()
    entry_speed.insert(0, '100')

    entry_delta = ttk.Entry(frame, width = 8)
    entry_delta.grid()
    entry_delta.insert(0, 5)

    button_forward = ttk.Button(frame, text = "Forward")
    button_forward.grid()
    button_forward['command'] = lambda: Handle_forward(mqtt_sender, entry_distance, entry_speed, entry_delta)

    button_backward = ttk.Button(frame, text = "Backward")
    button_backward.grid()
    button_backward['command'] = lambda : Handle_backward(mqtt_sender, entry_distance, entry_speed, entry_delta)

    entry_until_distance = ttk.Entry(frame, width = 8)
    entry_until_distance.grid()
    entry_until_distance.insert(0, '40')

    button_until_distance = ttk.Button(frame, text = "Go until Distance")
    button_until_distance.grid()
    button_until_distance['command'] = lambda: Handle_go_until_distance(mqtt_sender, entry_until_distance, entry_speed, entry_delta)

    # Return your frame:
    return frame


def Handle_forward(mqtt_sender, entry_distance, entry_speed, entry_delta):
    distance = int(entry_distance.get())
    print('The robot goes forward', distance)

    speed = int(entry_speed.get())
    print('with speed', speed)
    print()

    delta = int(entry_delta.get())

    mqtt_sender.send_message('Forward_or_Backward', [distance, speed, delta])


def Handle_backward(mqtt_sender, entry_distance, entry_speed, entry_delta):
    distance = int(entry_distance.get())
    print('The robot goes backward', distance)

    speed = int(entry_speed.get())
    print('with speed', speed)
    print()

    delta = int(entry_delta.get())

    mqtt_sender.send_message('Forward_or_Backward', [- distance, - speed, delta])


def Handle_go_until_distance(mqtt_sender, entry_until_distance, entry_speed, entry_delta):
    until_distance = int(entry_until_distance.get())
    print('The robot goes until distance', until_distance)

    speed = int(entry_speed.get())
    print('with initial speed', speed)
    print()

    delta = int(entry_delta.get())

    mqtt_sender.send_message('Go_until_distance', [until_distance, speed, delta])


class MyLaptopDelegate(object):
    """
    Defines methods that are called by the MQTT listener when that listener
    gets a message (name of the method, plus its arguments)
    from the ROBOT via MQTT.
    """
    def __init__(self, root):
        self.root = root  # type: tkinter.Tk
        self.mqtt_sender = None  # type: mqtt.MqttClient

    def set_mqtt_sender(self, mqtt_sender):
        self.mqtt_sender = mqtt_sender

    # TODO: Add methods here as needed.


# TODO: Add functions here as needed.
