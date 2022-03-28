import pygame
import random
import time

pygame.init()

cell_size = 1

WINDOW_X, WINDOW_Y = 500 * cell_size, 500 * cell_size

WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

pygame.display.set_caption("Sidewinder")

clock = pygame.time.Clock()

BIG_FONT = pygame.font.Font('font/dpcomic.ttf', 80)
DEFAULT_FONT = pygame.font.Font('font/dpcomic.ttf', 40)
SMALL_FONT = pygame.font.Font('font/dpcomic.ttf', 32)

cell_list = []
object_list = []
body_part_list = []

# width in pixels on each cell
cell_width = 20 * cell_size

# start at top left corner
cell_x, cell_y = 0, 0

# amount of cells in x and y
x_axis = 25
y_axis = 25

bg_color = (255, 225, 200)

grid_border_color = (225,200,175)#bg_color

# player start position
target_cell_x, target_cell_y = 200, 200

show_rects = False

player_head_image = pygame.image.load('images/head.png').convert()
player_head_image.set_colorkey((255,255,255))
player_head_image = pygame.transform.scale(player_head_image, (player_head_image.get_width()*2*cell_size , player_head_image.get_height()*2*cell_size))

player_body_image = pygame.image.load('images/body.png').convert()
player_body_image.set_colorkey((255,255,255))
player_body_image = pygame.transform.scale(player_body_image, (player_body_image.get_width()*2*cell_size , player_body_image.get_height()*2*cell_size))

player_tail_image = pygame.image.load('images/tail.png').convert()
player_tail_image.set_colorkey((255,255,255))
player_tail_image = pygame.transform.scale(player_tail_image, (player_tail_image.get_width()*2*cell_size , player_tail_image.get_height()*2*cell_size))

player_joint_image = pygame.image.load('images/joint.png').convert()
player_joint_image.set_colorkey((255,255,255))
player_joint_image = pygame.transform.scale(player_joint_image, (player_joint_image.get_width()*2*cell_size, player_joint_image.get_height()*2*cell_size))

class Object():
	def __init__(self, start_x, start_y, object_type='food'):
		self._id = len(object_list)
		self.object_type = object_type
		self.rect = pygame.Rect(start_x, start_y, cell_width, cell_width)
		self.width = cell_width
		self.image = pygame.image.load("images/"+object_type+".png").convert()
		self.image.set_colorkey((255,255,255))
		self.image = pygame.transform.scale(self.image, (self.width, self.width))
		self.active = True
		object_list.append(self)

		self.movement_count = 0 # counts how many times the object has moved from its start position

		if self.object_type == 'blue_food':
			self.directions = ['down', 'up']
			self.does_move = True
			self.direction = self.directions[0]
		elif self.object_type == 'green_food' or self.object_type == 'red_food':
			self.directions = ['right', 'left']
			self.direction = self.directions[0]
			self.does_move = True
		else:
			self.does_move = False

		self.movement_distance = 8

	def move(self):
		if self.does_move and self.active:
			if self.direction == 'down':
				self.rect.y += cell_width
				self.movement_count += 1

			elif self.direction == 'up':
				self.rect.y -= cell_width
				self.movement_count -= 1

			elif self.direction == 'right':
				self.rect.x += cell_width
				self.movement_count += 1

			elif self.direction == 'left':
				self.rect.x -= cell_width
				self.movement_count -= 1

			if self.movement_count == self.movement_distance:
				self.direction = self.directions[1]

			elif self.movement_count == 0:
				self.direction = self.directions[0]

	def update(self):
		if self.active:
			WINDOW.blit(self.image, (self.rect.x, self.rect.y))

			if self.rect.x + cell_width >= WINDOW_X:
				self.rect.x = 0

			if self.rect.y + cell_width >= WINDOW_Y:
				self.rect.y = 0

			if self.rect.x  <= 0:
				self.rect.x = WINDOW_X - cell_width

			if self.rect.y <= 0:
				self.rect.y = WINDOW_Y - cell_width

class BodyPart():
	def __init__(self, start_x, start_y):
		self._id = len(body_part_list)
		self.rect = pygame.Rect(start_x, start_y, cell_width, cell_width)
		self.image = player_body_image
		self.default_image = self.image
		self.coordinates = (self.rect.x, self.rect.y)

		body_part_list.append(self)

		if self == body_part_list[0]:
			self.direction = 'right'
		else:
			self.direction =  body_part_list[self._id-1].direction

	def update(self):
		# decide which image to show according to list
		if self == body_part_list[0]:
			self.image = player_head_image
		elif self == body_part_list[-1]:
			self.image = player_tail_image
		else:
			self.image = player_body_image

		if self._id == 0:
			if self.direction == "right":
				if self.rect.x + cell_width >= WINDOW_X:
					self.rect.x = 0
				else:
					self.rect.x += cell_width
					
				self.image = pygame.transform.rotate(self.image, 0)

			elif self.direction == "down":
				if self.rect.y + cell_width >= WINDOW_Y:
					self.rect.y = 0
				else:

					self.rect.y += cell_width
				self.image = pygame.transform.rotate(self.image, 270)

			elif self.direction == "left":
				if self.rect.x  <= 0:
					self.rect.x = WINDOW_X - cell_width
				else:
					self.rect.x -= cell_width
				self.image = pygame.transform.rotate(self.image, 180)

			elif self.direction == "up":
				if self.rect.y <= 0:
					self.rect.y = WINDOW_Y - cell_width
				else:
					self.rect.y -= cell_width
				self.image = pygame.transform.rotate(self.image, 90)

		else:
			if self.direction == "right":
				self.image = pygame.transform.rotate(self.image, 0)

			if self.direction == "down":
				self.image = pygame.transform.rotate(self.image, 270)

			if self.direction == "left":
				self.image = pygame.transform.rotate(self.image, 180)

			if self.direction == "up":
				self.image = pygame.transform.rotate(self.image, 90)

		self.coordinates = (self.rect.x, self.rect.y)

	def draw(self):
		if show_rects:
			pygame.draw.rect(WINDOW, (255,50,50), self.rect)
		WINDOW.blit(self.image, (self.rect.x, self.rect.y))

def start_game(): # reset game values
	obstacle_spawn_timer = pygame.time.get_ticks()
	display_update_timer = pygame.time.get_ticks()

	body_part_list.clear()
	object_list.clear()

	spawn_object()

	start_head_body_part = BodyPart(target_cell_x, target_cell_y)
	start_middle_body_part = BodyPart(start_head_body_part.rect.x-cell_width, start_head_body_part.rect.y)
	start_tail_body_part = BodyPart(start_middle_body_part.rect.x-cell_width, start_middle_body_part.rect.y)

def game_over(total_score_count):

	high_score_file = open('highscore.txt', 'r')
	high_score = int(high_score_file.read())
	high_score_file.close()

	game_over_message = "Game over !"

	# update high score and change color if total score surpasses it
	if total_score_count > high_score:
		highscore_color = (175,175,255)
		highscore_shadow_color = (50,50, 100)
		highscore_message = "New High score : " + str(total_score_count)

		high_score_file = open('highscore.txt', 'w+')
		high_score_file.write(str(total_score_count))
		high_score_file.close()

	else:
		highscore_message = "High score : " + str(high_score)
		highscore_color = (250,225,75)
		highscore_shadow_color = (100,75,25)

	highscore_text = SMALL_FONT.render(highscore_message, 1, highscore_color)
	highscore_text_shadow = SMALL_FONT.render(highscore_message, 1, highscore_shadow_color)

	game_over_text = BIG_FONT.render(game_over_message, 1, (100, 225, 100))
	game_over_text_shadow = BIG_FONT.render(game_over_message, 1, (25, 75, 50))

	score_count_text = BIG_FONT.render(str(total_score_count), 1, (255,50,0))
	score_count_text_shadow = BIG_FONT.render(str(total_score_count), 1, (125,25,0))

	game_over_timer = pygame.time.get_ticks()

	screen_layer = pygame.Surface((WINDOW_X, WINDOW_Y)).convert()
	screen_layer.set_colorkey((0,0,0))

	color_overlay = pygame.Surface((WINDOW_X, WINDOW_Y)).convert()
	color_overlay.fill((0,0,0))
	color_overlay.set_alpha(125)
	WINDOW.blit(color_overlay, (0,0))

	game_over_loop = True
	while game_over_loop:

		screen_layer.blit(game_over_text_shadow, ( int(WINDOW_X/2) - int(game_over_text.get_width()/2) + text_shadow_width, 200 + text_shadow_width * cell_size))
		screen_layer.blit(game_over_text, ( int(WINDOW_X/2)- int(game_over_text.get_width()/2), 200 * cell_size))			

		screen_layer.blit(highscore_text_shadow, ( int(WINDOW_X/2) - int(highscore_text.get_width()/2) + text_shadow_width, 440 + text_shadow_width * cell_size))
		screen_layer.blit(highscore_text, ( int(WINDOW_X/2) - int(highscore_text.get_width()/2), 440 * cell_size))

		WINDOW.blit(score_count_text_shadow, ( int(WINDOW_X/2) - int(score_count_text.get_width()/2) + text_shadow_width, 20 + text_shadow_width))
		WINDOW.blit(score_count_text, ( int(WINDOW_X/2)- int(score_count_text.get_width()/2), 20))

		WINDOW.blit(screen_layer, (0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					high_score_file = open('highscore.txt', 'w+')
					high_score_file.write("0")
					high_score_file.close()

					print("Highscore has been reset !")

			if event.type == pygame.KEYDOWN:
				if pygame.time.get_ticks() - game_over_timer > 2000:
					game_over_loop = False

		pygame.display.update()

	start_game()

# draw each individual cell to form the grid
def draw_grid_layout():
	for each_cell in cell_list:
		# draw borders
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

def spawn_object(object_type='food'):
	target_cell_occupied = False
	rx = random.randint(1, x_axis-1)
	ry = random.randint(1, y_axis-1)

	# if an object is already occupying the cell, get new coordinates
	for objects in object_list:
		if rx == objects.rect.x and ry == objects.rect.y:
			rx = random.randint(1, x_axis-1)
			ry = random.randint(1, y_axis-1)

	for bodies in body_part_list:
		if rx == bodies.rect.x and ry == bodies.rect.y:
			rx = random.randint(1, x_axis-1)
			ry = random.randint(1, y_axis-1)

	rx = rx * cell_width
	ry = ry * cell_width

	for bodypart in body_part_list:
		if rx == bodypart.rect.x and ry == bodypart.rect. y:
			target_cell_occupied = True
			print("Cell occupied by body part !") 
			spawn_object(object_type)

	for objects in object_list:
		if rx == objects.rect.x and ry == objects.rect.y:
			target_cell_occupied = True
			print("Cell occupied by obstacle !")
			if len(object_list) < 1:
				print("SPAWNING NEW !!!")
			spawn_object(object_type)

	if not target_cell_occupied:
		new_object = Object(rx, ry, object_type)
		print("Spawned new object at: " + str(rx) + ", " + str(ry) + " with id: " + str(new_object._id) )

def player_grow():
	# spawn a new body part behind the last body part	
	new_rect = BodyPart(body_part_list[-1].rect.x, body_part_list[-1].rect.y)


for each_object in object_list:
	if body_part_list[0].rect.colliderect(each_object.rect):
		print("player head has collided with a foreign object!")
		game_over()

for y_cell in range(y_axis):
	for x_cell in range(x_axis):
		individual_cell = pygame.Rect( (cell_width * x_cell), (cell_width * y_cell), cell_width * cell_size, cell_width * cell_size)
		cell_list.append(individual_cell)

# set fixed cell coordinates
for each_cell in cell_list:
	# dividing by cell width to get correct x and y of cells and not pixels
	each_cell_x = int(each_cell.x / cell_width)
	each_cell_y = int(each_cell.y / cell_width)

# timers to control various events
display_update_timer = pygame.time.get_ticks()
obstacle_spawn_timer = pygame.time.get_ticks()
direction_change_cooldown_timer = pygame.time.get_ticks()
direction_change_cooldown = 66
display_update_delay = 100
score_count = 0

# starter body rect
start_head_body_part = BodyPart(target_cell_x, target_cell_y)
start_middle_body_part = BodyPart(start_head_body_part.rect.x-cell_width, start_head_body_part.rect.y)
start_tail_body_part = BodyPart(start_middle_body_part.rect.x-cell_width, start_middle_body_part.rect.y)
text_shadow_width = 3

score_gathered = False # to prevent extra points
        
FPS = 60
running = True
while running:
	clock.tick(FPS) # set fixed framerate
	WINDOW.fill(bg_color) # draw background color

	score_count_text = BIG_FONT.render(str(score_count), 1, (255,100,0))
	score_count_text_shadow = BIG_FONT.render(str(score_count), 1, (125,50,0))
	draw_grid_layout() # draw cell rows and columns

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				if body_part_list[0].direction == 'up' or body_part_list[0].direction == 'down':
					if pygame.time.get_ticks() - direction_change_cooldown_timer > direction_change_cooldown:
						body_part_list[0].direction = 'right'
						direction_change_cooldown_timer = pygame.time.get_ticks()

			if event.key == pygame.K_DOWN:
				if body_part_list[0].direction == 'left' or body_part_list[0].direction == 'right':
					if pygame.time.get_ticks() - direction_change_cooldown_timer > direction_change_cooldown:
						body_part_list[0].direction = 'down'
						direction_change_cooldown_timer = pygame.time.get_ticks()

			if event.key == pygame.K_LEFT:
				if body_part_list[0].direction == 'up' or body_part_list[0].direction == 'down':
					if pygame.time.get_ticks() - direction_change_cooldown_timer > direction_change_cooldown:
						body_part_list[0].direction = 'left'
						direction_change_cooldown_timer = pygame.time.get_ticks()						

			if event.key == pygame.K_UP:
				if body_part_list[0].direction == 'left' or body_part_list[0].direction == 'right':
					if pygame.time.get_ticks() - direction_change_cooldown_timer > direction_change_cooldown:
						body_part_list[0].direction = 'up'
						direction_change_cooldown_timer = pygame.time.get_ticks()

			if event.key == pygame.K_SPACE:
				player_grow()

	# spawn a new object every third second
	if pygame.time.get_ticks() - obstacle_spawn_timer > 10000:
		obstacle_spawn_timer = pygame.time.get_ticks()
		rng = random.randint(0, 10)
		if rng == 0:
			spawn_object('blue_food')
		elif rng == 1:
			spawn_object('green_food')
		elif rng == 2:
			spawn_object('red_food')
		elif rng == 3:
			spawn_object('grey_food')
		elif rng == 4:
			spawn_object('obstacle')

	if pygame.time.get_ticks() - display_update_timer > display_update_delay:
		display_update_timer = pygame.time.get_ticks()
		score_gathered = False

		# we loop in reverse so we can find the x and y
		# values of each rect, prior to being updated
		# this means we can find the previous rect's old x and y values
		for body_id in range(len(body_part_list)-1, -1, -1): # loop from len of list to -1 (excluding -1), and decrement by 1 for each loop
			x_body = body_part_list[body_id]
			previous_x_body = body_part_list[body_id-1]

			if x_body == body_part_list[0]:
				pass
			else:
				x_body.rect.x = previous_x_body.rect.x
				x_body.rect.y = previous_x_body.rect.y

				if previous_x_body.direction != x_body.direction:
					x_body.direction = previous_x_body.direction

		for objects in object_list:
			objects.move()

		for bodypart in body_part_list:
			bodypart.update()

		for body_id in range(len(body_part_list)):
			x_body = body_part_list[body_id]
			next_x_body = body_part_list[body_id-1]
		
			if next_x_body != body_part_list[-1] and next_x_body:

				if next_x_body.direction != x_body.direction:
					if next_x_body.direction == 'right' and x_body.direction == 'down':
						next_x_body.image = pygame.transform.rotate(player_joint_image, 90)

					elif next_x_body.direction == 'left' and x_body.direction == 'down':
						next_x_body.image = pygame.transform.rotate(player_joint_image, 180)

					elif next_x_body.direction == 'left' and x_body.direction == 'up':
						next_x_body.image = pygame.transform.flip(player_joint_image, True, False)

					elif next_x_body.direction == 'up' and x_body.direction == 'left':
						next_x_body.image = pygame.transform.rotate(player_joint_image, 90)
  
					elif next_x_body.direction == 'up' and x_body.direction == 'right':
						next_x_body.image = pygame.transform.rotate(player_joint_image, 180)

					elif next_x_body.direction == 'down' and x_body.direction == 'right':
						next_x_body.image = pygame.transform.flip(player_joint_image, True, False)
					else:
						next_x_body.image = player_joint_image


	# call update method in every existing object
	for objects in object_list:
		objects.update()

	for bodypart in body_part_list:
		bodypart.draw()

	# spawn food if none are present in the game
	foods_available = None
	for objects in object_list: # check if food is available
		if objects.object_type == 'food' and objects.active:
			foods_available = True

	if not foods_available:
		spawn_object()

	WINDOW.blit(score_count_text_shadow, ( int(WINDOW_X/2)- int(score_count_text.get_width()/2) + text_shadow_width, 20 + text_shadow_width))
	WINDOW.blit(score_count_text, ( int(WINDOW_X/2)- int(score_count_text.get_width()/2), 20))

	# assign each rect an id and check if a body
	# rect has collided with the player head rect
	for body_id in range(len(body_part_list)):
		x_body_rect = body_part_list[body_id].rect
		if body_part_list[0].rect.colliderect(x_body_rect):
			if body_id == 0:
				pass
			else:
				print("player head has collided with: body rect id {0} !".format(body_id))
				total_score_count = score_count
				score_count = 0
				game_over(total_score_count)
				break # break so the loop does not continue after the game reset

	# check if an object has collided with player and give specific points
	for objects in object_list:
		for b in body_part_list:
			if b.rect.colliderect(objects.rect):
				pass
		if (body_part_list[0].rect.colliderect(objects) or body_part_list[1].rect.colliderect(objects.rect) ) and objects.active and score_gathered == False:# and score_gathered == False:
			if objects.object_type == 'red_food':
				player_grow()
				score_count += 9
				objects.active = False
				score_gathered = True

			elif objects.object_type == 'grey_food':
				player_grow()
				score_count += 12
				objects.active = False
				score_gathered = True

			elif objects.object_type == 'blue_food':
				player_grow()	
				score_count += 24
				objects.active = False
				score_gathered = True

			elif objects.object_type == 'green_food':
				player_grow()
				score_count += 12
				objects.active = False
				score_gathered = True

			elif objects.object_type == 'food':
				player_grow()
				score_count += 3
				objects.active = False
				score_gathered = True

			elif objects.object_type == 'obstacle':
				print("player head has collided with: obstacle id {0} !".format(objects._id))
				total_score_count = score_count
				score_count = 0
				game_over(total_score_count)
				break

			objects.active = False

	print(score_gathered)

	pygame.display.update()
