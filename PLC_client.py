from typing import Tuple

import snap7
import time
import threading
from snap7 import util
import tkinter as tk

# requirements
# 0. 使能：enable = 1， 判断 enabled ！= 1； 判断报警：error_code != 0，reset
# 1. 回零：首先go_zero信号设为1，在go_zero_ing=1将go_zero置为0, 判断go_zero_finish =! 1
# 2. 定位： 提供 position = 100,position_velocity = 50; delay(100ms) go_position =1;
# 判断 position_finish != 0 & position_ing != 0 , 执行定位，输出定位结果current_position


def get_coordinate(s):
    s = s.strip()
    if not s.startswith('(') or not s.endswith(')'):
        raise ValueError("Invalid input Format")
    s = s[1:-1]
    coord = s.split(',')
    x, y, z = [float(c[:-2]) for c in coord]
    return x, y, z


class PLCclient:
    def __init__(self, ip_address, rack, slot):
        self.plc = snap7.client.Client()
        self.ip = ip_address
        self.rack = rack
        self.slot = slot
        self.booldata = bytearray(3)
        self.realdata = bytearray(20)
        self.rundata = bytearray(1)
        self.errordata = bytearray(1)
        self.motors = [
            {"name": "Y", "bool_db": 100, "real_db": 101},
            {"name": "X", "bool_db": 102, "real_db": 103},
            {"name": "Z", "bool_db": 104, "real_db": 105}
        ]
        self.rundata_db = 111
        self.errordata_db = 112
    # run_data 复位 磁铁吸取 磁铁释放 db：111
    # error_data 112

    def plc_conn(self):
        self.plc.connect(self.ip, self.rack, self.slot)
        print(f"connect: {self.plc.get_connected()}")

    def plc_discon(self):
        self.plc.disconnect()
        print(f"connect: {self.plc.get_connected()}")
    # Judge if is Enable

    def reset_all(self):
        util.set_bool(self.rundata, 0, 0,  True)
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db,0, self.rundata)
        print("System has been reset")

    def reset(self, motor_name) -> float:
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            util.set_bool(self.booldata, 0, 1, True)
            self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
            print(f"Motor {motor_name} has been reset")
            time.sleep(1)
            db_real = self.plc.read_area(snap7.client.Areas.DB, motor["real_db"], 0, 20)
            error_code = util.get_real(db_real, 12)
            if error_code == 0:
                time.sleep(1)
                util.set_bool(self.booldata, 0, 1, False)
                self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                print(f"Successfully reset. Error code is {error_code}")
            else:
                print(f"Reset failed. Error code is {error_code}")
            return error_code
        else:
            print(f"Motor {motor_name} not found")

    def magnet_control(self) -> int:
        db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db, 0, 1)
        magnet_status = util.get_bool(db_run, 0, 1)
        cylinder_status = util.get_bool(db_run, 0, 2)
        time.sleep(0.1)
        if magnet_status:
            util.set_bool(self.rundata, 0,1, False)
            magnet_status = False
        else:
            util.set_bool(self.rundata, 0, 1, True)
            magnet_status = True
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db, 0, self.rundata)
        self.print_status("X")
        return magnet_status

    def magnet_take(self,mag_take) ->int:
        util.set_bool(self.rundata, 0, 2, mag_take)
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db, 0, self.rundata)
        time.sleep(0.1)
        db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db, 0, 1)
        cylinder_status = util.get_bool(db_run, 0, 2)
        self.print_status("X")
        return cylinder_status

    def enable_motor(self, motor_name) -> int:
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            util.set_bool(self.booldata, 0, 0, True)
            self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
            time.sleep(1)
            db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
            enabled = util.get_bool(db_bool, 2, 3)
            db_real = self.plc.read_area(snap7.client.Areas.DB, motor["real_db"], 0, 20)
            error_code = util.get_real(db_real, 12)
            if enabled == 1:
                if error_code == 0:
                    print(f"Motor {motor_name} enabled")
                    return 1
                else:
                    print("Error occurred, need reset")
                return 0
            else:
                print(f"{motor_name} Enabled is False, need reset")
                print(f"Error code is {error_code}")
                return 0
        else:
            print(f"Motor {motor_name} not found")

    def jog(self, motor_name, jog_dir, jog_vel):
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            if self.enable_motor(motor_name) == 1:
                db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
                position_ing = util.get_bool(db_bool, 2, 5)
                if not position_ing:
                    if jog_dir == 0:  # stop motor

                        util.set_bool(self.booldata, 0, 3, False)
                        util.set_bool(self.booldata, 0, 4, False)
                        self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                    else:
                        util.set_real(self.realdata, 4, 50)  # JOG 速度
                        self.plc.write_area(snap7.client.Areas.DB, motor["real_db"], 0, self.realdata)
                        time.sleep(0.1)
                        if jog_dir == 1:
                            util.set_bool(self.booldata, 0, 3, True)
                            util.set_bool(self.booldata, 0, 4, False)
                        elif jog_dir == 2:
                            util.set_bool(self.booldata, 0, 4, True)
                            util.set_bool(self.booldata, 0, 3, False)
                        self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                        # time.sleep(0.1)
                        # util.set_bool(self.booldata, 0, 3, False)
                        # util.set_bool(self.booldata, 0, 4, False)
                        # self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
            else:
                print(f"Motor {motor_name} is still running")
        else:
            print(f"Motor {motor_name} not found")

    def go_to_zero(self, motor_name) -> int:
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
            position_ing = util.get_bool(db_bool, 2, 5)
            if not position_ing:
                util.set_bool(self.booldata, 0, 2, True)
                self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                time.sleep(1)
                db_bool_new = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
                go_zero_ing = util.get_bool(db_bool_new, 2, 1)
                if go_zero_ing == 1:
                    util.set_bool(self.booldata, 0, 2, True)
                else:
                    util.set_bool(self.booldata, 0, 2, False)
                self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                time.sleep(1)
                go_zero_finish = util.get_bool(db_bool_new, 2, 0)
                if go_zero_finish == 1:
                    print(f"Motor {motor_name} go zero finished")
                    return 1
                else:
                    return 0
            else:
                print(f"Motor {motor_name} is still running")
        else:
            print(f"Motor {motor_name} not found")

    def go_position(self, motor_name, pos, vel) -> float:
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            if self.enable_motor(motor_name) == 1:
                db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
                position_ing = util.get_bool(db_bool, 2, 5)
                if not position_ing:
                    util.set_real(self.realdata, 0, pos)  # 位置
                    util.set_real(self.realdata, 8, vel)  # Position 速度
                    self.plc.write_area(snap7.client.Areas.DB, motor["real_db"], 0, self.realdata)
                    time.sleep(0.2)
                    util.set_bool(self.booldata, 0, 6, True)
                    self.plc.write_area(snap7.client.Areas.DB, motor["bool_db"], 0, self.booldata)
                    # thread = threading.Thread(target=self.wait_for_motor_finish, args=(motor_name,))
                    # thread.start()
                    while True:
                        db_bool_new = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
                        position_finish = util.get_bool(db_bool_new, 2, 4)
                        db_real = self.plc.read_area(snap7.client.Areas.DB, motor["real_db"], 0, 20)
                        current_position = util.get_real(db_real, 16)
                        if position_finish == 1:
                            print(f"Motor {motor_name} has finished moving to {pos}")
                            break

                        time.sleep(0.1)  # wait for 0.1 seconds before checking again
                    return current_position
                else:
                    print(f"Motor {motor_name} is still running")
            else:
                print("Motor not enabled")
        else:
            print(f"Motor {motor_name} not found")

    def wait_for_motor_finish(self, motor_name):
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        while True:
            db_bool_new = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
            position_finish = util.get_bool(db_bool_new, 2, 4)
            db_real = self.plc.read_area(snap7.client.Areas.DB, motor["real_db"], 0, 20)
            current_position = util.get_real(db_real, 16)
            if position_finish == 1:
                break
            time.sleep(0.1)  # wait for 0.1 seconds before checking again

        print(f"Motor {motor_name} has finished moving to {current_position}")
        return current_position

    def get_position(self) -> Tuple[float, float, float]:
        db_real_x = self.plc.read_area(snap7.client.Areas.DB, 101, 0, 20)
        current_position_x = util.get_real(db_real_x, 16)
        db_real_y = self.plc.read_area(snap7.client.Areas.DB, 103, 0, 20)
        current_position_y = util.get_real(db_real_y, 16)
        db_real_z = self.plc.read_area(snap7.client.Areas.DB, 105, 0, 20)
        current_position_z = util.get_real(db_real_z, 16)
        return current_position_x,current_position_y,current_position_z
# coordinate_input = input("Please enter location:")
# s = "(2.12m, 3.33m, 0.50m)"

    def cylinder_reset(self, reset_status) -> bool:
        util.set_bool(self.rundata,0, 5, reset_status)
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db, 0, self.rundata)
        time.sleep(0.1)
        db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db, 0, 1)
        cylinder_sta = util.get_bool(db_run, 0, 4)
        print(f"cylinder status change to{cylinder_sta}")
        return cylinder_sta

    def cylinder_mode_ctrl(self, mode) -> bool:
        util.set_bool(self.rundata, 0, 4, mode)
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db, 0, self.rundata)
        time.sleep(0.1)
        db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db, 0, 1)
        real_mode = util.get_bool(db_run, 0, 4)
        print(f"real mode change to {real_mode}")
        return real_mode

    def cylinder_manual_ctrl(self, cylinder_status) -> bool:
        util.set_bool(self.rundata, 0, 3, cylinder_status)
        self.plc.write_area(snap7.client.Areas.DB, self.rundata_db, 0, self.rundata)
        time.sleep(0.1)
        db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db, 0, 1)
        real_cylinder_status = util.get_bool(db_run, 0, 3)
        print(f"cylinder status {real_cylinder_status}")
        return real_cylinder_status

    def get_moving_status(self, motor_name) -> bool:
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
            position_ing = util.get_bool(db_bool, 2, 5)
            return position_ing

    def print_status(self, motor_name):
        motor = next((m for m in self.motors if m["name"] == motor_name), None)
        if motor:
            # read input
            print(f"--------------Print motor {motor_name} as follow:---------------------")
            db_bool = self.plc.read_area(snap7.client.Areas.DB, motor["bool_db"], 0, 3)
            enable = util.get_bool(db_bool, 0, 0)
            reset = util.get_bool(db_bool, 0, 1)
            go_zero = util.get_bool(db_bool, 0, 2)
            jog1 = util.get_bool(db_bool, 0, 3)
            jog2 = util.get_bool(db_bool, 0, 4)
            pause = util.get_bool(db_bool, 0, 5)
            go_position = util.get_bool(db_bool, 0, 6)
            print(f"enable:{enable}, reset:{reset}, go_zero:{go_zero}, jog1:{jog1}, jog2:{jog2}, pause:{pause}, "
                  f"go_position:{go_position}")

            # read output
            go_zero_finish = util.get_bool(db_bool, 2, 0)
            go_zero_ing = util.get_bool(db_bool, 2, 1)
            go_zero_overtime = util.get_bool(db_bool, 2, 2)
            enabled = util.get_bool(db_bool, 2, 3)
            position_finish = util.get_bool(db_bool, 2, 4)
            position_ing = util.get_bool(db_bool, 2, 5)
            print(f"go_zero_finish:{go_zero_finish}, go_zero_ing:{go_zero_ing}， go_zero_overtime:{go_zero_overtime}, "
                  f"enabled:{enabled}, position_finish:{position_finish}, position_ing:{position_ing}")
            db_real = self.plc.read_area(snap7.client.Areas.DB, motor["real_db"], 0, 20)
            position = util.get_real(db_real, 0)
            jog_velocity = util.get_real(db_real, 4)
            position_velocity = util.get_real(db_real, 8)

            error_code = util.get_real(db_real, 12)
            current_position = util.get_real(db_real, 16)
            print(f"position:{position}, jog_velocity:{jog_velocity}, position_velocity: {position_velocity}, "
                  f"error_code:{error_code}, current_position:{current_position}")
            db_run = self.plc.read_area(snap7.client.Areas.DB, self.rundata_db,0,1)
            all_reset = util.get_bool(db_run, 0, 0)
            magnet_control = util.get_bool(db_run, 0, 1)
            magnet_take = util.get_bool(db_run, 0, 2)
            cylinder_ctrl = util.get_bool(db_run, 0, 3)
            cylinder_mode = util.get_bool(db_run, 0, 4)
            db_error = self.plc.read_area(snap7.client.Areas.DB, self.errordata_db, 0, 1)
            extend_error = util.get_bool(db_error, 0, 0)
            withdraw_error = util.get_bool(db_error, 0, 1)
            in_stopping = util.get_bool(db_error, 0, 2)
            print(f"all_reset:{all_reset}, magnet_control:{magnet_control},magnet_take:{magnet_take},"
                  f"cylinder_ctrl:{cylinder_ctrl}, cylinder_mode:{cylinder_mode}"
                  f"extend_error:{extend_error}, withdraw_error:{withdraw_error}, in_stopping:{in_stopping}")
            print("-----------------------------------------------------")


if __name__ == '__main__':
    plc = PLCclient('192.168.2.10', 0, 0)
    plc.plc_conn()



    # plc.enable_motor("Z")
    # plc.go_to_zero("Z")
    # plc.print_status("Z")
    # time.sleep(5)

    # plc.jog("Y",1,50)
    # time.sleep(2)
    plc.jog("X",0,0)
    # ----------------full house control-------------------

    # plc.enable_motor("X")
    # plc.enable_motor("Y")
    # plc.enable_motor("Z")

    # time.sleep(5)
    # plc.print_status("X")
    # plc.print_status("Y")
    # plc.print_status("Z")
    # while True:
    #     coordinate_input = input("Please enter location:")
    #     x, y, z = get_coordinate(coordinate_input)
    #     print(x, y, z)
    #      #v X 50 Y 320 Z 250
    #      #p x1500 y2400 z1000
    #     plc.go_position("X", x, 50)
    #     plc.go_position("Y", y, 50)
    #     plc.go_position("Z", z, 50)
    #     print("All motors have finished moving")

