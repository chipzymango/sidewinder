import pygame
import random

pygame.init()

cell_size = 1

WINDOW_X, WINDOW_Y = 500 * cell_size, 500 * cell_size

WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

pygame.display.set_caption("Sidewinder")

clock = pygame.time.Clock()

class Object():
	def __init__(self, start_x, start_y):
		self.x = start_x
		self.y = start_y
		self.width = cell_width
		self.image = pygame.image.load("images/food.png").convert()
		self.rect = pygame.Rect(self.x, self.y, cell_width, cell_width)
		self.image = pygame.transform.scale(self.image, (self.width, self.width))
		object_list.append(self)

	def update(self):
		WINDOW.blit(self.image, (self.x, self.y))

# amount of pixels wide in a cell
cell_width = 20 * cell_size

# amount of cells in x and y
x_axis = 25
y_axis = 25

bg_color = (255, 225, 200)

grid_border_color = (225,200,175)

cell_list = []

for y_cell in range(y_axis):
	for x_cell in range(x_axis):
		individual_cell = pygame.Rect( (cell_width * x_cell), (cell_width * y_cell), cell_width * cell_size, cell_width * cell_size)
		cell_list.append(individual_cell)

cell_x, cell_y = 0, 0

# set fixed cell coordinates
for each_cell in cell_list:
	# dividing by cell width to get correct x and y of cells and not pixels
	each_cell_x = int(each_cell.x / cell_width)
	each_cell_y = int(each_cell.y / cell_width)

live_timer = pygame.time.get_ticks()
live_timer2 = pygame.time.get_ticks()

# start position
target_cell_x, target_cell_y = 200, 200
player_rect = pygame.Rect(target_cell_x, target_cell_y, cell_width, cell_width)
previous_player_x, previous_player_y = target_cell_x, target_cell_y
player_tail = pygame.Rect(previous_player_x, previous_player_y, cell_width, cell_width)

bad_block = pygame.Rect(10 * cell_width, 20 * cell_width, cell_width, cell_width)

movement_delay = 100

moving_right = True
moving_down = False
moving_left = False
moving_up = False

object_list = []

def spawn_object():
	rx = random.randint(1, x_axis-1)
	ry = random.randint(1, y_axis-1)
	rx = rx * cell_width
	ry = ry * cell_width
	new_object = Object(rx, ry)
	print("Spawned new object at: " + str(rx) + ", " + str(ry))

FPS = 60
running = True
while running:
	clock.tick(FPS)
	# draw background color
	WINDOW.fill(bg_color)

	# get the previous occupied cell of player
	pygame.draw.rect(WINDOW, (0, 255, 0), player_rect)
	pygame.draw.rect(WINDOW, (0, 200, 0), player_tail)

	# draw each individual cell to form the grid
	for each_cell in cell_list:
		# draw borders
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				if moving_down or moving_up:
					moving_right = True
					moving_down= False
					moving_left = False
					moving_up = False
				
			if event.key == pygame.K_DOWN:
				if moving_left or moving_right:
					moving_down = True
					moving_right= False
					moving_left = False
					moving_up = False
				
			if event.key == pygame.K_LEFT:
				if moving_up or moving_down:
					moving_left = True
					moving_right= False
					moving_down = False
					moving_up = False
				
			if event.key == pygame.K_UP:
				if moving_left or moving_right:
					moving_up = True
					moving_right= False
					moving_down = False
					moving_left = False

	# call update method in every existing object
	for each_object in object_list:
		each_object.update()

	# spawn a new object every third second
	if pygame.time.get_ticks() - live_timer2 > 3000:
		live_timer2 = pygame.time.get_ticks() 
		spawn_object()

	if pygame.time.get_ticks() - live_timer > movement_delay:
		live_timer = pygame.time.get_ticks()
		previous_player_x, previous_player_y = player_rect.x, player_rect.y

		if moving_right:
			if target_cell_x + cell_width >= WINDOW_X:
				target_cell_x = 0
			else:
				target_cell_x += cell_width

		elif moving_down:
			if target_cell_y + cell_width >= WINDOW_Y:
				target_cell_y = 0
			else:
				target_cell_y += cell_width

		elif moving_left:
			if target_cell_x  <= 0:
				target_cell_x = WINDOW_X - cell_width
			else:
				target_cell_x -= cell_width

		elif moving_up:
			if target_cell_y <= 0:
				target_cell_y = WINDOW_Y - cell_width
			else:
				target_cell_y -= cell_width

	# update cell coordinates
	player_rect.x = target_cell_x
	player_rect.y = target_cell_y
	player_tail.x = previous_player_x
	player_tail.y = previous_player_y

	for each_object in object_list:
		if player_rect.colliderect(each_object):
			print("Game over !")
			print("You died at: " + str(player_rect.x) + ", " + str(player_rect.y))
			running = False

	pygame.display.update()