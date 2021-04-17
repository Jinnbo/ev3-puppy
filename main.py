#!/usr/bin/env pybricks-micropython

import urandom
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch

# Puppy class
class Puppy:

    # Constants for leg angle
    HALF_UP_ANGLE = 25
    STAND_UP_ANGLE = 65
    STRETCH_ANGLE = 125

    
    # Loads the different eyes
    HEART_EYES = Image(ImageFile.LOVE)
    SQUINTY_EYES = Image(ImageFile.TEAR)  

    def __init__(self):
        
        # Sets up the brick 
        self.ev3 = EV3Brick()

        # Identifies which motor is connected to which ports
        self.left_leg_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
        self.right_leg_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)

        # Sets up the gear ratio (automatically translates it to the correct angle)
        self.head_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE,
                                gears=[[1, 24], [12, 36]])

        
        # Sets up touch sensor
        self.touch_sensor = TouchSensor(Port.S1)

        # Sets up constants for the eye 
        self.eyes_timer_1 = StopWatch()
        self.eyes_timer_1_end = 0
        self.eyes_timer_2 = StopWatch()
        self.eyes_timer_2_end = 0
        self.eyes_closed = False


    def movements(self):
    
        self.ev3.screen.load_image(ImageFile.EV3_ICON)
        self.ev3.light.on(Color.ORANGE)
        dog_pat = 0

        # Movement interactions
        while True:
            buttons = self.ev3.buttons.pressed()
            if Button.CENTER in buttons:
                break
            elif Button.UP in buttons:
                self.head_motor.run(20)
            elif Button.DOWN in buttons:
                self.head_motor.run(-20)
            elif self.touch_sensor.pressed():
                self.ev3.speaker.play_file(SoundFile.DOG_BARK_1)
                self.eyes = self.HEART_EYES
                self.sit_down()
                dog_pat +=1
                print(dog_pat)
            elif dog_pat == 3:
                self.go_to_bathroom()
                dog_pat -=3
                print(dog_pat)
            else:
                self.head_motor.stop()
            wait(100)

        self.head_motor.stop()
        self.head_motor.reset_angle(0)
        self.ev3.light.on(Color.GREEN) 


    # Below this line I honestly have no clue how it works. It came from the boiler plate of functions
    def move_head(self, target):
        self.head_motor.run_target(20, target)

    @property
    def eyes(self):
        return self._eyes

    @eyes.setter
    def eyes(self, value):
        if value != self._eyes:
            self._eyes = value
            self.ev3.screen.load_image(value)

    def update_eyes(self):
        if self.eyes_timer_1.time() > self.eyes_timer_1_end:
            self.eyes_timer_1.reset()
            if self.eyes == self.SLEEPING_EYES:
                self.eyes_timer_1_end = urandom.randint(1, 5) * 1000
                self.eyes = self.TIRED_RIGHT_EYES
            else:
                self.eyes_timer_1_end = 250
                self.eyes = self.SLEEPING_EYES

        if self.eyes_timer_2.time() > self.eyes_timer_2_end:
            self.eyes_timer_2.reset()
            if self.eyes != self.SLEEPING_EYES:
                self.eyes_timer_2_end = urandom.randint(1, 10) * 1000
                if self.eyes != self.TIRED_LEFT_EYES:
                    self.eyes = self.TIRED_LEFT_EYES
                else:
                    self.eyes = self.TIRED_RIGHT_EYES

    def stand_up(self):
        self.left_leg_motor.run_target(100, self.HALF_UP_ANGLE, wait=False)
        self.right_leg_motor.run_target(100, self.HALF_UP_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

        self.left_leg_motor.run_target(50, self.STAND_UP_ANGLE, wait=False)
        self.right_leg_motor.run_target(50, self.STAND_UP_ANGLE)
        while not self.left_leg_motor.control.done():
            wait(100)

        wait(500)

    
    def sit_down(self):
        self.left_leg_motor.run(-50)
        self.right_leg_motor.run(-50)
        wait(1000)
        self.left_leg_motor.stop()
        self.right_leg_motor.stop()
        wait(100)

    def go_to_bathroom(self):
        self.eyes = self.SQUINTY_EYES
        self.stand_up()
        wait(100)
        self.right_leg_motor.run_target(100, self.STRETCH_ANGLE)
        wait(800)
        self.ev3.speaker.play_file(SoundFile.HORN_1)
        wait(1000)
        for _ in range(3):
            self.right_leg_motor.run_angle(100, 20)
            self.right_leg_motor.run_angle(100, -20)
        self.right_leg_motor.run_target(100, self.STAND_UP_ANGLE)

   

    def run(self):
        self.movements()
        self.eyes = self.SLEEPING_EYES
        
       
        

if __name__ == '__main__':
    puppy = Puppy()
    puppy.run()
