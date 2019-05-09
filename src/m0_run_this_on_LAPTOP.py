"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Zixin Fan, Yunpu Zhang.
  Spring term, 2018-2019.
"""
# DONE 1:  Put the name of EACH team member in the above.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as mqtt
import m1_laptop_code as m1
import m2_laptop_code as m2
import m3_laptop_code as m3


class DelegateForLaptopCode(m1.MyLaptopDelegate,
                            m2.MyLaptopDelegate,
                            m3.MyLaptopDelegate):
    def __init__(self, root):
        super().__init__(root)

    def set_mqtt_sender(self, mqtt_sender):
        super().set_mqtt_sender(mqtt_sender)


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs and displays a GUI for teleoperation and EACH team
         member's part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("Team 7: Zixin Fan and Yunpu Zhang")
    # DONE 2:  Fill in the XX's above appropriately for your team.

    # -------------------------------------------------------------------------
    # Construct a delegate (for responding to MQTT messages from the robot)
    # and a mqtt_sender (to send messages to the robot).
    # Then connect the mqtt_sender (which also makes the MQTT listener
    # start running in a loop in the background).
    # -------------------------------------------------------------------------
    delegate = DelegateForLaptopCode(root)
    mqtt_sender = mqtt.MqttClient(delegate)
    delegate.set_mqtt_sender(mqtt_sender)

    mqtt_sender.connect_to_ev3(lego_robot_number=07)
    # DONE 3: Replace 99 in the above by YOUR team's robot number.

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()

    # -------------------------------------------------------------------------
    # The teleoperation (remote control) frame, defined later in this module.
    # -------------------------------------------------------------------------
    remote_control_frame = get_teleoperation_frame(root,
                                                   main_frame,
                                                   mqtt_sender)

    # -------------------------------------------------------------------------
    # Each team member has their own frame for their own GUI.
    # -------------------------------------------------------------------------
    frames = []
    for module in (m1, m2, m3):
        frames.append(module.get_my_frame(root, main_frame, mqtt_sender))

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    remote_control_frame.grid(row=0, column=0, padx=5, pady=10)
    frames[0].grid(row=0, column=1)
    frames[1].grid(row=1, column=0)
    frames[2].grid(row=1, column=1)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()
    mqtt_sender.close()


def get_teleoperation_frame(root, window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  root:         tkinter.Tk
      :type  window:       ttk.Frame | ttk.TopLevel
      :type  mqtt_sender:  mqtt.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Go Forward")
    backward_button = ttk.Button(frame, text="Go Backward")
    left_button = ttk.Button(frame, text="Spin Left")
    right_button = ttk.Button(frame, text="Spin Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################
def go(mqtt_sender, direction, left_wheel_speed, right_wheel_speed):
    """
    Sends a message to the robot to go in the given direction
    using the given wheel motor speeds.
      :type mqtt_sender:       mqtt.MqttClient
      :type direction:         str
      :type left_wheel_speed:  int
      :type right_wheel_speed: int
    """
    print()
    print("Sending a message to the robot to", direction)
    print("  using wheel motor speeds:", left_wheel_speed, right_wheel_speed)
    mqtt_sender.send_message("go", [left_wheel_speed, right_wheel_speed])


def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given, thus going FORWARD.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      mqtt.MqttClient
    """
    left = int(left_entry_box.get())
    right = int(right_entry_box.get())
    go(mqtt_sender, "GO FORWARD", left, right)


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes,
    thus going BACKWARD.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      mqtt.MqttClient
    """
    left = -int(left_entry_box.get())
    right = -int(right_entry_box.get())
    go(mqtt_sender, "GO BACKWARD", left, right)


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box,
    thus spinning LEFT.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      mqtt.MqttClient
    """
    left = -int(left_entry_box.get())
    right = int(right_entry_box.get())
    go(mqtt_sender, "SPIN LEFT", left, right)


def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
    thus spinning RIGHT.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      mqtt.MqttClient
    """
    left = int(left_entry_box.get())
    right = -int(right_entry_box.get())
    go(mqtt_sender, "SPIN RIGHT", left, right)


def handle_stop(mqtt_sender):
    """
    Tells the robot to stop.
      :type  mqtt_sender:  mqtt.MqttClient
    """
    print()
    print("Sending a message to the robot to STOP.")
    mqtt_sender.send_message("stop", [])


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
