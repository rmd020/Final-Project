from tkinter import *
from time import time, sleep
import random
import RPi.GPIO as GPIO

DEBUG = False
SETTLE_TIME = 2
CALIBRATIONS = 5      #how many calibrations will i check
CALIBRATION_DELAY = 2 #how much between calibrations
TRIGGER_TIME = 0.0001
SPEED_OF_SOUND = 343 # 343 m/s
known_distance = 35
difficulty = 1

GPIO.setmode(GPIO.BCM)
TRIG = 18
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def getDistance():
    #activate the trigger
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)
    
    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
        stop = time()
    # now that we have the time, convert it to distance in cm
    duration = stop-start
    distance = duration * SPEED_OF_SOUND
    distance /= 2 #divide the stance by 2
    distance *= 100 # change to cm
    return distance
 
def calibrate():
    print ("Calibrating.....")
    #ask the user to place my control measurment
    print ("-Place the sensor a measured distance away from an object")
    known_distance = 35
    distance_avg = 0
    
    # take a few known measurements and get the sum
    for i in range(CALIBRATIONS):
        distance = getDistance()
        distance_avg += distance
        sleep(CALIBRATION_DELAY)
        
    # then change it to an average
    distance_avg /= CALIBRATIONS
    
    if(DEBUG):
        print("--Average is {} cm".format(distance_avg))
    
    correction_factor = known_distance / distance_avg
    
    if(DEBUG):
        print("--Correction Factor is {}.".format(correction_factor))
    
    print ("Done\n")
    return correction_factor
 
def jump(correction_factor):
    distance = getDistance()
    if distance < (known_distance - correction_factor):
        return ("nay")
    else:
        return ("yay")
    
 
def reStart():
    again = input("\nPress enter to go again ")
    if again == " " or "":
        Main()

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, bg = "white")        
        self.master = master
        

    def Home(self):
        #Calibrates the sensor
        print("Initializing...")
        self.correction_factor = calibrate()
        print("Done with calibration")

        # widget can take all self
        self.pack(fill=BOTH, expand=1)

        # Makes the text
        Window.text = Label(self, text="Jump In", font = "Helvetica 100 bold", bg = "white" )
        Window.text.pack()

        # Makes the instructions
        Window.intro = Label(self, text = "INSTRUCTIONS: When the colored line reaches the bottom of the circle, JUMP!",\
                           font ="Helvetica 16", bg = "white", fg = "red" )
        Window.intro.place(x = 20, y = 450)

        # create button, link it to clicStartButton()
        Window.startButton = Button(self, text="START",font = "Helvetica 16 ", bg = "white", command=clickStartButton, width = 25, height = 3)
        Window.startButton.place(x =(WIDTH/3.25) , y = (HEIGHT/2))
        
   


    def clickBack(self):
        root.attributes('-fullscreen',False)




    # Allows user to pick color of rope and 
    def colorPicker(self):
        print("Color Picker")
        self.pack(fill=BOTH, expand=1)

       # Window.backButton = Button(Window, text = "BACK", bg = "grey", command=Window.clickBack, width = 10)
       # Window.backButton.place(x = 25 , y = 350)

        Window.text = Label(self, text="Rope Color", font = "Helvetica 60 bold", bg = "white" )
        Window.text.pack()
        
        Window.red = Button(self, text = "RED", bg = "red", command=clickRed, width = 15, height = 3)
        Window.red.place(x = (WIDTH - 620) , y = (HEIGHT/3))

        Window.blue = Button(self, text = "BLUE", bg = "blue", command=clickBlue, width = 15, height = 3)
        Window.blue.place(x = (WIDTH - 460) , y = (HEIGHT/3))

        Window.yellow = Button(self, text = "YELLOW", bg = "yellow", command=clickYellow, width = 15, height = 3)
        Window.yellow.place(x = (WIDTH - 300) , y = (HEIGHT/3))

        Window.purple = Button(self, text = "PURPLE", bg = "purple", command=clickPurple, width = 15, height = 3)
        Window.purple.place(x = (WIDTH - 620) , y = (HEIGHT/1.75))

        Window.green = Button(self, text = "GREEN", bg = "green", command=clickGreen, width = 15, height = 3)
        Window.green.place(x = (WIDTH - 460) , y = (HEIGHT/1.75))

        Window.orange = Button(self, text = "ORANGE", bg = "orange", command=clickOrange, width = 15, height = 3)
        Window.orange.place(x = (WIDTH - 300) , y = (HEIGHT/1.75))
        
    # Creates buttons that allow user to select rope speed
    def levelPicker(self):
        self.pack(fill=BOTH, expand=1)
        
        #Creates the buttons
        Window.easyButton = Button(self, text="SLOW",bg = "white",activebackground = "green", command=clickEasyButton, width = 20,height = 3)
        Window.easyButton.place(x = (WIDTH/2.5),  y = (HEIGHT/3))
        Window.medButton = Button(self, text="MEDIUM",bg = "white", activebackground = "yellow", command=clickMedButton, width = 20,height = 3)
        Window.medButton.place(x = (WIDTH/2.5), y = (HEIGHT/2))
        Window.hardButton = Button(self, text="FAST",bg = "white", activebackground = "red", command=clickHardButton, width = 20,height = 3)
        Window.hardButton.place(x = (WIDTH/2.5), y = (HEIGHT/1.5))
        
        # Makes the text
        Window.text = Label(self, text="Turning Speed", font = "Helvetica 70 bold", bg = "white" )
        Window.text.pack()

       
    # creates the jumprope    
    def createRope(self):
        Window.x = 0
        Window.score = 0
        clearLevel()
        self.c = Canvas(self, height = HEIGHT, width = WIDTH, bg="white")
        self.c.pack()

        
        Window.oval = self.c.create_oval(325,140,(325+150),(140 +200), fill = "grey")
        
        Window.l = self.c.create_line((WIDTH/2),HEIGHT,(WIDTH/2),(HEIGHT/2), width=5, fill = Window.ropeColor)

        Window.l2 = self.c.create_line((WIDTH - 200),HEIGHT,(WIDTH/2),(HEIGHT/2), width=5, fill = "white")
        Window.l3 = self.c.create_line(WIDTH,(HEIGHT/2),(WIDTH/2),(HEIGHT/2), width=5, fill = "white")

        Window.l4 = self.c.create_line(((WIDTH/2) + 200),0,(WIDTH/2),(HEIGHT/2), width=5, fill = "white")
        Window.l5 = self.c.create_line((WIDTH/2),0,(WIDTH/2),(HEIGHT/2), width=5, fill = "white")

        Window.l6 = self.c.create_line(200,((HEIGHT/2)- 250),(WIDTH/2),(HEIGHT/2), width=5, fill = "white")
        Window.l7 = self.c.create_line(0,(HEIGHT/2),(WIDTH/2),(HEIGHT/2), width=5, fill = "white")

        Window.l8 = self.c.create_line(((WIDTH/2)-200),HEIGHT,(WIDTH/2),(HEIGHT/2), width=5, fill = "white")
        

        #Window.oval = Window.c.create_oval(350+15,180+15,(435) ,(300), fill = "grey")
        Window.scorepic = self.c.create_text((WIDTH/2),(HEIGHT/2),text = Window.score,font = "Times 100 bold", fill = "black")

    # creates the rope animation   
    def turnRope(self):
        alist = [Window.l, Window.l2, Window.l3, Window.l4, Window.l5, Window.l6, Window.l7, Window.l8]
        print(Window.x)
        # Changes the first rope color to white
        self.c.itemconfig(alist[Window.x], fill= "white")
        if (Window.x == 7):
            self.c.itemconfig(alist[7], fill= "white")
            jump = jump(self.correction_factor)
            if( jump == "yay"):
                Window.x = -1
                Window.score += 1
                self.c.itemconfig(Window.scorepic,text = Window.score)
                print("yay, you jumped the rope.")
            else:
                self.endScreen()
           
        if (Window.x < 7):
            Window.x += 1
            self.c.itemconfig(alist[Window.x], fill= Window.ropeColor)
            self.c.after(Window.speed,self.turnRope)

    def clearRope(self):
        self.c.pack_forget()

    # creates the buttons and messages for the death screen    
    def endScreen(self):
        self.clearRope()
        Window.text2 = Label(self, text="SCORE", font = "Helvetica 80 bold", bg = "white" )
        Window.text2.place(x = 50, y = 35)

        Window.scorepic2 = Label(self, text= Window.score, font = "Helvetica 70 bold", bg = "white" )
        Window.scorepic2.place(x = 200, y = 150)

        Window.restart = Button(self, text="RESTART",font = "Helvetica 16 ", bg = "white", command = clickRestart, width = 20, height = 3)
        Window.restart.place(x = 500, y = 50)


        Window.newColor = Button(self, text="COLOR",font = "Helvetica 16 ", bg = "white", command = clickNewColor, width = 20, height = 3)
        Window.newColor.place(x = 500, y = 175)

        Window.newLevel = Button(self, text="SPEED",font = "Helvetica 16 ", bg = "white", command = clickNewSpeed, width = 20, height = 3)
        Window.newLevel.place(x = 500, y = 300)

 

# Clears the Start Screen and Goes to Color Picker screen
def clickStartButton():
    print("Initializing...")
    correction_factor = calibrate()
    print("Done with calibration")
    Window.startButton.destroy()
    Window.text.pack_forget()
    Window.intro.pack_forget()
    app.colorPicker()        

def clickRed():
    Window.ropeColor = "red"
    clearColor()
    app.levelPicker()
  
def clickBlue():
    Window.ropeColor = "blue"
    clearColor()
    app.levelPicker()
    
def clickYellow():
    Window.ropeColor = "yellow"
    clearColor()
    app.levelPicker()
    
def clickPurple():
    Window.ropeColor = "purple"
    clearColor()
    app.levelPicker()
    
def clickGreen():
    Window.ropeColor = "green"
    clearColor()
    app.levelPicker()
    
def clickOrange():
    Window.ropeColor = "orange"
    clearColor()
    app.levelPicker()
  

def clearEnd():
    Window.newLevel.destroy()
    Window.restart.destroy()
    Window.newColor.destroy()
    Window.text2.destroy()
    Window.scorepic2.destroy()

def clickRestart():
    print("restart Clicked")
    Window.clearEnd()
    app.createRope()
    app.turnRope()
    

def clickNewColor():
    print("color Clicked")
    clearEnd()
    app.colorPicker()

def clickNewSpeed():
    print(" new speed Clicked")
    clearEnd()
    app.levelPicker()
    
    
def clickEasyButton():
    Window.speed = 500
    app.createRope()
    app.c.after(Window.speed,app.turnRope)
    print(Window.ropeColor)

def clickMedButton():
    Window.speed = 250
    app.createRope()
    app.c.after(Window.speed,app.turnRope)
    print(Window.ropeColor)
    
def clickHardButton():
    Window.speed = 125
    app.createRope()
    app.c.after(Window.speed,app.turnRope)
    print(Window.ropeColor)

# clears the color picker screen
def clearColor():
    Window.red.destroy()
    Window.blue.destroy()
    Window.yellow.destroy()
    Window.purple.destroy()
    Window.green.destroy()
    Window.orange.destroy()
    Window.text.pack_forget()

#clears the Speed screen
def clearLevel():
    Window.easyButton.destroy()
    Window.medButton.destroy()
    Window.hardButton.destroy()
    Window.text.pack_forget()




HEIGHT = 480
WIDTH = 800

root = Tk()
app = Window(root)
app.Home()
root.wm_title("Jump In")
#root.attributes('-fullscreen',True)
root.geometry("{0}x{1}".format(WIDTH, HEIGHT))
root.mainloop()
