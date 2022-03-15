import pygame
import random

pygame.init()

cell_size = 1

WINDOW_X, WINDOW_Y = 500 * cell_size, 500 * cell_size

WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

pygame.display.set_caption("Sidewinder")

clock = pygame.time.Clock()

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

player_head_image = pygame.image.load('images/head.png')
player_head_image = pygame.transform.scale(player_head_image, (player_head_image.get_width()*2*cell_size , player_head_image.get_height()*2*cell_size))

player_body_image = pygame.image.load('images/body.png')
player_body_image = pygame.transform.scale(player_body_image, (player_body_image.get_width()*2*cell_size , player_body_image.get_height()*2*cell_size))

player_tail_image = pygame.image.load('images/tail.png')
player_tail_image = pygame.transform.scale(player_tail_image, (player_tail_image.get_width()*2*cell_size , player_tail_image.get_height()*2*cell_size))

player_joint_image = pygame.image.load('images/joint.png')
player_joint_image = pygame.transform.scale(player_joint_image, (player_joint_image.get_width()*2*cell_size, player_joint_image.get_height()*2*cell_size))

class Object():
	def __init__(self, start_x, start_y):
		self.rect = pygame.Rect(start_x, start_y, cell_width, cell_width)
		self.width = cell_width
		self.image = pygame.image.load("images/food.png").convert()
		self.image = pygame.transform.scale(self.image, (self.width, self.width))
		object_list.append(self)

	def update(self):
		WINDOW.blit(self.image, (self.rect.x, self.rect.y))

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
		pygame.draw.rect(WINDOW, (255,50,50), self.rect)
		WINDOW.blit(self.image, (self.rect.x, self.rect.y))

def start_game(): # reset game values
	obstacle_spawn_timer = pygame.time.get_ticks()
	display_update_timer = pygame.time.get_ticks()

	body_part_list.clear()
	object_list.clear()

	start_head_body_part = BodyPart(target_cell_x, target_cell_y)
	start_middle_body_part = BodyPart(start_head_body_part.rect.x-cell_width, start_head_body_part.rect.y)
	start_tail_body_part = BodyPart(start_middle_body_part.rect.x-cell_width, start_middle_body_part.rect.y)

def game_over():
	print("Game over !")
	print("You died !")

	game_over_loop = True

	screen_layer = pygame.Surface((WINDOW_X, WINDOW_Y)).convert_alpha()
	while game_over_loop:
		screen_layer.fill((0,0,0,0.5))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				game_over_loop = False

	start_game()

# draw each individual cell to form the grid
def draw_grid_layout():
	for each_cell in cell_list:
		# draw borders
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

def spawn_object():
	rx = random.randint(1, x_axis-1)
	ry = random.randint(1, y_axis-1)
	rx = rx * cell_width
	ry = ry * cell_width
	new_object = Object(rx, ry)
	print("Spawned new object at: " + str(rx) + ", " + str(ry))

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

display_update_delay = 100

# starter body rect
start_head_body_part = BodyPart(target_cell_x, target_cell_y)
start_middle_body_part = BodyPart(start_head_body_part.rect.x-cell_width, start_head_body_part.rect.y)
start_tail_body_part = BodyPart(start_middle_body_part.rect.x-cell_width, start_middle_body_part.rect.y)

FPS = 60
running = True
while running:
	clock.tick(FPS) # set 

	WINDOW.fill(bg_color) # draw background color

	draw_grid_layout() # draw cell rows and columns

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				if body_part_list[0].direction == 'up' or body_part_list[0].direction == 'down':
					body_part_list[0].direction = 'right'

			if event.key == pygame.K_DOWN:
				if body_part_list[0].direction == 'left' or body_part_list[0].direction == 'right':
					body_part_list[0].direction = 'down'

			if event.key == pygame.K_LEFT:
				if body_part_list[0].direction == 'up' or body_part_list[0].direction == 'down':
					body_part_list[0].direction = 'left'

			if event.key == pygame.K_UP:
				if body_part_list[0].direction == 'left' or body_part_list[0].direction == 'right':
					body_part_list[0].direction = 'up'

			if event.key == pygame.K_SPACE:
				player_grow()

	# call update method in every existing object
	for each_object in object_list:
		each_object.update()

	# spawn a new object every third second
	if pygame.time.get_ticks() - obstacle_spawn_timer > 3000:
		obstacle_spawn_timer = pygame.time.get_ticks() 
		spawn_object()

	if pygame.time.get_ticks() - display_update_timer > display_update_delay:
		display_update_timer = pygame.time.get_ticks()

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

	for bodypart in body_part_list:
		bodypart.draw()

	# assign each rect an id and check if a body
	# rect has collided with the player head rect
	for body_id in range(len(body_part_list)):
		x_body_rect = body_part_list[body_id].rect
		if body_part_list[0].rect.colliderect(x_body_rect):
			if body_id == 0:
				pass
			else:
				print("player head has collided with: body rect id {0} !".format(body_id))
				game_over()
				break # break so the loop does not continue after the game reset


	for objects in object_list:
		if body_part_list[0].rect.colliderect(objects):
			print("You died at: " + str(body_part_list[0].rect.x) + ", " + str(body_part_list[0].rect.y))
			game_over()
			break

	pygame.display.update()