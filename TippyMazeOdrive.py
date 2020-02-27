"""
Method to test Odrive with a joystick
currently being used for tests with Tippy Maze set up
"""

from time import sleep

import odrive
import ODrive_Ease_Lib

from pidev.Joystick import Joystick

# declaring joystick
joystick = Joystick(0, False)

# finding the odrive and setting the axis
OD = odrive.find_any()
axis = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)


if __name__ == '__main__':
    axis.clear_errors()
    axis.calibrate()

    # direction of homing determined by the way the ODrive is connected and subject to change
    axis.home_with_vel(5000, -1.0)
    print(axis.zero) # prints the location of the 0 in the raw position of the ODrive
    print(axis.get_pos(), " ", axis.get_raw_pos())

    axis.set_curr_limit(28)

    #previous value 187682
    full_length = 130000
    middle = full_length/2
    restricted_length = 20000

    # sets the maximum speed the ODrive can go, default set to 20,000
    axis.set_vel_limit(495000)
    vel_speed = 100000

    switch = True

    try:
        while True:

            pos = axis.get_pos()

            if pos < (full_length - restricted_length) and joystick.get_axis('y') < -.05:
                if switch:
                    sleep(.05)
                    print("up")
                    switch = False
                axis.set_vel(vel_speed*-joystick.get_axis('y'))

            elif pos > restricted_length and joystick.get_axis('y') > .05:
                if not switch:
                    sleep(.05)
                    print("down")
                    switch = True
                axis.set_vel(vel_speed*-joystick.get_axis('y'))

            else:
                axis.set_vel(0)


            if joystick.button_combo_check([6]):
                print("position: ", axis.get_pos(), " ", axis.get_raw_pos())
                print("velocity: ", axis.get_vel())
                print("current: ", axis.get_current())
                sleep(.2)

            if joystick.button_combo_check([3]):
                print("Oof")
                while abs(axis.get_pos() - middle) >= 10:
                    axis.set_pos_trap(middle)
                    axis.get_pos()
                    print("tracking...")

            if joystick.button_combo_check([10]):
                axis.set_pos(50000)


    except KeyboardInterrupt:
        axis.idle()
        quit()
