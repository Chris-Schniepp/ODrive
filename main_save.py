from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

joystick = Joystick(0, False)

OD = odrive.find_any()
axis_1 = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)
axis_0 = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)

def run_x_axis():
    pos = axis_1.get_pos()

    if pos > -(full_length - 15000) and joystick.get_axis('x') > .15:
        axis_1.set_vel(-vel_speed * joystick.get_axis('x'))

    elif pos < -15000 and joystick.get_axis('x') < -.15:
        axis_1.set_vel(vel_speed * -joystick.get_axis('x'))

    else:
        axis_1.set_vel(0)


def run_y_axis():
    pos = axis_0.get_pos()

    if pos > -(full_length - 15000) and joystick.get_axis('y') < -.15:
        axis_0.set_vel(vel_speed * joystick.get_axis('y'))

    elif pos < -15000 and joystick.get_axis('y') > .15:
        axis_0.set_vel(vel_speed * joystick.get_axis('y'))

    else:
        axis_0.set_vel(0)

def trajectory_mode(location):
    """
    blocking function to set motors at a specific location
    :param location: set point on track one wants the motors to go to
    :return: none
    """
    while abs(axis_1.get_pos() - -middle_x) >= 50:
        axis_1.set_pos_trap(-middle_x)
        axis_1.get_pos()

if __name__ == '__main__':
    axis_1.clear_errors()
    axis_0.clear_errors()
    axis_0.calibrate()
    axis_1.calibrate()
    axis_0.home_with_vel(-10000, -1)
    axis_1.home_with_vel(-10000, -1)
    print(axis_1.zero, " ", axis_0.zero)
    print(axis_1.get_pos(), " ", axis_0.get_pos())
    middle_x = (0 - axis_1.get_pos()) / 2
    middle_y = (0 - axis_0.get_pos()) / 2

    full_length = 112816

    # god tier code to switch variables if needed
    # right_end = right_end ^ left_end
    # left_end = right_end ^ left_end
    # right_end = right_end ^ left_end

    axis_1.set_vel_limit(250000)
    axis_0.set_vel_limit(250000)
    vel_speed = 50000

    # axis_1.set_pos_gain(30)
    # axis_1.set_vel_gain(.0002)

    switch = True

    try:
        while True:

            run_x_axis()
            run_y_axis()

            if joystick.button_combo_check([6]):
                print("position: ", axis_1.get_pos(), " y: ", axis_0.get_pos())
                print("velocity: ", axis_1.get_vel(), "y: ", axis_0.get_vel())
                sleep(.2)

            if joystick.button_combo_check([3]):
                print("Oof")
                while abs(axis_1.get_pos() - -middle_x) >= 50:
                    axis_1.set_pos_trap(-middle_x)
                    axis_1.get_pos()
                    print("tracking...")


    except KeyboardInterrupt:
        axis_1.idle()
        axis_0.idle()
        quit()
