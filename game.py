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
rect_list = []

# width in pixels on each cell
cell_width = 20 * cell_size

# start at top left corner
cell_x, cell_y = 0, 0

# amount of cells in x and y
x_axis = 25
y_axis = 25

bg_color = (255, 225, 200)

grid_border_color = bg_color

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

# start position
target_cell_x, target_cell_y = 200, 200

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

moving_right = True
moving_down = False
moving_left = False
moving_up = False

def reset_game(): # reset game values
	obstacle_spawn_timer = pygame.time.get_ticks()
	display_update_timer = pygame.time.get_ticks()
	rect_list.clear()
	object_list.clear()
	player_head_rect.x, player_head_rect.y = target_cell_x, target_cell_y
	rect_list.append(player_head_rect)

def game_over():
	print("Game over !")
	print("You died at: " + str(player_head_rect.x) + ", " + str(player_head_rect.y))

	game_over_loop = True

	screen_layer = pygame.Surface((WINDOW_X, WINDOW_Y)).convert_alpha()
	while game_over_loop:
		screen_layer.fill((0,0,0, 0.5))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				game_over_loop = False

	reset_game()

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
	new_rect = pygame.Rect(0,0,cell_width, cell_width)
	rect_list.append(new_rect)

# starter head
player_head_rect = pygame.Rect(target_cell_x, target_cell_y, cell_width, cell_width)
rect_list.append(player_head_rect)

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

		if moving_right:
			if player_head_rect.x + cell_width >= WINDOW_X: 
				player_head_rect.x = 0
			else:
				player_head_rect.x += cell_width
		elif moving_down:
			if player_head_rect.y + cell_width >= WINDOW_Y:
				player_head_rect.y = 0
			else:
				player_head_rect.y += cell_width
		elif moving_left:
			if player_head_rect.x  <= 0:
				player_head_rect.x = WINDOW_X - cell_width
			else:
				player_head_rect.x -= cell_width
		elif moving_up:
			if player_head_rect.y <= 0:
				player_head_rect.y = WINDOW_Y - cell_width
			else:
				player_head_rect.y -= cell_width

		# we loop in reverse so we can find the x and y
		# values of each rect, prior to being updated
		# this means we can find the old rect's x and y values
		for rect_id in range(len(rect_list)-1, 0, -1):
			rect_x = rect_list[rect_id]
			if rect_x == rect_list[0]:
				pass
			else:
				rect_x.x = rect_list[rect_id-1].x
				rect_x.y = rect_list[rect_id-1].y

	for rect in rect_list:
		pygame.draw.rect(WINDOW, (200,50,50), rect)

	for each_object in object_list:
		if player_head_rect.colliderect(each_object):
			game_over()

	for each_body in rect_list:
		if each_body == rect_list[0]:
			pass
		elif player_head_rect.colliderect(each_body):
			game_over()

	pygame.display.update()