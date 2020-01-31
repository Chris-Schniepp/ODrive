from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

joystick = Joystick(0, False)

OD = odrive.find_any()
axis = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)


if __name__ == '__main__':
    axis.clear_errors()
    axis.set_curr_limit(30)
    axis.calibrate()
    axis.home_with_vel(-10000, -112844.0)
    print(axis.zero)
    print(axis.get_pos())
    middle = (0 - axis.get_pos())/2

    full_length = 112816

    # god tier code to switch variables if needed
    # right_end = right_end ^ left_end
    # left_end = right_end ^ left_end
    # right_end = right_end ^ left_end

    axis.set_vel_limit(250000)

    # axis.set_pos_gain(30)
    # axis.set_vel_gain(.0002)

    switch = True

    try:
        while True:

            pos = axis.get_pos()

            if pos > -(full_length-15000) and joystick.get_axis('x') > .15:
                if switch:
                    print("right")
                    switch = False
                axis.set_vel(-225000*joystick.get_axis('x'))
                # axis.set_pos(pos-(1000*joystick.get_axis('x')))
            elif pos < -15000 and joystick.get_axis('x') < -.15:
                if not switch:
                    print("left")
                    switch = True
                axis.set_vel(225000*-joystick.get_axis('x'))
                # axis.set_pos(pos + (1000*-joystick.get_axis('x')))
            else:
                axis.set_vel(0)

            if joystick.button_combo_check([6]):
                print("position: ", axis.get_pos())
                print("velocity: ", axis.get_vel())
                sleep(.2)

            if joystick.button_combo_check([3]):
                print("Oof")
                while abs(axis.get_pos() - -middle) >= 50:
                    axis.set_pos_trap(-middle)
                    axis.get_pos()
                    print("tracking...")



    except KeyboardInterrupt:
        axis.idle()
        quit()
