import serial

ser = serial.Serial('com3',9600)
ser.setDTR(False)

while True:
    try:
        command = input()
        ser.write(command.encode())
    except KeyboardInterrupt:
        break
print("Close Port")
ser.close()
