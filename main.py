from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

joystick = Joystick(0, False)


OD = odrive.find_any()
axis_1 = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)
axis_0 = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)
both_axises = ODrive_Ease_Lib.double_ODrive(OD.axis1, OD.axis0)


if __name__ == '__main__':
    axis_1.clear_errors()
    axis_0.clear_errors()
    axis_1.set_curr_limit(30)
    axis_0.set_curr_limit(30)
    both_axises.calibrate()
    both_axises.home_with_vel(-10000, -112844.0)
    print(axis_1.zero, " ", axis_0.zero)
    print(axis_1.get_pos(), " ", axis_0.get_pos())
    middle = (0 - axis_1.get_pos())/2

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

            pos = axis_1.get_pos()
            pos1 = axis_0.get_pos()

            if pos > -(full_length-15000) and joystick.get_axis('x') > .15:
                if switch:
                    print("right")
                    switch = False
                axis_1.set_vel(-vel_speed*joystick.get_axis('x'))
                axis_0.set_vel(-vel_speed*joystick.get_axis('y'))
                # axis_1.set_pos(pos-(1000*joystick.get_axis_1('x')))
            elif pos < -15000 and joystick.get_axis('x') < -.15:
                if not switch:
                    print("left")
                    switch = True
                axis_1.set_vel(vel_speed*-joystick.get_axis('x'))
                axis_0.set_vel(vel_speed * joystick.get_axis('y'))
                # axis_1.set_pos(pos + (1000*-joystick.get_axis_1('x')))
            else:
                axis_1.set_vel(0)
                axis_0.set_vel(0)

            if joystick.button_combo_check([6]):
                print("position: ", axis_1.get_pos(), " y: ", axis_0.get_pos())
                print("velocity: ", axis_1.get_vel(), "y: ", axis_0.get_vel())
                sleep(.2)

            if joystick.button_combo_check([3]):
                print("Oof")
                while abs(axis_1.get_pos() - -middle) >= 50:
                    axis_1.set_pos_trap(-middle)
                    axis_1.get_pos()
                    print("tracking...")



    except KeyboardInterrupt:
        axis_1.idle()
        axis_0.idle()
        quit()
