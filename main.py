from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

joystick = Joystick(0, False)

OD = odrive.find_any()
axis = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)


def run_odrive_with_joystick():
    joystick.get_axis(0)


if __name__ == '__main__':
    axis.clear_errors()
    axis.calibrate()
    axis.home_with_vel(-6000, -112844.0)
    middle = (axis.zero - axis.get_pos())/2

    print(middle)

    full_length = 112814.0

    # god tier code to switch variables if needed
    # right_end = right_end ^ left_end
    # left_end = right_end ^ left_end
    # right_end = right_end ^ left_end

    axis.set_vel_limit(25000)

    # axis.set_pos_gain(30)
    # axis.set_vel_gain(.0002)

    switch = True

    # axis.set_curr_limit(20)
    # axis.set_current(15)

    try:
        while True:

            pos = axis.get_raw_pos()

            if pos > -(full_length-1000) and joystick.get_axis('x') > .15:
                if switch:
                    print("right")
                    switch = False
                axis.set_vel(-18000*joystick.get_axis('x'))
                # axis.set_pos(pos-(1000*joystick.get_axis('x')))
            elif pos < (axis.zero + 1000) and joystick.get_axis('x') < -.15:
                if not switch:
                    print("left")
                    switch = True
                axis.set_vel(18000*-joystick.get_axis('x'))
                # axis.set_pos(pos + (1000*-joystick.get_axis('x')))
            else:
                axis.set_vel(0)

            if joystick.button_combo_check([0]):
                print("position: ", axis.get_pos())
                print("position gain: ", axis.get_pos_gain())
                print("velocity: ", axis.get_vel())
                print("velocity gain: ", axis.get_vel_gain())
                sleep(.2)

            if joystick.button_combo_check([3]):
                print("Oof")
                axis.set_pos_trap(-middle)



    except KeyboardInterrupt:
        axis.idle()
        quit()
