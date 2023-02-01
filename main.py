import pygame
import serial

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

Axis1 = 0
Axis0 = 0
Axis4 = 0
ser = serial.Serial('COM8')  # open serial port()

from socket import *
import time

global latest
latest = ["0.00", "0.00", "0.00", "0.00", "0.00", "0.00"]
controlling_cam = 1
claw = "Open"
controlling_camera_one = True
cam_status = ["Center", "Center"]
# address = ('169.254.9.25', 80)
# client_socket = socket(AF_INET, SOCK_DGRAM)
#client_socket.bind(('169.254.168.151', '80'))
print("socket setup complete")

def crossCheck(msg, lastSent):
    if lastSent != "" and abs(float(msg[2:])) > 0.1 and abs(float(lastSent)) > 0.1:
        if abs(abs(float(msg[2:])) - abs(float(lastSent))) < 0.05:
            return False
    return True


def crossCheck(msg, lastSent):
    if lastSent != "" and abs(float(msg[2:])) > 0.1 and abs(float(lastSent)) > 0.1:
        if abs(abs(float(msg[2:])) - abs(float(lastSent))) < 0.05:
            return False
    return True


def message(msg, latest):
    if ser.is_open == False:
        ser.open()

    msg = msg[0] + " " + str(round(float(msg[2:]), 3))
    
    if(crossCheck(msg, latest) == True):
        ser.write(str(msg + "x").encode())  # send the serial message
        print(str(msg + "x"))
        return str(msg[2:])
    else:
        # print("Cancelled", msg)
        return str(latest[2:])
    #ser.close()
    # msg = msg[0] + " " + str(round(float(msg[2:]), 3))
    
    # if(crossCheck(msg, latest) == True):
    #     client_socket.sendto(str.encode(msg), address)
    #     print("Sending", msg)
    #     return str(msg[2:])
    # else:
    #     print("Cancelled", msg)
    #     return str(latest[2:])
    
   # rec_data, addr = client_socket.recvfrom(2048)  # Read response from arduino
    
    #rec_string = rec_data.decode('utf-8')
    #print("Recieved", rec_string)  # Print the response from Arduino

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()
print("ready")
print("wait for arduino")
fineMode = False
fineMultiplier = 0.2
# while True:
#     if ser.in_waiting:
#         break
print("arduino ready")
stopped = [True] * 10

# -------- Main Program Loop -----------
while not done:
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get():  # User did something.
        # print("event happened")
        # print(event.type)
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True  # Flag that we are done so we exit this loop.

        # elif event.type == pygame.JO YBUTTONDOWN:
        #     print("Joystick button pressed.")
        # elif event.type == pygame.JOYBUTTONUP:
        #     print("Joystick button released.")

        screen.fill(WHITE)
        textPrint.reset()
        # print(pygame.joystick)
        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()
        # print(joystick_count)
        textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
        textPrint.indent()

        # For each joystick:
        for i in range(joystick_count):
            # print("joystick")
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            textPrint.tprint(screen, "Joystick {}".format(i))
            textPrint.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            textPrint.tprint(screen, "Joystick name: {}".format(name))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.tprint(screen, "Number of axes: {}".format(axes))
            textPrint.indent()

            for j in range(axes):
                # while ser.in_waiting:
                #     print(ser.readline())
                axis = joystick.get_axis(j)
                textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(j, axis))
               
                if j != 4 and j != 5 and abs(axis) < 0.3:
                    if not stopped[j]:
                        stopped[j] = True
                        latest[j] = message(str(j) + " 0", latest[j])
                elif j == 4 and axis > 0.9:
                    message("4 1.00", "999")
                    claw = "Open"
                    print("Claw Open")
                elif j == 5 and axis > 0.9:
                    if fineMode:
                        message("4 -0.20", "999")
                        claw = "Close"
                        print("Claw close fine")
                    else:
                        message("4 -1.00", "999")
                        claw = "Open"
                        print("Claw Close")
                else:
                    if j != 4 and j != 5:
                        stopped[j] = False
                        
                        # if j != 4 and j != 5:
                        latest[j] = message(str(j) + " " + str(axis), latest[j])

            textPrint.unindent()
            textPrint.indent()
            textPrint.tprint(screen, "Fine mode: {}".format(fineMode))
            textPrint.tprint(screen, "Claw Status: {}".format(claw))
            textPrint.tprint(screen, "Camera 1 Status: {}".format(cam_status[0]))
            textPrint.tprint(screen, "Camera 2 Status: {}".format(cam_status[1]))
            if joystick.get_button(0) == 1:
                fineMode = not fineMode
                print("fine mode set to " + str(fineMode))
            elif joystick.get_button(3) == 1:
                
                inputR = input("run auto?")
                if inputR == "y":
                    while True:
                        message("1 -1.0", "999")
            elif joystick.get_button(5) == 1:
                message("5 0.95", "999")
                print("Claw Rotate Flip")
            elif joystick.get_button(4) == 1:
                message("5 -0.95", "999")
                print("Claw Rotate Flip")
            textPrint.unindent()
            textPrint.indent()
            hats = joystick.get_numhats()
            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (-1,0):
                    print("Camera is moved to left")
                    message(str(5 + int(controlling_cam)) + " -1.0", "999")
                    cam_status[controlling_cam - 1] = "Left"
                elif hat == (1,0):
                    print("Camera is moved to right")
                    message(str(5 + int(controlling_cam)) + " 1.875", "999")
                    cam_status[controlling_cam - 1] = "Right"
                elif hat == (0,1):
                    print("Camera is moved to normal position")
                    message(str(5 + int(controlling_cam)) + " 0.0", "999")
                    cam_status[controlling_cam - 1] = "Center"
                elif hat == (0,-1):
                    print("Switching camera control")
                    controlling_camera_one = not controlling_camera_one
                    if controlling_camera_one:
                        print("Controlling Cam 1")
                        controlling_cam = 1
                    else:
                        print("Controlling Cam 2")
                        controlling_cam = 2
            textPrint.tprint(screen, "Controlling Camera: {}".format(str(controlling_cam)))
            
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()