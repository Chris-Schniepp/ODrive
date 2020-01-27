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
    print(axis.get_raw_pos())
    print(axis.get_vel())

    right_end = 61000
    left_end = -35250

    right_end = right_end ^ left_end
    left_end = right_end ^ left_end
    right_end = right_end ^ left_end

    axis.set_vel_limit(25000)

    switch = True

    # axis.set_curr_limit(20)
    # axis.set_current(15)

    try:
        while True:

            pos = axis.get_raw_pos()

            if pos > right_end and joystick.get_axis('x') > .15:
                if switch:
                    print("right")
                    switch = False
                axis.set_pos(pos-(3200*joystick.get_axis('x')))
            elif pos < left_end and joystick.get_axis('x') < -.15:
                if not switch:
                    print("left")
                    switch = True
                axis.set_pos(pos + (3200*-joystick.get_axis('x')))

            if joystick.button_combo_check([0]):
                print("position: ", axis.get_raw_pos())
                print("position gain: ", axis.get_pos_gain())
                print("velocity: ", axis.get_vel())
                print("velocity gain: ", axis.get_vel_gain())
                sleep(.2)



    except KeyboardInterrupt:
        quit()
