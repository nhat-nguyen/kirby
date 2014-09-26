bg = 'background.jpg'
kirby_left = 'kirby_left.png'
kirby_right = 'kirby_right.png'
flat_right = 'kirby_crouch_right.png'
flat_left = 'kirby_crouch_left.png'
dash_l = 'kirby_dash_left.png'
dash_r = 'kirby_dash_right.png'
rocket = 'rocket.png'
startscreen = 'start_screen.jpg'
instruction = 'instruction.png'
lose = 'lose.png'
shield ='barrier.png'
button = 'score_button.png'

import pygame
import time
from pygame.locals import *
from sys import exit
from random import *
pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("Hello, Kirby!")

start_screen = pygame.image.load(startscreen).convert()
ins = pygame.image.load(instruction).convert()
you_lose = pygame.image.load(lose).convert()
background = pygame.image.load(bg).convert()
char_left = pygame.image.load(kirby_left).convert_alpha()
char_right = pygame.image.load(kirby_right).convert_alpha()
crouch_left = pygame.image.load(flat_left).convert_alpha()
crouch_right = pygame.image.load(flat_right).convert_alpha()
dash_left = pygame.image.load(dash_l).convert_alpha()
dash_right = pygame.image.load(dash_r).convert_alpha()
kirby_barrier = pygame.image.load(shield).convert_alpha()
score_button = pygame.image.load(button).convert_alpha()

rocket = pygame.image.load(rocket).convert_alpha()
timer = pygame.time.Clock() # Create a timer
rockets = [] # A list to store rockets
rockets_to_be_deleted = [] # A list to store rockets finishing traveling
""" FOR Kirby """
# Default: Facing right
right = True
left = False

# Default variables for jumping
flat = False
dash = False
barrier = False
barrier_duration = 3 # 3 seconds
barrier_frame_counter = 0
#Initial standing position of Kirby
x_move, y_move = 0, 0
x, y = 0, 350 
#count the number of frames used to display the Kirby's flat apperance
count = 0
normal_speed = 555 # pixels per second
super_speed = 1234
dash_length = 211

def Distance_Calc(time, speed):
	d = time * speed
	return d

class Rocket(object):
	y = 0
	y_check = 350
	finish_travelling = False
	eliminated = False
	def __init__(self, speed, x, time):
		self.speed = speed
		self.x = x
		self.time = time

	def Falling(self):
		distance = self.time * self.speed
		self.y += distance
		return self.y

	def Finished(self):
		if self.y > 10000:
			self.finish_travelling = True
		return self.finish_travelling

class Kirby(object):
	x = 0
	y = 350

	def __init__(self, speed, time, left, right, down, dash):
		self.speed = speed
		self.left = left
		self.right = right
		self.down = down
		self.dash = dash

	def left(self):
		self.x -= self.speed * self.time
		if self.x <= 1:
			self.x = 1
	def right(self):
		self.x += self.speed * self.time
		if self.x + 150 >= 799  :
			self.x = 799
	def down(self):
		screen.blit(crouch_right, (x,y))

font = pygame.font.SysFont("Segoe UI", 26)
font_big = pygame.font.Font("DK_Sleepy_Time.otf", 48)


lost = False
check_for_replay = False
skip_instructions = False
startscreen_frame = 0

rate = 0 # 5 frames
replay = True
score = 0

while True:
	"""GETTING EVENTS """
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

		if event.type == KEYDOWN:
			skip_instructions = True # If any button is pressed, the instruction will be skipped
			"""Display the crouch animation"""
			if event.key == K_DOWN:
				flat = True # flat is the boolean to determine whether we need the character to crouch or not
			"""Press Z to activate the dash animation"""
			if event.key == K_z:
				dash = True
				#Compute the coordinate where Kirby finishes dashing
				x_finish_dash_r = x + dash_length 
				x_finish_dash_l = x - dash_length
				if x_finish_dash_r > 599: #599 is the screen's width
					x_finish_dash_r = 599 #If the dash's length exceeds the screen's width, move it back to the screen's edge
				if x_finish_dash_l < 3: # Same as above
					x_finish_dash_l = 3
			"""Press X to turn on the barrier"""
			if event.key == K_x:
				barrier = True
			"""This is for the replay part, the check_for_replay boolean is only true when the player loses
			 so that the space button does nothing when the game is still running"""
			if event.key == K_SPACE and check_for_replay:
				replay = True
				score = 0
		if event.type == KEYUP:
			#If the right/left arrow is released, the character will stop moving
			if event.key == K_RIGHT:
				x_move = 0
			if event.key == K_LEFT:
				x_move = 0
			if event.key == K_DOWN: #If the down arrow is released, the character will stop crouching
				flat = False


	"""END OF GETTING EVENTS """

	time_passed = timer.tick(120) #FPS is locked at 120
	#score += timer.get_rawtime()/1000.0
	time_passed_seconds = time_passed / 1000.0 #Convert the time passed to seconds
	score += time_passed_seconds

	rocket_rate = int(1.1 / time_passed_seconds) #Create 1 rocket every 1.1 seconds
	barrier_duration = int (5 / time_passed_seconds) # Barrier lasts for 5 seconds
	pressed_keys = pygame.key.get_pressed() #STORE THE PRESSED KEYS
	################################
	startscreen_rate = int (1.5 / time_passed_seconds)# The startscreen appears for 1.5 seconds
	###############################
	"""CALCULATING MOVEMENT
	We use the x_move to compute how many pixels we need to move the character to the the specified direction
	At first, we check for the dash boolean, if the character is facing left then the x_finish_dash_l should be 
	lesser than the current x value, thus the [ >= ]; the opposite applies to the right direction.

	Because we want the character to dash a specified length, we will continue to compute the x_move until
	the character has reached that location. After that, we change the x_move to 0 and dash to False so that the 
	character stops moving
	"""
	if dash: 
		if left:
			if x >= x_finish_dash_l:		
				x_move = -Distance_Calc(time_passed_seconds, super_speed)
			else:
				x_move = 0
				dash = False
		elif right:
			if x <= x_finish_dash_r:
				x_move = Distance_Calc(time_passed_seconds, super_speed)
			else:
				x_move = 0
				dash = False
	else:

		if pressed_keys[K_LEFT]:
			x_move = -Distance_Calc(time_passed_seconds, normal_speed)
			left = True
			right = False
		elif pressed_keys[K_RIGHT]:
			x_move = Distance_Calc(time_passed_seconds, normal_speed)
			right = True
			left = False
	#########################
	"""Move the character coordinate, if the horizontal coordinate reaches the edge, stop"""
	x += x_move
	y += y_move
	
	if x + char_left.get_width() >= 799:
		x = 799 - 150
	if x <= 1:
		x = 1
	"""The barrier moves with the character"""
	x_barrier, y_barrier = x - 85, y - 100

	if dash:
		y_barrier += 30

	#########################
	if not skip_instructions:
		screen.blit(ins, (0, 0))
		if startscreen_frame <= startscreen_rate:
			screen.blit(start_screen, (0, 0))
			startscreen_frame += 1
	else:
		if (not replay) and (lost):   # 1)
			
			screen.blit(you_lose, (0, 0))
			del rockets_to_be_deleted[:]
			del rockets[:]
			check_for_replay = True
			lost = False
			my_score_big = font_big.render('Your score: '+ str(score), True, (255, 255, 255))

			screen.blit(my_score_big, (234, 400))

		elif (replay) and (not lost):
			check_for_replay = False
			screen.blit(background, (0, 0))
			rate += 1
			barrier_frame_counter += 1
			"""Rendering Kirby
			If left is true, render the left image, if 'flat', render the crouch image,
			if 'dash', render the dash image; otherwise render the regular image"""
			if left:		
				if flat:
					screen.blit(crouch_left, (x,y))
				elif dash:
					screen.blit(dash_left, (x, y))
				else:
					screen.blit(char_left, (x,y))
			if right:
				if flat:
					screen.blit(crouch_right, (x,y))
				elif dash:
					screen.blit(dash_right, (x, y))
				else:
					screen.blit(char_right, (x,y))

			"""If the barrier duration has been reached, turn it off"""
			if barrier_frame_counter >= barrier_duration:
				barrier = False
				barrier_frame_counter = 0
			if barrier:
				screen.blit(kirby_barrier, (x_barrier, y_barrier))
			
			###########################
			"""Create rockets according to the rate"""
			if rate >= rocket_rate:
				for i in range(0, randint(0, 4)):
					rockets.append(Rocket(randint(50, 600), randint(0, 800), time_passed_seconds))
				rate = 0
			#easy : 100
			#medium: randint(50, 600) every 1.1 seconds
			"""Rendering ROCKETS"""

			for i in range(0, len(rockets)):
				rockets[i].Falling()
				"""If the rockets touch the barrier when it's on, they will be marked as 'eliminated'
				Eliminate rockets won't be rendered"""
				if barrier:
					if (rockets[i].x >= x_barrier) and (rockets[i].x <= x_barrier + 250):
						if (rockets[i].y + 100 >= y_barrier):
							rockets[i].eliminated = True

				"""If the rocket hasn't finished travelling and is not eliminated, render it"""
				if (not rockets[i].Finished()) and (not rockets[i].eliminated):
					screen.blit(rocket, (rockets[i].x, rockets[i].y))

				"""Check for collision"""
				if rockets[i].y + 80 >= 350 and rockets[i].y + 80 < 600: # 80 is the height of the rocket
					for k in range(int(x + 42), int(x + 121)):
						rockets[i].y_check += 1
						R, G, B, transparent = tuple(screen.get_at((k, 350)))
						if (R == 255) and (G == 255) and (B == 255):
							lost = True
							replay = False

				"""Delete used rockets"""
				if rockets[i].Finished():
					rockets_to_be_deleted.append(i)
			for i in rockets_to_be_deleted:
					del rockets[i]
			del rockets_to_be_deleted[:]

			"""Render the score on screen"""
			my_score = font.render(str(score), True, (255, 255, 255))
			screen.blit(score_button, ((x - 20), (y + 107)))

			screen.blit(my_score, ((x + char_right.get_width() / 3.3), (y + char_right.get_height() - 2)))

	pygame.display.update()

