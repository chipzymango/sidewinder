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
body_rect_list = []

# width in pixels on each cell
cell_width = 20 * cell_size

# start at top left corner
cell_x, cell_y = 0, 0

# amount of cells in x and y
x_axis = 25
y_axis = 25

bg_color = (255, 225, 200)

grid_border_color = bg_color

# player start position
target_cell_x, target_cell_y = 200, 200

player_head_image = pygame.image.load('images/oldhead.png')
player_body_image = pygame.image.load('images/oldbody.png')
player_tail_image = pygame.image.load('images/oldtail.png')

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

def start_game(): # reset game values
	obstacle_spawn_timer = pygame.time.get_ticks()
	display_update_timer = pygame.time.get_ticks()
	body_rect_list.clear()
	object_list.clear()
	head_rect.x, head_rect.y = target_cell_x, target_cell_y
	body_rect_list.append(head_rect)
	body_rect_list.append(body_rect)

def game_over():
	print("Game over !")
	print("You died at: " + str(head_rect.x) + ", " + str(head_rect.y))

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
	new_rect = pygame.Rect(body_rect_list[-1].x, body_rect_list[-1].y ,cell_width, cell_width)
	body_rect_list.append(new_rect)

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

# starter head and body rect
head_rect = pygame.Rect(target_cell_x, target_cell_y, cell_width, cell_width)
body_rect = pygame.Rect(head_rect.x-cell_width, head_rect.y, cell_width, cell_width)

# append the rects
body_rect_list.append(head_rect)
body_rect_list.append(body_rect)

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

		# we loop in reverse so we can find the x and y
		# values of each rect, prior to being updated
		# this means we can find the previous rect's old x and y values
		for rect_id in range(len(body_rect_list)-1, -1, -1): # loop from len of list to -1 (excluding -1), and decrement by 1 for each loop
			rect_x = body_rect_list[rect_id]
			if rect_x == body_rect_list[0]:
				pass
			else:
				rect_x.x = body_rect_list[rect_id-1].x
				rect_x.y = body_rect_list[rect_id-1].y

		# then we update the player's movement
		if moving_right:
			if head_rect.x + cell_width >= WINDOW_X: 
				head_rect.x = 0
			else:
				head_rect.x += cell_width
		elif moving_down:
			if head_rect.y + cell_width >= WINDOW_Y:
				head_rect.y = 0
			else:
				head_rect.y += cell_width
		elif moving_left:
			if head_rect.x  <= 0:
				head_rect.x = WINDOW_X - cell_width
			else:
				head_rect.x -= cell_width
		elif moving_up:
			if head_rect.y <= 0:
				head_rect.y = WINDOW_Y - cell_width
			else:
				head_rect.y -= cell_width

	for body_rect in body_rect_list:
		if body_rect == body_rect_list[0]:
			pygame.draw.rect(WINDOW, (0, 180, 25), body_rect)
		elif body_rect == body_rect_list[-1]:
			pygame.draw.rect(WINDOW, (0,50,50), body_rect)
		else:
			pygame.draw.rect(WINDOW, (200,50,50), body_rect)

	for each_object in object_list:
		if head_rect.colliderect(each_object):
			print("player head has collided with a foreign object!")
			game_over()

	# assign each rect an id and check if a body
	# rect has collided with the player head rect
	for body_rect_id in range(len(body_rect_list)):
		x_body_rect = body_rect_list[body_rect_id]
		if head_rect.colliderect(x_body_rect):
			if body_rect_id == 0: # if it is the first body rect, drop it
				pass
			else:
				print("player head has collided with: rect id {0} !".format(body_rect_id))
				game_over()
				break # break so the loop does not continue after the game reset

	pygame.display.update()