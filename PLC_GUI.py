from tkinter import *
from tkinter.ttk import *


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_button_button_enable_x = self.__tk_button_button_enable_x(self)
        self.tk_label_label_PLC = self.__tk_label_label_PLC(self)
        self.tk_label_label_Enable = self.__tk_label_label_Enable(self)
        self.tk_button_button_enable_y = self.__tk_button_button_enable_y(self)
        self.tk_button_button_enable_z = self.__tk_button_button_enable_z(self)
        self.tk_text_text_enable_x = self.__tk_text_text_enable_x(self)
        self.tk_text_text_enable_y = self.__tk_text_text_enable_y(self)
        self.tk_text_text_enable_z = self.__tk_text_text_enable_z(self)
        self.tk_label_label_Gozero = self.__tk_label_label_Gozero(self)
        self.tk_text_text_gozero_x = self.__tk_text_text_gozero_x(self)
        self.tk_text_text_gozero_z = self.__tk_text_text_gozero_z(self)
        self.tk_button_button_gozero_z = self.__tk_button_button_gozero_z(self)
        self.tk_text_text_gozero_y = self.__tk_text_text_gozero_y(self)
        self.tk_button_button_gozero_x = self.__tk_button_button_gozero_x(self)
        self.tk_button_button_gozero_y = self.__tk_button_button_gozero_y(self)
        self.tk_label_label_reset = self.__tk_label_label_reset(self)
        self.tk_button_button_reset_all = self.__tk_button_button_reset_all(self)
        self.tk_button_button_reset_x = self.__tk_button_button_reset_x(self)
        self.tk_button_button_reset_y = self.__tk_button_button_reset_y(self)
        self.tk_button_button_reset_z = self.__tk_button_button_reset_z(self)
        self.tk_text_text_reset_all = self.__tk_text_text_reset_all(self)
        self.tk_text_text_reset_x = self.__tk_text_text_reset_x(self)
        self.tk_text_text_reset_y = self.__tk_text_text_reset_y(self)
        self.tk_text_text_reset_z = self.__tk_text_text_reset_z(self)
        self.tk_table_signal_display = self.__tk_table_signal_display(self)
        self.tk_input_position_X = self.__tk_input_position_X(self)
        self.tk_input_position_Y = self.__tk_input_position_Y(self)
        self.tk_input_position_Z = self.__tk_input_position_Z(self)
        self.tk_label_label_Control = self.__tk_label_label_Control(self)
        self.tk_label_Set_Position = self.__tk_label_Set_Position(self)
        self.tk_label_label_position_x = self.__tk_label_label_position_x(self)
        self.tk_label_label_position_Y = self.__tk_label_label_position_Y(self)
        self.tk_label_label_position_z = self.__tk_label_label_position_z(self)
        self.tk_button_input_position = self.__tk_button_input_position(self)
        self.tk_label_magnet_control = self.__tk_label_magnet_control(self)
        self.tk_button_magnet_take_on = self.__tk_button_magnet_take_on(self)
        self.tk_button_magnet_release = self.__tk_button_magnet_release(self)
        self.tk_button_display_signals = self.__tk_button_display_signals(self)
        self.tk_label_signal = self.__tk_label_signal(self)
        self.tk_button_magnet_take_off = self.__tk_button_magnet_take_off(self)
        self.tk_button_button_connect = self.__tk_button_button_connect(self)
        self.tk_button_button_disconnect = self.__tk_button_button_disconnect(self)
        self.tk_button_jog_y_pos = self.__tk_button_jog_y_pos(self)
        self.tk_button_jog_y_neg = self.__tk_button_jog_y_neg(self)
        self.tk_button_jog_x_neg = self.__tk_button_jog_x_neg(self)
        self.tk_button_jog_x_pos = self.__tk_button_jog_x_pos(self)
        self.tk_button_jog_z_pos = self.__tk_button_jog_z_pos(self)
        self.tk_button_jog_z_neg = self.__tk_button_jog_z_neg(self)
        self.tk_label_cylinder_control = self.__tk_label_cylinder_control(self)
        self.tk_button_cylinder_control_mode = self.__tk_button_cylinder_control_mode(self)
        self.tk_button_manual_control = self.__tk_button_manual_control(self)
        self.tk_button_cylinder_reset = self.__tk_button_cylinder_reset(self)
        self.tk_button_input_height = self.__tk_button_input_height(self)

    def __win(self):
        self.title("Drop control")
        # 设置窗口大小、居中
        width = 1000
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_button_button_enable_x(self, parent):
        btn = Button(parent, text="Enable MotorX", takefocus=False, )
        btn.place(x=20, y=80, width=110, height=30)
        return btn

    def __tk_label_label_PLC(self, parent):
        label = Label(parent, text="PLC_Start", anchor="center", )
        label.place(x=20, y=0, width=150, height=30)
        return label

    def __tk_label_label_Enable(self, parent):
        label = Label(parent, text="Motor Enable", anchor="center", )
        label.place(x=20, y=40, width=130, height=30)
        return label

    def __tk_button_button_enable_y(self, parent):
        btn = Button(parent, text="Enable MotorY", takefocus=False, )
        btn.place(x=20, y=120, width=110, height=30)
        return btn

    def __tk_button_button_enable_z(self, parent):
        btn = Button(parent, text="Enable MotorZ", takefocus=False, )
        btn.place(x=20, y=160, width=110, height=30)
        return btn

    def __tk_text_text_enable_x(self, parent):
        text = Text(parent)
        text.place(x=160, y=80, width=180, height=30)
        return text

    def __tk_text_text_enable_y(self, parent):
        text = Text(parent)
        text.place(x=160, y=120, width=180, height=30)
        return text

    def __tk_text_text_enable_z(self, parent):
        text = Text(parent)
        text.place(x=160, y=160, width=180, height=30)
        return text

    def __tk_label_label_Gozero(self, parent):
        label = Label(parent, text="Motor Go zero", anchor="center", )
        label.place(x=24, y=210, width=130, height=30)
        return label

    def __tk_text_text_gozero_x(self, parent):
        text = Text(parent)
        text.place(x=160, y=250, width=180, height=30)
        return text

    def __tk_text_text_gozero_z(self, parent):
        text = Text(parent)
        text.place(x=160, y=330, width=180, height=30)
        return text

    def __tk_button_button_gozero_z(self, parent):
        btn = Button(parent, text="Gozero MotorZ", takefocus=False, )
        btn.place(x=20, y=330, width=110, height=30)
        return btn

    def __tk_text_text_gozero_y(self, parent):
        text = Text(parent)
        text.place(x=160, y=290, width=180, height=30)
        return text

    def __tk_button_button_gozero_x(self, parent):
        btn = Button(parent, text="Gozero MotorX", takefocus=False, )
        btn.place(x=20, y=250, width=110, height=30)
        return btn

    def __tk_button_button_gozero_y(self, parent):
        btn = Button(parent, text="Gozero MotorY", takefocus=False, )
        btn.place(x=20, y=290, width=110, height=30)
        return btn

    def __tk_label_label_reset(self, parent):
        label = Label(parent, text="Motor Reset", anchor="center", )
        label.place(x=20, y=380, width=130, height=30)
        return label

    def __tk_button_button_reset_all(self, parent):
        btn = Button(parent, text="Reset all", takefocus=False, )
        btn.place(x=20, y=420, width=110, height=30)
        return btn

    def __tk_button_button_reset_x(self, parent):
        btn = Button(parent, text="Reset MotorX", takefocus=False, )
        btn.place(x=20, y=460, width=110, height=30)
        return btn

    def __tk_button_button_reset_y(self, parent):
        btn = Button(parent, text="Reset MotorY", takefocus=False, )
        btn.place(x=20, y=500, width=110, height=30)
        return btn

    def __tk_button_button_reset_z(self, parent):
        btn = Button(parent, text="Reset MotorZ", takefocus=False, )
        btn.place(x=20, y=540, width=110, height=30)
        return btn

    def __tk_text_text_reset_all(self, parent):
        text = Text(parent)
        text.place(x=160, y=420, width=180, height=30)
        return text

    def __tk_text_text_reset_x(self, parent):
        text = Text(parent)
        text.place(x=160, y=460, width=180, height=30)
        return text

    def __tk_text_text_reset_y(self, parent):
        text = Text(parent)
        text.place(x=160, y=500, width=180, height=30)
        return text

    def __tk_text_text_reset_z(self, parent):
        text = Text(parent)
        text.place(x=160, y=540, width=180, height=30)
        return text

    def __tk_table_signal_display(self, parent):
        # 表头字段 表头宽度
        columns = {"Signal": 132, "Value": 88}
        tk_table = Treeview(parent, show="headings", columns=list(columns), )
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        tk_table.place(x=759, y=47, width=221, height=408)
        return tk_table

    def __tk_input_position_X(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=440, y=80, width=60, height=30)
        return ipt

    def __tk_input_position_Y(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=560, y=80, width=60, height=30)
        return ipt

    def __tk_input_position_Z(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=680, y=80, width=60, height=30)
        return ipt

    def __tk_label_label_Control(self, parent):
        label = Label(parent, text="Control", anchor="center", )
        label.place(x=400, y=0, width=250, height=30)
        return label

    def __tk_label_Set_Position(self, parent):
        label = Label(parent, text="Set Position", anchor="center", )
        label.place(x=400, y=40, width=140, height=30)
        return label

    def __tk_label_label_position_x(self, parent):
        label = Label(parent, text="X/mm", anchor="center", )
        label.place(x=380, y=80, width=50, height=30)
        return label

    def __tk_label_label_position_Y(self, parent):
        label = Label(parent, text="Y/mm", anchor="center", )
        label.place(x=500, y=80, width=50, height=30)
        return label

    def __tk_label_label_position_z(self, parent):
        label = Label(parent, text="Z/mm", anchor="center", )
        label.place(x=620, y=80, width=50, height=30)
        return label

    def __tk_button_input_position(self, parent):
        btn = Button(parent, text="Input Position", takefocus=False, )
        btn.place(x=470, y=130, width=110, height=30)
        return btn

    def __tk_label_magnet_control(self, parent):
        label = Label(parent, text="Magnet Control", anchor="center", )
        label.place(x=400, y=170, width=140, height=30)
        return label

    def __tk_button_magnet_take_on(self, parent):
        btn = Button(parent, text="Magnet Take On", takefocus=False, )
        btn.place(x=400, y=210, width=120, height=30)
        return btn

    def __tk_button_magnet_release(self, parent):
        btn = Button(parent, text="Magnet Release", takefocus=False, )
        btn.place(x=400, y=250, width=120, height=30)
        return btn

    def __tk_button_display_signals(self, parent):
        btn = Button(parent, text="Display Signals", takefocus=False, )
        btn.place(x=820, y=480, width=100, height=30)
        return btn

    def __tk_label_signal(self, parent):
        label = Label(parent, text="Display Signals", anchor="center", )
        label.place(x=790, y=0, width=150, height=30)
        return label

    def __tk_button_magnet_take_off(self, parent):
        btn = Button(parent, text="Magnet Take Off", takefocus=False, )
        btn.place(x=570, y=210, width=120, height=30)
        return btn

    def __tk_button_button_connect(self, parent):
        btn = Button(parent, text="Connect", takefocus=False, )
        btn.place(x=179, y=20, width=90, height=45)
        return btn

    def __tk_button_button_disconnect(self, parent):
        btn = Button(parent, text="Disconnect", takefocus=False, )
        btn.place(x=290, y=20, width=90, height=45)
        return btn

    def __tk_button_jog_y_pos(self, parent):
        btn = Button(parent, text="Y+", takefocus=False, )
        btn.place(x=470, y=410, width=30, height=60)
        return btn

    def __tk_button_jog_y_neg(self, parent):
        btn = Button(parent, text="Y-", takefocus=False, )
        btn.place(x=470, y=490, width=30, height=60)
        return btn

    def __tk_button_jog_x_neg(self, parent):
        btn = Button(parent, text="X-", takefocus=False, )
        btn.place(x=400, y=460, width=60, height=30)
        return btn

    def __tk_button_jog_x_pos(self, parent):
        btn = Button(parent, text="X+", takefocus=False, )
        btn.place(x=510, y=460, width=60, height=30)
        return btn

    def __tk_button_jog_z_pos(self, parent):
        btn = Button(parent, text="Z+", takefocus=False, )
        btn.place(x=620, y=410, width=30, height=60)
        return btn

    def __tk_button_jog_z_neg(self, parent):
        btn = Button(parent, text="Z-", takefocus=False, )
        btn.place(x=620, y=490, width=30, height=60)
        return btn

    def __tk_label_cylinder_control(self, parent):
        label = Label(parent, text="Cyliner Control", anchor="center", )
        label.place(x=400, y=290, width=140, height=30)
        return label

    def __tk_button_cylinder_control_mode(self, parent):
        btn = Button(parent, text="Control Mode", takefocus=False, )
        btn.place(x=400, y=330, width=140, height=30)
        return btn

    def __tk_button_manual_control(self, parent):
        btn = Button(parent, text="Cylinder Manual Ctrl", takefocus=False, )
        btn.place(x=570, y=330, width=140, height=30)
        return btn

    def __tk_button_cylinder_reset(self, parent):
        btn = Button(parent, text="Cylinder Reset", takefocus=False, )
        btn.place(x=570, y=290, width=100, height=30)
        return btn

    def __tk_button_input_height(self, parent):
        btn = Button(parent, text="Input Height", takefocus=False, )
        btn.place(x=650, y=130, width=90, height=30)
        return btn


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_button_button_enable_x.bind('<Button-1>', self.ctl.enablex)
        self.tk_button_button_enable_y.bind('<Button-1>', self.ctl.enabley)
        self.tk_button_button_enable_z.bind('<Button-1>', self.ctl.enablez)
        self.tk_button_button_gozero_z.bind('<Button-1>', self.ctl.gozeroz)
        self.tk_button_button_gozero_x.bind('<Button-1>', self.ctl.gozerox)
        self.tk_button_button_gozero_y.bind('<Button-1>', self.ctl.gozeroy)
        self.tk_button_button_reset_all.bind('<Button-1>', self.ctl.reset_system)
        self.tk_button_button_reset_x.bind('<Button-1>', self.ctl.resetx)
        self.tk_button_button_reset_y.bind('<Button-1>', self.ctl.resety)
        self.tk_button_button_reset_z.bind('<Button-1>', self.ctl.resetz)
        self.tk_button_input_position.bind('<Button-1>', self.ctl.Input_Position)
        self.tk_button_magnet_take_on.bind('<Button-1>', self.ctl.mag_take_on)
        self.tk_button_magnet_release.bind('<Button-1>', self.ctl.mag_release)
        self.tk_button_display_signals.bind('<Button-1>', self.ctl.display_signals)
        self.tk_button_magnet_take_off.bind('<Button-1>', self.ctl.mag_take_off)
        self.tk_button_button_connect.bind('<Button-1>', self.ctl.connect)
        self.tk_button_button_disconnect.bind('<Button-1>', self.ctl.disconnect)
        # self.tk_button_jog_y_pos.bind('<Button-1>', self.ctl.jog_y_positive)
        # self.tk_button_jog_y_neg.bind('<Button-1>', self.ctl.jog_y_negative)
        # self.tk_button_jog_x_neg.bind('<Button-1>', self.ctl.jog_x_negative)
        # self.tk_button_jog_x_pos.bind('<Button-1>', self.ctl.jog_x_positive)
        # self.tk_button_jog_z_pos.bind('<Button-1>', self.ctl.jog_z_positive)
        # self.tk_button_jog_z_neg.bind('<Button-1>', self.ctl.jog_z_negative)
        self.tk_button_cylinder_control_mode.bind('<Button-1>', self.ctl.cylinder_mode_switch)
        self.tk_button_manual_control.bind('<Button-1>', self.ctl.cylinder_manual_control)
        self.tk_button_cylinder_reset.bind('<Button-1>', self.ctl.reset_cylinder)
        self.tk_button_input_height.bind('<Button-1>', self.ctl.input_height)
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()

# self.tk_button_jog_y_pos.bind('<ButtonPress-1>', self.ctl.jog_y_positive)
# self.tk_button_jog_y_pos.bind('<ButtonRelease-1>', self.ctl.jog_y_release)
# self.tk_button_jog_y_neg.bind('<ButtonPress-1>', self.ctl.jog_y_negative)
# self.tk_button_jog_y_neg.bind('<ButtonRelease-1>', self.ctl.jog_y_release)
# self.tk_button_jog_x_pos.bind('<ButtonPress-1>', self.ctl.jog_x_positive)
# self.tk_button_jog_x_pos.bind('<ButtonRelease-1>', self.ctl.jog_x_release)
# self.tk_button_jog_x_neg.bind('<ButtonPress-1>', self.ctl.jog_x_negative)
# self.tk_button_jog_x_neg.bind('<ButtonRelease-1>', self.ctl.jog_x_release)
# self.tk_button_jog_z_pos.bind('<ButtonPress-1>', self.ctl.jog_z_positive)
# self.tk_button_jog_z_pos.bind('<ButtonRelease-1>', self.ctl.jog_z_release)
# self.tk_button_jog_z_neg.bind('<ButtonPress-1>', self.ctl.jog_z_negative)
# self.tk_button_jog_z_neg.bind('<ButtonRelease-1>', self.ctl.jog_z_release)