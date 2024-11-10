import threading
import time
import tkinter
import queue

from PLC_GUI import Win
from PLC_client import PLCclient
from tkinter import messagebox


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self, plc_client):
        self.plc_client = plc_client
        # self.plc_client.plc_conn()
        self.mage_take = True
        self.mage_release = False
        self.cylinder_reset_status = None
        self.cylinder_mode = False
        # self.plc_client.cylinder_mode_ctrl(1)
        self.cylinder_status = None
        self.position_X = None
        self.position_Y = None
        self.position_Z = None
        self.real_position_x = None
        self.real_position_y = None
        self.real_position_z = None
        self.jog_running_y = threading.Event()
        self.jog_running_x = threading.Event()
        self.jog_running_z = threading.Event()
        self.jog_timer = None
        self.moving_status_X = None
        self.moving_status_Y = None
        self.moving_status_Z = None

        self.snap7_thread = None
        self.position_queue = queue.Queue()

        # offset between fixture and battery pack

        self.offset_x = 0
        #315
        self.offset_y = 0
        #740
        self.offset_z = 0
        #-71

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作

    def connect(self,evt):
        self.plc_client.plc_conn()
        print(f"connect: {self.plc_client.plc.get_connected()}")
        if self.plc_client.plc.get_connected():
            messagebox.showinfo("hint", "PLC connected!")
        else:
            messagebox.showinfo("hint", "PLC not connected!")

    def disconnect(self,evt):
        self.plc_client.plc_discon()
        print(f"connect: {self.plc_client.plc.get_connected()}")
        if self.plc_client.plc.get_connected():
            messagebox.showinfo("hint", "PLC still connected!")
        else:
            messagebox.showinfo("hint", "PLC disconnected!")

    def enablex(self, evt):
        enable_x = self.plc_client.enable_motor("X")
        if enable_x:
            self.ui.tk_text_text_enable_x.insert('1.0', 'Motor X enabled')

    def enabley(self, evt):
        enable_y = self.plc_client.enable_motor("Y")
        if enable_y:
            self.ui.tk_text_text_enable_y.insert('1.0', 'Motor Y enabled')

    def enablez(self, evt):
        enable_z = self.plc_client.enable_motor("Z")
        if enable_z:
            self.ui.tk_text_text_enable_z.insert('1.0', 'Motor Z enabled')

    def gozeroz(self, evt):
        gozero_z = self.plc_client.go_to_zero("Z")
        if gozero_z:
            self.ui.tk_text_text_gozero_z.insert('1.0', 'Motor Z go zero finished')

    def gozerox(self, evt):
        gozero_x = self.plc_client.go_to_zero("X")
        if gozero_x:
            self.ui.tk_text_text_gozero_x.insert('1.0', 'Motor X go zero finished')

    def gozeroy(self, evt):
        gozero_y = self.plc_client.go_to_zero("Y")
        if gozero_y:
            self.ui.tk_text_text_gozero_y.insert('1.0', 'Motor Y go zero finished')

    def reset_system(self, evt):
        self.plc_client.reset_all()

        self.ui.tk_text_text_reset_all.insert('1.0', 'System been reset')

    def resetx(self, evt):
        self.ui.tk_text_text_reset_x.delete('1.0', tkinter.END)
        x_reset = self.plc_client.reset("X")
        self.plc_client.print_status("X")
        if x_reset == 0:
            self.ui.tk_text_text_reset_x.insert('1.0', 'Motor X been reset')
        else:
            self.ui.tk_text_text_reset_x.insert('1.0', f'Motor X reset failed. Error code{x_reset}')

    def resety(self, evt):
        self.ui.tk_text_text_reset_y.delete('1.0', tkinter.END)
        y_reset = self.plc_client.reset("Y")
        self.plc_client.print_status("Y")
        if y_reset == 0:
            self.ui.tk_text_text_reset_y.insert('1.0', 'Motor Y been reset')
        else:
            self.ui.tk_text_text_reset_y.insert('1.0', f'Motor Y reset failed. Error code{y_reset}')

    def resetz(self, evt):
        self.ui.tk_text_text_reset_z.delete('1.0', tkinter.END)
        z_reset = self.plc_client.reset("Z")
        self.plc_client.print_status("Z")
        if z_reset == 0:
            self.ui.tk_text_text_reset_z.insert('1.0', 'Motor Z been reset')
        else:
            self.ui.tk_text_text_reset_z.insert('1.0', f'Motor Z reset failed. Error code{z_reset}')

    def Input_Position(self, evt):
        self.position_X = float(self.ui.tk_input_position_X.get())
        self.position_Y = float(self.ui.tk_input_position_Y.get())

        print(f"Set X position {self.position_X}, Set Y position  {self.position_Y}")

        # self.plc_client.go_position("X", self.position_X, 50)
        # self.plc_client.go_position("Y", self.position_Y, 50)

        self.plc_client.go_position("X", self.position_X+self.offset_x, 50)
        self.plc_client.go_position("Y", self.position_Y+self.offset_y, 50)

    def input_height(self, evt):
        self.position_Z = float(self.ui.tk_input_position_Z.get())
        print(f"Set Z Height {self.position_Z}")
        self.plc_client.go_position("Z", self.position_Z, 50)

        # Create a new thread to run the go_position method
        # thread = threading.Thread(target=self.go_position_thread, args=("X", self.position_X, 50))
        # thread.start()
        # thread = threading.Thread(target=self.go_position_thread, args=("Y", self.position_Y, 50))
        # thread.start()
        # thread = threading.Thread(target=self.go_position_thread, args=("Z", self.position_Z, 50))
        # thread.start()

    def go_position_thread(self, motor_name, pos, vel):
        self.plc_client.go_position(motor_name, pos, vel)

    def mag_take_on(self,evt):
        self.mage_take = True
        self.plc_client.magnet_take(self.mage_take)

    def mag_take_off(self,evt):
        self.mage_take = False
        self.plc_client.magnet_take(self.mage_take)

    def mag_release(self,evt):
        self.mage_release = self.plc_client.magnet_control()

    # def jog_y_positive(self,evt):
    #     self.jog_running_y.set()
    #     threading.Thread(target=self._jog_y_positive_thread).start()
    #     print("jog y+ press down")
    #
    # def _jog_y_positive_thread(self):
    #     while self.jog_running_y.is_set():
    #         try:
    #             self.plc_client.jog("Y", 1, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def jog_y_release(self,evt):
    #     self.jog_running_y.clear()
    #     self.plc_client.jog('Y', 0, 0)
    #     print("jog y button release")
    #
    # def jog_y_negative(self, evt):
    #     self.jog_running_y.set()
    #     threading.Thread(target=self._jog_y_negative_thread).start()
    #     print("jog y- press down")
    #
    # def _jog_y_negative_thread(self):
    #     while self.jog_running_y.is_set():
    #         try:
    #             self.plc_client.jog("Y", 2, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def jog_x_positive(self, evt):
    #     self.jog_running_x.set()
    #     threading.Thread(target=self._jog_x_positive_thread).start()
    #     print("jog x+ press down")
    #
    # def jog_x_negative(self, evt):
    #     self.jog_running_x.set()
    #     threading.Thread(target=self._jog_x_negative_thread).start()
    #     print("jog x- press down")
    #
    # def _jog_x_positive_thread(self):
    #     while self.jog_running_x.is_set():
    #         try:
    #             self.plc_client.jog("X", 1, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def _jog_x_negative_thread(self):
    #     while self.jog_running_x.is_set():
    #         try:
    #             self.plc_client.jog("X", 2, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def jog_x_release(self, evt):
    #     self.jog_running_x.clear()
    #     self.plc_client.jog('X', 0, 0)
    #     print("jog x button release")
    #
    # def jog_z_positive(self, evt):
    #     self.jog_running_z.set()
    #     threading.Thread(target=self._jog_z_positive_thread).start()
    #     print("jog z+ press down")
    #
    # def jog_z_negative(self, evt):
    #     self.jog_running_z.set()
    #     threading.Thread(target=self._jog_z_negative_thread).start()
    #     print("jog z- press down")
    #
    # def _jog_z_positive_thread(self):
    #     while self.jog_running_z.is_set():
    #         try:
    #             self.plc_client.jog("Z", 1, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def _jog_z_negative_thread(self):
    #     while self.jog_running_z.is_set():
    #         try:
    #             self.plc_client.jog("Z", 2, 50)
    #         except RuntimeError as e:
    #             if e.args[0] == b'CLI : Job pending':
    #                 print("Job pending, retrying...")
    #                 time.sleep(0.1)  # wait for 100ms before retrying
    #                 continue
    #             else:
    #                 raise
    #
    # def jog_z_release(self, evt):
    #     self.jog_running_z.clear()
    #     self.plc_client.jog('Z', 0, 0)
    #     print("jog z button release")

    def reset_cylinder(self, evt):
        self.cylinder_reset_status = not self.cylinder_reset_status
        self.plc_client.cylinder_reset(self.cylinder_reset_status)

    def cylinder_mode_switch(self,evt):
        self.cylinder_mode = not self.cylinder_mode
        self.plc_client.cylinder_mode_ctrl(self.cylinder_mode)

    def cylinder_manual_control(self,evt):
        self.cylinder_status = not self.cylinder_status
        self.plc_client.cylinder_manual_ctrl(self.cylinder_status)

    def display_signals(self,evt=None):
        self.ui.tk_table_signal_display.delete(*self.ui.tk_table_signal_display.get_children())

        [self.real_position_y, self.real_position_x, self.real_position_z] = self.plc_client.get_position()
        self.moving_status_X = self.plc_client.get_moving_status("X")
        self.moving_status_Y = self.plc_client.get_moving_status("Y")
        self.moving_status_Z = self.plc_client.get_moving_status("Z")

        self.ui.tk_table_signal_display.insert('', 'end', values=('Magnet take', self.mage_take))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Magnet release', self.mage_release))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Cylinder Reset', self.cylinder_reset_status))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Control Mode', self.cylinder_mode))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Cylinder Status', self.cylinder_status))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Set Position X', self.position_X))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Set Position Y', self.position_Y))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Set Position Z', self.position_Z))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Current position X', self.real_position_x))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Current position Y', self.real_position_y))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Current position Z', self.real_position_z))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Moving status X', self.moving_status_X))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Moving status Y', self.moving_status_Y))
        self.ui.tk_table_signal_display.insert('', 'end', values=('Moving status Z', self.moving_status_Z))

        self.ui.after(1000, self.display_signals)