from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

joystick = Joystick(0, True)

OD = odrive.find_any()
axis_1 = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)
axis_0 = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)

restricted_length = 20000

def run_x_axis():
    pos = axis_1.get_pos()

    if pos < (full_length - restricted_length) and joystick.get_axis('x') < -.05:
        axis_1.set_vel(vel_speed * -joystick.get_axis('x'))

    elif pos > restricted_length and joystick.get_axis('x') > .05:
        axis_1.set_vel(vel_speed * -joystick.get_axis('x'))

    else:
        axis_1.set_vel(0)


def run_y_axis():
    pos = axis_0.get_pos()

    if pos > restricted_length and joystick.get_axis('y') < -.05:
        axis_0.set_vel(vel_speed * joystick.get_axis('y'))

    elif pos < (full_length - restricted_length) and joystick.get_axis('y') > .05:
        axis_0.set_vel(vel_speed * joystick.get_axis('y'))

    else:
        axis_0.set_vel(0)


def trajectory_mode(location1, location2):
    """
    blocking function that sets the motors to a specific location
    :param location1: set point on the track one wants axis1 to go to
    :param location2: set point on the track one wants axis0 to go to
    :return: none
    """
    while abs(axis_1.get_pos() - location1) >= 10 or abs(axis_0.get_pos() - location2) >= 10:
        axis_0.set_pos_trap(location2)
        axis_1.set_pos_trap(location1)
        axis_1.get_pos()
        axis_0.get_pos()


def home(length_of_track):

    middle = length_of_track / 2

    axis_0.home_with_vel(10000, -1)
    while abs(axis_0.get_pos() - (middle-13000)) >= 20:
        print("tracking y")
        axis_0.set_pos_trap(middle)

    axis_1.home_with_vel(10000, -1)
    while abs(axis_1.get_pos() - middle) >= 20:
        print("tracking x")
        axis_1.set_pos_trap(middle)


if __name__ == '__main__':
    axis_1.clear_errors()
    axis_0.clear_errors()
    axis_0.set_calibration_current(10)
    axis_1.set_calibration_current(10)
    axis_0.calibrate()
    axis_1.calibrate()
    home(130000)
    print(axis_1.zero, " ", axis_0.zero)
    print(axis_1.get_pos(), " ", axis_0.get_pos())

    axis_0.set_curr_limit(40)
    axis_1.set_curr_limit(40)

    full_length = 112816  # axis1
    middle_x = full_length / 2
    middle_y = full_length / 2 - 13000

    # god tier code to switch variables if needed
    # right_end = right_end ^ left_end
    # left_end = right_end ^ left_end
    # right_end = right_end ^ left_end

    # sets the maximum speed the ODrive can go, default set to 20,000
    axis_1.set_vel_limit(250000)
    axis_0.set_vel_limit(250000)
    vel_speed = 150000

    try:
        while True:

            run_x_axis()
            run_y_axis()


            if joystick.button_combo_check([3]):
                trajectory_mode(middle_x, middle_y)

            if joystick.button_combo_check([0]):
                print("position: ", axis_1.get_pos(), "  y: ", axis_0.get_pos())
                print("velocity: ", axis_1.get_vel(), " y: ", axis_0.get_vel())
                print("current: ", axis_1.get_current(), " y: ", axis_0.get_current())
                sleep(.2)


    except KeyboardInterrupt:
        axis_1.idle()
        axis_0.idle()
        quit()
