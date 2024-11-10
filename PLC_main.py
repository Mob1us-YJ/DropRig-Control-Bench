
from PLC_GUI import Win as MainWin
# from PLC_UI_control import Controller as MainUIController
from PLC_Controller import Controller as MainUIController
from PLC_client import PLCclient

plc_client = PLCclient("192.168.2.10",0,0)
controller = MainUIController(plc_client)
app = MainWin(controller)

if __name__ == "__main__":
    app.mainloop()